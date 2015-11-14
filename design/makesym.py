#!/usr/python

"""
Create a .sym file from an .sch schematic
"""

import sys
import pprint

import pyparsing as pp

# http://wiki.geda-project.org/geda:file_format_spec
SCH_FORMAT = {
    "v": "version i:version i:fileformat_version",
    "C": "component i:x i:y u:selectable i:angle i:mirror s:basename",
    "T": "text i:x i:y i:color i:size i:visibility i:show_name_value i:angle i:alignment i:num_lines",
    "N": "net i:x1 i:y1 i:x2 i:y2 i:color",
}

TYPE_INTEGER = "i"
TYPE_STRING = "s"
ATTRIBUTES_START = "{"
ATTRIBUTES_END = "}"


class ParseError(Exception):
    pass


def main(args):
    if len(args) != 1:
        print "USAGE: %s schematic.sch" % sys.argv[0]
        return 2
    sch = args[0]
    parts = parse(open(sch))
    pprint.pprint(parts)


def parse(stream):
    objects = []
    try:
        while True:
            line = stream.next()
            parts = line.split()
            if parts[0] == ATTRIBUTES_START:
                objects[-1]["attributes"] = parse(stream)
            elif parts[0] == ATTRIBUTES_END:
                return objects
            else:
                object = parse_line(parts)
                if object["type"] == "text":
                    text = ""
                    for _ in range(object["num_lines"]):
                        text += stream.next()
                    object["text"] = text[:-1]
                objects.append(object)
    except StopIteration:
        pass
    return objects


def parse_line(parts):
    type = parts[0]
    if type not in SCH_FORMAT:
        raise ParseError("Unknown object: " + parts[0])
    format = SCH_FORMAT[type].split()
    if len(parts) != len(format):
        raise ParseError("Item count for object %s (%d) did not match definition (%s)" % (format[0], len(parts), len(format)))
    object = {"type": format[0]}
    for fmt, value in zip(format[1:], parts[1:]):
        type, name = fmt.split(":")
        if type == TYPE_INTEGER:
            value = int(value)
        object[name] = value
    return object


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
