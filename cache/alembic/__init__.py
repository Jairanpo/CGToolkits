import os

from PySide2 import QtCore
import pymel.core as pm


def export(metadata):
    """
        dictionary metadata:{
            "start":  frame at which start
            "end": frame at which end
            "path": path where the file will be saved,
            "filename": name that the file should have,
            "subfolder": subfolder name
            "shot": shot name,
            "root_flag": name that the node will have when imported to maya
            "version": version for the file suffix
        }
    """

    _root_flag = metadata["root_flag"]
    _filename = ""

    if metadata["shot"] == "":
        _filename = "{0}_{1}".format(metadata["filename"], metadata["version"])
    else:
        _filename = "{0}_{1}_{2}".format(metadata["shot"], metadata["filename"], metadata["version"])

    _filepath = os.path.join(metadata["path"], metadata["subfolder"])

    if not os.path.exists(_filepath):
        os.mkdir(_filepath)
        _filepath = os.path.join(_filepath, _filename)
    else:
        _filepath = os.path.join(_filepath, _filename)

    _filepath = os.path.normpath(_filepath)

    mel_command = '-frameRange {0} {1} -uvWrite -worldSpace -writeVisibility -dataFormat ogawa -root {2} -file {3}.abc'.format(
        metadata["start"],
        metadata["end"],
        _root_flag,
        _filepath)

    pm.AbcExport(j=mel_command)


def export_selected(QWidgetTable, metadata):
    """
        dictionary metadata:{
            "start":  frame at which start
            "end": frame at which end
            "path": path where the file will be saved,
            "subfolder": subfolder name
            "shot": shot name,
            "version": version for the file suffix
        }
    """
    result = {"status": False, "message": "Unable to export."}
    amount_of_nodes = QWidgetTable.rowCount()

    if amount_of_nodes > 0:
        for row in range(0, amount_of_nodes):
            node_filename = QWidgetTable.item(row, 1).data(QtCore.Qt.UserRole)
            node_root_flag = QWidgetTable.item(row, 2).data(QtCore.Qt.UserRole)

            export_data = {
                "start":  metadata["start"],
                "end": metadata["end"],
                "path": metadata["path"],
                "subfolder": metadata["subfolder"],
                "shot": metadata["shot"],
                "filename": node_filename,
                "root_flag": node_root_flag,
                "version": metadata["version"]
            }

            export(export_data)

        result = {"status": True,
                  "message": "Finished exporting your alembic files!"}

    return result
