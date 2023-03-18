import argparse
import os
import json
import json_cleaner
import schema_exporter

# Define command line arguments
parser = argparse.ArgumentParser(prog='breacherator', add_help=False)
parser.add_argument('directory', nargs='?', default='.', help='Directory containing JSON files')
parser.add_argument('-l', '--list', action='store_true', help='List JSON files in directory')
parser.add_argument('-e', '--export', action='store_true', help='Export schema from JSON files in directory')
parser.add_argument('-c', '--clean', action='store_true', help='Clean JSON files in directory')
parser.add_argument('--help', action='help', help='Show this help message and exit')

# Parse command line arguments
args = parser.parse_args()

# List JSON files in directory
if args.list:
    json_files = [f for f in os.listdir(args.directory) if f.endswith('.json.gz')]
    for f in json_files:
        print(os.path.join(args.directory, f))

# Extract schema from JSON files in directory
elif args.export:
    for filename in os.listdir(args.directory):
        if filename.endswith('_clean.json'):
            filepath = os.path.join(args.directory, filename)
            print(filepath)
            schema = schema_exporter.extract_schema_from_file(filepath)
            print(json.dumps(schema, indent=2))

# Clean JSON files in directory
elif args.clean:
    json_files = [f for f in os.listdir(args.directory) if f.endswith('.json.gz')]
    for f in json_files:
        filepath = os.path.join(args.directory, f)
        json_cleaner.clean_json_file(filepath)

# Default behavior: list JSON files in directory
else:
    json_files = [f for f in os.listdir(args.directory) if f.endswith('.json.gz')]
    for f in json_files:
        print(os.path.join(args.directory, f))