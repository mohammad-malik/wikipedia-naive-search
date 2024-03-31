import subprocess

# Simulated input
input_data = """
drunk\t1
real\t1
254880\tdrunk\t0.05
255052\tdrunk\t0.1
255070\tdrunk\t0.05
255077\treal\t0.05
255113\tdrunk\t0.05
255139\tdrunk\t0.05
255247\tdrunk\t0.05"""

# Call doc_ranking_reducer.py with the simulated input
process = subprocess.run(['python', './mapred/doc_ranking_reducer.py'], input=input_data, text=True, capture_output=True)

# Print the output
print(process.stderr)