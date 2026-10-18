"""JSON file storage helpers for blockchain data."""

import json


def load_json_file(file_path):
    """Load and return JSON data from a file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def save_json_file(data, file_path):
    """Save data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f)
