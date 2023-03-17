import ijson
import json
import os

filename = '/home/sansforensics/Desktop/working/cttout_MCCONTROLRMPC_20230311_15_30_40_clean.json'

def extract_schema(obj, schema):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, list):
                if len(value) > 0 and isinstance(value[0], dict):
                    schema[key] = [extract_schema(v, {}) for v in value]
                else:
                    schema[key] = [type(v).__name__ for v in value]
            elif isinstance(value, dict):
                schema[key] = extract_schema(value, {})
            else:
                schema[key] = type(value).__name__
        return schema
    elif isinstance(obj, list):
        if len(obj) > 0 and isinstance(obj[0], dict):
            return [extract_schema(elem, {}) for elem in obj]
        else:
            return [type(elem).__name__ for elem in obj]
    else:
        return type(obj).__name__

def sort_schema(schema):
    sorted_schema = {}
    for key in sorted(schema.keys()):
        value = schema[key]
        if isinstance(value, dict):
            sorted_schema[key] = sort_schema(value)
        elif isinstance(value, list):
            sorted_schema[key] = []
            for item in value:
                if isinstance(item, dict):
                    sorted_schema[key].append(sort_schema(item))
                else:
                    sorted_schema[key].append(item)
        else:
            sorted_schema[key] = value

    return sorted_schema

def remove_duplicates(schema):
    cleaned_schema = {}
    for key, value in schema.items():
        if isinstance(value, dict):
            cleaned_value = remove_duplicates(value)
            if cleaned_value not in cleaned_schema.values():
                cleaned_schema[key] = cleaned_value
        else:
            cleaned_schema[key] = value

    return cleaned_schema

with open(filename, 'rb') as file:
    parser = ijson.items(file, 'cyberTriageAgentOutput.item.cyberTriageOutputSection.item')

    schema = {}

    for obj in parser:
        extract_schema(obj, schema)

if schema:
    sorted_schema = sort_schema(schema)
    cleaned_schema = remove_duplicates(sorted_schema)

    schema_filename = os.path.splitext(filename)[0] + "_schema.json"

    with open(schema_filename, 'w', encoding='utf-8') as schema_file:
        json.dump(cleaned_schema, schema_file, ensure_ascii=False, indent=2)

    print(f"Schema of JSON data is saved to {schema_filename}")
else:
    print("Error: JSON data not found in file.")
