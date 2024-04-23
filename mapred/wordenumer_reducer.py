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
    key, count = line.split('\t', 1)

    # Split the key into document_id and word
    doc_id, word = key.split(',', 1)

    # Convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        # Count was not a number, so silently ignore this line
        continue

    # This IF-switch only works because Hadoop sorts map output
    # by key (here: docid+word) before it is passed to the reducer
    if current_word == word and current_doc_id == doc_id:
        current_count += count
    else:
        if current_word:
            # Write result to STDOUT
            print(f'{current_doc_id},{current_word}\t{current_count}')
        current_count = count
        current_word = word
        current_doc_id = doc_id

# Do not forget to output the last word if needed!
if current_word == word and current_doc_id == doc_id:
    print(f'{current_doc_id},{current_word}\t{current_count}')
