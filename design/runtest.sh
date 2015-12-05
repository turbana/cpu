#!/bin/bash

set -e

DESIGN=schem
BUILD=build
SYMBOLS=symbols/**/*.sym
VMODS=symbols/**/*.v

if [[ "$#" -ne "1" ]]; then
    echo "USAGE: $(basename $0) module.v"
    exit 2
fi

tmp=/tmp/$$.tmp
trap 'rm -f $tmp' EXIT

failon() {
    tee >(grep -c "$1" > $tmp)
    # For some reason grep -c is still running at this point. If we hit the return right away $tmp is empty and we return with success before grep has a change to write to $tmp. Putting a sleep here doesn't fix it, but ps'ing does. No idea why, very strange.
    ps aux | grep grep > /dev/null
    return $(cat $tmp)
}

module=$1
modname=$(basename ${module%%.sch})
modv=$BUILD/$modname.v
modtb=$BUILD/tb_$modname.v
modtest=$BUILD/$modname

[[ ! -d $BUILD ]] && mkdir -p $BUILD

echo " * netlisting"
gnetlist -g verilog -o $modv $SYMBOLS $module | \
    grep -v "^Loading schematic" | \
    grep -v "is not likely a valid Verilog identifier$" | \
    failon WARNING

echo " * checking netlist"
grep -q unconnected_pin $modv && (
    echo "ERROR: Unconnected wire(s):" $(grep unconnected_pin $modv | cut -f2 -d' ')
    exit 2
)

echo " * fixing netlist"
sed -i 's:^/\* continuous assignments \*/$:\0\nassign Vcc = 1;\nassign GND = 0;:' $modv

echo " * building test bench"
python testmod.py $modv > $modtb

echo " * compiling test bench"
iverilog $modtb $modv $VMODS -o $modtest 2>&1 | \
    failon "error" | \
    failon "was already declared here"

echo " * executing test bench"
$modtest 2>&1 | \
    grep -v "^VCD info" | \
    failon "FAILURE"
