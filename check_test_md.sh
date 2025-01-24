#!/bin/bash
echo "Current content of test.md:"
cat test.md
echo -e "\nNumber of lines in test.md:"
wc -l < test.md
echo -e "\nChecking for new lines:"
grep -n "this is a new line 1" test.md
grep -n "this is the sum of 2+3 =5" test.md
