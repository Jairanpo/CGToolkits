# Standar library
import sys
import os

# Third party
from PySide2 import QtWidgets, QtCore, QtGui

# Project
from components.directoryWidget import DirectoryWidget as DirectoryWidget
import CGAgnostics.GUI as agUI
import controllers.paths.execution as execution
import controllers.assets as assets


class Asset(DirectoryWidget):
    def __init__(self, parent=""):
        super().__init__(parent)

        self._widgets()
        self._layouts()
        self._methods()

    # Private methods:  -----------------------------------------

    def _widgets(self):
        self.instructions = '''
                <h2>Instructions:</h2>
                <ul>
                    <li>Set the path where you would like your directory to be created.</li>
                    <li>Specify the asset name using spaces, for example: "dr slump".</li>
                    <li>Spaces between words will be use to concatenate and capitalize <br>
                    a word, for example: "dr slump" -> "DrSlump".</li>
                    <li>Spaces at the beginning and at the end of a word will be eliminated,<br> 
                    for example: " dr slump  " -> "DrSlump".</li>
                </ul>
            '''

        self.asset_LNE = agUI.ToolkitQLineEdit()
        self.asset_LNE.setPlaceholderText("Name")

    def _layouts(self):
        _V_LYT = QtWidgets.QVBoxLayout()

        _V_creation_LYT = QtWidgets.QVBoxLayout()
        _H_creation_LNE_LYT = QtWidgets.QHBoxLayout()
        _H_creation_LNE_LYT.addStretch()
        _H_creation_LNE_LYT.addWidget(self.asset_LNE)
        _H_creation_LNE_LYT.addStretch()

        _H_creation_BTN_LYT = QtWidgets.QHBoxLayout()
        _H_creation_BTN_LYT.addStretch()
        _H_creation_BTN_LYT.addWidget(self.create_button)
        _H_creation_BTN_LYT.addStretch()
        
        _V_creation_LYT.addLayout(_H_creation_LNE_LYT)
        _V_creation_LYT.addLayout(_H_creation_BTN_LYT)

        _V_LYT.addStretch()
        _V_LYT.addWidget(self.instructions)
        _V_LYT.addLayout(self.savepath_layout)
        _V_LYT.addLayout(_V_creation_LYT)
        _V_LYT.addStretch()
        _V_LYT.setSpacing(20)

        self.layout = _V_LYT

    def _methods(self):
        def create_asset():
            path = self.savepath_LNE.text().strip()
            name = assets.create_asset_name(self.asset_LNE.text())

            if os.path.exists(path) and len(name) > 1:
                asset_path = os.path.join(path, name)
                if not os.path.exists(asset_path):
                    assets.create_asset_directory_structure(path, name)
                    self._console.log("Your asset was created!", "success")
                else:
                    self._console.log(
                        'That asset already exist at this location:\n' + asset_path, "error")
            else:
                self._console.log('''
                                Unable to create asset...
                                check the following issues:
                                    - Check if the assets path exist.
                                    - Your asset name has to be larger than one character.
                                ''', "error")

        self.create_button.clicked.connect(create_asset)
