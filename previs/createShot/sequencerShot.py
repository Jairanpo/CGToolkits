import pymel.core as pm

def create(shot_data, camera):
    new_shot = pm.shot('{0}_{1}_SHT'.format(shot_data["project"], shot_data["shot"]))
    new_shot.setStartTime(shot_data['start'])
    new_shot.setEndTime(shot_data['end'])
    new_shot.setSequenceStartTime(shot_data['start'])
    new_shot.setSequenceEndTime(shot_data['end'])
    new_shot.setCurrentCamera(camera)
