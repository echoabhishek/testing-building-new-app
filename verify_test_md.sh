#!/bin/bash
file_content=$(cat /home/user/testing-building-new-app/test.md)
if echo "$file_content" | grep -q "This is a new line 1" && echo "$file_content" | grep -q "The sum of 2 + 3 = 5"; then
    echo "The required lines are present in test.md"
else
    echo "Error: The required lines are not present in test.md"
fi
