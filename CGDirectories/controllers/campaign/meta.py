import json
import os
import datetime

import controllers.campaign.writeHTML as writeHTML

def write(path, campaign, project_data, mode="simple"):
    _fullpath = os.path.join(path, campaign["name"])
    norm_path = os.path.normpath(_fullpath)
    '''
    :param path: path where to save the file
    :param year: year in the naming
    :param prefix: sequence prefix
    :param name: sequence name
    :param suffix: sequence suffix
    :param shotcode: shot codes
    :param amount: amount of shots
    :param project_name: full name of the project
    :return: void
    '''
    if mode == "simple":
        data = {}
        now = datetime.datetime.now()
        data["campaign"] = campaign
        data['created_at'] = f'{now.day}-{now.month}-{now.year}'
        data["data"] = project_data
        data["path"] = norm_path

        with open(os.path.join(norm_path, 'metadata.json'), 'w+') as meta:
            json.dump(data, meta, indent=4, sort_keys=True)

        with open(os.path.join(norm_path, 'info.html'), 'w+') as info:
            info.write(writeHTML.simple(data))

    elif mode == "composed":
        data = {}
        now = datetime.datetime.now()
        data["campaign"] = campaign
        data['created_at'] = f'{now.day}-{now.month}-{now.year}'
        data["data"] = project_data
        data["path"] = norm_path

        with open(os.path.join(norm_path, 'metadata.json'), 'w+') as meta:
            json.dump(data, meta, indent=4, sort_keys=True)

        with open(os.path.join(norm_path, 'info.html'), 'w+') as info:
            info.write(writeHTML.composed(data))
