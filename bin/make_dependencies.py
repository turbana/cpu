"""
Generate hierarchical Makefile dependencies for a list of schematics.

A hierarchy is defined by underscores. Example:
execute_forward_a -> 7486, 7408
execute_forward_b -> 7486, 7432
--
execute_forward   -> 7486, 7408, 7432
execute           -> 7486, 7408, 7432
"""

import collections
import sys
import os.path
import json

import schematic

TESTS_CONFIG = "etc/test-cases.json"
CLOCK_SCH = "design/clock.sch"
CLOCK_SCH_FILENAME = "design/schem/clock.sch"
IGNORE_CHIPS = ["busripper", "ipad", "opad", "iopad", "gnd"]


def main(args):
    if len(args) == 0:
        print "USAGE: %s schematics..." % sys.argv[0]
        return 2
    config = json.loads(open(TESTS_CONFIG).read())
    deps = collections.defaultdict(set)
    schem_args = [fn for fn in args if fn.endswith(".sch")]
    verilog_args = [fn for fn in args if fn.endswith(".v")]
    schems = {base(fn): dependencies(fn) for fn in schem_args}
    verilogs = {base(fn): vdependencies(fn) for fn in verilog_args}
    expand(schems)
    add_schematics(deps, schems, schem_args, config)
    add_verilog(deps, verilogs, schems)
    emit_deps(sys.stdout, deps)


def emit_deps(stream, deps):
    for mod, mod_deps in sorted(deps.items()):
        if mod == "ALL_SCHEM_TESTS":
            continue
        stream.write("$(BUILD_DIR)/%s: " % mod)
        stream.write(" ".join("$(BUILD_DIR)/%s" % x for x in sorted(mod_deps)))
        stream.write("\n")
    stream.write("ALL_SCHEM_TESTS := $(ALL_SCHEM_TESTS) ")
    stream.write(" ".join("$(WF_DIR)/%s" % x for x in deps["ALL_SCHEM_TESTS"]))
    stream.write("\n")


def add_deps(deps, name, values):
    deps[name] |= set(values)


def add_dep(deps, name, value):
    add_deps(deps, name, [value])


def base(fn):
    return os.path.basename(fn).replace(".sch", "").replace(".v", "")


def add_schematics(deps, schems, args, config):
    for mod, mod_deps in schems.items():
        mod_test = "test_%s" % mod
        mod_v = "%s.v" % mod
        add_deps(deps, mod_test, ["%s.v" % fn for fn in mod_deps])
        schem_deps = schematics(mod, map(base, args))
        if schem_deps:
            add_deps(deps, mod_v, ["%s.sch" % fn for fn in schem_deps])
        else:
            add_dep(deps, mod_v, "%s.sch" % mod)
        if mod in config:
            add_dep(deps, "ALL_SCHEM_TESTS", "%s.vcd" % mod)


def add_verilog(deps, verilogs, schems):
    for mod, mod_deps in verilogs.items():
        mod_test = "test_%s" % mod
        add_deps(deps, mod_test, ["%s.v" % x for x in mod_deps])
        for mod_dep in mod_deps:
            sub_deps = deps["test_%s" % mod_dep]
            add_deps(deps, mod_test, sub_deps)


def schematics(key, keys):
    return [k for k in keys if k.startswith(key) and k != key]


def expand(deps):
    for name in deps.keys():
        parts = name.split("_")
        for i in range(len(parts)):
            part = "_".join(parts[:i + 1])
            if part not in deps:
                deps[part] = set()
            deps[part] |= deps[name]


def dependencies(filename):
    schem = schematic.Schematic(open(filename))
    devices = set(c.device for c in schem.findall(type="component",
                                                  attr="device=")
                  if c.device not in ["none", "IPAD", "OPAD", "IOPAD"])
    if filename != CLOCK_SCH_FILENAME:
        devices |= dependencies(CLOCK_SCH_FILENAME)
    return devices


def vdependencies(filename):
    data = open(filename).readlines()
    decls = [line for line in data if line.endswith("(\n")]
    return set(line.split()[0] for line in decls)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
