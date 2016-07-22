import argparse
import copy
import csv
import sys
import StringIO
import subprocess
import math
import itertools
from itertools import izip
import random


ENCODING_BITS = 5
ANY = "X"
CSV_FILE = "config/decode.csv"
RUNNING_LOG = "build/running.log"
BEST_LOG = "build/decode.log"

ESPRESSO = "bin/espresso -o eqntott".split()
INF = 2**32-1


def simple_encoding():
	return {
		"add":		(0, 0, 0, 0, 0),
		"and":		(0, 0, 0, 0, 1),
		"or":		(0, 0, 0, 1, 0),
		"xor":		(0, 0, 0, 1, 1),
		"shr":		(0, 0, 1, 0, 0),
		"sar":		(0, 0, 1, 0, 1),
		"shl":		(0, 0, 1, 1, 0),
		"sex":		(0, 0, 1, 1, 1),
		"s.cond": 	(0, 1, 0, 0, 0),
		"as.z":		(0, 1, 0, 0, 1),
		"as.nz": 	(0, 1, 0, 1, 0),
		"jmp":		(0, 1, 0, 1, 1),
		"ldw":		(0, 1, 1, 0, 0),
		"ldiw":		(0, 1, 1, 0, 1),
		"sub":		(0, 1, 1, 1, 0),
		"stiw":		(0, 1, 1, 1, 1),
		"ldw.i0":	(1, 0, 0, 0, 0),
		"ldw.i1":	(1, 0, 0, 0, 1),
		"ldw.i2":	(1, 0, 0, 1, 0),
		"ldw.i3":	(1, 0, 0, 1, 1),
		"stw.i0":	(1, 0, 1, 0, 0),
		"stw.i1":	(1, 0, 1, 0, 1),
		"stw.i2":	(1, 0, 1, 1, 0),
		"stw.i3":	(1, 0, 1, 1, 1),
		"lcr":		(1, 1, 0, 0, 0),
		"scr":		(1, 1, 0, 0, 1),
		"iret":		(1, 1, 0, 1, 0),
		"halt":		(1, 1, 0, 1, 1),
		"lui":		(1, 1, 1, 0, 0),
		"addi":		(1, 1, 1, 0, 1),
		"trap":		(1, 1, 1, 1, 0),
		"jmp.i":	(1, 1, 1, 1, 1),
	}

TRIBIT_INSTRUCTIONS = (
		"add", "sub", "and", "or", "shl", "shr", "sar", "xor", "s.cond", "as.z",
		"as.nz", "jmp", "ldw", "ldiw", "sex", "stiw", "lcr", "scr", "iret", "halt",
		"lui", "addi", "trap", "jmp.i")
PENTABIT_INSTRUCTIONS = ("ldw.i", "stw.i")


def load_config(filename):
	# load required outputs from csv file
	table = []
	reader = csv.reader(open(filename))
	header = reader.next()
	for row in reader:
		table.append(dict((header[i], parse_value(row[i])) for i in xrange(len(row))))
	return table


def parse_value(s):
	# parse csv value
	if s.upper() == ANY:
		return None
	try:
		return int(s)
	except ValueError:
		return s


def simple_muxes(config):
	is_int = lambda x: x is None or isinstance(x, int)
	all_values_ints = lambda k: all(map(is_int, set(out[k] for out in config)))
	keys = set(config[0].keys()) - set(["Inst"])
	mux_keys = [k for k in keys if not all_values_ints(k)]
	muxes = {}
	for key in mux_keys:
		choices = list(set(row[key] for row in config))
		bits = int(math.ceil(math.log(len(choices), 2)))
		choices += [None] * (2**bits - len(choices))
		nones = choices.count(None)
		if nones == len(choices) / 2:
			for _ in range(nones):
				choices.remove(None)
		muxes[key] = choices
	return muxes


