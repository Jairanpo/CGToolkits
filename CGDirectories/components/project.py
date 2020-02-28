# Standar library
import sys
import os

# Third party
from PySide2 import QtWidgets, QtCore, QtGui

# Project
import CGAgnostics.GUI as agUI
from components.directoryWidget import DirectoryWidget as DirectoryWidget
import controllers.shots as shots
import controllers.project as project


class Project(DirectoryWidget):

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
                <li>Provide the number of the sequence you would like to create, it <br>should be unique to the others projects in the path.</li>
                <li>Use pascal case to name your project: "NewYearsEve", "MyProjectName", "FooBarBaz".</li>
            </ul>
        '''

        self._project_LBL = agUI.ToolkitQLabel("<h4>Project</h4>")
        self._number_SBX = agUI.ToolkitQSpinBox("Number: ")
        self._number_SBX.setRange(1, 99)
        self._name_LNE = agUI.ToolkitQLineEdit("name")
        _name_validator = QtGui.QRegExpValidator()
        _name_validator.setRegExp(r"[a-zA-Z]{20}")
        self._name_LNE.setValidator(_name_validator)

        self._shots_LBL = agUI.ToolkitQLabel("<h4>Shots<h4/>")
        self._amount_SBX = agUI.ToolkitQSpinBox("Amount: ")
        self._amount_SBX.setRange(1, 99)
        self._code_LNE = agUI.ToolkitQLineEdit("name")
        _code_validator = QtGui.QRegExpValidator()
        _code_validator.setRegExp(r"[a-zA-Z]{3}")
        self._code_LNE.setValidator(_code_validator)

    def _layouts(self):
        _V_LYT = QtWidgets.QVBoxLayout()

        _H_LYT = QtWidgets.QHBoxLayout()
        _H_LYT.addStretch()
        _H_LYT.addWidget(self._project_LBL)
        _H_LYT.addWidget(self._number_SBX)
        _H_LYT.addWidget(self._name_LNE)
        _H_LYT.addStretch()

        _H_shots_LYT = QtWidgets.QHBoxLayout()
        _H_shots_LYT.addStretch()
        _H_shots_LYT.addWidget(self._shots_LBL)
        _H_shots_LYT.addWidget(self._amount_SBX)
        _H_shots_LYT.addWidget(self._code_LNE)
        _H_shots_LYT.addStretch()

        _H_create_button_LYT = QtWidgets.QHBoxLayout()
        _H_create_button_LYT.addStretch()
        _H_create_button_LYT.addWidget(self.create_button)
        _H_create_button_LYT.addStretch()

        _V_LYT.addStretch()
        _V_LYT.addWidget(self.instructions)
        _V_LYT.addLayout(self.savepath_layout)
        _V_LYT.addLayout(_H_LYT)
        _V_LYT.addLayout(_H_shots_LYT)
        _V_LYT.addLayout(_H_create_button_LYT)
        _V_LYT.addStretch()
        _V_LYT.setSpacing(20)

        self.layout = _V_LYT

    def _methods(self):
        def create():
            result = {"state": "error", "message": ""}
            _project_name = ""
            _path = ""

            if self._number_SBX.value() < 10:
                _project_name = f"0{self._number_SBX.value()}_{self._name_LNE.text()}"
            else:
                _project_name = f"{self._number_SBX.value()}_{self._name_LNE.text()}"

            _path = os.path.join(self.savepath, _project_name)

            if os.path.exists(_path):
                result["state"] = "error"
                result["message"] = "That project already exists at this location."
                self.console.log(result["message"], result["state"])
                return

            if self._name_LNE.text() == "":
                result["status"] = "error"
                result["message"] = "You didn't provide a valid project name."
                self.console.log(result["message"], result["state"])
                return result

            if self._code_LNE.text() == "" or len(self._code_LNE.text()) != 3:
                result["status"] = "error"
                result["message"] = "You didn't provide a correct code for your sequence shots."
                self.console.log(result["message"], result["state"])
                return result

            _shots_data = shots.create_shots_list(
                self._code_LNE.text(),
                self._amount_SBX.value() + 1)

            project.create(_path, _shots_data)
            result["status"] = "success"
            result["message"] = f"Project created successfully at: {_path}"
            self.console.log(result["message"], result["status"])

        self.create_button.clicked.connect(create)
