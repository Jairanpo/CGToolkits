# Standar library
import sys
import os
import datetime


# Third party
from PySide2 import QtWidgets, QtCore, QtGui

# Project
from components.directoryWidget import DirectoryWidget as DirectoryWidget
import CGAgnostics.GUI as agUI
import controllers.shots as shots
import controllers.campaign as campaign


class Campaign(DirectoryWidget):

    def __init__(self, parent=""):
        super().__init__(parent)
        self.subprojects = []

        self._widgets()
        self._layouts()
        self._methods()

    # Public methods:   -----------------------------------------

    # Private methods:  -----------------------------------------

    def _widgets(self):
        self.instructions = '''
            <h2>Instructions:</h2>
            <ul>
                <li>Set the path where you would like your directory to be created.</li>
                <li>Specify the campaign naming fields without using spaces.</li>
                <li>year:"2020", prefix:"foo", name: "bar", suffix: "baz" = "2020_FooBarBaz".</li>
                <li>Use a descriptive set of three characters that will help you to identify the <br>
                relation between campaign/project name and shots.</li>
                <li>If you don't know the amount of shots each project should have, set the amount <br>
                to a slightly larger quantity (the remainder could be deleted later).</li>
            </ul>
        '''
        self._has_subprojects_CBX = agUI.ToolkitQCheckBox(
            "Subproject campaign?")
        self._subprojects_amount_SBX = agUI.ToolkitQSpinBox(
            "How many?:  ")
        self._subprojects_amount_SBX.setVisible(False)
        self._subprojects_amount_SBX.setMinimum(1)
        self._subprojects_amount_SBX.setMaximum(20)

        self._agency_LNE = agUI.ToolkitQLineEdit()
        self._agency_LNE.setPlaceholderText("Agency name")

        self._project_year_LNE = agUI.ToolkitQLineEdit()
        now = datetime.datetime.now()
        year_validator = QtGui.QRegExpValidator()
        year_validator.setRegExp(r"[0-9]{4}")
        self._project_year_LNE.setValidator(year_validator)
        self._project_year_LNE.setText(str(now.year))

        fields_validator = QtGui.QRegExpValidator()
        fields_validator.setRegExp(r"[a-zA-Z]{20}")

        self._project_prefix_LNE = agUI.ToolkitQLineEdit()
        self._project_prefix_LNE.setPlaceholderText('First name (campaign)')
        self._project_prefix_LNE.setValidator(fields_validator)
        self._name_LNE = agUI.ToolkitQLineEdit()
        self._name_LNE.setValidator(fields_validator)
        self._name_LNE.setPlaceholderText('Second name (sequence)')
        self._project_suffix_LNE = agUI.ToolkitQLineEdit()
        self._project_suffix_LNE.setValidator(fields_validator)
        self._project_suffix_LNE.setPlaceholderText('Third name (optional)')

        self._shotcode_LBL = agUI.ToolkitQLabel('Shotcode(1-3 characters):')
        self._shotcode_LNE = agUI.ToolkitQLineEdit()
        self._shotcode_LNE.setValidator(fields_validator)
        self._shotcode_LNE.setMaximumWidth(40)
        sht_code_validator = QtGui.QRegExpValidator()
        sht_code_validator.setRegExp(r"[a-zA-Z]{3}")
        self._shotcode_LNE.setValidator(sht_code_validator)

        self._shot_amount_SBX = agUI.ToolkitQSpinBox('How many shots?: ')
        self._shot_amount_SBX.setRange(1, 99)

    def _layouts(self):
        _V_LYT = QtWidgets.QVBoxLayout()

        _H_project_type_LYT = QtWidgets.QHBoxLayout()
        _H_project_type_LYT.addStretch()
        _H_project_type_LYT.addWidget(self._has_subprojects_CBX)
        _H_project_type_LYT.addWidget(self._subprojects_amount_SBX)
        _H_project_type_LYT.addStretch()

        _H_agency_name_LYT = QtWidgets.QHBoxLayout()
        _H_agency_name_LYT.addStretch()
        _H_agency_name_LYT.addWidget(self._agency_LNE)
        _H_agency_name_LYT.addStretch()

        _H_project_name_LYT = QtWidgets.QHBoxLayout()
        _H_project_name_LYT.addWidget(self._project_year_LNE)
        _H_project_name_LYT.addWidget(self._project_prefix_LNE)
        _H_project_name_LYT.addWidget(self._name_LNE)
        _H_project_name_LYT.addWidget(self._project_suffix_LNE)

        _H_shot_LYT = QtWidgets.QHBoxLayout()
        _H_shot_LYT.addStretch()
        _H_shot_LYT.addWidget(self._shotcode_LBL)
        _H_shot_LYT.addWidget(self._shotcode_LNE)
        _H_shot_LYT.addWidget(self._shot_amount_SBX)

        _V_project_LYT = QtWidgets.QVBoxLayout()
        _V_project_LYT.addLayout(self.savepath_layout)
        _V_project_LYT.addLayout(_H_project_type_LYT)
        _V_project_LYT.addLayout(_H_agency_name_LYT)
        _V_project_LYT.addLayout(_H_project_name_LYT)
        _V_project_LYT.addLayout(_H_shot_LYT)

        _H_project_LYT = QtWidgets.QHBoxLayout()
        _H_project_LYT.addLayout(_V_project_LYT)

        self._V_subproject_name_LYT = QtWidgets.QVBoxLayout()
        self._subproject_name_WGT = QtWidgets.QWidget()
        self._V_subproject_name_LYT.addWidget(self._subproject_name_WGT)
        self._G_subproject_names_LYT = QtWidgets.QGridLayout()
        self._subproject_name_WGT.setLayout(self._G_subproject_names_LYT)
        self._G_subproject_names_LYT.setColumnStretch(0, 1)

        _H_create_project_button_LYT = QtWidgets.QHBoxLayout()
        _H_create_project_button_LYT.addStretch()
        _H_create_project_button_LYT.addWidget(self.create_button)
        _H_create_project_button_LYT.addStretch()

        _V_LYT.addStretch()
        _V_LYT.addWidget(self.instructions)
        _V_LYT.addLayout(_H_project_LYT)
        _V_LYT.addLayout(self._V_subproject_name_LYT)
        _V_LYT.addLayout(_H_create_project_button_LYT)
        _V_LYT.addStretch()
        _V_LYT.setSpacing(15)

        self.layout = _V_LYT

    def _methods(self):
        def subproject_options(state):
            self._subprojects_amount_SBX.setVisible(state)
            self._subproject_name_WGT.setVisible(state)
            self._subproject_name_WGT.setEnabled(state)
            self._shotcode_LBL.setVisible(not state)
            self._shotcode_LNE.setVisible(not state)
            self._shot_amount_SBX.setVisible(not state)
            self._append_subproject(1)

            self._name_LNE.setPlaceholderText(
                'Second name (Campaign)')

        def add_subproject_name(value):
            state = []

            def save_state():
                for name, code, amount in self.subprojects:
                    state.append(
                        [name.text(), code.text(), amount.value()])

            def clearLayout(layout):
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget() is not None:
                        child.widget().deleteLater()
                    elif child.layout() is not None:
                        clearLayout(child.layout())
                self.subprojects = []

            save_state()
            clearLayout(self._G_subproject_names_LYT)

            for each in range(0, value):
                state.append(None)
                self._append_subproject(each, state[each])

        self._has_subprojects_CBX.clicked.connect(subproject_options)
        self._subprojects_amount_SBX.valueChanged.connect(add_subproject_name)
        self.create_button.clicked.connect(self.create_sequence_strategy)

    # ==============================================================================

    def _append_subproject(self, row, state=None):
        _subproject_name_LNE = agUI.ToolkitQLineEdit("Sequence name")

        _shotcode_LNE = agUI.ToolkitQLineEdit("Shotcode")
        _shotcode_LNE.setMaximumWidth(65)
        _shotcode_validator = QtGui.QRegExpValidator()
        _shotcode_validator.setRegExp(r"[a-zA-Z]{3}")
        _shotcode_LNE.setValidator(_shotcode_validator)

        _amount_SBX = agUI.ToolkitQSpinBox("Amount: ")
        _amount_SBX.setRange(1, 99)

        if state is None:
            pass
        else:
            _subproject_name_LNE.setText(state[0])
            _shotcode_LNE.setText(state[1])
            _amount_SBX.setValue(state[2])

        self.subprojects.append(
            [_subproject_name_LNE, _shotcode_LNE, _amount_SBX])

        self._G_subproject_names_LYT.addWidget(_subproject_name_LNE, row, 0)
        self._G_subproject_names_LYT.addWidget(_shotcode_LNE, row, 1)
        self._G_subproject_names_LYT.addWidget(_amount_SBX, row, 2)

    def create_sequence_strategy(self):
        if self._has_subprojects_CBX.checkState():
            self.create_composed_campaign()
        else:
            self.create_simple_campaign()

    def create_simple_campaign(self):
        year = self._project_year_LNE.text() + '_'
        prefix = self._project_prefix_LNE.text().strip().replace(' ', '_')
        _name = self._name_LNE.text().strip().replace(' ', '_')
        suffix = self._project_suffix_LNE.text().strip().replace(' ', '_')

        _data = {}
        _data["shotcode"] = self._shotcode_LNE.text().strip().replace(' ', '_')
        _data["amount"] = self._shot_amount_SBX.value()

        _campaign = {}
        _campaign["name"] = year + prefix.capitalize() + _name.capitalize() + \
            suffix.capitalize()
        _campaign["agency"] = self._agency_LNE.text().upper(
        ) if self._agency_LNE.text() != "" else "UNKNOWN"

        result = {"status": "", "message": ""}

        if os.path.exists(os.path.join(self.savepath, _campaign["name"])) and prefix != '' and _campaign["name"] != '':
            self.console.log('That campaign folder already exists', "warning")
        elif self.savepath != '' and prefix != '' and _campaign["name"] != '' and _data["shotcode"] != '':
            print("Entering simple creation")
    
            shots_dict = shots.create_shots_list(
                _data["shotcode"], _data["amount"] + 1)

            result = campaign.simple(self.savepath, _campaign,
                                     shots_dict["list_of_shots"], _data)

            self.console.log(result["message"], result["status"])
        else:
            self.console.log('''
                            <p>Unable to create sequence folders:</p>
                            <p>check the following issues:</p>
                                <ul>
                                <li>Save location path.</li>
                                <li>Sequence naming(year, prefix, name, suffix).</li>
                                <li>Shot code.</li>
                                <li>Amount of shots.</li>
                                </ul>
                            ''', "error")

    def create_composed_campaign(self):
        year = self._project_year_LNE.text().strip() + "_"
        prefix = self._project_prefix_LNE.text().strip().replace(' ', '_')
        _name = self._name_LNE.text().strip().replace(' ', '_')
        suffix = self._project_suffix_LNE.text().strip().replace(' ', '_')

        _campaign = {}
        _campaign["name"] = year + prefix.capitalize() + _name.capitalize() + \
            suffix.capitalize()
        _campaign["agency"] = self._agency_LNE.text().upper(
        ) if self._agency_LNE.text() != "" else "UNKNOWN"
        
        _matrix = []

        def add_number(matrix):
            for i, element in enumerate(matrix, 1):
                if i < 10:
                    element[0] = f"0{i}_{element[0]}"
                else:
                    element[0] = f"{i}_{element[0]}"

        for project, code, amount in self.subprojects:
            cur_project = project.text()
            cur_code = code.text()
            cur_amount = amount.value()

            if cur_project == '':
                self.console.log(
                    "The field \"Sequence name\" of one of your sequences wasn't filled.", "warning")
                return
            elif cur_code == '':
                self.console.log(
                    "The field \"Shotcode\" of one of your sequences wasn't filled.", "warning")
                return
            _matrix.append([cur_project, cur_code, cur_amount])

        add_number(_matrix)

        result = campaign.composed(self.savepath, _campaign, _matrix)

        self.console.log(result["message"], result["status"])
