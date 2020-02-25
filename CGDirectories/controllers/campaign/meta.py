import json
import os
import datetime


def write(path, campaign, project_data):
    _fullpath = os.path.join(path, campaign)
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
    data = dict()
    data["campaign"] = campaign
    data['created_at'] = str(datetime.datetime.now())
    data["data"] = project_data
    data["path"] = norm_path

    with open(os.path.join(norm_path, 'metadata.json'), 'w+') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)
