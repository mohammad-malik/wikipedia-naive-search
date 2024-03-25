import pandas as pd
import re
from math import log
from collections import Counter
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


# Define the preprocessing function
def preprocess_text(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r"[0-9]+", "", text)
        text = re.sub(r"http\S+", "", text)
        text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)

        # Tokenize the text
        tokens = word_tokenize(text)

        # Remove stopwords and words with length of less than 3
        stop_words_set = set(stopwords.words("english"))
        tokens = [
            word for word in tokens if word not in stop_words_set and len(word) > 2
        ]

        # Lemmatize the words
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]

    else:
        tokens = []
    return tokens


file_path = "preprocessed_dataset.csv"
df = pd.read_csv(file_path)

# Group by ARTICLE_ID and concatenate SECTION_TEXT
df_grouped = (
    df.groupby("ARTICLE_ID")["SECTION_TEXT"].apply(lambda x: " ".join(x)).reset_index()
)

# Preprocess and tokenize text for each article
df_grouped["TOKENS"] = df_grouped["SECTION_TEXT"].apply(preprocess_text)

# Create a vocabulary with unique IDs
all_tokens = set(token for tokens_list in df_grouped["TOKENS"] for token in tokens_list)
vocabulary = sorted(all_tokens)
word_to_id = {word: idx for idx, word in enumerate(vocabulary)}

# Calculate Term Frequency (TF) for each article
df_grouped["TF"] = df_grouped["TOKENS"].apply(Counter)

# Calculate Document Frequency (DF)
document_frequencies = Counter(
    word for tokens in df_grouped["TOKENS"] for word in set(tokens)
)

# Calculate Inverse Document Frequency (IDF)
total_docs = len(df_grouped)
idfs = {
    word: log((total_docs / (document_frequencies[word] + 1))) + 1
    for word in vocabulary
}


# Calculate TF-IDF for each article
def calculate_tfidf(tf_dict, idfs):
    return {word_to_id[word]: tf * idfs[word] for word, tf in tf_dict.items()}


df_grouped["TFIDF"] = df_grouped["TF"].apply(lambda x: calculate_tfidf(x, idfs))

# Writing TFIDF output in the required format
tfidf_output_file = "article_tfidf_scores.csv"
with open(tfidf_output_file, "w", encoding="utf-8") as tfidf_file:
    for index, row in df_grouped.iterrows():
        tfidf_str = ", ".join(
            f"({word_id}, {weight:.2f})" for word_id, weight in row["TFIDF"].items()
        )
        tfidf_file.write(f"{row['ARTICLE_ID']},{tfidf_str}\n")

# Writing TF output in the required format
tf_output_file = "article_term_frequencies.csv"
with open(tf_output_file, "w", encoding="utf-8") as tf_file:
    for index, row in df_grouped.iterrows():
        tf_str = ", ".join(
            f"({word_to_id[word]}, {tf_count})" for word, tf_count in row["TF"].items()
        )
        tf_file.write(f"{row['ARTICLE_ID']},{tf_str}\n")

# Writing IDF output in the required format
idf_output_file = "article_inverse_document_frequencies.csv"
with open(idf_output_file, "w", encoding="utf-8") as idf_file:
    for word, idf_value in idfs.items():
        idf_file.write(f"{word_to_id[word]},{idf_value:.2f}\n")
