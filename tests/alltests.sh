#!/bin/bash

TEST=./runtest.py

$TEST bigintadd.asm
$TEST bigintsub.asm
#$TEST echo.asm
$TEST fib.asm
#$TEST macros.asm
$TEST pow.asm
#$TEST screen.asm
#$TEST sections.asm
#$TEST test1.asm
#$TEST test2.asm
#$TEST test3.asm
#$TEST testimem2.asm
#$TEST testimem.asm
$TEST testisa.asm
#$TEST timer.asm