class SearchState(object):
	def __init__(self, config, encoding=None, muxes=None):
		self.config = config
		self.encoding = encoding if encoding else simple_encoding()
		self.muxes = muxes if muxes else simple_muxes(config)
		self._score = None
		self._result = None


	def solve(self):
		efile = self.espresso_file
		proc = subprocess.Popen(ESPRESSO, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		stdout, stderr = proc.communicate(efile.getvalue())
		if proc.returncode:
			if stdout is not None: print stdout
			if stderr is not None: print stderr
			raise Exception("received exit %d from espresso" % proc.returncode)
		count_operators = lambda s: s.count("&") + s.count("!") + s.count("|")
		self._result = dict(l.split(" = ") for l in stdout.replace("\n", "").replace("  ", "").split(";") if l)
		self._score = sum(map(count_operators, self.result.values()))


	@property
	def espresso_file(self):
		# create file-object containing table in espresso format
		file = StringIO.StringIO()
		table = self.truth_table
		file.write(".i\t%d\n" % len(table["inputs"]))
		file.write(".o\t%d\n" % len(table["outputs"]))
		file.write(".ilb\t%s\n" % " ".join(table["inputs"]))
		file.write(".ob\t%s\n" % " ".join(table["outputs"]))
		for line in table["data"]:
			for value in line[:5]:
				file.write("-" if value is None else str(value))
			file.write(" ")
			for value in line[5:]:
				file.write("-" if value is None else str(value))
			file.write("\n")
		file.write(".e\n")
		file.seek(0)
		# XXX
		# open("table.dat", "w").write("".join(file.readlines()))
		# file.seek(0)
		return file


	@property
	def truth_table(self):
		table = {
			"inputs": ["I[%d]" % (15-i) for i in xrange(ENCODING_BITS)],
			"outputs": [key for key in self.config[0] if key != "Inst" and key not in self.muxes],
			"data": []
		}
		# fill outputs with muxes
		for mux,choices in self.muxes.items():
			for b in xrange(int(math.log(len(choices), 2))):
				table["outputs"].append("m_%s_%d" % (mux, b))
		table["outputs"].sort()
		# populate data
		for inst in self.config:
			encoding = self.encoding[inst["Inst"]]
			row = list(encoding)
			for name in table["outputs"]:
				if not name.startswith("m_"):
					row.append(inst[name])
				else:
					key = name[2:-2]
					bit = int(name[-1])
					value = inst[key]
					if value is None:
						choice = None
						check = None
					else:
						choice = self.muxes[key].index(value)
						check = (choice >> bit) & 1
					row.append(check)
			table["data"].append(row)
		return table


	def neighbor(self):
		muxes = copy.deepcopy(self.muxes)
		mux = muxes[random.choice(muxes.keys())]
		while len(mux) == 1:
			mux = muxes[random.choice(muxes.keys())]
		i = random.randint(0, len(mux)-1)
		j = i
		while j == i:
			j = random.randint(0, len(mux)-1)
		mux[i], mux[j] = mux[j], mux[i]
		return SearchState(self.config, self.encoding, muxes)


	def dump(self, stream):
		clean = lambda val: "X" if val is None else val
		enc_keys = self.encoding.keys()
		enc_keys.sort(key=self.encoding.get)
		for key in enc_keys:
			stream.write("%-8s = %s\n" % (key, "".join(map(str, self.encoding[key]))))
		stream.write("\n")
		for mux, choices in self.muxes.items():
			bits = int(math.log(len(choices), 2))
			pretty_choices = ",".join("%d=%s" % (i, clean(val)) for i,val in enumerate(choices))
			pretty = "MUX:%d(%s)" % (bits, pretty_choices)
			stream.write("%-16s = %s\n" % (mux, pretty))
		stream.write("\n")
		for name, expr in sorted(self.result.items()):
			stream.write("%-16s = %s\n" % (name, expr))
		stream.write("\nscore: %s\n" % self.score)


	@property
	def score(self):
		if self._score is None:
			self.solve()
		return self._score


	@property
	def result(self):
		if self._result is None:
			self.solve()
		return self._result


class MetaState(object):
	RANGES = {
		"temp": (0.5, 1000.0),
		"settle": (10, 100),
		# max_iterations remains unchanged (acts as escape valve)
		"cool_mod": (5, 1000),
		"cool_base": (0.05, 0.5),
		"_cool_mult": (0.10, 0.99),
	}

	def __init__(self, config, seed, options):
		self.config = config
		self.seed = seed
		self.options = options
		self.options["cool_func"] = lambda temp, _: temp * options["_cool_mult"]
		self._score = None

	def solve(self):
		# XXX
		print "solve", self.options, "     ",
		sys.stdout.flush()
		randstate = random.getstate()
		random.seed(self.seed)
		initial = SearchState(self.config)
		solution = sim_anneal(initial, self.options)
		self._score = solution.score
		random.setstate(randstate)

	def neighbor(self):
		options = dict(self.options)
		key = random.choice(MetaState.RANGES.keys())
		rand = random.randint if isinstance(MetaState.RANGES[key][0], int) else random.uniform
		options[key] = rand(*MetaState.RANGES[key])
		return MetaState(self.config, self.seed, options)

	@property
	def score(self):
		if self._score is None:
			self.solve()
		return self._score


def meta_anneal(config, seed):
	def emit(message):
		sys.stdout.write(message)
		sys.stdout.flush()
	meta_options = {
		"temp": 10.0,
		"settle": 50,
		"max_iterations": 1000,
		"cool_mod": 10,
		"cool_base": 0.1,
		"cool_func": lambda temp, _: temp * 0.85,
	}
	initial_options = {
		"temp": 100.0,
		"settle": 100,
		"max_iterations": 1000,
		"cool_mod": 100,
		"cool_base": 0.01,
		"_cool_mult": 0.85,
	}
	initial = MetaState(config, seed, initial_options)
	solution = sim_anneal(initial, meta_options, emit)
	print
	print solution.options


def sim_anneal(state, options, emit=None, emit_mod=1):
	iterations = 0
	settle = 0
	temp = options["temp"]
	settle_at = options["settle"]
	max_iterations = options["max_iterations"]
	cool_mod = options["cool_mod"]
	cool_base = options["cool_base"]
	cool_func = options["cool_func"]
	while settle != settle_at and iterations != max_iterations:
		iterations += 1
		settle += 1
		if emit and iterations % emit_mod == 0:
			emit("\rscore=%4d temp=%0.2f iterations=%d settle=%2d    " % (state.score, temp, iterations, settle))
		neighbor = state.neighbor()
		delta = neighbor.score - state.score
		if delta <= 0 or random.random() < math.exp(-delta/temp):
			state = neighbor
			if delta != 0: settle = 0
		if iterations % cool_mod == 0 and temp > cool_base:
			temp = cool_func(temp, iterations)
	return state


def parse_args():
	parser = argparse.ArgumentParser(description="Searches for efficient encoding of opcodes and decode stage")
	parser.add_argument("iterations", type=int, help="Stop after settling on a solution for ITERATIONS")
	parser.add_argument("-q", "--quiet", action="store_true", help="Suppress output")
	parser.add_argument("-m", "--max-iterations", type=int, default=-1, help="Maximum iterations to search")
	parser.add_argument("-s", "--seed", type=int, default=None, help="Random number generator seed")
	parser.add_argument("--meta-anneal", action="store_true", help="Perform a meta search to find optimal annealing parameters")
	return parser.parse_args()


def main(args):
	args = parse_args()
	random.seed(args.seed)
	outputs = load_config(CSV_FILE)
	initial = SearchState(outputs)
	def emit(message):
		if not args.quiet:
			sys.stdout.write(message)
			sys.stdout.flush()
	options = {
		"temp": 100.0,
		"settle": args.iterations,
		"max_iterations": args.max_iterations,
		"cool_mod": 100,
		"cool_base": 0.01,
		"cool_func": lambda temp, _: temp * 0.85,
	}
	if args.meta_anneal:
		return meta_anneal(outputs, args.seed)
	solution = sim_anneal(initial, options, emit, emit_mod=10)
	solution.dump(open(BEST_LOG, "w"))


if __name__ == "__main__":
	try:
		sys.exit(main(sys.argv[1:]))
	except KeyboardInterrupt:
		pass
