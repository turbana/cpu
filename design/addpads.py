#!/usr/bin/python

"""
Add pads to a schematic
"""

import sys

import schematic

# text attributes
SIZE = 10
COLOR = 5
X = 0
Y = 0

PAD_WIDTH = 900

OFFSET = 300
PADDING_X = 0
PADDING_Y = 100


def main(args):
    if len(args) < 2:
        print "USAGE: %s schematic.sch [--short] [ipad|opad]:name:bits ([ipad|opad]:name:bits).." % sys.argv[0]
        print "Creates ipads/opads in schematic.sch for every bit defined"
        print "  --short Generate short pin names (ex ALU_BS_SA0 -> SA0)"
        return 2
    sch = args[0]
    names = []
    gen_short = False
    for spec in args[1:]:
        if spec == "--short":
            gen_short = True
            continue
        if spec.count(":") != 2:
            print "ERROR: pads must be of the format: [ipad|opad]:name:bits"
            return 2
        dir, name, width = spec.split(":")
        if dir not in ("ipad", "opad"):
            print "ERROR: Unknown pad type: %s" % dir
            return 2
        names.extend(gen_names(name, dir, int(width), gen_short))
    schem = schematic.Schematic(open(sch))
    gen_pads(schem, names)
    schem.save(open(sch, "w"))


def gen_names(name, dir, width, gen_short):
    for n in reversed(range(width)):
        full = "%s%d:1" % (name, n)
        short = full[:-2]
        if gen_short:
            short = "%s%d" % (name[name.rfind("_")+1:], n)
        if width == 1:
            short = short[:-1]
        yield dir, full, short


def gen_pads(schem, names):
    count = 0
    def text(x, y, str, align, vis):
        obj = schematic.object("text", x=x, y=y, color=COLOR, size=SIZE, visibility=vis, show_name_value=1, angle=0, alignment=align, num_lines=1)
        obj["text"] = str
        return obj
    for dir, name, short in names:
        symbol = "%s-2.sym" % dir
        padx = X
        pady = Y + count*OFFSET
        textx = (padx + PADDING_X) if dir == "ipad" else (PAD_WIDTH - PADDING_X)
        texty = pady + PADDING_Y
        textalign = 1 if dir == "ipad" else 7
        component = schematic.object("component", x=0, y=pady, selectable=1, angle=0, mirror=0, basename=symbol)
        component["attributes"] = [
            text(textx, texty, "device=%s" % dir.upper(), textalign, vis=0),
            text(textx, texty, "net=%s" % name, textalign, vis=0),
            text(textx, texty, "refdes=%s" % short, textalign, vis=1),
        ]
        schem.add(component)
        count += 1


def gen_pads_old(schem, names):
    symbol = "%s-2.sym" % dir
    objx = X+PADDING_X if dir == "ipad" else PAD_WIDTH-PADDING_X
    align = 1 if dir == "ipad" else 7
    def text(y, str, vis):
        obj = schematic.object("text", x=objx, y=y+PADDING_Y, color=COLOR, size=SIZE, visibility=vis, show_name_value=1, angle=0, alignment=align, num_lines=1)
        obj["text"] = str
        return obj
    for n,name in enumerate(names):
        short_name = name[name.rfind("_")+1:-2]
        cury = Y + n*OFFSET
        component = schematic.object("component", x=0, y=cury, selectable=1, angle=0, mirror=0, basename=symbol)
        component["attributes"] = [
            text(cury, "device=%s" % dir.upper(), vis=0),
            text(cury, "refdes=%s" % short_name, vis=1),
            text(cury, "net=%s" % name, vis=0)
        ]
        schem.add(component)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
