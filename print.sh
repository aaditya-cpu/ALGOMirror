#!/bin/bash

# This script finds all relevant project files and prints their contents
# to the console, ignoring common junk directories and files.

echo "--- DUMPING PROJECT CONTENTS ---"
echo ""

# Use 'find' to locate all files (-type f).
# Use a series of '-not -path' expressions to exclude directories.
# Use '-not -name' to exclude specific files.
# Finally, loop through the results.
find . -type f \
    -not -path '*/bitto/*' \
    -not -path '*/.git/*' \
    -not -path '*/__pycache__/*' \
    -not -path '*/venv/*' \
    -not -path '*/env/*' \
    -not -path '*/.vscode/*' \
    -not -name 'print_project.py' \
    -not -name 'print_project.sh' \
    -not -name '.gitignore' \
    -not -name 'requirements.txt' \
| sort | while read -r file; do
    # Check if the file has one of the desired extensions
    if [[ "$file" == *.py || "$file" == *.js || "$file" == *.css || "$file" == *.html || "$file" == *.json ]]; then
        echo "================================================================================"
        echo "FILE: $file"
        echo "--------------------------------------------------------------------------------"
        # Use 'cat' to print the file's content. The '-s' flag squeezes multiple blank lines.
        cat -s "$file"
        echo ""
        echo ""
    fi
done

echo "--- END OF PROJECT DUMP ---"