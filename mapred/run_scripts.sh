#!/bin/bash

# Current dataset:
DATASET_FILE="/randomly_selected_chunk.csv"

# Setup environment variables
HDFS_INPUT_DIR=/naive_search/
HDFS_BASE_OUTPUT_DIR=/naive_search/output
BASE_DIR=/home/hadoopuser/naive_search/
QUERY_FILE=$BASE_DIR/query.txt

# Ensure the Hadoop directory exists
if ! hdfs dfs -test -d $HDFS_INPUT_DIR; then
    hdfs dfs -mkdir $HDFS_INPUT_DIR
    echo "Directory $HDFS_INPUT_DIR created."
fi

# Upload the dataset if not already present
if ! hdfs dfs -test -e $HDFS_INPUT_DIR/$DATASET_FILE; then
    hdfs dfs -put $BASE_DIR/$DATASET_FILE $HDFS_INPUT_DIR/$DATASET_FILE
    echo "Dataset uploaded to HDFS."
fi

# Upload the query file if not already present
if ! hdfs dfs -test -e $HDFS_INPUT_DIR/query.txt; then
    hdfs dfs -put $BASE_DIR/query.txt $HDFS_INPUT_DIR
    echo "Query file uploaded to HDFS."
fi

# Convert scripts to UNIX format
dos2unix $BASE_DIR/*

# Helper function to run MapReduce jobs
run_job() {
    hadoop jar $HADOOP_STR_JAR \
        -files $1 \
        -mapper $2 \
        -reducer $3 \
        -input $4 \
        -output $5
    if [ $? -ne 0 ]; then
        echo "$6 failed. Exiting."
        exit 1
    fi
}

# Run Preprocessing MapReduce Job
echo "Starting Preprocessing MapReduce Job..."
run_job "$BASE_DIR/preprocess_m.py,$BASE_DIR/preprocess_r.py" \
    "preprocess_m.py" "preprocess_r.py" \
    "$HDFS_INPUT_DIR/$DATASET_FILE" "${HDFS_BASE_OUTPUT_DIR}/preprocessed" \
    "Preprocessing MapReduce"

# Update the input for the Word Enumeration MapReduce job to use the preprocessed data
echo "Starting Word Enumeration MapReduce Job..."
run_job "$BASE_DIR/wordenumer_mapper.py,$BASE_DIR/wordenumer_reducer.py" \
    "wordenumer_mapper.py" "wordenumer_reducer.py" \
    "${HDFS_BASE_OUTPUT_DIR}/preprocessed/*" "${HDFS_BASE_OUTPUT_DIR}/word_enum" \
    "Word Enumeration MapReduce"

# Following jobs remain unchanged but now operate on the output of the previous job
echo "Starting Term Frequency and Document Frequency MapReduce Job..."
run_job "$BASE_DIR/mapper_tfidf.py,$BASE_DIR/reducer_tfidf.py" \
    "mapper_tfidf.py" "reducer_tfidf.py" \
    "${HDFS_BASE_OUTPUT_DIR}/word_enum/*" "${HDFS_BASE_OUTPUT_DIR}/tf_df" \
    "TF and DF MapReduce"

# Assuming the query is processed in the same way
echo "Starting Query Processing and Document Ranking..."
run_job "$BASE_DIR/query_vector_mapper.py,$BASE_DIR/doc_ranking_mapper.py,$BASE_DIR/doc_ranking_reducer.py" \
    "doc_ranking_mapper.py" "doc_ranking_reducer.py" \
    "${HDFS_BASE_OUTPUT_DIR}/tf_df/*,$HDFS_INPUT_DIR/query.txt" "${HDFS_BASE_OUTPUT_DIR}/ranked_docs" \
    "Query Processing and Document Ranking"

echo "All MapReduce jobs, including preprocessing and query processing, have completed successfully."
