"""
Update schematic nets from the form A0 to A[0]. This allows us to use gschem's auto text numbering (which doesn't work with A[0]) and also benfit from bus netlisting (which needs A[0]).

Also ensure ipad-2.sym have their net's set
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
    for pad in schem.findall(type="component", basename="[io]pad-2.sym"):
        value = "%s:1" % pad.netlabel
        set_attribute(pad, "refdes", value)
        set_attribute(pad, "net", value)
    schem.save(open(args[1], "w"))


def set_attribute(pad, attr, value):
    try:
        setattr(pad, attr, value)
    except AttributeError:
        new_attr = dict(pad["attributes"][0])
        del new_attr["text"]
        new_attr["visibility"] = 0
        attribute = schematic.object(**new_attr)
        attribute["text"] = "%s=%s" % (attr, value)
        pad["attributes"].append(attribute)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
