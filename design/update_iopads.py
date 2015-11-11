#!/usr/bin/python

"""
Will ensure that any IPAD/OPAD/IOPADs have a net= defined. This is required for
netlisting.
"""

import sys
import os

def main(args):
    if len(args) != 1:
        print "USAGE: %s schematic.sch" % sys.argv[0]
        return 2
    schem = args[0]
    temp = args[0] + ".tmp"
    update(open(temp, "w"), open(schem, "r"))
    os.rename(temp, schem)

def update(new, old):
    component = False
    net = False
    refdes = ""
    x = 0
    y = 0
    for line in old:
        line = line.strip()
        if line == "}":
            if component and not net:
                line = "T %d %d 5 10 0 0 0 0 1\nnet=%s\n%s" % (
                    x+100, y+100, refdes, line)
        elif line.startswith("C"):
            component = line.endswith("pad-1.sym")
            net = False
        elif line.startswith("net="):
            net = True
        elif line.startswith("refdes="):
            refdes = line.split("=")[1]
        elif line.startswith("T"):
            parts = line.split()
            x = int(parts[1])
            y = int(parts[2])
        new.write(line + "\n")

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
