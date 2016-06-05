"""
Generate hierarchical Makefile dependencies for a list of schematics.

A hierarchy is defined by underscores. Example:
execute_forward_a -> 7486, 7408
execute_forward_b -> 7486, 7432
--
execute_forward   -> 7486, 7408, 7432
execute           -> 7486, 7408, 7432
"""

import sys
import os.path

import schematic

#$(BUILD)/execute_forward.v: $(BUILD)/execute_forward_a.sch $(BUILD)/execute_forward_b.sch $(BUILD)/execute_forward_c.sch

def main(args):
	if len(args) == 0:
		print "USAGE: %s schematics..." % sys.argv[0]
		return 2
	filename = args[0]
	base = os.path.basename(filename).replace(".sch", "")
	base = lambda fn: os.path.basename(fn).replace(".sch", "")
	deps = {base(fn): dependencies(fn) for fn in args}
	expand(deps)
	# print chip dependencies
	for key in deps:
		_deps = " ".join("$(BUILD)/%s.v" % x for x in deps[key])
		print "$(BUILD)/test_%s: %s" % (key, _deps)
	# print schematic dependencies
	for key in deps:
		_deps = " ".join("$(BUILD)/%s.sch" % x for x in schematics(key, map(base, args)))
		if _deps:
			print "$(BUILD)/%s.v: %s" % (key, _deps)
		else:
			print  "$(BUILD)/%s.v: $(BUILD)/%s.sch" % (key, key)


def schematics(key, keys):
	return [k for k in keys if k.startswith(key) and k != key]


def expand(deps):
	for name in deps.keys():
		parts = name.split("_")
		for i in range(len(parts)):
			part = "_".join(parts[:i+1])
			if part not in deps:
				deps[part] = set()
			deps[part] |= deps[name]


def dependencies(filename):
	schem = schematic.Schematic(open(filename))
	components = set(c["basename"] for c in schem.findall(type="component"))
	clean = lambda s: s.replace("-1.sym", "").replace("-2.sym", "")
	chips = set(clean(c) for c in components if c.startswith("74"))
	return chips


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
