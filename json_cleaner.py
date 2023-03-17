import os
import re
import gzip

# Regular expression pattern to match non-ASCII characters
non_ascii_pattern = '[^\x00-\x7F\x80-\xFF\u001c]+'


# Replace non-ASCII characters with spaces
def clean_string(s):
    cleaned = re.sub(non_ascii_pattern, ' ', s)

    # Handle file separator character
    cleaned = re.sub('\x1c', '', cleaned)

    return ''.join(ch if ch.isprintable() or ch.isspace() else ' ' for ch in cleaned)


def clean_json_file(filepath):
    if filepath.endswith('.gz'):
        # Create a new filename for the cleaned JSON file
        cleaned_filename = os.path.splitext(filepath)[0] + "_clean.json"

        try:
            # Open the input file as a gzip file
            print(f"Reading {filepath}...")
            with gzip.open(filepath, 'rb') as input_file:
                # Open the output file as a regular file
                with open(cleaned_filename, 'wb') as output_file:
                    # Process the file in 1 MB chunks
                    chunk_size = 1024 * 1024
                    while True:
                        chunk = input_file.read(chunk_size)
                        if not chunk:
                            break
                        # Decode the chunk and clean it
                        chunk_decoded = chunk.decode('utf-8', 'ignore')
                        chunk_cleaned = clean_string(chunk_decoded)
                        # Write the cleaned chunk to the output file
                        chunk_encoded = chunk_cleaned.encode('utf-8')
                        output_file.write(chunk_encoded)

            print(f"Cleaning of JSON file is complete. Results are saved to {cleaned_filename}")

        except EOFError:
            print(f"Error: {filepath} is a corrupt .json.gz file.")
    else:
        print(f"Error: {filepath} is not a .json.gz file.")


if __name__ == "__main__":
    filepath = "/path/to/json/file.json.gz"
    clean_json_file(filepath)
