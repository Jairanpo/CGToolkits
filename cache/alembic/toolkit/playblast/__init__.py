import os
import maya.mel
import pymel.core as pm


def do(path, shot):
    '''
        Summary:
            Create a shot based from the given shot and save at a given path

        Parameters:
            shot: {
                "start": Start frame,
                "end": End frame,
                "camera": Shot camera
                "code": Shot code name,
                "version": Version to append to the filename 
            }
            path: Path where to save the file
    '''

    aPlayBackSliderPython = maya.mel.eval('$tmpVar=$gPlayBackSlider')
    MyAudio = pm.timeControl(aPlayBackSliderPython, s=True, query=True)

    shot["camera"].displayGateMask.set(0)
    shot["camera"].displayResolution.set(0)
    shot["camera"].displaySafeAction.set(0)
    shot["camera"].displaySafeTitle.set(0)
    shot["camera"].overscan.set(1)

    pm.playblast(startTime=shot["start"], endTime=shot["end"], p=100, qlt=50,
                 forceOverwrite=True, sequenceTime=True, orn=True, sound=MyAudio, clearCache=True,
                 filename=path + '/' + shot["code"] + "_Clip_" + shot["version"], format='qt', compression="H.264")
