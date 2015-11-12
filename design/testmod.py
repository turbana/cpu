""" Generate test cases for the specified verilog module. """

import sys
import re
import json
import random

import pyparsing as pp


CONFIG_FILE = "tests.json"
TEST_COUNT = 2**8


def main(args):
    if len(args) != 1:
        print "USAGE: %s module.v" % sys.argv[0]
        return 2
    module, wires = parse_module(args[0])
    stream = sys.stdout
    config = parse_config(CONFIG_FILE, module)
    tests = generate_tests(config)
    emit_header(stream, module, wires)
    emit_tests(stream, tests, config["delay"])
    emit_footer(stream, module, wires)


def wire_names(wires):
    for name in wires:
        for n in range(wires[name]["width"]):
            yield "%s%d" % (name, n)


def emit(stream, msg):
    stream.write(msg)


def emit_header(stream, module, wires):
    e = lambda s: emit(stream, s)

    e("`timescale 1 ns / 100 ps\n\n")
    e("module tb_%s;\n\n" % module)

    e("/* component wires */\n")
    for name in wire_names(wires):
        e("wire          %s;\n" % name)

    e("/* test bench wires/registers */\n")
    for name in wires:
        type = "reg" if wires[name]["dir"] == "in" else "wire"
        width = "[%d:0]" % (wires[name]["width"] - 1)
        e("%4s %8s TB_%s;\n" % (type, width, name))
    e("\n")

    e("/* instantiate component */\n")
    e("%s U0 (\n" % module)
    e(",\n".join("  .%s (%s)" % (name, name) for name in wire_names(wires)))
    e(");\n\n")

    e("/* assign test bench wires */\n")
    for name in wires:
        dir = wires[name]["dir"]
        for n in range(wires[name]["width"]):
            full_name = "%s%d" % (name, n)
            index_name = "TB_%s[%d]" % (name, n)
            left = full_name if dir == "in" else index_name
            right = full_name if dir == "out" else index_name
            e("assign %s = %s;\n" % (left, right))
    e("\n")

    e("/* begin test bench */\n")
    e("initial\nbegin\n")
    e('  $dumpfile("wf_%s.vcd");\n' % module)
    e("  $dumpvars;\n")
    return #XXX
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
    e("    $time, " + ", ".join("TB_"+name for name in vars) + ");\n\n")


def emit_footer(stream, module, wires):
    e = lambda s: emit(stream, s)
    e("  /* end test bench */\n")
    e("end\nendmodule\n")


def emit_tests(stream, tests, delay):
    emit(stream, "  /* test cases */\n\n")
    for test in tests:
        emit_test(stream, delay, test)
    return
    emit_test(stream, delay, {
        "inputs": [
            {"name": "TB_ALU_BS_A", "value": int("0100100011011010", 2), "width": 16},
            {"name": "TB_ALU_BS_S", "value": int("0001", 2), "width": 4},
            {"name": "TB_ALU_BS_R", "value": 0, "width": 1},
        ],
        "outputs": [
            {"name": "TB_ALU_BS_D", "value": int("1001000110110100", 2), "width": 16},
        ],
    })
    emit_test(stream, delay, {
        "inputs": [
            {"name": "TB_ALU_BS_A", "value": int("0100100011011010", 2), "width": 16},
            {"name": "TB_ALU_BS_S", "value": int("0001", 2), "width": 4},
            {"name": "TB_ALU_BS_R", "value": 1, "width": 1},
        ],
        "outputs": [
            {"name": "TB_ALU_BS_D", "value": int("0010010001101101", 2), "width": 16},
        ],
    })


def emit_test(stream, delay, test, count=[0]):
    e = lambda s: emit(stream, s)
    # test header
    count[0] += 1
    e("  /* test #%d */\n" % count[0])
    # setup inputs
    for item in test["inputs"]:
        e("  %s = %36s;\n" % (item["name"], binary(item["value"], item["width"])))
    e("  #%d\n" % (delay + 1))
    # check outputs
    check = " || ".join("(%s != %s)" % (item["name"], binary(item["value"], item["width"]))
                        for item in test["outputs"])
    e("  if (%s)\n" % check)
    # display diag info
    e('  begin\n    $display("\\nFAILED TEST #%d");\n' % count[0])
    for item in test["outputs"]:
        e('    $display("%16s=%%36b\\n%16s=%%36s", %s, "%s");\n' % (
            item["name"][3:], "", item["name"], binary_value(item["value"], item["width"])))
    for item in test["inputs"]:
        e('    $display("%16s=%36s");\n' % (item["name"][3:], binary_value(item["value"], item["width"])))
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
    module, all_wires, in_wires, out_wires = grammer().parseFile(filename)
    wires = {}
    split = re.compile("^\\\?([^0-9]*)([0-9]*)$")
    for full_name in all_wires:
        direction = "in" if full_name in list(in_wires) else "out"
        name, width = split.search(full_name).groups()
        if not width: width = "0"
        width = 1 if not width else (int(width) + 1)
        if name not in wires:
            wires[name] = {"dir": direction, "width": width}
        elif wires[name]["width"] < width:
            wires[name]["width"] = width
    return module, wires


def grammer():
    scolon = pp.Suppress(pp.Literal(";"))
    lparen = pp.Suppress(pp.Literal("("))
    rparen = pp.Suppress(pp.Literal(")"))
    module = pp.Suppress(pp.Keyword("module"))
    input  = pp.Suppress(pp.Keyword("input"))
    output = pp.Suppress(pp.Keyword("output"))
    iden   = pp.Word(pp.alphanums + "\\_", pp.alphanums + "_")
    idenlist = pp.delimitedList(iden, delim=",")

    defmod  = module + iden + lparen + pp.Group(idenlist) + rparen + scolon
    defins  = pp.Group(pp.OneOrMore(input + idenlist + scolon))
    defouts = pp.Group(pp.OneOrMore(output + idenlist + scolon))

    g = defmod + defins + defouts
    g.ignore(pp.cStyleComment)
    g.ignore("`" + pp.restOfLine)
    return g


def parse_config(filename, module):
    data = json.loads(open(filename).read())
    return data[module]


def generate_tests(config):
    for _ in range(TEST_COUNT):
        yield generate_test(config)


def randbits(bits):
    return random.randint(0, (2**bits)-1)


def generate_test(config):
    test = {"inputs": [], "outputs": []}
    env = {}
    for name in config["inputs"].keys():
        width = config["inputs"][name]["width"]
        value = randbits(width)
        test["inputs"].append({"value": value, "width": width, "name": "TB_"+name})
        env[name] = value
    for name in config["outputs"].keys():
        width = config["outputs"][name]["width"]
        formula = config["outputs"][name]["formula"]
        formula = "(%s) & %d" % (formula, (2**width)-1)
        value = eval(formula, {}, env)
        test["outputs"].append({"value": value, "width": width, "name": "TB_"+name})
    return test


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
