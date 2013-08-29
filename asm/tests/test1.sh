#!/bin/sh

set -e

egrep -o '; [ 01]* \|' test1.asm | tr -d ' ;|' | fold -w 8 > test1.good.o
python ../asm.py test1.asm test1.o
diff test1.o test1.good.o
