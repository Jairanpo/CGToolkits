import os
import json
import re
import sys


def create(config, savepath, asset):
    for step in config["steps"].values():
        _number = f'0{step["number"]}' if step["number"] < 10 else step["number"]
        _savepath = os.path.join(savepath, asset, f'{_number}_{step["name"]}')

        if not os.path.exists(_savepath):
            os.makedirs(_savepath)
            create_workarea(step, _savepath)

        create_child_data(step, _savepath)


def create_child_data(step, savepath):
    file_extention_pattern = re.compile(r"\.\w*$")
    if len(step["children"]) > 1:
        for child in step["children"]:
            if bool(re.search(file_extention_pattern, child)):
                open(os.path.join(savepath, child), "a").close()
            else:
                if not os.path.exists(os.path.join(savepath, child)):
                    os.makedirs(os.path.join(savepath, child))


def create_workarea(step, savepath):
    print(savepath)
    _playground = os.path.join(savepath, "Playground")
    _publish = os.path.join(savepath,  "Publish")

    if step["workarea"]:
        if not os.path.exists(_playground):
            os.makedirs(_playground)
        if not os.path.exists(_publish):
            os.makedirs(_publish)


if __name__ == "__main__":
    _config = None
    _abs_path = os.path.split(os.path.abspath(__file__))[0]
    with open(f'{os.path.join(_abs_path, "config", "config.json")}') as json_file:
        _config = json.load(json_file)

    print(sys.argv)
    if len(sys.argv) < 3:
        print('''
        You didn\'t provide the correct arguments
        python [script] [savepath] [Asset names...]
        Example
        python [script_path] "C:\\users\\Projects" Foo Bar Baz
        ''')

    elif not os.path.exists(sys.argv[1]):
        print(f"Invalid path name: {sys.argv[1]}")

    else:
        for name in sys.argv[2:]:
            create(_config, sys.argv[1], name)
