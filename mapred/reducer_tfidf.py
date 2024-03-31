#!/usr/bin/python3

import sys
from collections import defaultdict

# Stores count of each word in each document
word_doc_counts = defaultdict(lambda: defaultdict(int))
# Stores the set of unique documents in which each word appears
doc_appearances = defaultdict(set)

for line in sys.stdin:
    line = line.strip()
    key, value = line.split("\t", 1)
    word, identifier = key.split(",", 1)

    if identifier.strip() == "DF":
        # Add document ID to the set of documents in which the word appears
        doc_id = value
        doc_appearances[word].add(doc_id)
    else:
        # Increment term frequency for the word in a specific document
        doc_id = identifier
        count = int(value.split("/")[0])
        word_doc_counts[word][doc_id] += count

# Calculate and print TF, IDF (as the number of documents a word appears in)
# and TF-IDF for each word-document pair
for word, counts in word_doc_counts.items():
    idf = len(
        doc_appearances[word]
    )  # The number of unique documents in which the word appears
    for doc_id, tf in counts.items():
        tfidf = tf / idf if idf > 0 else 0
        print(f"{doc_id}\t{word}\t{tfidf}")
