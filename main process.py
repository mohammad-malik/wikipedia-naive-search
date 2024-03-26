import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


file_path = "preprocessed_dataset.csv"
df = pd.read_csv(file_path)

# Group by ARTICLE_ID and concatenate SECTION_TEXT
df_grouped = (
    df.groupby("ARTICLE_ID")["SECTION_TEXT"].apply(lambda x: " ".join(x)).reset_index()
)

# Preprocess and tokenize text for each article
df_grouped["TOKENS"] = df_grouped["SECTION_TEXT"].apply(word_tokenize)

vocabulary = sorted(
    set(token for tokens_list in df_grouped["TOKENS"] for token in tokens_list)
)
word_to_id = {word: index for index, word in enumerate(vocabulary)}

# Calculate TF for each article
df_grouped["TF"] = df_grouped["TOKENS"].apply(Counter)
print(f"before:{df_grouped.shape}")

# df_grouped['TF'] = df_grouped['TF'].apply(lambda tf_dict: {word_id: tf for word_id, tf in tf_dict.items() if tf != 0})

# Calculate Inverse Document Frequency (IDF)
dfs = Counter(word for tokens_list in df_grouped["TOKENS"] for word in set(tokens_list))


# Calculate TF-IDF
def calculate_tfidf(tf_dict, dfs, total_docs):
    return {word: (tf / dfs[word]) for word, tf in tf_dict.items() if word in dfs}


# Apply TF-IDF calculation
df_grouped["TFIDF"] = df_grouped["TF"].apply(
    lambda tf: calculate_tfidf(tf, dfs, len(df_grouped))
)

tf_output_file = "article_term_frequencies.csv"
with open(tf_output_file, "w", encoding="utf-8") as file:
    for _, row in df_grouped.iterrows():
        tf_str = ", ".join(
            f"({word_to_id[word]}, {tf})" for word, tf in row["TF"].items()
        )
        file.write(f"{row['ARTICLE_ID']},{tf_str}\n")

idf_output_file = "article_document_frequencies.csv"
with open(idf_output_file, "w", encoding="utf-8") as file:
    for word, df in dfs.items():
        file.write(f"{word_to_id[word]},{df}\n")

tfidf_output_file = "article_tfidf_scores.csv"
with open(tfidf_output_file, "w", encoding="utf-8") as file:
    for _, row in df_grouped.iterrows():
        tfidf_str = ", ".join(
            f"({word_to_id[word]}, {tfidf:.2f})" for word, tfidf in row["TFIDF"].items()
        )
        file.write(f"{row['ARTICLE_ID']},{tfidf_str}\n")
