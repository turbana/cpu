""" Generate verilog module from encoding searcher results."""

import math
import re
import sys


PARAMETERS = {
    "FD_I":  ("input",  16),
    "R_A":   ("input",  16),
    "R_B":   ("input",  16),
    "D_A":   ("output", 16),
    "D_B":   ("output", 16),
    "D_C":   ("output", 16),
    "D_Ca":  ("output", 1),
    "D_H":   ("output", 1),
    "D_J":   ("output", 1),
    "D_Mr":  ("output", 1),
    "D_Mt":  ("output", 1),
    "D_Mw":  ("output", 1),
    "D_Op":  ("output", 3),
    "D_RFa": ("output", 4),
    "D_RFb": ("output", 4),
    "D_Ra":  ("output", 4),
    "D_Rb":  ("output", 4),
    "D_Rc":  ("output", 4),
    "D_Rd":  ("output", 4),
    "D_S":   ("output", 1),
    "D_SF":  ("output", 3),
    "D_T":   ("output", 1),
}

ALIASES = {
    "I":       ("FD_I", 16),
    "s7imm":   ("{{9{I[12]}}, I[12-:7]}", 16),
    "s8imm":   ("{{8{I[10]}}, I[10-:8]}", 16),
    "s11imm":  ("{{8{I[10]}}, I[10-:11]}", 16),
    "spi":     ("{{12{I[10]}},I[10-:4]}", 16),
    "SPI":     (" (spi[15]) ? spi : spi+1", 16),
    "RFB_I":   (" (I[6]) ? SPI : R_B", 16),
    "D_RFb_I": (" (I[6]) ? 4'b0 : D_RFb", 4),
}


def main(args):
    if len(args) != 1:
        sys.stderr.write("USAGE: %s results.log\n" % sys.argv[0])
        return 2
    filename = args[0]
    data = parse(open(filename))
    emit_module(data)


def parse(stream):
    data = {
        "encoding": {},
        "muxes": {},
        "wires": {},
    }
    clean = lambda val: 0 if val == "X" else val
    for line in section(stream):
        inst, value = line.split("=")
        data["encoding"][inst] = value
    for line in section(stream):
        i = line.find("=")
        name = line[:i].strip()
        mux_def = line[i + 1:].strip()
        mux_def = mux_def.strip()[6:-1].split(",")
        mux_def = dict(val.split("=") for val in mux_def)
        mux = []
        for key, val in sorted(mux_def.items()):
            mux.append(clean(val))
        data["muxes"][name.strip()] = mux
    for line in section(stream):
        name, value = line.split("=")
        if name.startswith("m_"):
            name = name.replace("[", "").replace("]", "")
        data["wires"][name.strip()] = value.strip()
    return data


def section(stream):
    for line in stream:
        line = line.strip()
        if not line:
            raise StopIteration()
        else:
            yield line


def lookup_name(name):
    if "[" not in name:
        return name
    name = name.replace("[", "").replace("]", "")
    i = name.rfind("_")
    return "m_%s_%s" % (name[:i], name[i + 1:])


def lookup_wires(data):
    all_names = set(data["wires"].keys() + data["muxes"].keys() +
                    ALIASES.keys())
    names = set(map(wire_name, all_names))
    _size = lambda n: wire_size(n, all_names)
    return sorted(zip(names, map(_size, names)))


def wire_name(name):
    if "[" not in name:
        return name
    return name.split("[")[0]


def wire_size(name, names):
    def index(n):
        if "[" not in n:
            return 0
        i = n.index("[")
        j = n.index("]")
        return int(n[i + 1:j])
    if name in PARAMETERS:
        return PARAMETERS[name][1]
    match = re.compile("^%s\W" % name).match
    matches = [n for n in names if match(n)]
    if not matches:
        if name in ALIASES:
            return ALIASES[name][1]
        return 1
    return max(index(n) + 1 for n in matches)


def emit_module(data):
    e = sys.stdout.write
    e("`timescale 1 ns / 100 ps\n\n")
    e("module decode_decode (")
    e(",".join(PARAMETERS))
    e(");\n\n")

    e("/* port directions */\n")
    for name, (dir, size) in PARAMETERS.items():
        if dir == "ignore":
            continue
        width = "" if size == 1 else "[%d:0]" % (size - 1)
        e("%s %s %s;\n" % (dir, width, name))

    e("\n/* wires */\n")
    for wire, size in lookup_wires(data):
        width = "" if size == 1 else "[%d:0]" % (size - 1)
        e("wire %s %s;\n" % (width, wire))

    e("\n/* continuous assignments */\n")
    for wire, value in sorted(data["wires"].items()):
        if not value:
            value = "0"
        e("assign %s = %s;\n" % (wire, value))

    e("\n/* aliases */\n")
    for alias, (value, size) in ALIASES.items():
        e("assign %s = %s;\n" % (alias, value))

    e("\n/* muxes */\n")
    for name, mux in sorted(data["muxes"].items()):
        if len(mux) == 1:
            e("assign %s = %s;\n" % (name, mux[0]))
            continue
        lhs = "assign %s = " % name
        join = "\n" + " " * len(lhs)
        bits = int(math.log(len(mux), 2))
        name = name.replace("[", "").replace("]", "")
        var = "{%s}" % ",".join("m_%s_%d" % (name, i)
                                for i in reversed(range(bits)))
        e(lhs)
        e(join.join("(%s == %d) ? %s :" % (var, i, val)
                    # for i, val in enumerate(mux)))
                    for i, val in enumerate(mux)))
        e(" Z;\n")
    e("\nendmodule\n")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
