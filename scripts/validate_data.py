# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "jsonschema>=4.25",
# ]
# ///

import argparse
import json
import logging
import os
from typing import Any, Dict

import jsonschema


def get_schema(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r") as f:
        return json.load(f)


def validate_file(file_path: str) -> None:
    with open(file_path, "r") as f:
        instance = json.load(f)
    schema = {
        "type" : "object",
        "properties" : {
            "price" : {"type" : "number"},
            "name" : {"type" : "string"},
        },
    }
    jsonschema.validate(instance, schema)


def expand_paths(paths: str) -> str:
    """Expand folders to file paths"""
    file_paths = []
    for path in paths:
        if os.path.isfile(path) and path.endswith(".json"):
            file_paths.append(file_paths)
        elif os.path.isdir(path):
            for root, _, file_names in os.walk(path):
                for file_name in file_names:
                    if file_name.endswith(".json"):
                        file_paths.append(os.path.join(root, file_name))
        else:
            raise Exception(f"Could not find file or directory at path: {path}")
    return file_paths
    

def main():
    parser = argparse.ArgumentParser(
        prog="validate_data",
        description="Validates that the JSON data conforms to the Pydantic schema",
    )
    parser.add_argument('paths', nargs="+", type=str, help="File or folder paths to the JSON data")
    parser.add_argument('-s', '--schema-path', type=str, help="File path to the JSON schema", required=True)
    args = parser.parse_args()
    file_paths = expand_paths(args.paths)
    has_errors = False
    schema = get_schema(args.schema_path)
    for file_path in file_paths:
        try:
            validate_file(file_path)
        except Exception as e:
            has_errors = True
            print(str(e))
    if has_errors:
        exit(1)
    


if __name__ == "__main__":
    main()
