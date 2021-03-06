# Standard library imports
import os

# Third party imports
from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import pymel.core as pm

# Local application imports
import CGAgnostics.GUI as agUI
import populate
import frameRange
import cache.alembic as abc
import previs.editorial as editorial
import playblast


__version__ = 'v1.0.0'
_NAME = "Alembic Manager"


def maya_main_window():
    """
    return the Maya main window widget as Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class GUI(agUI.ToolkitQDialog):
    GUI_instance = None
    @classmethod
    def show_dialog(cls):
        if not cls.GUI_instance:
            cls.GUI_instance = GUI()
        if cls.GUI_instance.isHidden():
            cls.GUI_instance.show()
        else:
            cls.GUI_instance.raise_()
            cls.GUI_instance.activateWindow()

    def __init__(self, parent=maya_main_window(), standalone=True):
        super(GUI, self).__init__(parent)
        self._SHOTS_DATA = []
        self.setWindowFlags(
            self.windowFlags() ^
            QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(
            '{0} | {1}'.format(_NAME, __version__))
        self._main_path = os.path.dirname(__file__)
        self._icons_path = os.path.join(self._main_path, 'icons')
        self._win_icon = QtGui.QIcon(
            os.path.join(self._icons_path, "alembic.ico"))
        self.setWindowIcon(self._win_icon)
        self.setMinimumWidth(500)
        self.setMaximumWidth(1200)
        self.setMinimumHeight(200)
        self.setMaximumHeight(1200)
        self.resize(800, 800)
        self.root_window_LYT = QtWidgets.QVBoxLayout()
        self.setLayout(self.root_window_LYT)

    # ---------------------------------------------------------------------------
    # Initialization strategy:

        if standalone:
            self._set_title()
            self._set_group()
            self._set_save_path()
            self._set_use_sequence()
            self._set_version()
            self._set_range()
            self._set_export_items()
            self._set_shot_table()
            self._set_export_button()
            self._set_console()
            self._set_footer()
        else:
            self._set_title()
            self._set_group()
            self._set_save_path()
            self._set_use_sequence()
            self._set_version()
            self._set_range()
            self._set_export_items()
            self._set_shot_table()
            self._set_export_button()
    # ---------------------------------------------------------------------------
    # Public methods:

    def showEvent(self, event):
        super(GUI, self).showEvent(event)
        self._SHOTS_DATA = populate.with_shots(self.shots_TBL)

    def get_group(self):
        return self.root_group_V_LYT

    def get_widget(self, console):
        self._SHOTS_DATA = populate.with_shots(self.shots_TBL)
        self.console = console
        alembic_toolkit_WGT = QtWidgets.QWidget()
        alembic_toolkit_WGT.setLayout(self.root_group_V_LYT)
        return alembic_toolkit_WGT

    # ---------------------------------------------------------------------------
    # Private methods:

    def _set_title(self):
        self.root_title_LYT = None

        def _widgets():
            self._title_LBL = QtWidgets.QLabel(
                "<h3>Alembic Manager:</h3>")

        def _layouts():
            _H_LYT = QtWidgets.QHBoxLayout()
            _H_LYT.addWidget(self._title_LBL)
            self.root_title_LYT = _H_LYT

        _widgets()
        _layouts()

        self.root_window_LYT.addLayout(self.root_title_LYT)

    def _set_group(self):
        self.root_group_V_LYT = None

        def _widgets():
            self._settings_GBX = agUI.ToolkitQGroupBox("Export:")

        def _layouts():
            _V_LYT = QtWidgets.QVBoxLayout()
            self.root_group_V_LYT = _V_LYT
            self.root_group_V_LYT.setContentsMargins(15, 0, 15, 0)
            self._settings_GBX.setLayout(self.root_group_V_LYT)

        _widgets()
        _layouts()
        self.root_window_LYT.addWidget(self._settings_GBX)

    def _set_save_path(self):
        self.root_save_path = None

        def _widgets():
            self.path_LNE = agUI.ToolkitQLineEdit()
            self.path_BTN = agUI.ToolkitQPushButton("Browse")

        def _layouts():
            _H_LYT = QtWidgets.QHBoxLayout()
            _browse_H_LYT = QtWidgets.QHBoxLayout()
            _browse_H_LYT.addWidget(self.path_LNE)
            _browse_H_LYT.addWidget(self.path_BTN)

            _form_LYT = QtWidgets.QFormLayout()
            _form_LYT.insertRow(0, "Save to: ", _browse_H_LYT)
            _H_LYT.addLayout(_form_LYT)
            self.root_save_path = _H_LYT
            self.root_group_V_LYT.addLayout(self.root_save_path)

        def _methods():
            def _fill_path():
                _file_FLD = QtWidgets.QFileDialog()
                _path = _file_FLD.getExistingDirectory(self, "Select folder")
                if _path:
                    self.path_LNE.setText(_path)

            self.path_BTN.clicked.connect(_fill_path)

        _widgets()
        _layouts()
        _methods()

    def _set_version(self):
        self.root_version_LYT = None

        def _widgets():
            self.version_CBX = agUI.ToolkitQComboBox()
            for i in range(0, 20):
                if i < 9:
                    self.version_CBX.insertItem(i, "v00{0}".format(str(i + 1)))
                else:
                    self.version_CBX.insertItem(i, "v0{0}".format(str(i + 1)))

        def _layouts():
            _H_LYT = QtWidgets.QHBoxLayout()
            _version_form_LYT = QtWidgets.QFormLayout()
            _version_form_LYT.addRow("Select version suffix", self.version_CBX)
            _H_LYT.addLayout(_version_form_LYT)
            _H_LYT.addStretch()
            self.root_version_LYT = _H_LYT
            self.root_group_V_LYT.addLayout(self.root_version_LYT)

        _widgets()
        _layouts()

    def _set_use_sequence(self):
        self.root_use_sequence_LYT = None

        def _widgets():
            self._use_sequence_CBX = QtWidgets.QCheckBox()

        def _layouts():
            _H_LYT = QtWidgets.QHBoxLayout()
            _H_LYT.setContentsMargins(0, 15, 0, 5)

            _F_use_sequence_LYT = QtWidgets.QFormLayout()
            _F_use_sequence_LYT.insertRow(
                0, "<h4>Use sequencer?: </h2>", self._use_sequence_CBX)
            _H_LYT.addLayout(_F_use_sequence_LYT)
            _H_LYT.addStretch()
            self.root_use_sequence_LYT = _H_LYT

        def _methods():
            def _manage_use_sequence_status(state):
                self.shots_TBL.setVisible(state)
                self.shots_TBL.setEnabled(state)
                self.refresh_shots_BTN.setVisible(state)
                self.refresh_shots_BTN.setEnabled(state)
                self.range_visibility_WGT.setEnabled(not state)
                self.range_visibility_WGT.setVisible(not state)

            self._use_sequence_CBX.stateChanged.connect(
                _manage_use_sequence_status)

        _widgets()
        _layouts()
        _methods()

        self.root_group_V_LYT.addLayout(self.root_use_sequence_LYT)

    def _set_range(self):
        self.root_range_LYT = None

        def _widgets():
            self.range_visibility_WGT = QtWidgets.QWidget()
            self.start_LNE = agUI.ToolkitQLineEdit()
            self.end_LNE = agUI.ToolkitQLineEdit()
            self.start_LNE.setPlaceholderText('Start')
            self.start_LNE.setValidator(QtGui.QIntValidator())
            self.end_LNE.setPlaceholderText('End')
            self.end_LNE.setValidator(QtGui.QIntValidator())

        def _layouts():
            _H_LYT = QtWidgets.QHBoxLayout()

            _visibility_H_LYT = QtWidgets.QHBoxLayout()
            self.range_visibility_WGT.setLayout(_visibility_H_LYT)

            _form_LYT = QtWidgets.QFormLayout()
            _range_H_LYT = QtWidgets.QHBoxLayout()
            _range_H_LYT.addWidget(self.start_LNE)
            _range_H_LYT.addWidget(self.end_LNE)
            _form_LYT.addRow('Range:', _range_H_LYT)

            _visibility_H_LYT.addLayout(_form_LYT)

            _H_LYT.addWidget(self.range_visibility_WGT)
            _H_LYT.addStretch()

            self.root_range_LYT = _H_LYT

        _widgets()
        _layouts()
        self.root_group_V_LYT.addLayout(self.root_range_LYT)

    def _set_export_items(self):
        self.root_export_items_LYT = None

        def _widgets():
            _button_size = 120, 25
            _populate_icon = QtGui.QIcon(
                os.path.join(self._icons_path, "add.ico"))
            self.populate_BTN = agUI.ToolkitQPushButton("")
            self.populate_BTN.setIcon(_populate_icon)
            self.populate_BTN.setIconSize(
                QtCore.QSize(_button_size[0], _button_size[1]))

            self.export_items_TBL = agUI.ToolkitQTableWidget()
            self.export_items_TBL.setMinimumHeight(30)
            self.export_items_TBL.setColumnCount(3)
            self.export_items_TBL.setHorizontalHeaderLabels(
                ["Node", "Filename", "Root flag"])

        def _layouts():
            _V_LYT = QtWidgets.QVBoxLayout()

            _buttons_H_LYT = QtWidgets.QHBoxLayout()
            _buttons_H_LYT.addStretch()
            _buttons_H_LYT.addWidget(self.populate_BTN)

            _table_H_LYT = QtWidgets.QHBoxLayout()
            _table_H_LYT.addWidget(self.export_items_TBL)

            _V_LYT.addLayout(_buttons_H_LYT)
            _V_LYT.addLayout(_table_H_LYT)
            _V_LYT.setSpacing(5)

            self.root_export_items_LYT = _V_LYT

        def _methods():
            def _populate_signal():
                populate.with_items(self.export_items_TBL)
                pm.select(clear=True)

            def _update_table(row, column):
                populate.update_item(self.export_items_TBL, row, column)

            self.populate_BTN.clicked.connect(_populate_signal)
            self.export_items_TBL.cellChanged.connect(_update_table)

        _widgets()
        _layouts()
        _methods()
        self.root_group_V_LYT.addLayout(self.root_export_items_LYT)

    def _set_shot_table(self):
        self.root_export_sequencer_LYT = None

        def _widgets():
            self.shots_TBL = agUI.ToolkitQTableWidget()
            self.shots_TBL.setSortingEnabled(True)
            self.shots_TBL.setColumnCount(6)
            self.shots_TBL.setHorizontalHeaderLabels(
                ["Shot", "Range", "Camera", "Export", "Camera?", "Clip?"])
            self.shots_TBL.setVisible(self._use_sequence_CBX.isChecked())

            self.refresh_shots_BTN = agUI.ToolkitQPushButton("Refresh")
            self.refresh_shots_BTN.setVisible(
                self._use_sequence_CBX.isChecked())

        def _layouts():
            _V_LYT = QtWidgets.QVBoxLayout()

            _V_shots_widgets_LYT = QtWidgets.QVBoxLayout()
            _H_sequencer_table_LYT = QtWidgets.QHBoxLayout()
            _H_sequencer_table_LYT.addWidget(self.shots_TBL)
            _H_refresh_shots_table_LYT = QtWidgets.QHBoxLayout()
            _H_refresh_shots_table_LYT.addStretch()
            _H_refresh_shots_table_LYT.addWidget(self.refresh_shots_BTN)

            _V_LYT.addLayout(_H_sequencer_table_LYT)
            _V_LYT.addLayout(_H_refresh_shots_table_LYT)

            self.root_export_sequencer_LYT = _V_LYT
            self.root_group_V_LYT.addLayout(self.root_export_sequencer_LYT)

        def _methods():
            def refresh_table():
                populate.with_shots(self.shots_TBL)

            self.refresh_shots_BTN.clicked.connect(refresh_table)

        _widgets()
        _layouts()
        _methods()

    def _set_export_button(self):
        self.root_export_button_LYT = None

        def _widgets():
            _button_size = 120, 30
            _export_icon = QtGui.QIcon(
                os.path.join(self._icons_path, "export.ico"))
            self.export_BTN = agUI.ToolkitQPushButton("")
            self.export_BTN.setIcon(_export_icon)
            self.export_BTN.setIconSize(
                QtCore.QSize(_button_size[0], _button_size[1]))

        def _layouts():
            _H_LYT = QtWidgets.QHBoxLayout()
            _H_LYT.addStretch()
            _H_LYT.addWidget(self.export_BTN)
            _H_LYT.addStretch()
            self.root_export_button_LYT = _H_LYT

        def _methods():
            def export_range():
                _start = 0 if self.start_LNE.text() == "" else int(self.start_LNE.text())
                _end = 0 if self.end_LNE.text() == "" else int(self.end_LNE.text())

                _range = frameRange.validate(_start, _end)
                if _range["status"]:
                    abc.export_selected(
                        self.export_items_TBL,
                        {
                            "start": _start,
                            "end": _end,
                            "path": self.path_LNE.text(),
                            "subfolder": "Alembics",
                            "shot": "",
                            "version": self.version_CBX.currentText()
                        })

                    self.console.log(_range["message"], "success")
                else:
                    self.console.log(_range["message"], "error")

            def export_shots():
                def get_shots_to_export():
                    result = []
                    for shot in self._SHOTS_DATA:
                        if shot["widget"].isChecked():
                            result.append(shot)
                    return result

                shots = get_shots_to_export()

                if len(shots) > 0:
                    for shot in shots:
                        abc.export_selected(
                            self.export_items_TBL,
                            {
                                "start": shot["range"]["start"],
                                "end": shot["range"]["end"],
                                "path": self.path_LNE.text(),
                                "subfolder": "Alembics",
                                "shot": shot["shot"].split("_")[1],
                                "version": self.version_CBX.currentText()
                            })

                        # Export camera?: -------------------------------------------------------
                        def do_export_camera():
                            if shot["export_camera_widget"].isChecked():
                                return True
                            return False

                        camera_exported = False

                        if do_export_camera() and camera_exported != True:
                            editorial.export(
                                path=self.path_LNE.text(),
                                shotcode=shot["shot"].split("_")[1],
                                version=self.version_CBX.currentText())

                            self.console.log("Editorial exported", "success")
                            abc.export(
                                {
                                    "start":  shot["range"]["start"],
                                    "end": shot["range"]["end"],
                                    "path": self.path_LNE.text(),
                                    "filename": "Camera",
                                    "subfolder": "Cameras",
                                    "shot": shot["shot"].split("_")[1],
                                    "root_flag": shot["camera"].longName(),
                                    "version": self.version_CBX.currentText()
                                })
                            camera_exported = True
                            self.console.log("Camera exported", "success")

                        # Export clip?: -------------------------------------------------------
                        def do_export_clip():
                            if shot["export_clip_widget"].isChecked():
                                return True
                            return False

                        clip_exported = False

                        if do_export_camera() and clip_exported != True:
                            playblast.do(self.path_LNE.text(), {
                                "start": shot["range"]["start"],
                                "end": shot["range"]["end"],
                                "camera": shot["camera"],
                                "code": shot["shot"].split("_")[1],
                                "version": self.version_CBX.currentText()
                            })

                    self.console.log("Exporting process finished", "success")

                else:
                    self.console.log(
                        "You didn't checked any shot to be exported.", "warning")

            def export_strategy():
                if self._use_sequence_CBX.isChecked():
                    if len(self._SHOTS_DATA) > 0:
                        export_shots()
                    else:
                        self.console.log(
                            "This scene doesn't contain shots in the sequencer.", "warning")
                else:
                    export_range()

            def export():
                path_exists = os.path.exists(self.path_LNE.text())
                if self.export_items_TBL.rowCount() > 0 and path_exists:
                    export_strategy()
                else:
                    self.console.log(
                        "No path was stablished or there is no objects to export in the table.", "error")

            self.export_BTN.clicked.connect(export)

        _widgets()
        _layouts()
        _methods()
        self.root_group_V_LYT.addLayout(self.root_export_button_LYT)

    def _set_console(self):
        self.root_console_LYT = None

        def _widgets():
            self.console = agUI.ToolkitQConsole()

        def _layouts():
            _H_LYT = QtWidgets.QHBoxLayout()
            _H_LYT.addWidget(self.console.widget)

            self.root_console_LYT = _H_LYT

        _widgets()
        _layouts()
        self.root_window_LYT.addLayout(self.root_console_LYT)

    def _set_footer(self):
        self.root_footer_LYT = None

        _footer = agUI.ToolkitQFooter(self)
        self.root_footer_LYT = _footer.getLayout()

        self.root_window_LYT.addLayout(self.root_footer_LYT)
