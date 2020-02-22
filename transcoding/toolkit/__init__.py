# -*- coding: utf-8 -*-
import sys
import os

import modules
import CGAgnostics.GUI as agUI
from Qt import QtCore, QtWidgets, QtGui

import transcoding.controllers as ctrl
from transcoding.components.source import Source
import transcoding.controllers.sources as sources
import transcoding.controllers.export as exp
import json

_logs_dir = os.path.join(os.getcwd(), "transcoding", "logs")
if not os.path.exists(_logs_dir):
    os.makedirs(_logs_dir)


__version__ = "1.0.0"

class Transcoding(agUI.ToolkitQDialog):
    def __init__(self):
        super().__init__(parent=None)

        self.setWindowTitle(f"Transcoding | {__version__}")
        self._main_path = self.execution_path().replace(
            "CGAgnostics\GUI", "transcoding\\toolkit")
        self._icons_path = os.path.join(self._main_path, 'icons')
        self._window_icon = QtGui.QIcon(
            os.path.join(self._icons_path, "video.ico"))
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(self._window_icon)
        self.resize(1000, 1000)
    

        self._widgets()
        self._layouts()
        self._methods()

    def _widgets(self):
        self._title = agUI.ToolkitQLabel("<h3>Transcoding Toolkit:</h3>")
        self._title.setStyleSheet("color:rgb(200,150,70)")
        self._splitter_SPL = agUI.ToolkitQSplitter()
        self._splitter_SPL.setOrientation(QtCore.Qt.Vertical)
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

        self._splitter_SPL.addWidget(self.master.widget)
        self._splitter_SPL.addWidget(self.generic.widget)
        self._splitter_SPL.addWidget(self.intergeneric.widget)
        self._splitter_SPL.addWidget(self._export_WGT)
        self._splitter_SPL.addWidget(self.console.widget)
        self._splitter_SPL.addWidget(self.footer.widget)

        _V_LYT.addWidget(self._title)
        _V_LYT.addWidget(self._splitter_SPL)
        self.V_root_window_LYT = _V_LYT

    def _methods(self):
        
        def transcode():
            _sources = [self.master, self.generic, self.intergeneric] 
            _export_path = self._export_path_LNE.text()
            _messages = []
            _outputs = []
            _commands = []

            for each in _sources:
                if each.is_enabled:
                    _outputs.append(each)

            if len(_outputs) == 0:
                self.console.log("<h4> -> Nothing to export.</h4>", "standar")
                return

            if os.path.isdir(_export_path):
                _outputs = sources.outputs(_outputs, _export_path, _messages)
                for val in _outputs.values():
                    self.create_folders_from_config_file(val)
                    _commands.append(exp.with_source(val))
                    

                self.console.log_list(_messages)
            else:
                self.console.log("<h4> -> Set your destination path first.</h4>", "warning")
            

            with open(os.path.join(_logs_dir, "_01_outputs.json"), "w") as fp:
                json.dump(_outputs, fp, indent=4, sort_keys=True)

            with open(os.path.join(_logs_dir, "_02_commands.json"), "w") as fp:
                json.dump(_commands, fp, indent=4, sort_keys=True)

        self._export_BTN.clicked.connect(transcode)

    @staticmethod
    def create_folders_from_config_file(config):
        print(f'VALUES: {config["images"]["enable"]}')
        if config["images"]["enable"]:
            os.makedirs(os.path.dirname(config["images"]["output"]))

        if config["video"]["UNCOMPRESS"]["enable"]:
            os.makedirs(os.path.dirname(config["video"]["UNCOMPRESS"]["output"]))

        if config["video"]["QT"]["enable"]:
            os.makedirs(os.path.dirname(config["video"]["QT"]["output"]))

        if config["video"]["HD"]["enable"]:
            os.makedirs(os.path.dirname(config["video"]["HD"]["output"]))

    

        

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = Transcoding()
    window.show()
    app.exec_()
