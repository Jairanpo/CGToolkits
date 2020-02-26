import os
import config as config


def create_shot_directory_structure(path, shot_name):
    workarea = config.get("workarea")
    steps = config.get("shot_steps")

    def make_users_folders(playground_path):
        users = config.get("users")
        for user in users:
            os.mkdir(os.path.join(playground_path, user))

    def make_vfx_project_folders(playground_path):
        users = config.get("vfx_users")
        for user in users:
            os.mkdir(os.path.join(playground_path, user))

    def make_workarea(shot_path, step):
        step_dir = os.path.join(shot_path, step)
        playground_dir = os.path.join(step_dir, workarea[0])
        publish_dir = os.path.join(step_dir, workarea[1])

        os.makedirs(playground_dir)
        os.makedirs(publish_dir)

        if not "VFX" in step:
            make_users_folders(playground_dir)
        else:
            make_vfx_project_folders(playground_dir)

    if not os.path.exists(os.path.join(path, shot_name)):
        shot_dir = os.path.join(path, shot_name)
        os.mkdir(shot_dir)
        for step in steps:
            make_workarea(shot_dir, step)


def create_shots(path, list_of_shots):
    for each in list_of_shots:
        create_shot_directory_structure(path, each)


def create_shots_list(shotcode, amount):
    '''
    :param shotcode: Three characters long shotcode \"SHT\"
    :param amount: Amount of shots to create
    :return: A dictionary with bool key \"exists\" and \"list_of_shots\" with the shots to create
    '''

    result = {"exist": False, "list_of_shots": [], "message": ""}

    def create_shots_codes_list():
        for index in range(0, int(amount)):
            if index < 10:
                result["list_of_shots"].append(
                    "{}0{}0".format(shotcode.upper(), index))
            elif index > 9 and index < 100:
                result["list_of_shots"].append(
                    "{}{}0".format(shotcode.upper(), index))
            elif index > 99:
                result["list_of_shots"].append(
                    "{}{}".format(shotcode.upper(), index))

    if len(shotcode) != 3:
        result["message"] = "Your shotcode hast to be 3 characters long"
        return result
    elif not amount:
        result["message"] = "You didn\'t provide a valid amount of shots to create"
        return result
    else:
        result["exist"] = True
        create_shots_codes_list()
        return result


def create_shot_code(shotcode, number):
    shotcode = shotcode.upper()

    if number < 10:
        return "{}0{}0".format(shotcode, number)
    elif 9 < number < 100:
        return "{}{}0".format(shotcode, number)
    elif number > 99:
        return "{}{}".format(shotcode, number)


if __name__ == '__main__':
    path = os.getcwd()

    shots = input('Give me a list of shots to create separated by space: ')
    list_of_shots = shots.split(" ")

    if type(list_of_shots) == list:
        for shot in list_of_shots:
            create_shot_directory_structure(path, shot.upper())
