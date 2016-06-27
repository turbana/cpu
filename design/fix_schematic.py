"""
Update schematic nets from the form A0 to A[0]. This allows us to use gschem's auto text numbering (which doesn't work with A[0]) and also benfit from bus netlisting (which needs A[0]).

Also ensure ipad-2.sym have their net's set

Add title bar information (title, author, page #)
"""

import datetime
import glob
import os.path
import re
import subprocess
import sys

import schematic


TITLE_BAR = {
    "size":        12,
    "color":    10,
    # coordinates relative to title block
    "title":    (16250, 900),
    "page":        (16250, 300),
    "pages":    (18000, 300),
    "revision": (20250, 550),
    "author":    (20250, 300),
    "module":   (0, 0),
}


def main(args):
    if len(args) != 2:
        print "USAGE: %s module.sch output.sch" % sys.argv[0]
        print "Updates schemtic wires from X0 to X[0] to facilitate netlisting"
        return 2
    filename = args[0]
    schem = schematic.Schematic(open(filename))
    fix_wires(schem, filename)
    fix_busses(schem)
    add_title_block(schem, filename)
    schem.save(open(args[1], "w"))


def fix_wires(schem, prefix):
    count = 0
    for pad in schem.findall(type="component", basename="[io]pad-1.sym"):
        value = "%s:1" % pad.netlabel
        refdes = "%s_%s%d" % (prefix, pad.netlabel, count)
        count += 1
        set_attribute(pad, "refdes", refdes)
        set_attribute(pad, "net", value)


def fix_busses(schem):
    for pad in schem.findall(type="component", basename="[io]pad-2.sym"):
        name = pad.netlabel.split("[")[0]
        search = "netname=%s[0-9]+" % name
        for net in schem.findall(type="net", attr=search):
            num = net.netname[len(name):]
            net.netname = "%s[%s]" %  (name, num)


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


def add_title_block(schem, filename):
    num, count = pages(filename)
    rev, author = git_info(filename)
    add_text(schem, "title", title(filename))
    add_text(schem, "page", num)
    add_text(schem, "pages", count)
    add_text(schem, "revision", rev)
    add_text(schem, "author", author)
    module = "module_name=%s" % os.path.basename(filename).replace(".sch", "")
    add_text(schem, "module", module, hidden=True)


def title(filename):
    name = os.path.basename(filename).replace(".sch", "")
    name = re.sub(r"_[0-9]+\b", "", name)
    return name.replace("_", " ").upper()


def pages(filename):
    match = re.search(r"_([0-9]+).sch$", filename)
    if match:
        num = match.groups()[0]
        wildcard = filename.replace("_"+num, "_[0-9]")
        return num, len(glob.glob(wildcard))
    return 1, 1


def git_info(filename):
    cmd = "git log -1 -- %s" % filename
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    stdout,stderr = proc.communicate()
    if proc.returncode:
        sys.exit(1)
    if not stdout:
        return "unknown", "unknown"
    author = re.search("Author: *([A-Za-z ]+) <", stdout).groups()[0]
    date = re.search("Date: *([^ ].*)", stdout).groups()[0]
    date = date[:-6] # strip timezone
    date = datetime.datetime.strptime(date, "%a %b %d %H:%M:%S %Y")
    rev = date.strftime("%Y-%m-%d-%H%M%S")
    return rev, author


def add_text(schem, name, value, hidden=False):
    dx, dy = title_block_position(schem)
    x, y = TITLE_BAR[name]
    color = TITLE_BAR["color"]
    size = TITLE_BAR["size"]
    vis = 0 if hidden else 1
    text = schematic.object(
        "text", x=dx+x, y=dy+y, color=color, size=size, visibility=vis,
        show_name_value=1, angle=0, alignment=0, num_lines=1)
    text["text"] = str(value)
    schem.add(text)


def title_block_position(schem):
    title = schem.findall(type="component", basename="title-*").next()
    return title["x"], title["y"]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
