#!/bin/bash

BUILD=build
ASM=../asm/asm.py
TEST=./runtest.py
status=0

run() {
	$@ 2>&1
	ec=$?
	status=$(($status+$ec))
	if [[ $ec -ne 0 ]]; then
		echo "FAIL $@"
	fi
	return $ec
}

assemble() {
	$ASM $1 $2
}

# run assembler test (check for valid encoding)
test_asm() {
	fn=${1%%.asm}
	out=$BUILD/${fn}.o
	good=$BUILD/${fn}.good.bin
	check=$BUILD/${fn}.test.bin
	egrep -o '; [ 01]* \|' $1 | tr -d ' ;|' > $good
	assemble $1 $out
	[[ $? -ne 0 ]] && return 1
	xxd -b -c 1 $out | cut -f2 -d' ' | sed 'N;s/\n//' > $check
	diff -y $good $check | tr '\t' ' ' | grep -n ' | ' | sed 's/  */ /'
	# return exit status
	diff -q $good $check > /dev/null
}

# run test through python functional simulator
test_func_sim() {
	$TEST $@
}

# run test through verilog functional simulator
test_vfunc_sim() {
	: # NOT IMPLEMENTED
}

# run test though verilog behavioral simulator
test_behave_sim() {
	: # NOT IMPLEMENTED
}

# run all tests
run_tests() {
	out=$BUILD/${1%%.asm}.o
	run assemble $1 $out || return 0
	run test_func_sim $1 $out
	run test_vfunc_sim $1 $out
	run test_behave_sim $1 $out
}


################################################################################
# Tests
################################################################################

cd $(dirname $0)

# ensure build directory exists
mkdir -p $BUILD

# assembler tests
run test_asm test1.asm

# main tests
#run_tests bigintadd.asm
#run_tests bigintsub.asm
#run_tests echo.asm
#run_tests fib.asm
#run_tests immediates.asm
#run_tests macros.asm
#run_tests pow.asm
#run_tests screen.asm
#run_tests sections.asm
#run_tests test1.asm
#run_tests test2.asm
#run_tests test3.asm
#run_tests testimem2.asm
#run_tests testimem.asm
run_tests testisa.asm
#run_tests timer.asm

exit $status
