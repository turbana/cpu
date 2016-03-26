#!/usr/bin/python

"""
Fixes verilog code generated by the netlister.
  1. Changes Vcc/GND from wires into supply1/supply0 respectively
  2. Suppresses identical input declarations for modules
  3. Set module name (numbered modules have ic prepended [7408 -> ic7408])
  4. Set module parameters (for multi-schematics: inputs that match outputs are not generated as module parameters)
  5. Ensure the width of wires match the module input width (the netlister only generates wires to the width that it needs to generate the circuit; if we use fewer wires than the input is declared as we get a mis-match)
"""

import sys
import StringIO
import os.path
import schematic
import itertools


class NetlistException(Exception):
    pass


def main(args):
    try:
        if len(args) < 2:
            print "USAGE: %s module.v module.sch [module2.sch...]" % sys.argv[0]
            print "Fixes netlisted verilog code"
            return 2
        filename = args[0]
        schems = map(schematic.Schematic, map(open, args[1:]))
        modname = os.path.basename(filename[:-2])
        out_stream = StringIO.StringIO()
        with open(filename) as in_stream:
            fixup(in_stream, out_stream, modname, schems)
        out_stream.seek(0)
        with open(filename, "w") as new_stream:
            map(new_stream.write, out_stream)
    except NetlistException, e:
        print "ERROR: %s {%s}" % (str(e), " ".join(args))
        return 1


def fixup(in_stream, out_stream, modname, schems):
    wires = parse_wires(schems)
    if modname[0] in "0123456789":
        modname = "ic" + modname
    for line in in_stream:
        if line.startswith("module"):
            ignore_module(in_stream)
            emit_module(out_stream, modname, wires)
        elif line == "/* Wires from the design */\n":
            out_stream.write(line)
            emit_wires(in_stream, out_stream, wires)
        elif line == "/* Package instantiations */\n":
            out_stream.write(line)
            emit_instantiations(in_stream, out_stream)
        else:
            out_stream.write(line)


def ignore_module(stream):
    port_dirs = False
    for line in stream:
        if line == "/* Port directions begin here */\n":
            port_dirs = True
        elif line == "\n" and port_dirs:
            break


def emit_module(stream, name, wires):
    names = [wire[0] for wire in wires]
    stream.write("module %s (\n\t" % name)
    stream.write(",\n\t".join(names))
    stream.write("\n);\n\n\n")
    stream.write("/* Port directions begin here */\n")
    for name, width, direction in wires:
        stream.write("%s %s %s ;\n" % (direction, width, name))
    stream.write("\n")


def emit_wires(in_stream, out_stream, wires):
    wires = {w[0]: dict(zip(["name", "width", "direction"], w)) for w in wires}
    for line in in_stream:
        if line == "\n":
            out_stream.write(line)
            return
        name = line.split()[-2]
        if name == "Vcc":
            out_stream.write("supply1 Vcc ;\n")
        elif name == "GND":
            out_stream.write("supply0 GND ;\n")
        elif name in wires:
            out_stream.write("wire %(width)s %(name)s ;\n" % wires[name])
        else:
            out_stream.write(line)


def emit_instantiations(in_stream, out_stream):
    written = set()
    for line in in_stream:
        if line.endswith(" ( \n"):
            out_stream.write(line)
            written = set()
        elif line.endswith(" );\n"):
            out_stream.write(",\n".join(written))
            out_stream.write("\n);\n\n")
        else:
            written.add(line.strip(",\n"))
        if line == "endmodule\n":
            out_stream.write(line)
            return


def parse_wires(schems):
    wires = set()
    def clean_name(pad):
        name = pad.netlabel
        return name.split("[")[0] if "[" in name else name
    def clean_width(pad):
        name = clean_name(pad)
        width = pad.netlabel.replace(name, "")
        return width
        return 0 if not width else int(width)
    # read all wires
    for schem in schems:
        for pad in schem.findall(basename="[io]pad-[12].sym"):
            name = clean_name(pad)
            width = clean_width(pad)
            direction = "input" if pad.device == "IPAD" else "output"
            wires.add((name, width, direction))
    # check matching wires
    for name, width, direction in list(wires):
        opp_direction = "input" if direction == "output" else "output"
        opposite = (name, width, opp_direction)
        if opposite in wires:
            wires.remove(opposite)
    # check for width mis-match
    key_name = lambda wire: wire[0]
    key_width = lambda wire: wire[1]
    wire_list = sorted(wires, key=key_name)
    for name, widths in itertools.groupby(wire_list, key_name):
        widths = list(widths)
        if len(widths) > 1:
            raise NetlistException("Width mis-match found for %s: %s" % (name, ", ".join(map(key_width, widths))))
    return wires


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
