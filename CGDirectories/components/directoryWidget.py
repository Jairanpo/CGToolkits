# Standar library
import sys
import os

# Third party
from PySide2 import QtWidgets, QtCore, QtGui

# Project
import CGAgnostics.GUI as agUI
import controllers.paths.execution as execution


class DirectoryWidget:
    def __init__(self, parent=""):
        self.parent = parent
        self._main_path = os.path.join(execution.root(), "components")
        self._icons_path = os.path.join(self._main_path, 'icons')
        self._search_icon = QtGui.QIcon(
            os.path.join(self._icons_path, "folder.ico"))
        self._create_icon = QtGui.QIcon(
            os.path.join(self._icons_path, "create.ico"))
        self.V_root_LYT = None
        self.V_savepath_LYT = None

        DirectoryWidget._widgets(self)
        DirectoryWidget._layouts(self)
        DirectoryWidget._methods(self)

    def _widgets(self):
        b_size = 40, 30
        self._instructions = agUI.ToolkitQLabel('')

        self.savepath_LBL = agUI.ToolkitQLabel('<h3>Path:</h3>')
        self.savepath_LNE = agUI.ToolkitQLineEdit()
        self.savepath_BTN = agUI.ToolkitQPushButton('')
        self.savepath_BTN.setIcon(self._search_icon)
        self.savepath_BTN.setIconSize(
            QtCore.QSize(b_size[0], b_size[1]))

        self.create_BTN = agUI.ToolkitQIconButton(self._create_icon)
        self.create_BTN.setIconSize(QtCore.QSize(200, 120))
        self.create_BTN.setMaximumWidth(270)
        self.create_BTN.setMinimumWidth(200)
        self.create_BTN.setMinimumHeight(55)
        self.create_BTN.setMaximumHeight(55)

    def _layouts(self):
        _V_LYT = QtWidgets.QVBoxLayout()
        _H_savepath_LYT = QtWidgets.QHBoxLayout()
        _H_savepath_LYT.addWidget(self.savepath_LBL)
        _H_savepath_LYT.addWidget(self.savepath_LNE)
        _H_savepath_LYT.addWidget(self.savepath_BTN)
        _V_LYT.addLayout(_H_savepath_LYT)

        self.V_savepath_LYT = _V_LYT

    def _methods(self):
        def set_savepath():
            file_path_FLD = QtWidgets.QFileDialog()
            path = file_path_FLD.getExistingDirectory(
                self.parent, "Select folder")
            if path:
                self.savepath_LNE.setText(path)

        self.savepath_BTN.clicked.connect(set_savepath)

    @property
    def savepath(self):
        return self.savepath_LNE.text().strip()

    @property
    def savepath_layout(self):
        return self.V_savepath_LYT

    @property
    def layout(self):
        return self.V_root_LYT

    @layout.setter
    def layout(self, value):
        self.V_root_LYT = value

    @property
    def console(self):
        return self._console

    @console.setter
    def console(self, ToolkitQConsole):
        self._console = ToolkitQConsole

    @property
    def create_button(self):
        return self.create_BTN

    @property
    def instructions(self):
        return self._instructions

    @instructions.setter
    def instructions(self, text):
        self._instructions.setText(text)
