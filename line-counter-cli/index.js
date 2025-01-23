#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function countLines(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');
    return lines.length;
  } catch (error) {
    if (error.code === 'ENOENT') {
      console.error(`Error: File not found - ${filePath}`);
    } else {
      console.error(`Error reading file ${filePath}: ${error.message}`);
    }
    return -1;
  }
}

const args = process.argv.slice(2);
const verbose = args.includes('-v') || args.includes('--verbose');
const filePaths = args.filter(arg => !arg.startsWith('-'));

if (filePaths.length === 0) {
  console.error('Please provide at least one file path');
  process.exit(1);
}

let totalLines = 0;
let validFiles = 0;

filePaths.forEach(filePath => {
  const absolutePath = path.resolve(filePath);
  const lineCount = countLines(absolutePath);
  
  if (lineCount >= 0) {
    validFiles++;
    totalLines += lineCount;
    if (verbose) {
      console.log(`${filePath}: ${lineCount} line${lineCount !== 1 ? 's' : ''}`);
    }
  }
});

if (filePaths.length > 1 || verbose) {
  console.log(`\nTotal: ${totalLines} line${totalLines !== 1 ? 's' : ''} in ${validFiles} file${validFiles !== 1 ? 's' : ''}`);
} else if (validFiles > 0) {
  console.log(totalLines);
}

if (validFiles === 0) {
  process.exit(1);
}
