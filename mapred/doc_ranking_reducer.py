#!/usr/bin/python3
import sys
from collections import defaultdict


def calculate_inner_product_similarity(vec1, vec2):
    score = 0
    for term, tfidf in vec1.items():
        if term in vec2:
            score += tfidf * vec2[term]
    return score


# Vectors storage
doc_vectors = defaultdict(dict)
query_vector = {}

# Process each line from the mappers
for line in sys.stdin:
    parts = line.strip().split("\t")
    if len(parts) == 2:
        # Query vector
        term, tf = parts
        query_vector[term] = float(tf)
    elif len(parts) == 3:
        # Document vectors
        doc_id, term, tfidf = parts[0], parts[1], float(parts[2])
        doc_vectors[doc_id][term] = tfidf

# Calculate and emit inner product similarity for each document
for doc_id, vec in doc_vectors.items():
    similarity = calculate_inner_product_similarity(vec, query_vector)
    print(f"{doc_id}\t{similarity}")
