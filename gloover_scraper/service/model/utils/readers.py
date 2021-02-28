import json
import sys


def read_items(file_path):
    try:
        json_file = open(file_path)
        return json.load(json_file)
    except Exception as e:
        print(e, file=sys.stderr)
        return []