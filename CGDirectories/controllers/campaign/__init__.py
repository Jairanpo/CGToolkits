import os

import config as config
import controllers.project as project
import controllers.assets as assets
import controllers.shots as shots
import controllers.utilities.subfolders as subfolders
import controllers.campaign.meta as meta


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


def simple(path, campaign, list_of_shots, data):
    """
    Simple campaing creation

    Arguments:
        path {string} -- Root path for the campaign creation, this has to be the
                         \"Brand\" root folder.
        campaign {string} -- Campaign name where the directory will be created.
        list_of_shots {[string]} -- [description]
    """

    result = {"status": "error", "message": ""}

    _campaign_path = os.path.normpath(os.path.join(path, campaign["name"]))

    if os.path.exists(_campaign_path):
        result["status"] = "error"
        result["message"] = "That campaign already exists."
        return result

    _config = config.get("simple")

    _keys = ["client", "art", "timetable",
             "sequence", "audio", "final", "reviews"]

    _paths = {}

    for key in _keys:
        _paths[key] = os.path.join(
            path, campaign["name"], _config[key]["name"])

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

    meta.write(
        path,
        campaign,
        project_data={
            "type": "simple",
            "shots": {
                "code": data["shotcode"].upper(),
                "amount": data["amount"]
            }
        }
    )

    return result


def composed(path, campaign, matrix):
    """
    This function will create a composed campaign

    Arguments:
        path {string} -- Root path for the campaign creation, this has to be the
                         \"Brand\" root folder.
        campaign {String} -- Campaign name where the directory will be created.
        matrix {matrix 3x3} --  [project_name, shotcode, shots_amount]
    """
    result = {"status": "error", "message": ""}

    _campaign_path = os.path.normpath(os.path.join(path, campaign["name"]))
    if os.path.exists(_campaign_path):
        result = {"status": "error",
                  "message": "That campaign already exists."}
        return result

    _config = config.get("composed")
    _keys = ["projects", "assets", "timetable", "client", "final"]

    _paths = {}

    for key in _keys:
        _paths[key] = os.path.join(
            path, campaign["name"], _config[key]["name"])

        if os.path.exists(_paths[key]):
            pass
        else:
            os.makedirs(_paths[key])
            subfolders.create(
                _paths[key], config_string="composed", key=key)

    assets.directory(_campaign_path)
    create_projects_matrix(os.path.join(_campaign_path, "Projects"), matrix)

    _project = {"type": "composed", "subprojects": []}

    for subproject, code, amount in matrix:
        entry = {"name": subproject, "shots": {
            "code": code.upper(), "amount": amount}}
        _project["subprojects"].append(entry)

    meta.write(
        path=path, campaign=campaign, project_data=_project, mode="composed")

    result["status"] = "success"
    result["message"] = f"Campaign created successfully at: {_campaign_path}"

    return result
