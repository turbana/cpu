"""
Generate verilog modules from json definition.

This is used to generate verilog code for all basic 74 series logic gates.
"""

import sys
import json
import re
import functools
import collections

DEFINITIONS = "74HCxxx.json"

_BASIC_WIRE_REGEX	= "[0-9A-Z]+"
_WIRE_REGEX			= "\??%s" % _BASIC_WIRE_REGEX
_EXPR_REGEX			= "\?%s" % _BASIC_WIRE_REGEX


def main(args):
	if len(args) != 1:
		print "USAGE: %s module" % sys.argv[0]
		print "Generates verilog code for module"
		return 2
	module = args[0]
	spec = load_spec(module)
	if not spec:
		error("module %s not found" % module)
	code = gen_code(spec)
	print code


def error(msg):
	sys.stderr.write("ERROR: %s\n" % msg)
	sys.exit(1)


def load_spec(module):
	specs = json.load(open(DEFINITIONS))
	spec = specs.get(module, None)
	if spec:
		spec["module"] = module
	return spec


def gen_code(spec):
	module = spec["module"]
	delay = spec["delay"]
	code = "/* %s */\n`timescale 1 ns / 100 ps\n" % module
	code += "module %s (" % escape(module)
	code += ", ".join(map(escape, range(1, wire_count(spec)+1)))
	code += ");\n\tinput "
	code += ", ".join(map(escape, input_wires(spec)))
	code += ";\n\toutput "
	code += ", ".join(map(escape, output_wires(spec)))
	code += ";\n\n"
	for assign in assignments(spec):
		code += "\tassign #%d %s;\n" % (delay, assign)
	code += "\nendmodule"
	return code


def escape(x):
	x = str(x)
	e = "\\" if x and x[0] in "0123456789" else ""
	return e + x


def assignments(spec):
	for value, expr in spec["assign"].items():
		expr = expand_basic_wires(spec, "%s = %s" % (value, expr))
		for assign in expand_expr(spec, expr):
			yield assign


def wire_count(spec):
	if spec["package"].startswith("DIP"):
		return int(spec["package"].replace("DIP", ""))
	error("invalid package for %s" % spec["module"])


def input_wires(spec):
	_expand = functools.partial(expand, spec)
	_findall = functools.partial(findall, _WIRE_REGEX)
	names = flatmap(_findall, spec["assign"].values())
	return flatmap(_expand, names)


def output_wires(spec):
	_expand = functools.partial(expand, spec)
	return flatmap(_expand, spec["assign"].keys())


def wire_name(spec, name):
	names = spec.get("names", None)
	if not names or name not in names:
		return name
	return 1 + names.index(name)


def flatmap(f, lst):
	outputs = set()
	for val in lst:
		for result in f(val):
			outputs.add(result)
	return outputs


def findall(regex, data):
	return [x for x in re.findall(regex, data) if x]


def expand_basic_wires(spec, expr):
	_wire_name = functools.partial(wire_name, spec)
	regex = "(%s)" % _BASIC_WIRE_REGEX
	return "".join(map(escape, map(_wire_name, re.split(regex, expr))))


def expand(spec, name):
	_wire_name = functools.partial(wire_name, spec)
	if "?" not in name:
		return [wire_name(spec, name)]
	regex = name.replace("?", "[0-9]+")
	matches = findall(regex, " ".join(spec["names"]))
	return map(_wire_name, matches)


def expand_expr(spec, expr):
	_expand = functools.partial(expand, spec)
	names = collections.OrderedDict()
	count = 0
	for name in re.findall(_EXPR_REGEX, expr):
		if name and name not in names:
			var = "var%d" % count
			names[name] = var
			expr = expr.replace(name, "{%s}" % var)
			count += 1
	expansions = map(_expand, names.keys())
	length = len(expansions[0])
	length_check = lambda l: len(l) == length
	if not all(map(length_check, expansions)):
		error("unbalanced variables for %s" % spec["module"])
	for values in zip(*expansions):
		env = {"var%d"%i: escape(v) for i,v in enumerate(values)}
		yield expr.format(**env)


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
