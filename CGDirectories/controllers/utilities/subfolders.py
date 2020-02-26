import os

import config as config
import controllers.assets as assets
import controllers.shots as shots
import controllers.workarea as workarea


def create_subfolders_with_workarea(path, config, key):
    for subfolder in config[key]["subfolders"]:
        _subfolder_path = os.path.join(path, subfolder)
        os.makedirs(_subfolder_path)

        workarea.create(_subfolder_path)


def create(path, config_string, key):
    _config = config.get(config_string)

    if key == "art":
        create_subfolders_with_workarea(path, _config, key)

    else:
        if _config[key]["subfolders"]:
            for subfolder in _config[key]["subfolders"]:
                _subfolder_path = os.path.join(path, subfolder)
                if os.path.exists(_subfolder_path):
                    pass
                else:
                    os.makedirs(_subfolder_path)
