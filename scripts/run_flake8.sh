#!/bin/sh

cd "$(dirname "$0")/.."

flake8 pysmith
codeStatus=$?

flake8 tests
testStatus=$?

finalStatus=0
[ $codeStatus == 1 ] || [ $testStatus == 1 ] && finalStatus=1

exit $finalStatus
