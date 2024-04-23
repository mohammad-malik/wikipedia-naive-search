#!/usr/bin/python3
import sys

current_article_id = None
current_text = []

for line in sys.stdin:
    line = line.strip()
    if "\t" not in line:
        continue
    article_id, section_text = line.split("\t", 1)

    if current_article_id == article_id:
        current_text.append(section_text)
    else:
        if current_article_id:
            # Output aggregated text for the current article ID
            print(f"{current_article_id}\t{' '.join(current_text)}")
        current_article_id = article_id
        current_text = [section_text]
