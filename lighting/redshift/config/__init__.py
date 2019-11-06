import json
import os


def get_id_values():
    current_path = os.path.dirname(__file__)
    file_path = os.path.join(current_path, "config.json")
    with open(file_path, "r") as config_data:
        return json.load(config_data)["settings"]["ID_values"]



