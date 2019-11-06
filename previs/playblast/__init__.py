# -*- coding: utf-8 -*-
import pymel.core as pm
import os
import maya.mel

aPlayBackSliderPython = maya.mel.eval('$tmpVar=$gPlayBackSlider')
MyAudio = pm.timeControl(aPlayBackSliderPython, s=True, query=True)
playblast_Path = os.path.normpath(os.path.join(os.getenv("HOME"), 'Playblast'))
is_folder_in_desktop = os.path.exists(playblast_Path)

pm.headsUpDisplay('HUDFocalLength', visible=True, blockSize='small', labelFontSize='small', dataFontSize='large',
                  edit=True)
pm.headsUpDisplay('HUDCurrentFrame', visible=True, blockSize='small', labelFontSize='small', dataFontSize='large',
                  edit=True)
pm.headsUpDisplay('HUDCameraNames', visible=True, blockSize='large', labelFontSize='small', dataFontSize='large',
                  edit=True)
pm.headsUpDisplay('HUDFrameRate', visible=False, edit=True)
pm.headsUpDisplay('HUDViewAxis', visible=False, edit=True)


# ======================================================================================================================

def by_shots():
    result = {"status": "", "message": ""}
    list_of_shots = pm.ls(sl=True, type='shot')
    create_directory_in_desktop()
    if is_list_of_shots(list_of_shots):
        sequence_path = create_directory(list_of_shots[0].split('_')[0])
        for each in list_of_shots:
            setup_camera_settings(each)
            shot_range = shot_frame_range(each)
            pm.playblast(startTime=shot_range[0], endTime=shot_range[1], p=100, qlt=50,
                         forceOverwrite=True, sequenceTime=True, orn=True, sound=MyAudio, clearCache=True,
                         filename=sequence_path + '/' + each.name().split('_')[1], format='qt', compression="H.264")
        result["status"] = "success"
        result["message"] = "Playblast created at: {0}".format(sequence_path)
    else:
        result["status"] = "error"
        result["status"] = "Select shots to playblast in your sequencer."

    return result


def by_sequence():
    result = {"status": "", "message": ""}
    list_of_shots = pm.ls(sl=True, type='shot')
    create_directory_in_desktop()
    if is_list_of_shots(list_of_shots):
        sequence_path = create_directory(list_of_shots[0].split('_')[0])
        min_frame = get_min_frame_from_shots(list_of_shots)
        max_frame = get_max_frame_from_shots(list_of_shots)
        name = format_name_from_shots(min_frame.keys()[0], max_frame.keys()[0])
        pm.playblast(startTime=min_frame.values()[0], endTime=max_frame.values()[0], p=100, qlt=50,
                     forceOverwrite=True, sequenceTime=True, orn=True, sound=MyAudio, clearCache=True,
                     filename=sequence_path + '/' + '{0}_{1}'.format(
                         list_of_shots[0].name().split('_')[1], list_of_shots[-1].name().split('_')[1]),
                     format='qt', compression="H.264")
        result["status"] = "success"
        result["message"] = "Playblast created at: {0}".format(sequence_path)
    else:
        result["status"] = "error"
        result["message"] = "Select shots to playblast in your sequencer."

    return result


def is_shot_selected(list_of_shots):
    if len(list_of_shots) > 0:
        return True
    else:
        return False


# ======================================================================================================================


def format_name_from_shots(first_shot_name, last_shot_name):
    return '{0}-{1}'.format(first_shot_name[0:12], last_shot_name[8:12])


def get_min_frame_from_shots(list_of_shots):
    min_frame = None
    min_shot = {}
    for each_shot in list_of_shots:
        current_frame = each_shot.startFrame.get()
        if min_frame is None or min_frame > current_frame:
            min_shot = {each_shot.name(): each_shot.startFrame.get()}
            min_frame = each_shot.startFrame.get()
        else:
            pass
    return min_shot


def get_max_frame_from_shots(list_of_shots):
    max_frame = None
    max_shot = {}
    for each_shot in list_of_shots:
        f = each_shot.endFrame.get()
        if f > max_frame:
            max_shot = {each_shot.name(): each_shot.endFrame.get()}
            max_frame = each_shot.endFrame.get()
        else:
            pass
    return max_shot


# ======================================================================================================================

def is_list_of_shots(list_of_shots):
    if len(list_of_shots) > 0:
        return True
    else:
        return False


# ======================================================================================================================

def create_directory_in_desktop():
    try:
        if is_folder_in_desktop:
            print(
                'You already have a "Playblast" folder in your system, your playblast will be saved there')
        else:
            os.mkdir(playblast_Path)
            pm.warning(
                'You do not have a "Playblast" folder, one will be created')
    except:
        pm.error("Unable to create playblast folder")


def create_directory(sequence_name):
    subfolder_path = os.path.normpath(
        os.path.join(playblast_Path, sequence_name))
    if os.path.exists(subfolder_path):
        print('Sub-folder found')
    else:
        pm.warning('Sub-folder has been created in your system')
        os.mkdir(subfolder_path)
    return subfolder_path


# ======================================================================================================================

def setup_camera_settings(shot_name):
    camera_from_shot = pm.shot(shot_name, currentCamera=True, query=True)
    pm.setAttr(camera_from_shot + ".displayGateMaskColor", 0, 0, 0)
    pm.setAttr(camera_from_shot + ".displayGateMaskOpacity", 1)
    pm.setAttr(camera_from_shot + ".displayGateMask", 1)
    pm.setAttr(camera_from_shot + ".displayResolution", 1)
    pm.setAttr(camera_from_shot + ".overscan", 1)
    pm.setAttr(camera_from_shot + ".displaySafeAction", 0)


#        .......................................

def shot_frame_range(shot_name):
    range = []
    range.insert(0, pm.shot(shot_name, sequenceStartTime=True, query=True))
    range.insert(1, pm.shot(shot_name, sequenceEndTime=True, query=True))
    return range
