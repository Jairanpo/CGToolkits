 import os
 import maya.app.edl.importExport as EDL
 import pymel.core as pm

 def export_editorial(self, path, name):
        editorial_path = os.path.join(path, name)
        EDL.doExport(editorial_path, 0)