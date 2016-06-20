""" Generate test cases for the specified verilog module. """

import sys
import re
import json
import random

import pyparsing as pp


CONFIG_FILE = "tests.json"
WAVEFORM_DIR = "build/waveforms"
TEST_COUNT = 2**8
SHOW_WAVEFORM = False
DELAY = 1000
MAX_TRIES = 50

DONTCARE = object()
CONFIG_KEYS = ("inputs", "assert", "values")


class FatalTestException(Exception):
    pass


def main(args):
    if len(args) != 1:
        print "USAGE: %s module.v" % sys.argv[0]
        return 2
    module, wires = parse_module(args[0])
    stream = sys.stdout
    config = parse_config(CONFIG_FILE, module)
    try:
        tests = generate_tests(config)
        emit_header(stream, module, wires)
        emit_tests(stream, tests, DELAY)
        emit_footer(stream, module, wires)
    except FatalTestException, e:
        sys.stderr.write(str(e))
        return 1


def emit(stream, msg):
    stream.write(msg)


def emit_header(stream, module, wires):
    e = lambda s: emit(stream, s)

    e("`timescale 1 ns / 100 ps\n\n")
    e("module tb_%s;\n\n" % module)

    e("/* test bench wires/registers */\n")
    for name in sorted(wires):
        type = "reg" if wires[name]["dir"] == "in" else "wire"
        width = "[%d:0]" % (wires[name]["width"] - 1)
        e("%4s %8s %s;\n" % (type, width, name))
    if "_CLK" not in wires:
        e("reg _CLK = 0;\n")
    e("\n")

    e("/* instantiate component */\n")
    e("%s U0 (\n" % module)
    e(",\n".join("  .%s (%s)" % (name, name) for name in wires))
    e(");\n\n")

    e("/* test bench variables */\n")
    e("integer _TB_ERRORS;\n")
    e("integer _TB_DONE = 0;\n")
    e("integer _TB_TEST_ID;\n")
    e("\n")

    e("/* setup clock */\n")
    e("always #%s _CLK = ~_CLK;\n" % (DELAY/8))
    e("\n")

    e("/* begin test bench */\n")
    e("initial\nbegin\n")
    e('  $dumpfile("%s/%s.vcd");\n' % (WAVEFORM_DIR, module))
    e("  $dumpvars;\n")
    e("  _TB_ERRORS = 0;\n")
    e("  _TB_TEST_ID = 0;\n")
    e("  _CLK = 0;\n")
    if not SHOW_WAVEFORM: return
    vars = wires.keys()
    maxlen = max([max(wires[name]["width"], len(name)) for name in vars])
    fmt = "%%%ds" % maxlen
    bfmt = "%%%db" % maxlen
    e('  $display("                time ')
    e(" ".join(fmt % name for name in vars))
    e('");\n')
    e('  $monitor("%d ')
    e(" ".join(bfmt for _ in vars))
    e('",\n')
    e("    $time, " + ", ".join(name for name in vars) + ");\n\n")


def emit_footer(stream, module, wires):
    e = lambda s: emit(stream, s)
    e("  /* end test bench */\n")
    e("  if (_TB_ERRORS > 0)\n")
    e("  begin\n")
    e('    $display("\\nFAILURE %%1d error(s) testing %s", _TB_ERRORS);\n' % module)
    e("  end\n")
    e("  $finish;\n")
    e("end\nendmodule\n")


def emit_tests(stream, tests, delay):
    emit(stream, "  /* test cases */\n\n")
    for test in tests:
        emit_test(stream, delay, test)


def emit_test(stream, delay, test, count=[0]):
    e = lambda s: emit(stream, s)
    # test header
    count[0] += 1
    e("  /* test #%d */\n" % count[0])
    e("  _TB_TEST_ID = %d;\n" % count[0])
    # setup inputs
    for item in sorted(test["inputs"]):
        e("  %8s = %36s;\n" % (item["name"], binary(item["value"], item["width"])))
    e("  #%d\n" % (delay + 1))
    # check outputs
    check = " || ".join("(%s !== %s)" % (item["name"], binary(item["value"], item["width"]))
                        for item in test["outputs"])
    e("  if (%s)\n" % check)
    # display diag info
    e('  begin\n    $display("\\nFAIL (test #%d)");\n' % count[0])
    e("    _TB_ERRORS = _TB_ERRORS + 1;\n")
    for item in sorted(test["outputs"]):
        e('    $display("%16s=%%36b\\n%16s=%%36s", %s, "%s");\n' % (
            item["name"], "Expected", item["name"], binary_value(item["value"], item["width"])))
    for item in sorted(test["inputs"]):
        e('    $display("%16s=%36s");\n' % (item["name"], binary_value(item["value"], item["width"])))
    e("  end\n\n")


def binary(n, width):
    val = bin(n)[2:].zfill(width)
    return "%d'b%s" % (width, val)


def binary_value(n, width):
    return bin(n)[2:].zfill(width)


def notequal(var, width, value):
    return " || ".join("%s[%d] != %d" % (var, n, (value >> n) & 1) for n in range(width))
    msg = ""
    for n in range(width):
        cond = "%s[%d] != %d" % (var, n, (value >> n) & 1)


