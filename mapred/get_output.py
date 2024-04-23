import subprocess


def get_merged_output():
    # Define the Hadoop command to fetch the output
    hadoop_cmd = "hadoop fs -cat /naive-search/output/merged_output"

    # Execute the command and get the output
    process = subprocess.Popen(
        hadoop_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    # Check for errors
    if process.returncode != 0:
        print(f"Error executing command: {stderr.decode()}")
        return

    # Write the output to the file
    with open("merged_output.txt", "w") as f:
        f.write(stdout.decode())


def fetch_mapreduce_output(job_path, output_file):
    # Define the Hadoop command to fetch the output
    hadoop_cmd = f"hadoop fs -cat {job_path}/part-*"

    # Execute the command and get the output
    process = subprocess.Popen(
        hadoop_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    # Check for errors
    if process.returncode != 0:
        print(f"Error executing command: {stderr.decode()}")
        return

    # Write the output to the file
    with open(output_file, "w") as f:
        f.write(stdout.decode())


# Prompt the user for a number
output_map = {
    "1": "preprocessed",
    "2": "word_enum",
    "3": "tf_df",
    "4": "doc_ranking",
    "5": "query_vector",
    "6": "ranked_docs",
    "7": get_merged_output,
}

prompt = "Enter the output number to fetch ("
prompt += ', '.join(f"{key}: {value}"
                    for key, value in output_map.items() if key not in ["7"])
prompt += ", 7: merged_output): "

output_to_get = "unset"
while output_to_get == "unset":
    output_to_get = input(prompt)

    if output_to_get in output_map:
        if callable(output_map[output_to_get]):
            output_map[output_to_get]()
            exit()
        else:
            output_to_get = output_map[output_to_get]
    else:
        output_to_get = "unset"

# Specify the path to the MapReduce job output and the output file
job_path = f"/naive-search/output/{output_to_get}/"
output_file = f"output_{output_to_get}.txt"

# Fetch the output
fetch_mapreduce_output(job_path, output_file)
