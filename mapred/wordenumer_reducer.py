#!/usr/bin/python3

import sys

current_word = None
current_doc_id = None
current_count = 0
word = None
doc_id = None

# input comes from STDIN
for line in sys.stdin:
    # Remove leading and trailing whitespace
    line = line.strip()

    # Parse the input we got from mapper.py
    doc_id, word, count = line.split('\t', 2)

    # Convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        # Count was not a number, so silently ignore this line
        continue

    # This IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_word == word and current_doc_id == doc_id:
        current_count += count
    else:
        if current_word:
            # Write result to STDOUT
            print('%s\t%s\t%s' % (current_doc_id, current_word, current_count))
        current_count = count
        current_word = word
        current_doc_id = doc_id

# Do not forget to output the last word if needed!
if current_word == word and current_doc_id == doc_id:
    print('%s\t%s\t%s' % (current_doc_id, current_word, current_count))