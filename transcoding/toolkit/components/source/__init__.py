import os
import sys
import re

from Qt import QtCore, QtWidgets, QtGui
import CGAgnostics.GUI as agUI


class Source(agUI.ToolkitQWidget):
    def __init__(self, parent, name="NO_NAME", is_file=True):
        self._name = name
        self.parent = parent
        self._WGT = QtWidgets.QWidget()
        self._V_root_LYT = None
        self._icons_path = os.path.join(
            self.root_path(), "CGAgnostics", "icons")

        self._widgets()
        self._layouts()
        self._methods()

    @property
    def layout(self):
        return self._V_root_LYT

    @property
    def widget(self):
        self._WGT.setLayout(self._V_root_LYT)
        return self._WGT

    def _widgets(self):
        self._enable_CBX = agUI.ToolkitQCheckBox(self._name)
        self._enable_CBX.setCheckState(QtCore.Qt.Checked)

        self._content_WGT = QtWidgets.QWidget()

        self._source_LBL = agUI.ToolkitQLabel(f"<h3>Source:</h3>")
        self._source_LNE = agUI.ToolkitQLineEdit()
        self._source_BTN = agUI.ToolkitQBrowseButton(
            self.parent,
            lineedit=self._source_LNE,
            is_file=True,
            size=[20, 20],
            filter="Videos(*.mp4 * .avi * .mov * .webmd)")

        self._filename_LBL = agUI.ToolkitQLabel(f"Filename:")
        self._filename_LNE = agUI.ToolkitQLineEdit("Filename")

        self._videos_CBX = agUI.ToolkitQCheckBox("Video")
        self._videos_CBX.setCheckState(QtCore.Qt.Checked)
        self._video_foldername_LNE = agUI.ToolkitQLineEdit("Carpeta 01")
        self._QT_CBX = agUI.ToolkitQCheckBox("QT")
        self._QT_CBX.setCheckState(QtCore.Qt.Checked)
        self._HD_CBX = agUI.ToolkitQCheckBox("HD")
        self._HD_CBX.setCheckState(QtCore.Qt.Checked)
        self._UNCOMPRESS_CBX = agUI.ToolkitQCheckBox("UNCOMPRESS")
        self._UNCOMPRESS_CBX.setCheckState(QtCore.Qt.Checked)

        self._image_sequence_CBX = agUI.ToolkitQCheckBox("Image sequence")
        self._image_sequence_CBX.setCheckState(QtCore.Qt.Checked)
        self._image_sequence_foldername_LNE = agUI.ToolkitQLineEdit(
            "Carpeta 03")

    def _layouts(self):
        _V_LYT = QtWidgets.QVBoxLayout()

        _V_enable_LYT = QtWidgets.QVBoxLayout()
        _V_enable_LYT.addStretch()
        _V_enable_LYT.addWidget(self._enable_CBX)
        _V_enable_LYT.addStretch()

        _H_LYT = QtWidgets.QHBoxLayout()
        _H_LYT.addLayout(_V_enable_LYT)

        _Grid_LYT = QtWidgets.QGridLayout()
        _Grid_LYT.addWidget(self._source_LBL, 0, 0)
        _Grid_LYT.addWidget(self._source_LNE, 0, 1)
        _Grid_LYT.addWidget(self._source_BTN, 0, 2)
        _Grid_LYT.addWidget(self._filename_LBL, 1, 0)
        _Grid_LYT.addWidget(self._filename_LNE, 1, 1)
        _Grid_LYT.addWidget(self._videos_CBX, 2, 0)
        _Grid_LYT.addWidget(self._video_foldername_LNE, 2, 1)
        _Grid_LYT.addWidget(self._QT_CBX, 2, 2)
        _Grid_LYT.addWidget(self._HD_CBX, 2, 3)
        _Grid_LYT.addWidget(self._UNCOMPRESS_CBX, 2, 4)
        _Grid_LYT.addWidget(self._image_sequence_CBX, 3, 0)
        _Grid_LYT.addWidget(self._image_sequence_foldername_LNE, 3, 1)

        self._content_WGT.setLayout(_Grid_LYT)
        _H_LYT.addWidget(self._content_WGT)
        _V_LYT.addLayout(_H_LYT)

        self._V_root_LYT = _V_LYT

    def _methods(self):

        def _disable_content():
            if self._enable_CBX.isChecked():
                self._content_WGT.setEnabled(True)
                self._videos_CBX.setCheckState(QtCore.Qt.Checked)
                self._QT_CBX.setCheckState(QtCore.Qt.Checked)
                self._HD_CBX.setCheckState(QtCore.Qt.Checked)
                self._UNCOMPRESS_CBX.setCheckState(QtCore.Qt.Checked)
                self._image_sequence_CBX.setCheckState(QtCore.Qt.Checked)

            else:
                self._videos_CBX.setCheckState(QtCore.Qt.Unchecked)
                self._QT_CBX.setCheckState(QtCore.Qt.Unchecked)
                self._HD_CBX.setCheckState(QtCore.Qt.Unchecked)
                self._UNCOMPRESS_CBX.setCheckState(QtCore.Qt.Unchecked)
                self._image_sequence_CBX.setCheckState(QtCore.Qt.Unchecked)
                self._content_WGT.setEnabled(False)

        def _disable_video():
            if self._videos_CBX.isChecked():
                self._video_foldername_LNE.setEnabled(True)
                self._QT_CBX.setEnabled(True)
                self._QT_CBX.setCheckState(QtCore.Qt.Checked)
                self._HD_CBX.setEnabled(True)
                self._HD_CBX.setCheckState(QtCore.Qt.Checked)
                self._UNCOMPRESS_CBX.setEnabled(True)
                self._UNCOMPRESS_CBX.setCheckState(QtCore.Qt.Checked)
            else:
                self._video_foldername_LNE.setEnabled(False)
                self._video_foldername_LNE.setEnabled(False)
                self._QT_CBX.setEnabled(False)
                self._QT_CBX.setCheckState(QtCore.Qt.Unchecked)
                self._HD_CBX.setEnabled(False)
                self._HD_CBX.setCheckState(QtCore.Qt.Unchecked)
                self._UNCOMPRESS_CBX.setEnabled(False)
                self._UNCOMPRESS_CBX.setCheckState(QtCore.Qt.Unchecked)

        def _disable_image():
            if self._image_sequence_CBX.isChecked():
                self._image_sequence_foldername_LNE.setEnabled(True)
            else:

                self._image_sequence_foldername_LNE.setEnabled(False)

        self._enable_CBX.clicked.connect(_disable_content)
        self._videos_CBX.clicked.connect(_disable_video)
        self._image_sequence_CBX.clicked.connect(_disable_image)
