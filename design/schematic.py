import sys
import pprint
import re

# http://wiki.geda-project.org/geda:file_format_spec
SCH_FORMAT = {
    "v": "version i:version i:fileformat_version",
    "C": "component i:x i:y u:selectable i:angle i:mirror s:basename",
    "T": "text i:x i:y i:color i:size i:visibility i:show_name_value i:angle i:alignment i:num_lines",
    "N": "net i:x1 i:y1 i:x2 i:y2 i:color",
    "B": "box i:x i:y i:width i:height i:color i:widthline i:capstyle i:dashstyle i:dashlength i:dashspace i:filltype i:fillwidth i:angle1 i:pitch1 i:angle2 i:pitch2",
    "P": "pin i:x1 i:y1 i:x2 i:y2 i:color i:pintype i:whichend",
    "U": "bus i:x1 i:y1 i:x2 i:y2 i:color i:ripperdir",
}
OBJECT_MAP = {fmt.split()[0]:key for key,fmt in SCH_FORMAT.items()}


TYPE_INTEGER = "i"
TYPE_STRING = "s"
ATTRIBUTES_START = "{"
ATTRIBUTES_END = "}"


class SchematicException(Exception):
    pass

class SchematicParseError(SchematicException):
    pass


class Schematic(list):
    def __init__(self, stream=None):
        if stream:
            objects = _parse(stream)
        else:
            objects = [object("version", version=20110115, fileformat_version=2)]
        super(Schematic, self).__init__(objects)

    def save(self, stream):
        _emit_objects(stream, self)

    def add(self, object):
        self.append(object)

    def findall(self, attr=None, **kwargs):
        terms = [(k, re.compile(v)) for k,v in kwargs.items()]
        for object in self:
            match_terms = True
            for attribute, regex in terms:
                if attribute in object and regex.search(object[attribute]):
                    continue
                match_terms = False
                break
            if match_terms:
                if attr:
                    regex = re.compile(attr)
                    for attribute in object.get("attributes", []):
                        if regex.search(attribute["text"]):
                            yield object
                else:
                    yield object


class SchematicObject(dict):
    def __getattr__(self, item):
        for attr in self.get("attributes", []):
            name, value = attr["text"].split("=")
            if name == item:
                return value
        raise AttributeError("'SchematicObject' object has no attribute '%s'" % item)

    def __setattr__(self, item, value):
        for attr in self.get("attributes", []):
            name = attr["text"].split("=")[0]
            if name == item:
                attr["text"] = "%s=%s" % (name, str(value))
                return attr["text"]
        raise AttributeError("'SchematicObject' object has no attribute '%s'" % item)


def object(type, **kwargs):
    if type not in OBJECT_MAP:
        raise SchematicException("Unknown object type %s" % type)
    format = SCH_FORMAT[OBJECT_MAP[type]].split()[1:]
    if len(kwargs) != len(format):
        raise SchematicException("Wrong number of arguments for %s. Received %d expected %d" % (type, len(kwargs), len(format)))
    keys = set(item.split(":")[1] for item in format)
    for key in kwargs:
        if key not in keys:
            raise SchematicException("Unknown argument for %s: %s" % (type, key))
    kwargs["type"] = type
    return SchematicObject(kwargs)


def _emit_objects(stream, objects):
    for object in objects:
        _emit(stream, object)
        if "attributes" in object and object["attributes"]:
            stream.write("{\n")
            _emit_objects(stream, object["attributes"])
            stream.write("}\n")


def _emit(stream, object):
    code = OBJECT_MAP[object["type"]]
    format = SCH_FORMAT[code]
    fmt = code
    for part in format.split()[1:]:
        type, name = part.split(":")
        fmt += ' {%s}' % name
    stream.write(fmt.format(**object) + "\n")
    if object["type"] == "text":
        stream.write(object["text"] + "\n")


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
    return map(SchematicObject, objects)


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
    return SchematicObject(object)


def main(args):
    if len(args) < 3:
        print "USAGE: %s schematic.sch attr term=value [term2=value2]" % sys.argv[0]
        print "Search through schematic.sch for all objects matching the terms and print attr"
        return 2
    schem = Schematic(open(args[0]))
    attr = args[1]
    terms = dict(term.split("=", 1) for term in args[2:])
    for obj in schem.findall(**terms):
        if attr.startswith("."):
            print getattr(obj, attr[1:])
        else:
            print obj.get(attr)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
