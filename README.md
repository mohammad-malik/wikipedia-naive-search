# Hadoop MapReduce Naive Search Engine

This repository houses a basic search engine implementation utilizing Hadoop's MapReduce framework to process an extensive text corpus efficiently. 
The dataset used for this project is a subset of the English Wikipedia dump. It is 5.2 GB in total.
The project focuses on implementing a naive search algorithm to address challenges in information.

## Dataset Preparation:
We started by dividing the 5 GB Wikipedia dataset into smaller, manageable chunks to facilitate easier processing and analysis. This of course was only temporary, as the dataset would later be used in full for the final search engine.

## Data Preprocessing:
Our code cleaned and standardized the text data, removing stopwords, and normalized terms for consistency across the dataset.

## TF-IDF Score Calculation:
The implementation calculates Term Frequency (TF) and Inverse Document Frequency (IDF) scores to evaluate the importance of words within documents relative to the entire dataset.
Then it uses the Vector Space Model Implementation, which involves coding a model to represent both documents and queries as vectors, to measure similarities for ranking purposes.

### Developing the Search Engine with MapReduce:
<li> Word Enumeration: Our code will scan the dataset to identify unique words, assigning each a unique identifier.</li>
<li> Document Count: We'll compute the IDF for each term, essentially counting the documents each term appears in.</li>
<li> Indexing: The script will process each document to create a TF/IDF vector representation, forming the basis of our search index.</li>
<li> Query Processing: We'll develop functions to convert user queries into vectors and find the most relevant documents by comparing these vectors with our document index.</li>


## Dependencies:
To run this implementation of a Hadoop-MapReduce Search Engine, you'll need the following:

- **Apache Hadoop** [(install)](https://hadoop.apache.org/releases.html)
- **Python** [(install)](https://www.python.org/downloads/)
- **NLTK** [(install)](https://www.nltk.org/)
- **pandas** [(install)](https://pandas.pydata.org/docs/getting_started/install.html)
- **numpy** [(install)](https://numpy.org/)
- **Dataset link** [Download Dataset](https://drive.google.com/file/d/1lGVGqzF5CNWaoV-zoz8_mlThvHwMgcsP/view?usp=sharing)

Ensure you have these software and libraries installed on your system before proceeding.


## Features

- Efficient Indexing: Utilizing MapReduce tasks to efficiently analyze the entire corpus and generate unique word IDs, calculate Inverse Document Frequency (IDF), and create a consolidated vocabulary.
- Vectorized Representation: The Indexer computes a machine-readable representation of the entire document corpus using TF/IDF weighting.
- Relevance Analysis: The Ranker Engine generates a vectorized representation for user queries and conducts relevance analysis by calculating the relevance function between the query and each document. This enables the retrieval of sorted lists of relevant documents based on relevance scores.


## Team:

- **Manal Aamir**: [GitHub](https://github.com/manal-aamir)
- **Mohammad Malik**: [GitHub](https://github.com/mohammad-malik)
- **Aqsa Fayaz**: [GitHub](https://github.com/Aqsa-Fayaz)

