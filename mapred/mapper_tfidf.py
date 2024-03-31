#!/usr/bin/python3
import sys
import re


def tokenize(text):
    return re.findall(r"\w+", text.lower())


for line in sys.stdin:
    line = line.strip()
    article_id, section_text = line.split("\t", 1)
    words = tokenize(section_text)
    total_words = len(words)

    # Emit for TF calculation
    for word in words:
        print(f"{word},{article_id}\t{1}/{total_words}")

    # For DF calculation, emit once per document per word
    unique_words = set(words)
    for word in unique_words:
        print(f"{word},DF\t{article_id}")

