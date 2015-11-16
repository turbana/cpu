#!/usr/python

"""
Read/Write gschem files (.sch/.sym)
"""

import sys
import pprint

# http://wiki.geda-project.org/geda:file_format_spec
SCH_FORMAT = {
    "v": "version i:version i:fileformat_version",
    "C": "component i:x i:y u:selectable i:angle i:mirror s:basename",
    "T": "text i:x i:y i:color i:size i:visibility i:show_name_value i:angle i:alignment i:num_lines",
    "N": "net i:x1 i:y1 i:x2 i:y2 i:color",
    "B": "box i:x i:y i:width i:height i:color i:widthline i:capstyle i:dashstyle i:dashlength i:dashspace i:filltype i:fillwidth i:angle1 i:pitch1 i:angle2 i:pitch2",
    "P": "pin i:x1 i:y1 i:x2 i:y2 i:color i:pintype i:whichend",
}

TYPE_INTEGER = "i"
TYPE_STRING = "s"
ATTRIBUTES_START = "{"
ATTRIBUTES_END = "}"


class SchematicParseError(Exception):
    pass


class Schematic(list):
    def __init__(self, stream=None):
        objects = _parse(stream) if stream else []
        super(Schematic, self).__init__(objects)



def _parse(stream):
    objects = []
    try:
        while True:
            line = stream.next()
            parts = line.split()
            if parts[0] == ATTRIBUTES_START:
                objects[-1]["attributes"] = _parse(stream)
            elif parts[0] == ATTRIBUTES_END:
                return objects
            else:
                object = _parse_line(parts)
                if object["type"] == "text":
                    text = ""
                    for _ in range(object["num_lines"]):
                        text += stream.next()
                    object["text"] = text[:-1]
                objects.append(object)
    except StopIteration:
        pass
    return objects


def _parse_line(parts):
    type = parts[0]
    if type not in SCH_FORMAT:
        raise SchematicParseError("Unknown object: " + parts[0])
    format = SCH_FORMAT[type].split()
    if len(parts) != len(format):
        raise SchematicParseError("Item count for object %s (%d) did not match definition (%s)" % (format[0], len(parts), len(format)))
    object = {"type": format[0]}
    for fmt, value in zip(format[1:], parts[1:]):
        type, name = fmt.split(":")
        if type == TYPE_INTEGER:
            value = int(value)
        object[name] = value
    return object


def main(args):
    if len(args) != 1:
        print "USAGE: %s schematic.sch" % sys.argv[0]
        return 2
    sch = args[0]
    parts = Schematic(open(sch))
    pprint.pprint(parts)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
