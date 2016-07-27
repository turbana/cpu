"""
Generate verilog modules from json definition.

This is used to generate verilog code for all basic 74 series logic gates.
"""

import sys
import json
import re
import functools
import collections

DEFINITIONS = "etc/74-series-chips.json"

_SPACE_CHARS		= "(){},;|"
_BASIC_WIRE_REGEX	= "[0-9A-Z]+(?!')"
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
	all_wires = map(escape, range(1, wire_count(spec)+1))
	outputs = map(escape, output_wires(spec))
	inputs = map(escape, set(all_wires) - set(outputs))
	registers = map(escape, expand_wires(spec, spec.get("registers", [])))
	code = "/* %s */\n`timescale 1 ns / 100 ps\n" % module
	code += "module %s (" % escape(module)
	code += ",".join(map(escape, range(1, wire_count(spec)+1)))
	code += ");\n\tinput "
	code += ",".join(inputs)
	code += ";\n\toutput "
	code += ",".join(outputs)
	if registers:
		code += ";\n\treg "
		code += ",".join("%s = 0" % r for r in registers)
	code += ";\n\n"
	for assign in assignments(spec):
		code += "\tassign #%d %s;\n" % (delay, assign)
	code += "\n"
	for if_stmnt, expr in clocked_expressions(spec):
		code += "\talways @(%s)\n\tbegin\n\t\t#%s %s\n\tend\n" % (if_stmnt, delay, expr)
	code += "\nendmodule"
	for char in _SPACE_CHARS:
		code = code.replace(char, " " + char + " ")
	return code


def escape(x):
	x = str(x)
	e = "\\" if x and x[0] in "0123456789" and "'" not in x else ""
	return e + x


def output_wires(spec):
	assign = expand_wires(spec, spec.get("assign", {}).keys())
	clocked = expand_wires(spec, spec.get("registers", []))
	return set(assign) | set(clocked)


def assignments(spec):
	for value, expr in spec.get("assign", {}).items():
		expr = expand_basic_wires(spec, "%s = %s" % (value, expr))
		for assign in expand_expr(spec, expr):
			yield assign


def clocked_expressions(spec):
	sep = "/|\\"
	for test, expr in spec.get("clocked", {}).items():
		full_expr = "%s %s %s" % (test, sep, expr)
		full_expr = expand_basic_wires(spec, full_expr)
		for expansion in expand_expr(spec, full_expr):
			test, expr = expansion.split(sep)
			yield test, expr


def wire_count(spec):
	if spec["package"].startswith("DIP"):
		return int(spec["package"].replace("DIP", ""))
	error("invalid package for %s" % spec["module"])


def input_wires(spec):
	_expand = functools.partial(expand, spec)
	_findall = functools.partial(findall, _WIRE_REGEX)
	names = flatmap(_findall, spec["assign"].values())
	return flatmap(_expand, names)


def expand_wires(spec, wires):
	_expand = functools.partial(expand, spec)
	_findall = functools.partial(findall, _WIRE_REGEX)
	names = flatmap(_findall, wires)
	return flatmap(_expand, names)


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
	regex = r"(\b%s\b)" % _BASIC_WIRE_REGEX
	return "".join(map(escape, map(_wire_name, re.split(regex, expr))))


def expand(spec, name):
	_wire_name = functools.partial(wire_name, spec)
	if "?" not in name:
		return [wire_name(spec, name)]
	regex = r"\b%s\b" % name.replace("?", "[0-9]+")
	matches = findall(regex, " ".join(spec["names"]))
	return map(_wire_name, sorted(matches))


def expand_expr(spec, expr):
	_expand = functools.partial(expand, spec)
	names = collections.OrderedDict()
	count = 0
	found = re.findall(_EXPR_REGEX, expr)
	for name in sorted(found, key=len, reverse=True):
		if name and name not in names:
			var = "var%d" % count
			names[name] = var
			expr = expr.replace(name, "{%s}" % var)
			count += 1
	if not names.keys():
		yield expr
		return
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
