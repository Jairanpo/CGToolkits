import os

from PySide2 import QtWidgets, QtCore, QtGui

import CGAgnostics.GUI as agUI


class Playblast:
    def __init__(self, parent):
        self._parent = parent
        self._V_root_LYT = None
        
        self._widgets()
        self._layouts()

    @property
    def widget(self):
        _WGT = QtWidgets.QWidget()
        _WGT.setLayout(self._V_root_LYT)
        return _WGT

    
    def _widgets(self):
        self._export_path = agUI.ToolkitQLineEdit()
        self._browse_button = agUI.ToolkitQBrowseButton(self._parent, lineedit=self._export_path, is_file=False, size=[30,30])
        #self._export_button = agUI.ToolkitQIconButton()


    def _layouts(self):
        _V_LYT = QtWidgets.QVBoxLayout()

        _H_export_path_LYT = QtWidgets.QHBoxLayout()
        _H_export_path_LYT.addWidget(self._export_path)
        _H_export_path_LYT.addWidget(self._browse_button)
        _V_LYT.addLayout(_H_export_path_LYT)

        self._V_root_LYT = _V_LYT


