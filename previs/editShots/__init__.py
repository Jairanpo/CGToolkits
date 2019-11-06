import pymel.core as pm
import re

NOMENCLATURE_PATTERN = re.compile(r'\w{2}\d{3}')


def rename_shots(list_of_shots, strategy):
    '''
    :param list_of_shots:
    :param strategy: {'type':'shot', 'new_name':'SH010'}
    Rename current shot using 'project' or 'shot' strategies,
    Project strategy changes the name of the project on a shot.
    Shot strategy changes the shot nomenclature of the shot and the camera nodes associated.
    '''
    result = {"status": "", "message": ""}
    camera_nodes = None

    def validate_shot_renaming():
        existing_shot = pm.ls('*{}*'.format(strategy['new_name']))

        if len(list_of_shots) == 1 and len(existing_shot) == 0:
            return True
        else:
            return False

    def rename_camera_nodes(replace):
        for node in camera_nodes:
            node.rename(node.name().replace(replace, strategy['new_name']))

    if strategy['type'] == 'project':
        if len(list_of_shots) > 0 and len(strategy["new_name"]) > 2:
            for shot in list_of_shots:
                splitted_name = shot.split('_')
                splitted_name[0] = strategy['new_name']
                shot.shotName.set('_'.join(splitted_name))
                shot.rename('_'.join(splitted_name))
            result["status"] = "success"
            result["message"] = "Project name updated for selected shots."
        else:
            result["status"] = "error"
            result["message"] = '''
                - Select at least one shot in the sequencer.
                - Your new name should be at least three characters long.
                '''
    elif strategy['type'] == 'shot' and validate_shot_renaming():
        for shot in list_of_shots:
            splitted_name = shot.split('_')
            camera_nodes = pm.ls('*{}*'.format(splitted_name[1]))
            rename_camera_nodes(splitted_name[1])
            splitted_name[1] = strategy['new_name']
            shot.shotName.set('_'.join(splitted_name))
            shot.rename('_'.join(splitted_name))
        result["status"] = "success"
        result["message"] = "Shotcode updated for selected shot."
    else:
        result["status"] = "error"
        result["message"] = '''
            You can only change shotcode to one shot at the time, or maybe 
            some nodes in your scene had been named as the new name.
            Tips:
                - Try selection only one shot in the sequencer window.
                - Search your scene for nodes with the name you are trying to replace with.
            '''

    return result


def delete_shots():
    result = {"status": "", "message": ""}
    list_of_shots = pm.ls(sl=True, type='shot')

    if len(list_of_shots) > 0:
        for shot in list_of_shots:
            shot_nomenclature = re.search(NOMENCLATURE_PATTERN, shot.name())
            pm.delete(pm.ls('*{}*'.format(shot_nomenclature.group())))
        result["status"] = "success"
        result["message"] = "Shot data deleted."
    else:
        result["status"] = "error"
        result["message"] = "You didn\'t select any shot to delete."

    return result
