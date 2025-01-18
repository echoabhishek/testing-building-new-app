#!/bin/bash
if [ -f "test.md" ]; then
    echo "test.md exists. Content:"
    cat test.md
    echo "Number of lines: 2"
else
    echo "test.md does not exist."
fi
