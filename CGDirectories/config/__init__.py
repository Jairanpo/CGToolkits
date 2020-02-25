import json
import os


def get(data_string):
    current_path = os.path.dirname(__file__)
    file_path = os.path.join(current_path, "config.json")
    with open(file_path, "r") as config_data:
        return json.load(config_data)[data_string]
