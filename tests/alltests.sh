#!/bin/bash

TEST=./runtest.py
status=0

run_test() {
	$TEST $1
	status=$(($status+$?))
}


run_test bigintadd.asm
run_test bigintsub.asm
#run_test echo.asm
run_test fib.asm
#run_test macros.asm
run_test pow.asm
#run_test screen.asm
#run_test sections.asm
#run_test test1.asm
#run_test test2.asm
#run_test test3.asm
#run_test testimem2.asm
#run_test testimem.asm
run_test testisa.asm
#run_test timer.asm

exit $status
