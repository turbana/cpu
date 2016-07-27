#!/bin/bash

set -e

tmp=/tmp/$$.tmp
trap 'rm -f $tmp' EXIT

if [[ $# -ne 1 ]]; then
    echo "USAGE: $(basename $0) pattern"
    echo "Copies stdin to stdout and exits with failure when pattern matches any line"
    exit 2
fi

2>&1 tee $tmp
exit $(grep -c "$1" $tmp)
