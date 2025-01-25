#!/bin/bash
if grep -q "this is a new line 1" test.md && grep -q "this is the sum of 2+3 =???" test.md; then
    echo "Verification successful: Both new lines are present in test.md"
    exit 0
else
    echo "Verification failed: One or both new lines are missing from test.md"
    exit 1
fi
