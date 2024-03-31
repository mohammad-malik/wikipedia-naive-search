# Introduction:
In order to create a naïve search engine capable of processing large volumes of data the following steps were followed:

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

### Important notes:
<li> Hadoop sucks. </li>
<li> Honest to God, no other assignment has made me this angry in my life. The constant issues that plagued it to the very end has made this the most displeasurable experience since joining university.</li>
