import pandas as pd
from scipy.sparse import csr_matrix
import numpy as np
import os
import re
from ast import literal_eval
from collections import Counter
# Check file accessibility
def check_file_access(file_path):
    # Check existence
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return False
    # Check readability
    if not os.access(file_path, os.R_OK):
        print(f"Error: No read access to {file_path}.")
        return False
    return True

# Load IDF values from a CSV file and convert them into a dictionary
def load_idf(file_path):
    # Check if the file is accessible
    if not check_file_access(file_path):
        return {}
    # Load the CSV as a DataFrame, setting the first column as the index
    df_idf = pd.read_csv(file_path, header=None, names=["term_id", "idf"], index_col=0)
    # Convert the DataFrame column to a dictionary for easy lookup
    return df_idf["idf"].to_dict()

# Load the vocabulary from a file, mapping term IDs to terms
def load_vocabulary(file_path):
    vocabulary = {}
    # Check if the file is accessible
    if not check_file_access(file_path):
        return vocabulary
    # Read the file line by line and populate the vocabulary dictionary
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            term_id, term = line.strip().split(",")
            vocabulary[int(term_id)] = term
    return vocabulary

# Load TF-IDF scores from a file, constructing document vectors
    """The document vectors are constructed in the 
    load_tfidf_scores function based on the pre-computed 
    TF-IDF scores loaded from a file. Here, each document
    is represented as a vector where the number 
    of dimensions equals the size of the vocabulary, 
    with each dimension corresponding to a term from 
    the vocabulary. The value in each dimension
    represents the TF-IDF score for the corresponding 
    term in that document.
    """
#total dimension= 78848
#creating a document vector for each doc in the file
def load_tfidf_scores(file_path, vocabulary):
    doc_vectors = {} #key=doc_id, value=vector
    # Check if the file is accessible
    if not check_file_access(file_path):
        return doc_vectors
    # Read the file line by line
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:  #line by line
            parts = line.strip().split(",", 1) #splitting at commas
            doc_id, scores_str = int(parts[0]), parts[1]
            # Parse the scores string into a list of tuples (term_id, tfidf)
            scores_list = literal_eval(scores_str)
            # Initialize a zero vector for the document
            vector = np.zeros(len(vocabulary))
            # Populate the vector with TF-IDF scores
            for term_id, tfidf in scores_list:
                if term_id in vocabulary:  
                    index = int(term_id)
                    vector[index] = tfidf
            doc_vectors[doc_id] = vector
    return doc_vectors

# Directory where your CSV files are stored
directory = "result\\"

# Load IDF scores
idf_scores = load_idf(os.path.join(directory, "article_document_frequencies.csv"))
# Load the vocabulary
vocabulary = load_vocabulary(os.path.join(directory, "vocabulary.csv"))
# Load document vectors constructed from TF-IDF scores
doc_vectors = load_tfidf_scores(os.path.join(directory, "article_tfidf_scores.csv"), vocabulary)

# prinitng as an exmaple
print("First 5 Document Vectors:")
for doc_id in list(doc_vectors.keys())[:5]:
    vector = doc_vectors[doc_id]
    print(f"Document ID {doc_id}: Vector -> {vector}")

#Function to vectorize a search query using IDF scores
# Vectorize the search query into a sparse representation using IDF scores
def vectorize_query(query, vocabulary, idf_scores):
    # Initialize an empty dictionary for the query's vector representation
    query_vector_sparse = {}
    # Tokenize the query into words
    words = query.lower().split()
    # Calculate term frequency (TF) for each word in the query
    tf_query = Counter(words)
    
    for word, tf in tf_query.items():
        term_id = next((k for k, v in vocabulary.items() if v == word), None)
        # Check if the term is in the vocabulary and has an IDF score
        if term_id is not None and term_id in idf_scores:
            # Calculate TF-IDF score and update the query vector
            tfidf = tf / idf_scores[term_id]
            query_vector_sparse[term_id] = tfidf
    return query_vector_sparse



def calculate_inner_product_similarity(query_vector_sparse, doc_vector):
    score = 0
    for term_id, tfidf in query_vector_sparse.items():
        # Ensure term_id is within the bounds of the doc_vector
        if term_id < len(doc_vector):
            score += tfidf * doc_vector[term_id]
    return score


def process_query(query, vocabulary, idf_scores, doc_vectors):
    """
    Processes a search query, computes relevance scores, and returns the top 5 documents.
    """
    # Vectorize the query into a sparse TF-IDF vector
    query_vector_sparse = vectorize_query(query, vocabulary, idf_scores)
    
    # Initialize a dictionary to hold similarity scores
    similarity_scores = {}
    
    # Calculate the similarity score for each document
    for doc_id, doc_vector in doc_vectors.items():
        score = calculate_inner_product_similarity(query_vector_sparse, doc_vector)
        similarity_scores[doc_id] = score

    # Sort documents by their similarity scores in descending order and return top 5
    sorted_docs = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_docs[:5]


def is_valid_query(query):
    """
    Checks if the query is valid (not empty and contains alphanumeric characters).
    """
    return bool(query.strip()) and bool(re.search(r"\w", query))

def main():
    while True:
        query = input("Enter your search query (or type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            break
        elif not is_valid_query(query):
            print("Invalid query. Please enter a non-empty query without only special characters.")
            continue

        top_documents = process_query(query, vocabulary, idf_scores, doc_vectors)
        print(f"Top {len(top_documents)} documents ranked by similarity:")
        for doc_id, score in top_documents:
            print(f"Document ID: {doc_id}, Similarity Score: {score:.4f}")
        print()

if __name__ == "__main__":
    main()