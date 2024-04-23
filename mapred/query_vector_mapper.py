#!/usr/bin/python3

import re
import sys


for line in sys.stdin:
    # Parse the input line
    text = line.strip()

    # Tokenize the text
    terms = re.findall(r'\w+', text)

    # Emit term frequencies for the document
    for term in set(terms):
        print(f'{term}\t{terms.count(term)}')