def parse_module(filename):
    module, params, all_wires = grammer().parseFile(filename)
    def make_wire(wire, dir):
        if len(wire) == 2:
            return wire[1], {"width": wire[0], "dir": dir}
        else:
            return wire[0], {"width": 1, "dir": dir}
    wires = {}
    for wire in all_wires:
        if len(wire) == 3:
            dir, width, name = wire
        else:
            dir, name = wire
            width = 1
        wires[name] = {"width": width, "dir": "in" if dir=="input" else "out"}
    return module, wires


def grammer():
    colon  = pp.Suppress(pp.Literal(":"))
    scolon = pp.Suppress(pp.Literal(";"))
    lparen = pp.Suppress(pp.Literal("("))
    rparen = pp.Suppress(pp.Literal(")"))
    lbrack = pp.Suppress(pp.Literal("["))
    rbrack = pp.Suppress(pp.Literal("]"))
    module = pp.Suppress(pp.Keyword("module"))
    input  = pp.Keyword("input")
    output = pp.Keyword("output")
    num    = pp.Word(pp.nums).addParseAction(lambda s,l,t: int(t[0]))
    width  = (lbrack + num + colon + num + rbrack).setParseAction(lambda s,l,t: t[0]+1)
    iden   = pp.Word(pp.alphanums + "\\_", pp.alphanums + "_")
    idenlist = pp.delimitedList(iden, delim=",")

    def check_module(s,l,t):
        if t[0] == '\\not':
            raise pp.ParseException(s, l, "Error parsing module definition. Ensure the schematic has a module_name= attribute defined")
    mod_iden = iden.copy()
    mod_iden.addParseAction(check_module)

    defmod  = module + mod_iden + lparen + pp.Group(idenlist) + rparen + scolon
    wires  = pp.Group(pp.OneOrMore(pp.Group((input | output) + pp.Optional(width) + iden) + scolon))

    g = defmod + wires
    g.ignore(pp.cStyleComment)
    g.ignore("`" + pp.restOfLine)
    return g


def parse_config(filename, module):
    data = json.loads(open(filename).read())
    expand_config(data, module)
    return data[module]


def expand_config(data, module):
    parent = data.get(module, {})
    parent["name"] = module
    data[module] = parent
    depth = module.count("_")
    children = [name for name in data if name.startswith(module) and name.count("_") == depth+1]
    for child_name in children:
        expand_config(data, child_name)
        child = data[child_name]
        config_merge_inputs(parent, child)
        config_merge_assert(parent, child)
        config_merge_values(parent, child)


def config_merge_inputs(left, right):
    lvalue = left.get("inputs", {})
    rvalue = right.get("inputs", {})
    for rkey in rvalue.keys():
        if rkey not in lvalue:
            lvalue[rkey] = rvalue[rkey]
        elif lvalue[rkey] != rvalue[rkey]:
            name = "%s.%s" % (key, rkey)
            raise FatalTestException("Config mis-match found for %s in %s and %s" % (name, left["name"], right["name"]))
    left["inputs"] = lvalue


def config_merge_assert(left, right):
    # only merge string if parent doesn't have it and child does
    if "assert" not in left and "assert" in right:
        left["assert"] = right["assert"]


def config_merge_values(left, right):
    # strip width from child formulas as we don't want to export child values to test bench
    rvalues = []
    for formula in right.get("values", []):
        name, width, expr = parse_formula(formula)
        rvalues.append("%s = %s" % (name, expr))
    left["values"] = rvalues + left.get("values", [])


def generate_tests(config):
    for _ in range(TEST_COUNT):
        yield generate_test(config)


def randbits(bits):
    return random.randint(0, (2**bits)-1)


def generate_test(config, _count=0):
    test = {"inputs": [], "outputs": []}
    env = {"DONTCARE": DONTCARE}
    # generate inputs
    for name in config.get("inputs", {}).keys():
        width = config["inputs"][name]["width"]
        alias = config["inputs"][name].get("alias", None)
        value = randbits(width)
        test["inputs"].append({"value": value, "width": width, "name": name})
        env[name] = value
        if alias:
            env[alias] = value
    # check assertions
    if "assert" in config:
        if not eval(config["assert"], {}, env):
            return generate_test(config)
    # evaluate values
    for formula in config["values"]:
        name, export_width, expr = parse_formula(formula)
        value = eval_formula(expr, env, config["name"], export_width)
        env[name] = value
        # don't add condition when result is a don't care
        if value is DONTCARE:
            continue
        if export_width:
            test["outputs"].append({"value": value, "width": export_width, "name": name})
    # generate a new test if we only had don't cares
    if not test["outputs"]:
        if _count == MAX_TRIES:
            raise FatalTestException("Exceeded MAX_TRIES (%d) attempts for %s" % (MAX_TRIES, config["name"]))
        return generate_test(config, _count+1)
    return test


def parse_formula(formula):
    parts = formula.split("=")
    if ":" in parts[0]:
        name, width = parts[0].split(":")
        width = int(width)
    else:
        name = parts[0].strip()
        width = None
    return name, width, "=".join(parts[1:])


def eval_formula(formula, env, name, width=None):
    try:
        value = eval(formula, {}, env)
        # if we have an actual value constrain it to it's width
        if value is not DONTCARE and width is not None:
            formula = "(%s) & %d" % (value, (2**width)-1)
            value = eval(formula, {}, env)
    except Exception, e:
        message = "Error evaluating formula for %s: %s\n" % (name, formula)
        message += str(e) + "\n"
        raise FatalTestException(message)
    return value


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
