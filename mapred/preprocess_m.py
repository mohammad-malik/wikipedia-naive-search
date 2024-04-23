#!/usr/bin/python3

import sys
import re


def preprocess_text(text):
    # Lowercasing and removing non-alphanumeric characters
    text = text.lower()
    text = re.sub(r"\b\w{1,2}\b", "", text)  # remove words of length <= 2
    text = re.sub(r"\W+", " ", text)  # remove non-word characters
    return text


for line in sys.stdin:
    line = line.strip()
    # Removing extra columns.
    columns = line.split(",")
    if len(columns) >= 4:
        article_id = columns[0]
        section_text = columns[3]
        preprocessed_text = preprocess_text(section_text)
        print(f"{article_id}\t{preprocessed_text}")
    else:
        continue
    preprocessed_text = preprocess_text(section_text)
    print(f"{article_id}\t{preprocessed_text}")
