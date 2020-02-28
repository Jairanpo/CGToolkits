# !/usr/bin/env_python
import sys
import os

from PySide2 import QtWidgets, QtCore, QtGui

import CGAgnostics.GUI as agUI
from components.tabs import Tabs
from components.campaign import Campaign
from components.project import Project
from components.asset import Asset
from components.shot import Shot

__author__ = "Jair Anguiano"
__version__ = "4.2.0"
_NAME = "CGDirectories"


class DirectoriesGUI(agUI.ToolkitQDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        def select_correct_execution_path():
            if getattr(sys, 'frozen', False):
                datadir = os.path.dirname(sys.executable)
            else:
                datadir = os.path.dirname(__file__)
            return datadir

        self._main_path = select_correct_execution_path()
        self._icons_path = os.path.join(self._main_path, 'icons')
        self._window_icon = QtGui.QIcon(
            os.path.join(self._icons_path, "filesystem.ico"))
        self._create_icon = QtGui.QIcon(
            os.path.join(self._icons_path, "create.ico"))
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(self._window_icon)
        self.setWindowTitle(f'{_NAME} | v{__version__}')
        self.setMinimumWidth(300)
        self.setMinimumHeight(300)
        self.resize(700, 800)

        self.list_of_sequence_widgets = []

        self._widgets()
        self._layouts()

    def _widgets(self):
        self.tabs = Tabs()
        self.console = agUI.ToolkitQConsole()
        self.footer = agUI.ToolkitQFooter(self)

        self.campaign = Campaign(self)
        self.campaign.console = self.console

        self.asset = Asset(self)
        self.asset.console = self.console

        self.shot = Shot(self)
        self.shot.console = self.console

        self.project = Project(self)
        self.project.console = self.console

        self._splitter_SPL = agUI.ToolkitQSplitter()
        self._splitter_SPL.setOrientation(QtCore.Qt.Vertical)
        self._splitter_SPL.addWidget(self.tabs.widget)
        self._splitter_SPL.addWidget(self.console.widget)
        self._splitter_SPL.addWidget(self.footer.widget)

    def _layouts(self):
        self.V_root_window_LYT = QtWidgets.QVBoxLayout(self)

        self.tabs.campaign.addLayout(self.campaign.layout)
        self.tabs.project.addLayout(self.project.layout)
        self.tabs.asset.addLayout(self.asset.layout)
        self.tabs.shot.addLayout(self.shot.layout)

        self.V_root_window_LYT.addWidget(self._splitter_SPL)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = DirectoriesGUI()
    ex.show()
    sys.exit(app.exec_())
