""" Generate Makefile dependencies for a schematic """

import sys
import os.path

import schematic


def main(args):
	if len(args) != 1:
		print "USAGE: %s schematic" % sys.argv[0]
		return 2
	filename = args[0]
	base = os.path.basename(filename).replace(".sch", "")
	schem = schematic.Schematic(open(filename))
	components = set(c["basename"] for c in schem.findall(type="component"))
	clean = lambda s: s.replace("-1.sym", "").replace("-2.sym", "")
	chips = set(clean(c) for c in components if c.startswith("74"))
	deps = " ".join("$(BUILD)/%s.v" % c for c in chips)
	make = "$(BUILD)/test_%s : %s\n" % (base, deps)
	make += "DEPS_%s := %s\n" % (base, deps)
	print make


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
