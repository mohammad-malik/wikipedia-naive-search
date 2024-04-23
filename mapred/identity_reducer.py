#!/usr/bin/python3

import sys

# input comes from STDIN
for line in sys.stdin:
    # write the results to STDOUT;
    # what we got, we output unchanged
    line = line.strip()
    if line != "":
        print(line)
