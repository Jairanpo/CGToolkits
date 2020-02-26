import os

import config as config
import controllers.assets as assets
import controllers.shots as shots
import workareaDir


def create(path, config_data):
    if os.path.exists(path):
        workareaDir.create(path, config_data)
    else:
        os.mkdir(path)
        workareaDir.create(path, config_data)
