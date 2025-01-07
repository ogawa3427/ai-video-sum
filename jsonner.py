import json

# Function to extract timestamps and corresponding text
def extract_timestamps(input_text):
    lines = input_text.splitlines()
    entries = []

    for line in lines:
        # Extract timestamp and text using a simple split
        if line[:5].replace(':', '').isdigit():
            timestamp = line[:5]
            text = line[6:]
            entries.append({"timestamp": timestamp, "text": text})

    return entries

# Function to process file input
def process_file(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        input_text = f.read()
    return extract_timestamps(input_text)

# Specify input and output files
input_file = "transcript.txt"
output_file = "timestamps.json"

# Process the input file
output_data = process_file(input_file)

# Convert the result to JSON
json_output = json.dumps(output_data, indent=4, ensure_ascii=False)

# Save the JSON to a file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(json_output)

print(f"JSON data saved to {output_file}")
