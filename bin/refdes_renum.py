""" Renumber refdes found in schematic files. """

import sys
import re
import os.path

import schematic


SYMBOL_PATH = "design/symbols/74xxx"


def main(args):
	if not args:
		print "USAGE: %s [--overwrite] schem.sch [..schem.sch]" % sys.argv[0]
		print "Renames all U? refdes found in schematics."
		print "  --overwrite renames all refdes"
		return 2
	overwrite = False
	if args[0] == "--overwrite":
		overwrite = True
		args = args[1:]
	schems = map(schematic.Schematic, map(open, args))
	all_components = map(components, schems)
	if overwrite:
		rename = [filter(refdes_set, cs) for cs in all_components]
		named = []
	else:
		rename = [filter(refdes_blank, cs) for cs in all_components]
		invert = lambda f: lambda *args, **kwargs: not f(*args, **kwargs)
		named = flatten(filter(refdes_set, cs) for cs in all_components)
	seq = refdes_sequence(named)
	for i,comps in enumerate(rename):
		set_refdes(comps, seq)
	for schem, filename in zip(schems, args):
		schem.save(open(filename, "w"))


def set_refdes(comps, seq):
	letters = "ABCDEFGH"
	while comps:
		comp = comps.pop(0)
		refdes = seq.next()
		slots = slot_count(comp.device)
		if slots in (0, 1):
			comp.refdes = refdes
		else:
			comp.refdes = refdes + letters[0]
			comp.slot = 1
			others = find(comps, comp.device, slots-1)
			for i, comp in enumerate(others):
				comps.remove(comp)
				comp.slot = i+2
				comp.refdes = refdes + letters[i+1]


def slot_count(device, _cache={}):
	if device in _cache: return _cache[device]
	filename = os.path.join(SYMBOL_PATH, device+"-1.sym")
	schem = schematic.Schematic(open(filename))
	attr = schem.findall(text="numslots").next()
	slots = int(attr["text"].split("=")[-1])
	_cache[device] = slots
	return slots


def find(comps, device, count):
	result = []
	for comp in comps:
		if count == 0: break
		if comp.device == device:
			result.append(comp)
			count -= 1
	return result


def refdes_sequence(named):
	high = 0
	if named:
		regex = re.compile("U([0-9]*)")
		names = map(regex.search, map(refdes, named))
		high = max(int(r.groups()[0]) for r in names if r is not None)
	while True:
		high += 1
		yield "U%d" % high


def components(schem):
	return filter(refdes, schem)


def flatten(lists):
	result = []
	map(result.extend, lists)
	return result


def refdes(component):
	return getattr(component, "refdes", "")


def refdes_blank(component):
	return refdes(component) == "U?"


def refdes_set(component):
	name = refdes(component)
	return name.startswith("U") and name != "U?"


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
