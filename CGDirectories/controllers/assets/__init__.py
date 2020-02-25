import os
import CGDirectories.config as config


def directory(path, name="Assets"):
    _root = os.path.join(path, name)
    _config = config.get("assets")
    _folders = ["environments", "fx", "props", "vehicles", "characters"]

    _paths = {}

    def create_subfolders(path, folder):
        if _config[folder]["subfolders"]:
            for subfolder in _config[folder]["subfolders"]:
                _subfolder_path = os.path.join(path, subfolder)
                if os.path.exists(_subfolder_path):
                    pass
                else:
                    os.makedirs(_subfolder_path)

    for folder in _folders:
        _paths[folder] = os.path.join(_root, _config[folder]["name"])

        if os.path.exists(_paths[folder]):
            pass
        else:
            os.makedirs(_paths[folder])
            create_subfolders(_paths[folder], folder)


def create_asset_directory_structure(path, asset_name, type="standar"):
    os.mkdir(os.path.join(path, asset_name))
    asset_steps = config.get("assets_steps")
    list_of_users = config.get("users")
    workarea = config.get("workarea")

    def create_asset_workarea(step):
        os.mkdir(os.path.join(path, asset_name, step, workarea[0]))
        os.mkdir(os.path.join(path, asset_name, step, workarea[1]))

    if type == "standar":
        for step in asset_steps:
            os.mkdir(os.path.join(path, asset_name, step))
            create_asset_workarea(step)


def create_asset_name(name):
    final = ''
    splitted_name = name.split(' ')

    if len(splitted_name) > 0:
        for i in range(0, len(splitted_name)):
            formatted = splitted_name[i].lower().capitalize()
            final += formatted

    return final


if __name__ == '__main__':
    name = input("Assests folder name (Assets or AssetsLibrary)")
    path = os.getcwd()
    directory(path, name)
