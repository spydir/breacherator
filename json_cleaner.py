import os
import re
import json

# Regular expression pattern to match non-ASCII characters
non_ascii_pattern = '[^\x00-\x7F\x80-\xFF\u001c]+'


# Replace non-ASCII characters with spaces
def clean_string(s):
    cleaned = re.sub(non_ascii_pattern, ' ', s)

    # Handle file separator character
    cleaned = re.sub('\x1c', '', cleaned)

    return ''.join(ch if ch.isprintable() or ch.isspace() else ' ' for ch in cleaned)


def clean_json_file(filepath):
    # Create a new filename for the cleaned JSON file
    cleaned_filename = os.path.splitext(filepath)[0] + "_clean.json"

    # Read the entire JSON file into memory
    print(f"Reading {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as file:
        file_contents = file.read()

    # Replace the "fileContent" value with null and remove newline characters within the base64-encoded string
    file_contents = re.sub(r'("fileContent"\s*:\s*)"[^"]*"', r'\1null', file_contents)

    # Clean the contents of the JSON file
    cleaned_contents = clean_string(file_contents)

    # Write the cleaned JSON file
    print(f"Writing {cleaned_filename}...")
    with open(cleaned_filename, 'w', encoding='utf-8') as cleaned_file:
        cleaned_file.write(cleaned_contents)

    print(f"Cleaning of JSON file is complete. Results are saved to {cleaned_filename}")
