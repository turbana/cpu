#!/bin/sh

set -e

egrep -o '; [ 01]* \|' test1.asm | tr -d ' ;|' > test1.good.bin
python ../asm.py test1.asm test1.o
xxd -b -c 1 test1.o | cut -f2 -d' ' | sed 'N;s/\n//' > test1.test.bin
diff test1.test.bin test1.good.bin
