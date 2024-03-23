import pandas as pd
import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

file_path = 'dataset.csv'
df = pd.read_csv(file_path)
print(df.head(10))
# print(df.tail(10))
# view title column in the dataset
# print(df.columns.tolist())

# print("Initial number of rows, columns:", df.shape)
# df_deduplicated = df.drop_duplicates()
# print("Number of rows, columns after removing duplicates:", df_deduplicated.shape)

# Ensure the full text is displayed
pd.set_option('display.max_colwidth', None)
df = pd.read_csv(file_path, usecols=['ARTICLE_ID', 'SECTION_TEXT'])

article_df = df.loc[df['ARTICLE_ID'] == 0, 'SECTION_TEXT']
article = " ".join(article_df.astype(str).tolist())
# print(f"Text for ARTICLE_ID 0:")
# print(full_article_text)

# Save the full text to a file
with open('ARTICLE_ID_0_full_text.txt', 'w', encoding='utf-8') as file:
    file.write(article)

# Load the dataset with only ARTICLE_ID and SECTION_TEXT columns
df = pd.read_csv(file_path, usecols=['ARTICLE_ID', 'SECTION_TEXT'])
# print(df)
print(df.columns.tolist())

# Checking for missing values in SECTION_TEXT column
missing_values = df['SECTION_TEXT'].isnull().sum()
if missing_values > 0:
    df.dropna(subset=['SECTION_TEXT'], inplace=True)
    # print(f"Dropped {missing_values} missing values in SECTION_TEXT column")
    # print(df.shape)
    
# removing extra whitespaces
with open('ARTICLE_ID_0_full_text.txt', 'r', encoding='utf-8') as file:
    text = file.read()
    cleaned_text = re.sub(r'\s+', ' ', text.strip())
    # with open('cleaned_text.txt', 'w', encoding='utf-8') as file:
    #     file.write(cleaned_text)

# Ensure NLTK components are downloaded
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')

pd.set_option('display.max_colwidth', None)
file_path = 'cleaned_text.txt'

with open(file_path, 'r', encoding='utf-8') as file:
    full_article_text = file.read()

tokens = word_tokenize(full_article_text)
tokens = [word.lower() for word in tokens]

# Removing punctuation from each word
table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in tokens]

# Removing remaining tokens that are not alphabetic
words = [word for word in stripped if word.isalpha()]

# Filtering out stop words
stop_words = set(stopwords.words('english'))
words = [w for w in words if not w in stop_words]

# Lemmatization
lemmatizer = WordNetLemmatizer()
lemmatized = [lemmatizer.lemmatize(w) for w in words]
lemmatized = [word for word in lemmatized if len(word) > 2]
# print(lemmatized)

# final_text = ' '.join(lemmatized)
# with open('cleaned_text.txt', 'w', encoding='utf-8') as cleaned_file:
#     cleaned_file.write(final_text)
    
vocabulary = set(lemmatized)
word_to_id = {word: idx for idx, word in enumerate(sorted(vocabulary))}

# Calculat ing Frequency (TF) for each word in each article
word_frequencies = {word: lemmatized.count(word) for word in vocabulary}

with open('vocabulary.txt', 'w', encoding='utf-8') as vocab_file:
    for word, idx in word_to_id.items():
        vocab_file.write(f"{idx}: {word}\n")

with open('word_frequencies.txt', 'w', encoding='utf-8') as freq_file:
    for word, freq in word_frequencies.items():
        word_id = word_to_id[word]
        freq_file.write(f"{word_id}: {freq}\n")