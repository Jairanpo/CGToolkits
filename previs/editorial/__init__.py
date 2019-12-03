
import os
import maya.app.edl.importExport as EDL
import pymel.core as pm


def export(path, shotcode='', version=''):
    '''
        Summary: 
            Export formatted editorial file

        Parameters:
            path: Path where to save the file
            shotcode: Shotcode prefix
            version: Editorial version
    '''

    path_and_scene = os.path.split(path)
    editorial_name = shotcode + "_Editorial_" + version + ".xml"
    editorial_path = os.path.join(path, editorial_name)
    EDL.doExport(editorial_path, 0)
