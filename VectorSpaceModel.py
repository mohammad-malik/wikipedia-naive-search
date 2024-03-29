import pandas as pd
import numpy as np
import os
from scipy.spatial.distance import cosine
from ast import literal_eval

def load_idf(file_path):
    df_idf = pd.read_csv(file_path, header=None, names=['term_id', 'idf'], index_col=0)
    return df_idf['idf'].to_dict()

def load_vocabulary(file_path):
    vocabulary = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            term_id, term = line.strip().split(': ')
            vocabulary[int(term_id)] = term
    return vocabulary

def load_tfidf_scores(file_path, vocabulary):
    doc_vectors = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',', 1)
            doc_id, scores_str = int(parts[0]), parts[1]
            # Parse the scores string as a list of tuples
            scores_list = literal_eval(scores_str)
            # Convert the list of tuples into a dictionary
            scores = dict((int(term_id), float(tfidf)) for term_id, tfidf in scores_list)
            vector = np.zeros(len(vocabulary))
            for term_id, tfidf in scores.items():
                if term_id in vocabulary:  # Ensure term_id is an integer
                    index = list(vocabulary.keys()).index(term_id)
                    vector[index] = tfidf
            doc_vectors[doc_id] = vector
    return doc_vectors


# Assuming CSV files and vocabulary.txt are in a specific directory
directory = "D:\\naive-search"  # Ensure this is correctly pointing to your data directory

idf_scores = load_idf(os.path.join(directory, 'article_inverse_document_frequencies.csv'))
vocabulary = load_vocabulary(os.path.join(directory, 'vocabulary.txt'))
doc_vectors = load_tfidf_scores(os.path.join(directory, 'article_tfidf_scores.csv'), vocabulary)

# Vectorization and Cosine Similarity
def vectorize_query(query, vocabulary, idf_scores):
    vector = np.zeros(len(vocabulary))
    words = query.lower().split()
    # Assuming the query does not require TF weighting and using binary occurrence
    for word in words:
        term_id = next((k for k, v in vocabulary.items() if v == word), None)
        if term_id and term_id in idf_scores:
            index = list(vocabulary.keys()).index(term_id)
            vector[index] = idf_scores[term_id]  # Using IDF score directly; adjust as needed
    return vector

def cosine_similarity(vector1, vector2):
    if not np.any(vector1) or not np.any(vector2):
        return 0
    return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

# Interactive Query Handling
def process_query(query, vocabulary, idf_scores, doc_vectors):
    query_vector = vectorize_query(query, vocabulary, idf_scores)
    similarity_scores = {doc_id: cosine_similarity(vector, query_vector) for doc_id, vector in doc_vectors.items()}
    return sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

def main():
    while True:
        query = input("Enter your search query (or type 'exit' to quit): ").strip()
        if query.lower() == 'exit':
            break
        ranked_documents = process_query(query, vocabulary, idf_scores, doc_vectors)
        N = 5
        print("\nTop {} documents ranked by similarity:".format(N))
        for doc_id, score in ranked_documents[:N]:
            print(f'Document ID: {doc_id}, Similarity Score: {score:.4f}')
        print("\n")

if __name__ == "__main__":
    main()
