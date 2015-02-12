#!/bin/bash

set -e

if [[ $# -ne 1 ]]; then
	echo "USAGE: $(basename $0) testfile.asm"
	exit 2
fi

ASM="python $(dirname $0)/asm.py"
SIM="python $(dirname $0)/../sim/functional/cpu.py"

parse_stop() {
	awk 'BEGIN{FS="[)(]"} { if($1 == ";@; stop") print $2 }' $1
}

parse_asserts() {
	awk 'BEGIN{FS="[)(]"} { if($1 == ";@; assert") print $2 }' $1 | tr -d ' '
}

source=$1
binary=${source%%.asm}.o
macros=${source%%.asm}.py
if [[ ! -f "$macros" ]]; then
	macros=""
fi

clocks=$(parse_stop $source)
asserts=$(parse_asserts $source)

[[ -z "$clocks" ]] && echo "ERROR: No stop() found in '$source'" && exit 3
[[ -z "$asserts" ]] && echo "ERROR: No assert()'s found in '$source'" && exit 3

$ASM $source $macros $binary
results=$($SIM $binary --dump $clocks | tr ' ' =)
failed=0

for assert in $asserts; do
	set +e
	found=$(echo -e $results | grep -cwF $assert)
	set -e
	if [[ $found = 0 ]]; then
		reg=$(echo ${assert%%=*})
		found=$(echo $results | grep -o "\\${reg}=[xX0-9a-fA-F]*")
		echo "ERROR: Assertion failure in '$source': expected ($assert) received ($found)"
		failed=$(($failed + 1))
	fi
done

exit $failed
