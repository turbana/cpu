#!/usr/bin/python

import csv
import json
import math
import re
import sys

import gen_decode_verilog

DONTCARE = 0

bit_widths = {
	"D_Op": 3,
	"D_RFa": 4,
	"D_RFb": 4,
	"D_Rd": 4,
	"D_Ra": 4,
	"D_Rb": 4,
	"D_Rc": 4,
	"D_A": 16,
	"D_B": 16,
	"D_C": 16,
	"D_SF": 3,
}


def main(args):
	if len(args) != 2:
		print "USAGE: %s decode.csv best.log" % sys.argv[0]
		return 2
	csv_filename, log_filename = args
	table = read_csv(csv_filename)
	solution = read_log(log_filename)
	testcase = gen_testcase(table, solution)
	print json.dumps({"values": testcase}, indent=4)


def read_csv(filename):
	return list(csv.reader(open(filename)))
	for i, inst in enumerate(table[0]):
		table[0][i] = clean_wire(inst)
	for i in range(len(table)):
		table[i][0] = clean_keyword(table[i][0])
	return table


def read_log(filename):
	data = gen_decode_verilog.parse(open(filename))
	for inst, opcode in data["encoding"].items():
		new_inst = clean_keyword(inst)
		if new_inst != inst:
			del data["encoding"][inst]
			data["encoding"][new_inst] = opcode
	return data


def clean_keyword(inst):
	inst = inst.strip()
	if inst == "and": inst = "_and"
	if inst == "or":  inst = "_or"
	return inst.replace(".", "_")


def clean_wire(name):
	return name.replace("[", "").replace("]", "")


def clean_value(val):
	if val == DONTCARE or val == "X":
		val = "DONTCARE"
	return val


def rewrite_muxes(muxes):
	wires = {}
	for mux, values in muxes.items():
		pass


def bit_width(stem, tests):
	def match((other, _)):
		return other.startswith(stem) and other[-1] in "0123456789"
	return sum(map(match, tests))


def gen_testcase(table, solution):
	tests = [
		("sign", "lambda n, b: n-(2**b) if 2**(b-1) <= n else n"),
		("slice", "lambda start, size: (FD_I>>start) & (2**size)-1"),
		("op5", "FD_I >> 11"),
		("I", "[int(b) for b in reversed(bin(FD_I)[2:].zfill(16))]"),
		("s4imm", "sign(slice(7, 4), 4)"),
		("s7imm", "sign(slice(6, 7), 7)"),
		("s8imm", "sign(slice(3, 8), 8)"),
		("s11imm", "sign(slice(0, 11), 11)"),
		("SPI", "s4imm+1 if s4imm>=0 else s4imm"),
		("RFB_I", "SPI if I[6]==1 else R_B"),
	]
	exports = [clean_wire(w) for w in table.pop(0)[1:]]
	insts = [clean_keyword(row[0]) for row in table]
	table = [row[1:] for row in table]
	tests += gen_opcodes(solution)
	tests += gen_instructions(exports, insts, table)
	tests += gen_exports(exports)
	return ["%s = %s" % (name, expr) for name, expr in tests]


def gen_opcodes(solution):
	tests = []
	for op,  value in sorted(solution["encoding"].items()):
		code = int(value, 2)
		tests.append((op, "op5 == %s" % code))
	return tests


def gen_instructions(exports, insts, values):
	tests = []
	for col, wire in enumerate(exports):
		expr = ""
		for row, op in enumerate(insts):
			val = clean_value(values[row][col])
			expr += "%s if %s else " % (val, op)
		expr += "None"
		tests.append((wire, expr))
		# if we're finishing with a wire: generate the concatenated version
		if wire.endswith("0"):
			stem = wire[:-1]
			width = bit_width(stem, tests)
			expr = " | ".join("(%s%d<<%d)" % (stem, b, b) for b in range(width))
			expr += " if DONTCARE not in (%s) else DONTCARE" % ",".join("%s%d" % (stem, b) for b in range(width))
			tests.append((stem, expr))
	return tests


def gen_exports(exports):
	tests = []
	stems = set(re.sub("[0-9]", "", wire) for wire in exports)
	for stem in stems:
		width = bit_widths.get(stem, 1)
		tests.append(("%s:%d" % (stem, width), stem))
	return tests


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
