#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function countLines(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');
    return lines.length;
  } catch (error) {
    console.error();
    process.exit(1);
  }
}

const filePath = process.argv[2];

if (!filePath) {
  console.error('Please provide a file path');
  process.exit(1);
}

const absolutePath = path.resolve(filePath);
const lineCount = countLines(absolutePath);

console.log();
