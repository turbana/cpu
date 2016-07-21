import argparse
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
SKIP_RANGE = 2**1, 2**6

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


def load_truth_table(filename):
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


_encodings = list(itertools.product([0, 1], repeat=5))
_opcodes   = list(itertools.product([0, 1], repeat=3))
def all_encodings():
	# generate all possible instruction encodings
	for p1, p2 in itertools.permutations(_opcodes, 2):
		master_encoding = {}
		encodings = set(_encodings)
		# set multi bit instructions ldw.i/stw.i
		for i, bits in enumerate(itertools.product([0, 1], repeat=2)):
			master_encoding["ldw.i%d"%i] = p1 + bits
			master_encoding["stw.i%d"%i] = p2 + bits
			encodings -= set((p1 + bits, p2 + bits))
		# set other instructions
		for enc_permutation in itertools.permutations(encodings):
			encoding = dict(master_encoding)
			encoding.update(dict(zip(TRIBIT_INSTRUCTIONS, enc_permutation)))
			yield encoding


def truth_tables(inputs, outputs):
	# generate all possible truth tables
	is_int = lambda x: x is None or isinstance(x, int)
	all_values_ints = lambda k: all(map(is_int, set(out[k] for out in outputs)))
	keys = set(outputs[0].keys()) - set(["Inst"])
	int_keys = [k for k in keys if all_values_ints(k)]
	mux_keys = sorted(keys - set(int_keys))
	mux_bits = dict(all_mux_bits(outputs, mux_keys))
	out_keys = sorted(int_keys)
	out_names = out_keys + ["m_%s_%s" % (clean_name(k),b)
							for k,bits in all_mux_bits(outputs, mux_keys)
							for b in xrange(bits)]
	in_keys = xrange(ENCODING_BITS)
	in_names = ["I[%d]" % (15-i) for i in in_keys]
	table = {
		"inputs": in_names,
		"outputs": out_names,
		"encoding": inputs,
		"data": initial_data(inputs, outputs, in_keys, out_keys, mux_keys),
		"mux_configs": None,
	}
	mux_index = {mux:5+out_names.index("m_%s_0" % clean_name(mux)) for mux in mux_keys}
	# first output is total number of possible tables
	yield 2**sum(mux_bits.values())
	for muxes in iterate_muxes(outputs, mux_keys):
		table["mux_configs"] = muxes
		for row, output in enumerate(outputs):
			for mux, config in muxes:
				key = config["key"]
				i = mux_index[key]
				val = output[key]
				for b,v in enumerate(reversed(mux[str(val)])):
					table["data"][row][i+b] = v
		yield table


def initial_data(inputs, outputs, in_keys, out_keys, mux_keys):
	data = []
	for output in outputs:
		encoding = inputs[output["Inst"]]
		row = []
		for k in in_keys:
			row.append(encoding[k])
		for k in out_keys:
			row.append(output[k])
		for k, bits in all_mux_bits(outputs, mux_keys):
			row.extend([None] * bits)
		data.append(row)
	return data


def all_mux_bits(outputs, mux_keys):
	# iteration must match iterate_muxes()
	all_possible = [set(o[key] for o in outputs if o[key] is not None)
					for key in mux_keys]
	bits = lambda possible: int(math.ceil(math.log(len(possible), 2)))
	all_bits = map(bits, all_possible)
	# ensure 0 bit muxes are treated as 1 bit
	all_bits = [max(b, 1) for b in all_bits]
	return zip(mux_keys, all_bits)


def iterate_muxes(outputs, mux_keys):
	# generate all possible mux configurations
	iters = [gen_muxes(key, set(o[key] for o in outputs if o[key] is not None))
			 for key in mux_keys]
	muxes = map(list, iters)
	return itertools.product(*muxes)


def gen_muxes(key, possible):
	# generate all possible mux configurations for a single mux
	bits = int(math.ceil(math.log(len(possible), 2)))
	possible = map(str, possible)
	possible += "X" * ((2**bits) - len(possible))
	bit_patterns = list(itertools.product((0, 1), repeat=bits))
	config = {
		"names": ["m_%s_%s" % (clean_name(key),str(i)) for i in xrange(bits)],
		"key": key,
		"bits": bits,
	}
	for chosen in itertools.permutations(possible, len(possible)):
		mux = dict(zip(chosen, bit_patterns))
		mux["None"] = "-" * bits
		config["chosen"] = chosen
		yield mux, config


def clean_name(name):
	return name.replace("[", "").replace("]", "")


def score(solution):
	# solution's score (smaller is better)
	if solution is None:
		return INF
	if "score" not in solution:
		#simplify(solution)
		count_operators = lambda s: s.count("&") + s.count("!") + s.count("|")
		solution["score"] = sum(map(count_operators, solution["decoding"].values()))
	return solution["score"]


def simplify(solution):
	# minimize amount of logic in a solution
	logic = solution["decoding"]
	def replace(expr, name):
		if not expr:
			return
		for key, value in logic.items():
			if key == name:
				continue
			logic[key] = logic[key].replace(expr, name)
	# simple substitutions
	for name in logic:
		replace(logic[name], name)
	terms = sorted(all_terms(logic), key=len, reverse=True)
	count = 0
	for term in common_terms(logic, terms):
		name = "w" + str(count)
		count += 1
		replace(term, name)
		logic[name] = term


