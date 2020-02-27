# Standar library
import sys
import os

# Third party
from PySide2 import QtWidgets, QtCore, QtGui

# Project
import CGAgnostics.GUI as agUI
from components.directoryWidget import DirectoryWidget as DirectoryWidget
import controllers.shots as shots


class Shot(DirectoryWidget):
    def __init__(self, parent=""):
        super().__init__(parent)

        self._widgets()
        self._layouts()
        self._methods()

    def _widgets(self):
        self.instructions = '''
            <h2>Instructions:</h2>
            <ul>
                <li>Set the path where you would like your directory to be created.</li>
                <li>The three characters should help to identify the shot, for example, if the project is named "NewYearsEve", the 
                three characters should be "NYE", "N" for "New", "Y" for "Years" and "E" for "Eve".</li>
                <li>The number you set will be padded using a three digits nomenclature, for example: 1 will be turned into 010, 20 will be turned into 200".</li>
            </ul>
        '''
        self.shot_code_LBL = agUI.ToolkitQLabel(
            'Shot code (three characters and three digits):')
        self.shot_code_LNE = agUI.ToolkitQLineEdit()
        shot_code_validator = QtGui.QRegExpValidator()
        shot_code_validator.setRegExp(r"[a-zA-Z]{3}[0-9]{3}")
        self.shot_code_LNE.setValidator(shot_code_validator)

    def _layouts(self):
        _V_LYT = QtWidgets.QVBoxLayout()

        _H_fields_LYT = QtWidgets.QHBoxLayout()
        _H_fields_LYT.addStretch()
        _H_fields_LYT.addWidget(self.shot_code_LBL)
        _H_fields_LYT.addWidget(self.shot_code_LNE)
        _H_fields_LYT.addStretch()

        _H_create_button_LYT = QtWidgets.QHBoxLayout()
        _H_create_button_LYT.addStretch()
        _H_create_button_LYT.addWidget(self.create_button)
        _H_create_button_LYT.addStretch()

        _V_LYT.addStretch()
        _V_LYT.addWidget(self.instructions)
        _V_LYT.addLayout(self.savepath_layout)
        _V_LYT.addLayout(_H_fields_LYT)
        _V_LYT.addLayout(_H_create_button_LYT)
        _V_LYT.addStretch()
        _V_LYT.setSpacing(20)

        self.layout = _V_LYT

    def _methods(self):
        def create_shot():
            path = self.savepath
            shotcode = self.shot_code_LNE.text().upper()

            if os.path.exists(path) and len(shotcode) == 6:
                if not os.path.exists(os.path.join(path, shotcode)):
                    shots.create_shot_directory_structure(path, shotcode)
                    self.console.log(
                        f"Your shot was created at: {os.path.join(path, shotcode)}", "success")
                else:
                    self.console.log('That shot already exists', "error")
            else:
                self.console.log('''
                                <p>Unable to create shot</p>
                                <p>check the following issues:<p>
                                <ul>
                                    <li>The specified shots path doesn't exists.</li>
                                    <li>The shot code field is incorrect.</li>
                                </ul>
                                ''', "error")

        self.create_button.clicked.connect(create_shot)
