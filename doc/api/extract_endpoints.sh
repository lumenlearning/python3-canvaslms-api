#!/bin/sh

# First argument indicates the path of a saved copy of the "All Resources"
# documentation page for the Canvas REST API.
API_DOC=$1
# Second argument indicates where to save the output
OUTPUT_FILE=$2

# Extract the API endpoints from the 
perl -ne 'print "$2\t$1\n" while m#([A-Z]+) (/api/[^\s]+)#g' "$API_DOC" | sort > "$OUTPUT_FILE"
