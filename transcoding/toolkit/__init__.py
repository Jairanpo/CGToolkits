
import sys
import subprocess
import os

import modules
import CGAgnostics.GUI as agUI
from Qt import QtCore, QtWidgets, QtGui
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
            os.path.join(self._icons_path, "icon.ico"))
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(self._window_icon)

        self._widgets()
        self._layouts()

    def _widgets(self):
        self.console = agUI.ToolkitQConsole()
        self.footer = agUI.ToolkitQFooter(self)

        self.source = Source(self, is_file=True)
        self.source.console = self.console

        self._splitter_SPL = agUI.ToolkitQSplitter()
        self._splitter_SPL.setOrientation(QtCore.Qt.Vertical)
        self._splitter_SPL.addWidget(self.source.widget)
        self._splitter_SPL.addWidget(self.console.widget)
        self._splitter_SPL.addWidget(self.footer.widget)

    def _layouts(self):
        self.V_root_window_LYT = QtWidgets.QVBoxLayout(self)
        self.V_root_window_LYT.addWidget(self._splitter_SPL)


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = Transcoding()
    window.show()
    app.exec_()
