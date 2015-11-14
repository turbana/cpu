#!/usr/python

"""
Create a .sym file from an .sch schematic
"""

import sys
import pprint

import pyparsing as pp


def main(args):
    if len(args) != 1:
        print "USAGE: %s schematic.sch" % sys.argv[0]
        return 2
    sch = args[0]
    parts = parse(open(sch))
    pprint.pprint(parts)


def parse(sch):
    g = sch_grammer()
    result = g.parseFile(sch)
    return {
        "version": result["version"],
        "components": [x.asDict() for x in result["components"]]
    }


def sch_grammer():
    replace = lambda g,x: g.setParseAction(lambda s,l,t: x)
    type = lambda s,t: replace(pp.Literal(s), t).setResultsName("type")
    v = type("v", "version")
    c = type("C", "component")
    t = type("T", "text")
    n = type("N", "net")
    eol = pp.Suppress(pp.LineEnd())
    num = lambda n: pp.Word(pp.nums).setParseAction(lambda s,l,t: int(t[0])).setResultsName(n)
    text = lambda n: pp.Word(pp.printables).setResultsName(n)
    items = pp.Forward()
    attributes = pp.Suppress("{") + eol + pp.Group(pp.OneOrMore(items)) + pp.Suppress("}") + eol
    def item(n, g):
        g = pp.Group(g + eol + pp.Optional(attributes)).setResultsName(n)
        items << g
        return g

    version = item("version", v + num("version") + num("format"))
    component = item("component", c + num("x") + num("y") + num("selectable") + num("angle") + num("mirror") + text("basename"))
    textitem = item("text", t + num("x") + num("y") + num("color") + num("size")
                    + num("visibility") + num("show_name_value") + num("angle")
                    + num("alignment") + num("num_lines"))

    return version + pp.Group(pp.OneOrMore(items)).setResultsName("components")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
