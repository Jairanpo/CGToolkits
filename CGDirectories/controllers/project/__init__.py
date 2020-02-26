
import os

import config as config
import controllers.shots as shots
import controllers.utilities as utils


def create(path, shots_data):
    _config = config.get("standalone_project")
    _keys = ["final", "sequence", "art", "audio", "review"]
    _paths = {}

    for key in _keys:
        _paths[key] = os.path.join(path, _config[key]["name"])

        if os.path.exists(_paths[key]):
            pass
        else:
            os.makedirs(_paths[key])
            utils.subfolders.create(
                _paths[key], config_string="standalone_project", key=key)

            if key == "sequence":
                for shot in shots_data["list_of_shots"]:
                    shots.create_shot_directory_structure(
                        _paths[key], shot.upper())
