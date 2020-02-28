# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import json
import shutil

from Qt import QtCore, QtWidgets, QtGui

import CGAgnostics.GUI as agUI
import controllers as ctrl
from components.source import Source
import controllers.sources as sources
import controllers.export as exp

_logs_dir = os.path.join(os.getcwd(), "logs")
if not os.path.exists(_logs_dir):
    os.makedirs(_logs_dir)


__version__ = "1.0.0"
_NAME = "OolTranscoder"
__author__ = "Jair Anguiano"


class Transcoding(agUI.ToolkitQDialog):
    def __init__(self):
        super().__init__(parent=None)

        self.setWindowTitle(f"{_NAME} | {__version__}")
        self._main_path = self.execution_path().replace(
            "CGAgnostics\GUI", "")
        self._icons_path = os.path.join(self._main_path, 'icons')
        self._window_icon = QtGui.QIcon(
            os.path.join(self._icons_path, "video.ico"))
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(self._window_icon)
        self.resize(1320, 800)

        self._widgets()
        self._layouts()
        self._methods()

    def _widgets(self):
        self._H_splitter_SPL = agUI.ToolkitQSplitter()
        self._H_splitter_SPL.setOrientation(QtCore.Qt.Horizontal)
        self._V_splitter_SPL = agUI.ToolkitQSplitter()
        self._V_splitter_SPL.setOrientation(QtCore.Qt.Vertical)
        self.console = agUI.ToolkitQConsole()
        self.footer = agUI.ToolkitQFooter(self)

        self.master = Source(parent=self, name="MASTER")
        self.generic = Source(parent=self, name="GENERICO")
        self.intergeneric = Source(parent=self, name="INTERGENERICO")

        self._export_WGT = QtWidgets.QWidget()
        self._export_path_LBL = agUI.ToolkitQLabel("<h3>Destination:</h3>")
        self._export_path_LNE = agUI.ToolkitQLineEdit()
        self._export_path_BTN = agUI.ToolkitQBrowseButton(
            self, lineedit=self._export_path_LNE, size=[40, 40])
        self._export_BTN = agUI.ToolkitQCreateButton(size=[100, 40])

    def _layouts(self):
        _V_LYT = QtWidgets.QVBoxLayout(self)
        _H_export_button_LYT = QtWidgets.QHBoxLayout()
        _H_export_button_LYT.addWidget(self._export_path_LBL)
        _H_export_button_LYT.addWidget(self._export_path_LNE)
        _H_export_button_LYT.addWidget(self._export_path_BTN)
        _H_export_button_LYT.addWidget(self._export_BTN)

        self._export_WGT.setLayout(_H_export_button_LYT)

        self._V_splitter_SPL.addWidget(self.master.widget)
        self._V_splitter_SPL.addWidget(self.generic.widget)
        self._V_splitter_SPL.addWidget(self.intergeneric.widget)
        self._V_splitter_SPL.addWidget(self._export_WGT)

        self._H_splitter_SPL.addWidget(self._V_splitter_SPL)
        self._H_splitter_SPL.addWidget(self.console.widget)
        _V_LYT.addWidget(self._H_splitter_SPL)
        _V_LYT.addWidget(self.footer.widget)
        self.V_root_window_LYT = _V_LYT

    def _methods(self):

        def transcode():

            _sources = [self.master, self.generic, self.intergeneric]
            _export_path = self._export_path_LNE.text()
            _messages = []
            _outputs = []
            _commands_dictionary = []

            _messages.append(["<h4>User input:</h4>", "standar"])

            for each in _sources:
                if each.is_enabled:
                    _outputs.append(each)

            if len(_outputs) == 0:
                self.console.log("<h4>Nothing to export.</h4>", "standar")
                return

            if os.path.isdir(_export_path):
                _configs = sources.outputs(_outputs, _export_path, _messages)
                _messages.append(
                    ["<h4>Directories creation:</h4>", "standar"])
                for val in _configs.values():
                    self.create_folders_from_config_file(val, _messages)

                    self.console.log_list(_messages)
                    _commands_dictionary.append(exp.with_source(val))

                self.console.log_list(_messages)


                with open(os.path.join(_logs_dir, "_02_commands.txt"), "w") as fp:
                    fp.write(str(_commands_dictionary))
                

                if self.valid_sources(_outputs):
                    self.run_commands(_commands_dictionary)
                else:
                    self.console.log_list(
                    [['Something went wrong, check for the following errors:', "standar"],
                    ['<img src="./CGAgnostics/icons/x_XS.png"></img> - Your sources files path doesn\'t exists or is invalid.', "error"]])
            else:
                self.console.log_list(
                    [['Something went wrong, check for the following errors:', "standar"],
                    ['<img src="./CGAgnostics/icons/x_XS.png"></img> - Your destination path doesn\'t exists.', "error"]])

        self._export_BTN.clicked.connect(transcode)

    @staticmethod
    def create_folders_from_config_file(config, messages=[]):
        result = {"enable": False}

        def _create(setup):
            path = setup["path"].replace('"', "")
            if setup["enable"] and not os.path.exists(path):
                os.makedirs(path)
                messages.append(
                    [f'<img src="./CGAgnostics/icons/check_XS.png"></img> - {config["name"]}: {setup["name"]} directory created.', "success"])
            else:
                messages.append(
                    [f'<img src="./CGAgnostics/icons/check_XS.png"></img> - {config["name"]}: {setup["name"]} directory exists.', "success"])

        if config['enable']:
            _images = {
                "enable": config["images"]["enable"],
                "name": "IMAGES",
                "path": os.path.dirname(config["images"]["output"])
            }

            _UNCOMPRESS = {
                "enable": config["video"]["UNCOMPRESS"]["enable"],
                "name": "UNCOMPRESS",
                "path": os.path.dirname(
                    config["video"]["UNCOMPRESS"]["output"])
            }

            _QT = {
                "enable": config["video"]["QT"]["enable"],
                "name": "QT",
                "path": os.path.dirname(
                    config["video"]["QT"]["output"])
            }

            _HD = {
                "enable": config["video"]["HD"]["enable"],
                "name": "HD",
                "path": os.path.dirname(
                    config["video"]["HD"]["output"]
                )
            }

            _create(_images)
            _create(_UNCOMPRESS)
            _create(_QT)
            _create(_HD)
            result["enable"] = True
        else:
            messages.append(
                [f'<img src="./CGAgnostics/icons/warning_XS.png"></img> - {config["name"]}: Directories were not created due missing information.', "warning"])

        return result

    def run_commands(self, list_of_commands_dict):
        result = []
        for command_config in list_of_commands_dict:
            for command in command_config.values():
                if command["valid"]:
                    if command["mode"] == "ffmpeg":
                        #_QProcess = QtCore.QProcess()
                        #_QProcess.start(command["composed"][0], command["composed"][1:])
                        result = subprocess.run(command["composed"], stdout=True, text=True)
                        self.console.log(result)
                    elif command["mode"] == "copy":
                        shutil.copyfile(command["composed"][0], command["composed"][1])
                else:
                    pass

        return result

    def valid_sources(self, outputs):
        for output in outputs:
            if not os.path.isfile(output.source):
                return False
        return True
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = Transcoding()
    window.show()
    app.exec_()
