# Save a copy of your scene in publish area
import os
import pymel.core as pm
import re
import maya.app.edl.importExport as EDL

version = 'v003'
step = '01_Previs'

seq_path_pattern = re.compile(r'.*?Sequence')
pm.sceneName()
seq_path = os.path.normpath(re.search(seq_path_pattern, pm.sceneName()).group())
shots = os.listdir(seq_path)


def save_to_published_areas(path, list_of_shots, step_name, version):
    for each in list_of_shots:
        save_path = os.path.normpath(os.path.join(path, each, step, 'Publish', version))
        scene_name = '{0}_{1}{2}_{3}.ma'.format(each, step_name.lower(), 'Scene', version)
        scene_path = os.path.normpath(os.path.join(save_path, scene_name))

        if not os.path.exists(save_path):
            os.mkdir(save_path)
            pm.saveAs(scene_path)
        else:
            pm.saveAs(scene_path, force=True)


# save_to_published_areas(seq_path, shots, 'previs', version)


def export_editorial():
    path_and_scene = os.path.split(pm.sceneName())
    editorial_name = path_and_scene[1].replace('previsScene', 'editorial').replace('.ma', '.xml')
    editorial_path = os.path.join(path_and_scene[0], editorial_name)
    EDL.doExport(editorial_path, 0)


# export_editorial()






