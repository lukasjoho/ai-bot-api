import json
import os

def get_data(filename: str):
    # Get the data directory relative to this file
    data_path = os.path.join(os.path.dirname(__file__), "data", filename)
    try:
        with open(data_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []