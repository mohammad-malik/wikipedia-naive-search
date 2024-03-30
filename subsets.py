import pandas as pd
import random
import math


dataset_path = "enwiki-20170820.csv"
chunk_size = 10000

total_rows = sum(1 for row in open(dataset_path, "r", encoding="utf-8")) - 1
total_chunks = math.ceil(total_rows / chunk_size)
random_chunk_index = random.randint(0, total_chunks - 1)


chunk_counter = 0
processed = False

for chunk in pd.read_csv(dataset_path, chunksize=chunk_size):
    if chunk_counter == random_chunk_index:
        processed = True

        chunk.reset_index(drop=True, inplace=True)
        chunk.to_csv("randomly_selected_chunk.csv", index=False)

        print(chunk.head(10))
        break
    chunk_counter += 1

if not processed:
    first_50_chunks = []
    for i, chunk in enumerate(pd.read_csv(dataset_path, chunksize=chunk_size)):
        if i < 50:
            first_50_chunks.append(chunk)

    random_chunk = random.choice(first_50_chunks)

    random_chunk.reset_index(drop=True, inplace=True)
    random_chunk.to_csv("randomly_selected_chunk.csv", index=False)

    print(random_chunk.head(10))
