import os
import CGDirectories.config as config

import CGDirectories.controllers.assets as assets
import CGDirectories.controllers.shots as shots
import workareaDir


def create(path, config_data):
    if os.path.exists(path):
        workareaDir.create(path, config_data)
    else:
        os.mkdir(path)
        workareaDir.create(path, config_data)
