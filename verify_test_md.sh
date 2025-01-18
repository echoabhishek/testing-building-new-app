#!/bin/bash
lines=$(wc -l < test.md)
if [ $lines -lt 2 ]; then
  echo "Error: test.md should have at least 2 more lines"
  exit 1
else
  echo "test.md has enough lines"
fi
