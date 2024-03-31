import pandas as pd
from collections import Counter
from nltk.tokenize import word_tokenize


file_path = "preprocessed_dataset.csv"
df = pd.read_csv(file_path)

# Group by ARTICLE_ID and concatenate SECTION_TEXT.
df_grouped = (
    df.groupby("ARTICLE_ID")["SECTION_TEXT"].apply(
        lambda x: " ".join(x)).reset_index()
)

# Preprocess and tokenize text for each article.
df_grouped["TOKENS"] = df_grouped["SECTION_TEXT"].apply(word_tokenize)


# Create vocabulary and word-to-id mapping.
vocabulary = sorted(
    set(token for tokens_list in df_grouped["TOKENS"] for token in tokens_list)
)
word_to_id = {word: index for index, word in enumerate(vocabulary)}


# Calculate TF for each article.
df_grouped["TF"] = df_grouped["TOKENS"].apply(Counter)
df_grouped["TF"] = df_grouped["TF"].apply(
    lambda tf_dict: {word_id: tf for word_id, tf in tf_dict.items() if tf != 0}
)

# Calculate Inverse Document Frequency (IDF).
dfs = Counter(
    word for tokens_list in df_grouped["TOKENS"] for word in set(tokens_list))


# Apply TF-IDF calculation.
def calculate_tfidf(tf_dict, dfs):
    return {
        word: (tf / dfs[word]) for word, tf in tf_dict.items() if word in dfs}


df_grouped["TFIDF"] = df_grouped["TF"].apply(
    lambda tf: calculate_tfidf(tf, dfs))


# Writing resultant files.
output_files = {
    "vocabulary": "result/vocabulary.csv",
    "TF": "result/article_term_frequencies.csv",
    "idf": "result/article_document_frequencies.csv",
    "TFIDF": "result/article_tfidf_scores.csv",
}

# Write vocabulary to file.
with open(output_files["vocabulary"], "w", encoding="utf-8") as file:
    file.write(
        "\n".join(f"{index},{word}" for index, word in enumerate(vocabulary)))

# Write term frequencies and tf-idf scores to files.
for output_type in ["TF", "TFIDF"]:
    with open(output_files[output_type], "w", encoding="utf-8") as file:
        for _, row in df_grouped.iterrows():
            data_str = ", ".join(
                f"({word_to_id[word]}, {row[output_type][word]:.2f})"
                for word in row[output_type]
            )
            file.write(f"{row['ARTICLE_ID']},{data_str}\n")

# Write document frequencies to file.
with open(output_files["idf"], "w", encoding="utf-8") as file:
    for word, df in dfs.items():
        file.write(f"{word_to_id[word]},{df}\n")
