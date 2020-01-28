import os

from Qt import QtCore, QtWidgets, QtGui
import CGAgnostics.GUI as agUI


class Source(agUI.ToolkitQDirectory):
    def __init__(self,  parent='', is_file=False):
        super().__init__(parent, is_file)
        self.savepath_LBL.setText('<h3>Source:</h3>')

        self._widgets()
        self._layouts()
        self._methods()

    def _widgets(self):
        self.name_LNE = agUI.ToolkitQLineEdit("new name")
        self.master_CBX = QtWidgets.QCheckBox("Master")
        self.generic_CBX = QtWidgets.QCheckBox("Generic")
        self.intergeneric_CBX = QtWidgets.QCheckBox("Intergeneric")

        self.master_LNE = agUI.ToolkitQLineEdit("MASTER")
        self.generic_LNE = agUI.ToolkitQLineEdit("GENERICO")
        self.intergeneric_LNE = agUI.ToolkitQLineEdit("INTERGENERICO")

    def _layouts(self):
        _V_LYT = QtWidgets.QVBoxLayout()

        _G_LYT = QtWidgets.QGridLayout()
        _G_LYT.addWidget(self.master_CBX, 0, 0)
        _G_LYT.addWidget(self.master_LNE, 0, 1)
        _G_LYT.addWidget(self.generic_CBX, 1, 0)
        _G_LYT.addWidget(self.generic_LNE, 1, 1)
        _G_LYT.addWidget(self.intergeneric_CBX, 2, 0)
        _G_LYT.addWidget(self.intergeneric_LNE, 2, 1)

        _V_LYT.addLayout(self.savepath_layout)
        _V_LYT.addWidget(self.name_LNE)
        _V_LYT.addLayout(_G_LYT)

        self.layout = _V_LYT

    def _methods(self):
        pass

    @property
    def widget(self):
        _wgt = QtWidgets.QWidget()
        _wgt.setLayout(self.layout)
        return _wgt

    @property
    def name(self):
        return self.name_LNE.text()
