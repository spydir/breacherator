import os
import re
import subprocess

# Regular expression pattern to match non-ASCII characters
non_ascii_pattern = '[^\x00-\x7F\x80-\xFF\u001c]+'


# Replace non-ASCII characters with spaces

def clean_json_file(filepath):
    if filepath.endswith('.json.gz'):
        # Create a new filename for the cleaned JSON file
        dirname, basename = os.path.split(filepath)
        filename, ext = os.path.splitext(basename)
        filename, ext = os.path.splitext(filename)
        tmp_filename = os.path.join(dirname, f"{filename}.tmp")
        cleaned_filename = os.path.join(dirname, f"{filename}_clean.json")

        # Call zgrep command to remove "fileContent" key:value pair
        print(f"Removing 'fileContent' key:value pair from {filepath}...")
        print(f"Cleaning {cleaned_filename}...")
        subprocess.run(['chmod', '+x', './json_cleaner.sh'])
        subprocess.run(['./json_cleaner.sh', filepath, tmp_filename, cleaned_filename])

    else:
        print(f"Error: {filepath} is not a .json.gz file.")

if __name__ == "__main__":
    filepath = "/path/to/json/file.json.gz"
    clean_json_file(filepath)