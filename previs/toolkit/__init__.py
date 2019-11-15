# Standard library imports
import os
import re

# Third party imports
from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import pymel.core as pm
import maya.mel as mel

# Local application imports
import agnostics.GUI as agUI
import previs.createShot.simpleCameraRig as simpleCameraRig
import previs.createShot.sequencerShot as sequencerShot
import previs.editShots as editShots
import previs.camOps as camOps
import previs.moveShots as moveShots
import previs.playblast as playblast
import previs.panels as panels

reload(agUI)
reload(camOps.cameraOperations)
reload(camOps.transformationOperations)
reload(editShots)
reload(moveShots)
reload(playblast)
reload(moveShots)

__version__ = 'v3.0.0'
_NAME = "Previs Toolkit"


def maya_main_window():
    """
    return the Maya main window widget as Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class GUI(agUI.ToolkitQDialog):
    GUI_instance = None
    _SHOT_DATA = {"project": None, "shot": None, "start": None, "end": None}

    @classmethod
    def show_dialog(cls):
        if not cls.GUI_instance:
            cls.GUI_instance = GUI()

        if cls.GUI_instance.isHidden():
            cls.GUI_instance.show()
        else:
            cls.GUI_instance.raise_()
            cls.GUI_instance.activateWindow()

    def __init__(self, parent=maya_main_window()):
        # Call the super function with class and current instance(self)
        super(GUI, self).__init__(parent)
        self.setWindowTitle('{0} | {1}'.format(_NAME, __version__))

        # Get root path parent:
        self._root_path = re.sub(r"previs.*", "", os.path.dirname(__file__))

        self._icons_path = os.path.join(self._root_path, 'icons')
        self._cam_icon = QtGui.QIcon(os.path.join(
            self._icons_path, "video-camera.ico"))
        self.setWindowIcon(self._cam_icon)
        self.setMinimumWidth(600)
        self.setMaximumWidth(1200)
        self.setMinimumHeight(600)
        self.setMaximumHeight(800)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.previsPanel = panels.playblast.Window()
        self.storyboardPanel = panels.storyboard.Window()

        self.V_root_window_LYT = QtWidgets.QVBoxLayout(self)
        self.H_root_main_LYT = QtWidgets.QHBoxLayout()
        self.V_root_window_LYT.addLayout(self.H_root_main_LYT)

        self._set_tabs()
        self._set_shot_creation_group()
        self._set_shots_editing_group()
        self._set_right_widgets_group()
        self._set_console()
        self._set_footer()

    # --------------------------------------------------------------------------
    # Public methods:

    def showEvent(self, event):
        super(GUI, self).showEvent(event)

    # --------------------------------------------------------------------------
    # Private methods:

    def _set_tabs(self):
        self.H_root_tab_LYT = None

        def _widgets():
            self.previs_TAB = agUI.ToolkitQTab()

            self.work_tab_WGT = QtWidgets.QWidget()
            self.export_tab_WGT = QtWidgets.QWidget()

            self.previs_TAB.addTab(self.work_tab_WGT, "Work")
            self.previs_TAB.addTab(self.export_tab_WGT, "Export")

        def _layouts():
            _H_LYT = QtWidgets.QHBoxLayout()
            self.work_tab_LYT = QtWidgets.QVBoxLayout()
            self.work_tab_WGT.setLayout(self.work_tab_LYT)

            self.export_tab_LYT = QtWidgets.QVBoxLayout()
            self.export_tab_WGT.setLayout(self.export_tab_LYT)

            _H_LYT.addWidget(self.previs_TAB)
            self.H_root_tab_LYT = _H_LYT
            self.H_root_main_LYT.addLayout(self.H_root_tab_LYT)

        _widgets()
        _layouts()

    def _set_shot_creation_group(self):
        self.root_creation_group_LYT = None

        def _widgets():
            self.create_GRP = agUI.ToolkitQGroupBox('Create:')
            self._shotname_LNE = agUI.ToolkitQLineEdit()
            self._shotcode_LNE = agUI.ToolkitQLineEdit()

            self._start_LNE = agUI.ToolkitQLineEdit()
            self._start_LNE.setPlaceholderText('Start')

            self._end_LNE = agUI.ToolkitQLineEdit()
            self._end_LNE.setPlaceholderText('End')

            self.create_BTN = agUI.ToolkitQPushButton('', '')
            _create_icon = QtGui.QIcon(
                os.path.join(self._icons_path, "create.ico"))
            self.create_BTN.setIcon(_create_icon)
            self.create_BTN.setIconSize(QtCore.QSize(110, 30))

        def _validators():
            _shotcode_validator = QtGui.QRegExpValidator()
            _shotcode_validator.setRegExp(
                QtCore.QRegExp("[a-zA-Z]{3}[0-9]{3}"))
            self._shotcode_LNE.setValidator(_shotcode_validator)
            self._start_LNE.setValidator(QtGui.QIntValidator())
            self._end_LNE.setValidator(QtGui.QIntValidator())

        def _layouts():
            _V_LYT = QtWidgets.QVBoxLayout()

            _V_inner_group_LYT = QtWidgets.QVBoxLayout()

            _range_LYT = QtWidgets.QHBoxLayout()
            _range_LYT.addWidget(self._start_LNE)
            _range_LYT.addWidget(self._end_LNE)

            _creation_form_LYT = QtWidgets.QFormLayout()
            _creation_form_LYT.addRow(
                'Project:',
                self._shotname_LNE)
            _creation_form_LYT.addRow(
                'Nomenclature:',
                self._shotcode_LNE)
            _creation_form_LYT.addRow(
                'Duration:',
                _range_LYT)

            _H_create_button_LYT = QtWidgets.QHBoxLayout()
            _H_create_button_LYT.setSpacing(0)
            _H_create_button_LYT.addStretch()
            _H_create_button_LYT.addWidget(self.create_BTN)

            _V_inner_group_LYT.addLayout(_creation_form_LYT)
            _V_inner_group_LYT.addLayout(_H_create_button_LYT)
            _V_inner_group_LYT.addStretch()

            self.create_GRP.setLayout(_V_inner_group_LYT)
            _V_LYT.addWidget(self.create_GRP)
            self.root_creation_group_LYT = _V_LYT
            self.work_tab_LYT.addLayout(self.root_creation_group_LYT)

        def _methods():
            def create():
                self._SHOT_DATA['project'] = self._shotname_LNE.text()
                self._SHOT_DATA['shot'] = self._shotcode_LNE.text().upper()
                self._SHOT_DATA['start'] = self._start_LNE.text()
                self._SHOT_DATA['end'] = self._end_LNE.text()

                search_for_shot = pm.ls('*{}*'.format(self._SHOT_DATA['shot']))

                if len(search_for_shot) != 0 or len(self._SHOT_DATA["shot"]) == 0:
                    self.console.log('''
                                    Check for one of the following errors:
                                        - That shot has been already created.
                                        - Clear the scene from any node that has the name of your shot.
                                        - You didn't provide a valid sequence name.
                                        - You didn't provide a valid and distinctive shot name.
                                    ''', "error")

                elif len(self._SHOT_DATA["shot"]) != 6:
                    self.console.log(
                        "Your shotcode has to contain 3 characters and 3 digits", "error")
                elif int(self._SHOT_DATA["end"]) <= int(self._SHOT_DATA["start"]):
                    self.console.log(
                        "Your end frame cannot be lower or equal to your start frame.", "error")
                else:
                    self._SHOT_DATA['shot'] = self._SHOT_DATA['shot'].upper()
                    self._SHOT_DATA['start'] = int(self._SHOT_DATA['start'])
                    self._SHOT_DATA['end'] = int(self._SHOT_DATA['end'])
                    xform, camera = simpleCameraRig.create(self._SHOT_DATA)
                    sequencerShot.create(self._SHOT_DATA, camera)
                    self.console.log("{0} was created!".format(
                        self._SHOT_DATA["shot"]), "success")

            self.create_BTN.clicked.connect(create)

        _widgets()
        _validators()
        _layouts()
        _methods()

    def _set_shots_editing_group(self):
        self.root_editing_group_LYT = None

        def _widgets():
            self.edit_GRP = agUI.ToolkitQGroupBox('Edit:')
            self._editing_instruction_LBL = QtWidgets.QLabel(
                '<i>Select a shot to modify in the camera sequencer</i>')
            self._editing_instruction_LBL.setStyleSheet(
                "background-color:rgba(0,0,0,0)")

            self.ammountFrames_LNE = agUI.ToolkitQLineEdit()
            self._amount_of_frames_BTN = agUI.ToolkitQPushButton('Move', '')
            self.ammountFrames_LNE.setPlaceholderText('1, 20, -10, etc...')
            self.ammountFrames_LNE.setMaximumWidth(110)
            self.ammountFrames_LNE.setValidator(QtGui.QIntValidator())

            self._editing_project_LNE = agUI.ToolkitQLineEdit()
            self._editing_project_BTN = agUI.ToolkitQPushButton('Rename', '')
            self._editing_shotcode_LNE = agUI.ToolkitQLineEdit()
            self._editing_shotcode_BTN = agUI.ToolkitQPushButton(
                'Rename', '')
            self._delete_shot_BTN = agUI.ToolkitQPushButton("")
            _delete_shot_icon = QtGui.QIcon(
                os.path.join(self._icons_path, "recyclebin.ico"))
            self._delete_shot_BTN.setIcon(_delete_shot_icon)
            self._delete_shot_BTN.setIconSize(QtCore.QSize(50, 50))
            self._delete_shot_BTN.setStyleSheet("background:rgb(100,40,40)")

        def _validators():
            _shotcode_validator = QtGui.QRegExpValidator()
            _shotcode_validator.setRegExp(
                QtCore.QRegExp("[a-zA-Z]{3}[0-9]{3}"))
            self._editing_shotcode_LNE.setValidator(_shotcode_validator)

        def _layouts():
            _V_H_LYT = QtWidgets.QHBoxLayout()
            _V_inner_group_LYT = QtWidgets.QVBoxLayout()

            _H_editing_project_LYT = QtWidgets.QHBoxLayout()
            _H_editing_project_LYT.addWidget(self._editing_project_LNE)
            _H_editing_project_LYT.addWidget(self._editing_project_BTN)

            _H_editing_shotcode_LYT = QtWidgets.QHBoxLayout()
            _H_editing_shotcode_LYT.addWidget(self._editing_shotcode_LNE)
            _H_editing_shotcode_LYT.addWidget(self._editing_shotcode_BTN)

            _H_editing_delete_LYT = QtWidgets.QHBoxLayout()
            _H_editing_delete_LYT.addWidget(self._delete_shot_BTN)

            moveShots_LYT = QtWidgets.QHBoxLayout()
            moveShots_LYT.addWidget(self.ammountFrames_LNE)
            moveShots_LYT.addWidget(self._amount_of_frames_BTN)
            moveShots_LYT.addStretch()

            _form_LYT = QtWidgets.QFormLayout()
            _form_LYT.addRow('Frames:',
                             moveShots_LYT)
            _form_LYT.addRow('Project:',
                             _H_editing_project_LYT)
            _form_LYT.addRow('Nomenclature:',
                             _H_editing_shotcode_LYT)
            _form_LYT.addRow('Delete selected shot(s): ',
                             _H_editing_delete_LYT)

            _V_inner_group_LYT.addWidget(self._editing_instruction_LBL)
            _V_inner_group_LYT.addLayout(_form_LYT)

            self.edit_GRP.setLayout(_V_inner_group_LYT)
            _V_H_LYT.addWidget(self.edit_GRP)

            self.root_editing_group_LYT = _V_H_LYT
            self.work_tab_LYT.addLayout(self.root_editing_group_LYT)

        def _methods():
            def change_shotcode():
                strategy = {'type': 'shot',
                            'new_name': self._editing_shotcode_LNE.text().upper()}

                result = editShots.rename_shots(
                    pm.ls(sl=True, type='shot'), strategy)
                self.console.log(result["message"], result["status"])

            def retime_shots():
                frames = 0 if self.ammountFrames_LNE.text(
                ) == "" else int(self.ammountFrames_LNE.text())

                result = moveShots.move_shots(
                    pm.ls(sl=True, type="shot"), frames)

                self.console.log(result["message"], result["status"])

            def change_project_name():
                strategy = {'type': 'project',
                            'new_name': self._editing_project_LNE.text()}
                result = editShots.rename_shots(
                    pm.ls(sl=True, type='shot'), strategy)
                self.console.log(result["message"], result["status"])

            def delete_shots():
                result = editShots.delete_shots()
                self.console.log(result["message"], result["status"])

            self._editing_shotcode_BTN.clicked.connect(change_shotcode)
            self._amount_of_frames_BTN.clicked.connect(retime_shots)
            self._editing_project_BTN.clicked.connect(change_project_name)
            self._delete_shot_BTN.clicked.connect(delete_shots)

        _widgets()
        _validators()
        _layouts()
        _methods()

    def _set_right_widgets_group(self):
        self.H_right_LYT = None

        def _widgets():
            self._playblast_GRP = agUI.ToolkitQGroupBox('Playblast by:')
            self._playblast_sequence_BTN = agUI.ToolkitQPushButton(
                'Sequence', '')
            self._playblast_shot_BTN = agUI.ToolkitQPushButton('Shot', '')

            self._utilities_GRP = agUI.ToolkitQGroupBox('Utilities:')
            self._frame_camera_BTN = agUI.ToolkitQPushButton(
                'Go to camera',
                tooltip="Frame in view the camera for the selected shot")
            self._align_BTN = agUI.ToolkitQPushButton(
                'Align',
                tooltip="All selected objects will go to the position of the last one")
            self._reset_xform_BTN = agUI.ToolkitQPushButton(
                'Reset',
                tooltip='Reset transformations of selected objects')
            self._previs_panel_BTN = agUI.ToolkitQPushButton(
                'Previs panel',
                tooltip='Window attached to sequencer cameras')
            self._storyboard_panel_BTN = agUI.ToolkitQPushButton(
                'Storyboard panel',
                tooltip='Window with a storyboard camera')
            self._sequencer_BTN = agUI.ToolkitQPushButton("Sequencer")
            self._create_groups_BTN = agUI.ToolkitQPushButton('Groups')
            self._scene_cleanup_BTN = agUI.ToolkitQPushButton('Cleanup')
            self._sequencer_BTN.setStyleSheet(
                "background-color: rgb(60,100,120)")

        def _layouts():
            _H_LYT = QtWidgets.QHBoxLayout()

            _V_right_inner_LYT = QtWidgets.QVBoxLayout()

            playblastButtons_LYT = QtWidgets.QVBoxLayout()
            playblastButtons_LYT.addWidget(self._playblast_sequence_BTN)
            playblastButtons_LYT.addWidget(self._playblast_shot_BTN)
            self._playblast_GRP.setLayout(playblastButtons_LYT)
            _V_right_inner_LYT.addWidget(self._playblast_GRP)

            utilitiesButtons_LYT = QtWidgets.QVBoxLayout()
            utilitiesButtons_LYT.addWidget(self._previs_panel_BTN)
            utilitiesButtons_LYT.addWidget(self._storyboard_panel_BTN)
            utilitiesButtons_LYT.addWidget(self._sequencer_BTN)
            utilitiesButtons_LYT.addWidget(self._frame_camera_BTN)
            utilitiesButtons_LYT.addWidget(self._align_BTN)
            utilitiesButtons_LYT.addWidget(self._reset_xform_BTN)
            self._utilities_GRP.setLayout(utilitiesButtons_LYT)
            _V_right_inner_LYT.addWidget(self._utilities_GRP)

            _H_LYT.addLayout(_V_right_inner_LYT)
            self.H_right_LYT = _H_LYT
            self.H_root_main_LYT.addLayout(self.H_right_LYT)

        def _methods():

            def playblast_by_sequence():
                result = playblast.by_sequence()
                self.console.log(result["message"], result["status"])

            def playblast_by_shot():
                result = playblast.by_shots()
                self.console.log(result["message"], result["status"])

            def create_previs_window():
                self.previsPanel.create()
                pm.sequenceManager(modelPanel='Playblast_modelPanel')
                self.console.log("Previs panel created.", "success")

            def create_storyboard_window():
                self.storyboardPanel.create()
                self.console.log("Storyboard panel created.", "success")

            def align():
                result = camOps.transformationOperations.align()
                self.console.log(result["message"], result["status"])

            def reset():
                result = camOps.transformationOperations.reset_transform()
                self.console.log(result["message"], result["status"])

            def show_sequencer():
                mel.eval("SequenceEditor;")

            def frame_shot_camera():
                result = camOps.cameraOperations.fit_select_camera()
                self.console.log(result["message"], result["status"])

            self._previs_panel_BTN.clicked.connect(create_previs_window)

            self._storyboard_panel_BTN.clicked.connect(
                create_storyboard_window)

            self._playblast_sequence_BTN.clicked.connect(playblast_by_sequence)

            self._playblast_shot_BTN.clicked.connect(playblast_by_shot)

            self._sequencer_BTN.clicked.connect(show_sequencer)

            self._frame_camera_BTN.clicked.connect(frame_shot_camera)

            self._align_BTN.clicked.connect(align)

            self._reset_xform_BTN.clicked.connect(reset)

        _widgets()
        _layouts()
        _methods()

    def _set_console(self):
        self.H_root_console_LYT = None

        def _widgets():
            self.console = agUI.ToolkitQConsole()

        def _layouts():
            _H_LYT = QtWidgets.QHBoxLayout()
            _H_LYT.addWidget(self.console)

            self.H_root_console_LYT = _H_LYT
            self.V_root_window_LYT.addLayout(self.H_root_console_LYT)

        _widgets()
        _layouts()

    def _set_footer(self):
        self.H_root_footer_LYT = None

        def _widgets():
            self._footer_WGT = agUI.ToolkitQFooter(self)

        def _layouts():
            _H_LYT = QtWidgets.QHBoxLayout()
            _H_LYT.addLayout(self._footer_WGT.getLayout())

            self.H_root_footer_LYT = _H_LYT
            self.V_root_window_LYT.addLayout(self.H_root_footer_LYT)

        _widgets()
        _layouts()
