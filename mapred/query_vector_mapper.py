#!/usr/bin/python3

import os
import re

# Query is passed as an environment variable or command line argument
query = os.environ.get('QUERY', 'default query').lower()
query_terms = re.findall(r'\w+', query)

# Emit term frequencies for the query
for term in set(query_terms):
    print(f'{term}\t{query_terms.count(term)}')
