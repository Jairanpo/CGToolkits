import pymel.core as pm


def fit_select_camera():
    result = {"status": False,
              "message": ""}

    list_of_shots = pm.ls(sl=True, type='shot')
    if is_only_one_shot_selected(list_of_shots):
        s = list_of_shots[0]
        cam = get_camera_from_shot(s)
        ctrl = get_control_name_from_camera_name(cam)
        frame_select_camera_control(ctrl)
        result = {"status": "success",
                  "message": "Camera framed."}
    else:
        result = {"status": "error",
                  "message": "Select only one shot from your sequencer."}

    return result


def frame_select_camera_control(control_name):
    pm.select(control_name)
    pm.viewFit('persp')


# ---------------------------------------------------------


def get_control_name_from_camera_name(camera_name):
    shot_number = camera_name.split('_')[0]
    return '{}_main_CTL'.format(shot_number)


def get_camera_from_shot(shot_node):
    return shot_node.getCurrentCamera()


# ---------------------------------------------------------


def is_only_one_shot_selected(list_of_shots):
    if len(list_of_shots) == 1:
        return True
    else:
        return False
