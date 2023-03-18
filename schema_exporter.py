import ijson
import json
import os
from decimal import Decimal
def extract_schema_from_file(filepath):
    with open(filepath, 'r') as file:
        objects = ijson.items(file, 'cyberTriageAgentOutput.item.cyberTriageOutputSection.item')
        schema = {}
        for obj in objects:
            schema = extract_schema(obj, schema)

        # Sort schema keys alphabetically and remove duplicates
        schema = sort_and_remove_duplicates(schema)

        # Write schema to file
        schema_filepath = f"{os.path.splitext(filepath)[0]}_schema.json"
        with open(schema_filepath, 'w') as outfile:
            json.dump(schema, outfile, indent=4)

        return schema

def extract_schema(obj, schema):
    for key, value in obj.items():
        if isinstance(value, dict):
            schema[key] = extract_schema(value, schema.get(key, {}))
        else:
            schema[key] = schema.get(key, set())
            schema[key].add(type(value).__name__)
    return schema


def cast_decimals_to_float(schema):
    for key, value in schema.items():
        if isinstance(value, dict):
            schema[key] = cast_decimals_to_float(value)
        elif isinstance(value, set):
            if 'Decimal' in value:
                value.remove('Decimal')
                value.add('float')
            schema[key] = list(value)  # convert set to list
    return schema

def sort_and_remove_duplicates(schema):
    new_schema = {}
    for key, value in schema.items():
        if isinstance(value, dict):
            new_schema[key] = sort_and_remove_duplicates(value)
        else:
            new_schema[key] = sorted(list(set(value)))
    return new_schema

def extract_schemas_from_directory(directory):
    for filename in os.listdir(directory):
        print(filename)
        if filename.endswith('_clean.json'):
            filepath = os.path.join(directory, filename)
            extract_schema_from_file(filepath)