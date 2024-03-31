import pandas as pd
import numpy as np
import os
import re
from ast import literal_eval
from collections import Counter


# Load IDF values from a CSV file and convert them into a dictionary.
def load_idf(file_path):
    df_idf = pd.read_csv(
        file_path, header=None, names=["term_id", "idf"], index_col=0)

    # Convert the DataFrame column to a dictionary for easy lookup.
    return df_idf["idf"].to_dict()


# Load the vocabulary from a file, mapping term IDs to terms.
def load_vocabulary(file_path):
    vocabulary = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            term_id, term = line.strip().split(",")
            vocabulary[int(term_id)] = term

    return vocabulary


# Creating a document vector for each doc in the file.
def load_tfidf_scores(file_path, vocabulary):
    """
    The document vectors are constructed in this function based on the
    pre-computed TF-IDF scores loaded from a file. Here, each document
    is represented as a vector where the number of dimensions equals
    the size of the vocabulary, with each dimension corresponding to a term
    from the vocabulary. The value in each dimension represents the TF-IDF
    score for the corresponding term in that document.
    """

    # key=doc_id, value=vector
    doc_vectors = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # Split the line into document ID and the rest of the line.
            parts = line.strip().split(",", 1)
            doc_id, scores_str = int(parts[0]), parts[1]

            # Parse the scores string into a list of tuples (term_id, tfidf).
            scores_list = literal_eval(scores_str)

            # Initialize zero vector for each document and store TF-IDF scores.
            vector = np.zeros(len(vocabulary))
            for term_id, tfidf in scores_list:
                if term_id in vocabulary:
                    index = int(term_id)
                    vector[index] = tfidf
            doc_vectors[doc_id] = vector

    return doc_vectors


# Directory where CSV files are stored.
directory = "result\\"

# Load IDF scores.
idf_scores = load_idf(
    os.path.join(directory, "article_document_frequencies.csv"))
# Load the vocabulary.
vocabulary = load_vocabulary(
    os.path.join(directory, "vocabulary.csv"))
# Load document vectors constructed from TF-IDF scores.
doc_vectors = load_tfidf_scores(
    os.path.join(directory, "article_tfidf_scores.csv"), vocabulary
)

print("Vector Space Model loaded successfully.")


def vectorize_query(query, vocabulary, idf_scores):
    '''
    Vectorizes the search query into a sparse representation using IDF scores.
    '''

    # Initialize an empty dictionary for the query's vector representation.
    query_vector_sparse = {}

    # Calculate TF-IDF score and update the query vector.
    words = query.lower().split()
    tf_query = Counter(words)

    for word, tf in tf_query.items():
        term_id = next(
            (k for k, v in vocabulary.items() if v == word), None)
        if term_id is not None and term_id in idf_scores:
            tfidf = tf / idf_scores[term_id]
            query_vector_sparse[term_id] = tfidf

    return query_vector_sparse


def calculate_inner_product_similarity(query_vector_sparse, doc_vector):
    score = 0
    for term_id, tfidf in query_vector_sparse.items():
        # Ensure term_id is within the bounds of the doc_vector.
        if term_id < len(doc_vector):
            score += tfidf * doc_vector[term_id]

    return score


def process_query(query, vocabulary, idf_scores, doc_vectors):
    """
    Creates query vector, computes relevance scores, returns top 5 documents.
    """

    # Vectorize the query into a sparse TF-IDF vector.
    query_vector_sparse = vectorize_query(query, vocabulary, idf_scores)

    # Calculate the similarity score for each document.
    similarity_scores = {}
    for doc_id, doc_vector in doc_vectors.items():
        score = calculate_inner_product_similarity(
            query_vector_sparse,
            doc_vector
        )
        similarity_scores[doc_id] = score

    # Sort documents by similarity scores in descending order and return top 5.
    sorted_docs = sorted(
        similarity_scores.items(), key=lambda x: x[1], reverse=True)

    return sorted_docs[:5]


def is_valid_query(query):
    """
    Checks if query is valid (not empty, contains alphanumeric characters etc).
    """
    return bool(query.strip()) and bool(re.search(r"\w", query))


def main():
    while True:
        query = input(
            "Enter your search query (or type 'exit' to quit): ").strip()

        if query.lower() == "exit":
            break

        elif not is_valid_query(query):
            print(
                "Invalid query.\
                Please enter a non-empty query without special characters."
            )
            continue

        top_documents = process_query(
            query, vocabulary, idf_scores, doc_vectors)

        print(f"Top {len(top_documents)} documents ranked by similarity:")
        for doc_id, score in top_documents:
            print(f"Document ID: {doc_id}, Similarity Score: {score:.4f}")

        print()


if __name__ == "__main__":
    main()
