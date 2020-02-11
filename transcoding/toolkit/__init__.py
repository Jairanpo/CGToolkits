# -*- coding: utf-8 -*-
import sys
import subprocess
import os

import modules
import CGAgnostics.GUI as agUI
from Qt import QtCore, QtWidgets, QtGui

import transcoding.controllers as ctrl
from transcoding.toolkit.components.source import Source

__version__ = "1.0.0"


class Transcoding(agUI.ToolkitQDialog):
    def __init__(self):
        super().__init__(parent=None)

        self.setWindowTitle(f"Transcoding | {__version__}")
        self._main_path = self.execution_path().replace(
            "CGAgnostics\GUI", "transcoding\\toolkit")
        print(self._main_path)
        self._icons_path = os.path.join(self._main_path, 'icons')
        self._window_icon = QtGui.QIcon(
            os.path.join(self._icons_path, "video.ico"))
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(self._window_icon)
        self.resize(1000, 400)

        self._widgets()
        self._layouts()
        self._methods()

    def _widgets(self):
        self._title = agUI.ToolkitQLabel("<h2>Transcoding Toolkit:</h2>")
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
            print("test")
            #print(self.master.is_enabled)
            #print(self.master.source)
            #print(self.master.do_export_videos)    
            #print(self.master.do_export_QT)
            #print(self.master.do_export_HD)
            #print(self.master.do_export_uncompress)
            #print(self.master.do_export_image_sequence)
            #print(self.master.image_sequence_path)


        self._export_BTN.clicked.connect(transcode)


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = Transcoding()
    window.show()
    app.exec_()
