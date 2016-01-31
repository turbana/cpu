"""
Update schematic nets from the form A0 to A[0]. This allows us to use gschem's auto text numbering (which doesn't work with A[0]) and also benfit from bus netlisting (which needs A[0]).
"""

import sys
import schematic


def main(args):
    if len(args) != 2:
        print "USAGE: %s module.sch output.sch" % sys.argv[0]
        print "Updates schemtic wires from X0 to X[0] to facilitate netlisting"
        return 2
    schem = schematic.Schematic(open(args[0]))
    for pad in schem.findall(type="component", basename="[io]pad-1.sym"):
        name = pad.netlabel.split("[")[0]
        search = "netname=%s[0-9]+" % name
        for net in schem.findall(type="net", attr=search):
            num = net.netname[len(name):]
            net.netname = "%s[%s]" %  (name, num)
    schem.save(open(args[1], "w"))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
