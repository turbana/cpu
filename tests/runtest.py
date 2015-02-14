#!/usr/bin/python

import os
import os.path
import subprocess
import string
import sys

import pyparsing as pp

root = os.path.dirname(sys.argv[0])
ASM = os.path.join(root, "../asm/asm.py")
SIM = os.path.join(root, "../sim/functional/cpu.py")
errors = [0]


def error(msg):
	print "error: %s" % msg
	errors[0] += 1


def grammer():
	lparen = pp.Suppress("(")
	rparen = pp.Suppress(")")
	equal = pp.Suppress("=")
	nl = pp.Suppress(pp.LineEnd())
	reg = pp.Combine("$" + pp.Optional("cr") + pp.Word(pp.srange("[0-7]"), max=1))
	num = pp.Word(pp.srange("[0-9]")).setParseAction(lambda s,l,t: int(t[0]))
	val = pp.Word(pp.srange("[0-9a-fA-F]")).setParseAction(lambda s,l,t: int(t[0], 16))
	values = pp.Dict(pp.OneOrMore(pp.Group(reg + equal + val)))
	return num + lparen + values + rparen + nl


def parse_output(lines):
	g = grammer()
	results = {}
	for line in lines:
		if not line.split(): continue
		res = g.parseString(line)
		results[res[0]] = res
	return results


def parse_input(stream):
	def inner():
		for line in stream:
			line = line.strip()
			if line.startswith(";@;"):
				yield line[3:]
	return parse_output(inner())


def assemble(asm, macro, exe):
	do_proc("%s %s %s %s" % (ASM, asm, macro, exe))


def simulate(exe, clocks):
	trace = exe.replace(".o", ".trace.log")
	fmt = "%s %s --no-debugger --randomize --test-clock %s --stop-clock %d --trace %s"
	cmd = fmt % (SIM, exe, " ".join(map(str, clocks)), max(clocks), trace)
	return do_proc(cmd).split("\n")


def asserts(output, checks):
	for clock, values in sorted(checks.items()):
		try:
			result = output[clock]
		except KeyError:
			error("clock %s not found in output" % clock)
		for key, value in sorted(values.items()):
			if value != result[key]:
				error("@%d %s expected %04X got %04X" % (clock, key, value, result[key]))


def do_proc(cmd):
	proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	output, _ = proc.communicate()
	if proc.returncode != 0:
		print output,
		raise Exception("Return code %d received from '%s'" % (proc.returncode, cmd))
	return output


def main(args):
	if len(args) != 1:
		print "USAGE: %s testfile.asm" % sys.argv[0]
		return 2
	asm_filename = args[0]
	macro_filename = asm_filename.replace(".asm", ".py")
	exe_filename = asm_filename.replace(".asm", ".o")
	if not os.path.exists(asm_filename):
		print "ERROR: could not open file: " + asm_filename
		return 1
	if not os.path.exists(macro_filename):
		macro_filename = ""
	try:
		checks = parse_input(open(asm_filename))
		assemble(asm_filename, macro_filename, exe_filename)
		output = simulate(exe_filename, checks.keys())
		output = parse_output(output)
		asserts(output, checks)
	except (pp.ParseException, pp.ParseFatalException), err:
		print err.line
		print " "*(err.column-1) + "^"
		print err
		return 1
	return errors[0]


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
