#!/usr/bin/python3

import sys

# This mapper does nothing but pass the data along
for line in sys.stdin:
    doc_id, word, count = line.split('\t', 2)
    if doc_id and word and count:
        print(f'{doc_id}\t{word}\t{count}')
