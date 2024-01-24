import json

def read_config(config_file):
    """Read configuration settings from a JSON file."""
    with open(config_file, 'r') as file:
        return json.load(file)
