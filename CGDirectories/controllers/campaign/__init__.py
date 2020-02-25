import os

import CGDirectories.config as config
import CGDirectories.controllers.project as project
import CGDirectories.controllers.assets as assets
import CGDirectories.controllers.shots as shots
import CGDirectories.controllers.utilities.subfolders as subfolders
import CGDirectories.controllers.campaign.meta as meta


def create_projects_matrix(path, matrix):
    """
    Create project using a configuration matrix

    Arguments:
        path {string} -- Root path for the project creation, this has to be the
                         \"Projects\" root folder under the campaign folder.
        matrix {matrix 3x3} --  [project_name, shotcode, shots_amount]
    """
    for name, code, amount in matrix:
        _project_path = os.path.join(path, name)
        os.makedirs(_project_path)
        shots_dict = shots.create_shots_list(code, amount + 1)
        project.create(_project_path, shots_dict)


def simple(path, campaign, list_of_shots, shot_code, shot_amount):
    """
    Simple campaing creation

    Arguments:
        path {string} -- Root path for the campaign creation, this has to be the 
                         \"Brand\" root folder.
        campaign {string} -- Campaign name where the directory will be created.
        list_of_shots {[string]} -- [description]
    """
    result = {"status": "error", "message": ""}

    _campaign_path = os.path.normpath(os.path.join(path, campaign))

    if os.path.exists(_campaign_path):
        result["status"] = "error"
        result["message"] = "That campaign already exists."
        return result

    _config = config.get("simple")

    _keys = ["client", "art", "timetable",
             "sequence", "audio", "final", "reviews"]

    _paths = {}

    for key in _keys:
        _paths[key] = os.path.join(path, campaign, _config[key]["name"])

        if os.path.exists(_paths[key]):
            pass
        else:
            os.makedirs(_paths[key])
            subfolders.create(
                _paths[key], config_string="simple", key=key)

    assets.directory(_campaign_path)
    shots.create_shots(_paths["sequence"], list_of_shots)
    result["status"] = "success"
    result["message"] = f"Campaign created successfully at: {_campaign_path}"

    meta.write(path, campaign, project_data={
        "type": "simple",
        "shots": {"code": shot_code.upper(), "amount": shot_amount}})

    return result


def agUIlex(path, campaign, matrix):
    """
    This function will create a agUIlex campaign

    Arguments:
        path {string} -- Root path for the campaign creation, this has to be the 
                         \"Brand\" root folder.
        campaign {String} -- Campaign name where the directory will be created.
        matrix {matrix 3x3} --  [project_name, shotcode, shots_amount]
    """
    result = {"status": "error", "message": ""}

    _campaign_path = os.path.normpath(os.path.join(path, campaign))
    if os.path.exists(_campaign_path):
        result = {"status": "error",
                  "message": "That campaign already exists."}
        return result

    _config = config.get("agUIlex")
    _keys = ["projects", "assets", "timetable", "client", "final"]

    _paths = {}

    for key in _keys:
        _paths[key] = os.path.join(path, campaign, _config[key]["name"])

        if os.path.exists(_paths[key]):
            pass
        else:
            os.makedirs(_paths[key])
            subfolders.create(
                _paths[key], config_string="agUIlex", key=key)

    assets.directory(_campaign_path)
    create_projects_matrix(os.path.join(_campaign_path, "Projects"), matrix)

    _project = {"type": "agUIosed", "subprojects": []}

    for subproject, code, amount in matrix:
        entry = {"name": subproject, "shots": {
            "code": code.upper(), "amount": amount}}
        _project["subprojects"].append(entry)

    meta.write(
        path=path, campaign=campaign, project_data=_project)

    result["status"] = "success"
    result["message"] = f"Campaign created successfully at: {_campaign_path}"

    return result


if __name__ == '__main__':
    path = os.getcwd()
    sequence = input('Sequence name: ')
    shotcode = input('Shot code (only three characters): ')
    amount = input('How many shots you need? ')

    shots = shots.create_shots_list(shotcode, amount)

    if sequence and shots["exist"]:
        simple(path, sequence, shots["list_of_shots"])
    else:
        print('Game over, try again!')
