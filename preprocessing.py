import pandas as pd
import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def preprocess_text(text):
    # Checking for null values.
    if pd.isnull(text):
        return ""
    
    # Converting to lowercase and removing numbers and punctuation.
    text = text.lower()
    text = re.sub(r"[0-9]+", "", text)
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)

    # Removing stopwords and words with length of less than 3.
    stop_words = set(stopwords.words("english"))
    tokens = [
         word 
         for word in word_tokenize(text) 
         if word not in stop_words and len(word) > 2
        ]

    # Applying lemmatization.
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(word) for word in tokens]

    return " ".join(lemmatized)


# Loading the dataset with only ARTICLE_ID and SECTION_TEXT columns.
file_path = "randomly_selected_chunk.csv"
df = pd.read_csv(file_path, usecols=["ARTICLE_ID", "SECTION_TEXT"])

# Applying the preprocessing function to the SECTION_TEXT column.
df["SECTION_TEXT"] = df["SECTION_TEXT"].apply(preprocess_text)

# Dropping rows with missing values or empty strings in SECTION_TEXT column.
df = df[df["SECTION_TEXT"].str.strip() != ""]

# Saving the preprocessed dataset.
output_file = "preprocessed_dataset.csv"
df.to_csv(output_file, index=False)
print(df.head(20))
