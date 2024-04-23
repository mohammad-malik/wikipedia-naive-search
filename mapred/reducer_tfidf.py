#!/usr/bin/python3

import sys
from collections import defaultdict

# Stores count of each word in each document
word_doc_counts = defaultdict(int)
word_doc_count = defaultdict(int)
current_word = None

for line in sys.stdin:
    line = line.strip()
    key, count = line.split("\t", 1)
    doc_id, word = key.split(",", 1)

    # If we've moved to a new word, print the TF/IDF for the previous word
    if current_word and current_word != word:
        for doc_id, count in word_doc_counts.items():
            tfidf = (
                count / word_doc_count[current_word]
                if word_doc_count[current_word] > 0
                else 0
            )
            print(f"{doc_id}\t{current_word}\t{tfidf}")
        word_doc_counts = defaultdict(int)

    current_word = word
    word_doc_counts[doc_id] += int(count)
    word_doc_count[word] += 1

# Print the TF/IDF for the last word
if current_word:
    for doc_id, count in word_doc_counts.items():
        tfidf = (
            count / word_doc_count[current_word]
            if word_doc_count[current_word] > 0
            else 0
        )
        print(f"{doc_id}\t{current_word}\t{tfidf}")