def all_terms(logic):
	terms = set()
	for expr in logic.values():
		terms |= set(split_expr(expr))
	return terms


def split_expr(expr):
	for s1 in expr.split(")"):
		for s2 in s1.split("("):
			if s2.count("&") > 0:
				splits = s2.split("&")
				for comb in combinations(splits):
					yield "&".join(comb)


def combinations(L):
	for i in xrange(len(L)-1):
		for j in xrange(i+1, len(L)):
			yield L[i:j+1]


def common_terms(logic, terms):
	def count(term):
		return sum(expr.count(term) for expr in logic.values())
	for term in terms:
		if count(term) > 1:
			yield term


def espresso_file(table):
	# create file-object containing table in espresso format
	file = StringIO.StringIO()
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
	# open("table.dat", "w").write("".join(file.readlines()))
	file.seek(0)
	return file


def solve(table):
	# generate a solution
	efile = espresso_file(table)
	proc = subprocess.Popen(ESPRESSO, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	stdout, stderr = proc.communicate(efile.getvalue())
	if proc.returncode:
		if stdout is not None: print stdout
		if stderr is not None: print stderr
		raise Exception("received exit %d from espresso" % proc.returncode)
	return {
		"decoding": dict(l.split(" = ") for l in stdout.replace("\n", "").replace("  ", "").split(";") if l),
		"encoding": table["encoding"],
		"mux_configs": table["mux_configs"],
	}


def write_solution(solution, stream):
	insts = solution["encoding"].keys()
	insts.sort(key=solution["encoding"].get)
	for i in insts:
		stream.write("%-8s %s\n" % (i, "".join(map(str, solution["encoding"][i]))))
	stream.write("\n")
	configs = [c for m,c in solution["mux_configs"]]
	for config in sorted(configs, key=lambda c: c["key"]):
		pretty = "MUX:%d(%s)" % (config["bits"], ",".join(config["chosen"]))
		stream.write("%-6s = %s\n" % (config["key"], pretty))
	stream.write("\n")
	for name, expr in sorted(solution["decoding"].items()):
		stream.write("%-6s = %s\n" % (name, expr))
	stream.write("\nscore: %s    \n" % solution["score"])


def skip_random(iter):
	skipped = 0
	while True:
		yield skipped, iter.next()
		skipped = random.randint(*SKIP_RANGE)
		for _ in xrange(skipped):
			iter.next()


def show_table(table, stream=sys.stdout):
	fmt = "%12s"
	j = " "
	def number(t, n=0):
		if not t: return n
		return number(t[1:], (n<<1)+t[0])
	enc = {number(t):i for i,t in table["encoding"].items()}
	def write_row(row):
		stream.write(j.join(fmt % x for x in row))
	write_row(["", "enc"] + table["outputs"])
	stream.write("\n")
	for i,row in enumerate(table["data"]):
		write_row([enc[i], hex(i)] + row[5:])
		stream.write("\n")


class NullStream(object):
	def write(self, *args):
		pass
	def flush(self):
		pass


def parse_args():
	parser = argparse.ArgumentParser(description="Searches for efficient encoding of opcodes and decode stage")
	parser.add_argument("--max-iterations", type=int, default=0, help="Maximum iterations to search")
	parser.add_argument("-q", "--quiet", action="store_true", help="Suppress output")
	return parser.parse_args()


def main(args):
	args = parse_args()
	outputs = load_truth_table(CSV_FILE)
	running_log = open(RUNNING_LOG, "w")
	best_solution = None
	out_stream = NullStream() if args.quiet else sys.stdout
	x = 0
	enc_count = 0
	iterations = 0
	done = False
	encodings = iter([1, simple_encoding()])
	encoding_total = float(encodings.next())
	for encoding in encodings:
		enc_count += 1
		count = 0
		table_iter = truth_tables(encoding, outputs)
		table_count = float(table_iter.next())
		for skipped, table in skip_random(table_iter):
			count += 1 + skipped
			iterations += 1
			solution = solve(table)
			if score(solution) < score(best_solution):
				best_solution = solution
				out_stream.write("\n")
				write_solution(solution, out_stream)
				out_stream.write("\n")
				write_solution(solution, running_log)
				write_solution(solution, open(BEST_LOG, "w"))
			out_stream.write("\rencoding=%d/%d (%1.2f%%)  table=%d/%d (%1.2f%%)  score=%s   " % (
				enc_count, encoding_total, (enc_count*100/encoding_total),
				count, table_count, (count*100/table_count), str(score(solution))))
			out_stream.flush()
			if iterations == args.max_iterations:
				done = True
				break
		if done:
			break
	write_solution(solution, out_stream)
	write_solution(solution, open(BEST_LOG, "w"))


if __name__ == "__main__":
	try:
		sys.exit(main(sys.argv[1:]))
	except KeyboardInterrupt:
		pass
