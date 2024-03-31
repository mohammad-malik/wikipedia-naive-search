#!/usr/bin/python3

import sys
import re

for line in sys.stdin:
    # Split the line into document_id and text
    document_id, text = line.strip().split(' ', 1)

    # Split the text into words
    words = re.findall(r"[\w']+", text)

    # Increase counters
    for word in words:
        # Write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py.
        #
        # tab-delimited; the trivial word count is 1
        print('%s\t%s\t%s' % (document_id, word.lower(), 1))