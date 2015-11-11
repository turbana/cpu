#!/bin/bash

set -e

DESIGN=schem
BUILD=$DESIGN/build

if [[ "$#" -ne "1" ]]; then
    echo "USAGE: $(basename $0) module.v"
    exit 2
fi

module=$1
modname=$(basename ${module%%.sch})
modv=$BUILD/$modname.v
modtb=$BUILD/tb_$modname.v
modtest=$BUILD/$modname

echo " * netlisting"
gnetlist -g verilog -o $modv $module | \
    grep -v "is not likely a valid Verilog identifier$"
echo " * fixing netlist"
sed -i 's:^/\* continuous assignments \*/$:\0\nassign Vcc = 1;\nassign GND = 0;:' $modv
echo " * building test bench"
python testmod.py $modv > $modtb
echo " * compiling test bench"
iverilog $modtb $modv $DESIGN/74* -o $modtest
echo " * executing test bench"
$modtest
