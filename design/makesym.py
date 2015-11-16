#!/usr/python

"""
Read/Write gschem files (.sch/.sym)
"""

import sys
import re

import schematic

# all measurements are in mils
PIN_HEIGHT = 300
PIN_WIDTH = 300
OUTER_PADDING = 100
INNER_PADDING = 50
BOX_WIDTH = 2500
TEXT_SINK = 50

PIN_COLOR = 5
PIN_SIZE = 10


def main(args):
    if len(args) != 1:
        print "USAGE: %s schematic.sch"
        return 2
    schem = schematic.Schematic(open(args[0]))
    sym = create_symbol(schem)
    sym.save(open(args[0][:-4]+".sym", "w"))


def create_symbol(schem):
    sym = schematic.Schematic()
    ipads = find_pads(schem, "ipad-1.sym")
    opads = find_pads(schem, "opad-1.sym")
    most = max(len(ipads), len(opads))
    top = (most + 1) * PIN_HEIGHT + OUTER_PADDING
    gen_pins(sym, "left", ipads, OUTER_PADDING, top)
    gen_pins(sym, "right", opads, OUTER_PADDING + BOX_WIDTH + 2*PIN_WIDTH, top, len(ipads))
    gen_box(sym, OUTER_PADDING, top)
    #gen_misc(sym, most)
    #print list(ipads)
    #print list(opads)
    return sym


def find_pads(schem, symbol):
    pads = []
    for object in schem:
        if object["type"] == "component" and object["basename"] == symbol:
            for attr in object["attributes"]:
                if attr["text"].startswith("net="):
                    pads.append(attr["text"][4:])
    pads.sort(key=sort_pads_key)
    return pads


def sort_pads_key(name):
    def tryint(s):
        try:
            return int(s)
        except ValueError:
            return s
    parts = re.split('(\D+)', name)
    return map(tryint, parts)


def gen_pins(sym, direction, pads, startx, starty, seq=0):
    dirmod = 1 if direction == "left" else -1
    x = startx
    y = starty
    for net in pads:
        y -= PIN_HEIGHT
        seq += 1
        name = net.split(":")[0].split("_")[-1]
        def gentext(text):
            object = schematic.object("text", x=x+dirmod*(PIN_WIDTH+INNER_PADDING), y=y-TEXT_SINK, color=PIN_COLOR, size=PIN_SIZE, visibility=0, show_name_value=1, angle=0, alignment=0 if direction == "left" else 6, num_lines=1)
            object["text"] = text
            return object
        pin = schematic.object("pin", x1=x, y1=y, x2=x+dirmod*PIN_WIDTH, y2=y, color=1, pintype=0, whichend=0)
        pintype = gentext("pintype=out")
        pinlabel = gentext("pinlabel=" + net)
        pinnumber = gentext("pinnumber=" + name)
        pinnumber["visibility"] = 1
        pinseq = gentext("pinseq=" + str(seq))
        pin["attributes"] = [pintype, pinlabel, pinnumber, pinseq]
        sym.add(pin)


def gen_box(sym, startx, starty):
    box = schematic.object("box", x=OUTER_PADDING+PIN_WIDTH, y=OUTER_PADDING, width=BOX_WIDTH, height=starty-OUTER_PADDING, color=3, widthline=0, capstyle=0, dashstyle=0, dashlength=-1, dashspace=-1, filltype=0, fillwidth=-1, angle1=-1, pitch1=-1, angle2=-1, pitch2=-1)
    sym.add(box)
    # B 400 300 2100 5100 3 0 0 0 -1 -1 0 -1 -1 -1 -1 -1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
