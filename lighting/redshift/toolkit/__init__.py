# Standard library imports
import os

# Third party imports
from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import pymel.core as pm

# Local application imports
import agnostics.GUI as agUI
import lighting.redshift.rsLayers as layers
import lighting.redshift.config as config
import lighting.redshift.rsID as rsID
import lighting.redshift.rsMatteParams as rsMP

__version__ = 'v2.0.0'


def maya_main_window():
    """
    return the Maya main window widget as Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class GUI(agUI.ToolkitQDialog):
    GUI_instance = None

    def __init__(self, parent=maya_main_window()):
        super(GUI, self).__init__(parent)
        self.setWindowTitle('Redshift Toolkit {}'.format(__version__))
        self._main_path = os.path.dirname(__file__)
        self._icons_path = os.path.join(self._main_path, 'icons')
        self._rs_icon = QtGui.QIcon(
            os.path.join(self._icons_path, "rs_icon.ico"))
        self.rs_refresh_icon = QtGui.QIcon(
            os.path.join(self._icons_path, "refresh.ico"))
        self.setWindowIcon(self._rs_icon)
        self.setMinimumWidth(300)
        self.setMaximumWidth(1920)
        self.setMinimumHeight(200)
        self.setMaximumHeight(900)
        self.rs_matteParams = rsMP.MatteParams()
        self.rs_ids_instance = rsID.RedShiftIDs()

        self.create_tab_widgets()
        self.create_ID_tab()
        self.create_layers_tab()
        self.create_agnostics()
        self.create_layouts()
        self.create_connections()

    @classmethod
    def show_dialog(cls):
        if not cls.GUI_instance:
            cls.GUI_instance = GUI()

        if cls.GUI_instance.isHidden():
            cls.GUI_instance.show()
        else:
            cls.GUI_instance.raise_()
            cls.GUI_instance.activateWindow()

    def create_tab_widgets(self):
        self.rs_TAB = agUI.ToolkitQTab()
        self.rs_ID_tab_WGT = QtWidgets.QWidget()
        self.rs_ID_tab_LYT = QtWidgets.QVBoxLayout()
        self.rs_ID_tab_WGT.setLayout(self.rs_ID_tab_LYT)
        self.rs_TAB.addTab(self.rs_ID_tab_WGT, "IDs")

        self.rs_layers_tab_WGT = QtWidgets.QWidget()
        self.rs_layers_tab_LYT = QtWidgets.QVBoxLayout()
        self.rs_layers_tab_WGT.setLayout(self.rs_layers_tab_LYT)
        self.rs_TAB.addTab(self.rs_layers_tab_WGT, "layers")

    def create_ID_tab(self):
        self.id_LNE = agUI.ToolkitQLineEdit()
        self.id_LNE.setMaximumWidth(50)
        self.id_LNE.setValidator(QtGui.QIntValidator())

        self.assign_id_to_selected_BTN = agUI.ToolkitQPushButton(
            'Assign to selection')

        self.ID_TBL = agUI.ToolkitQTableWidget()
        self.ID_TBL.setColumnCount(2)
        self.ID_TBL.setHorizontalHeaderLabels(
            ['ID', 'Geometry'])
        self.ID_TBL.setColumnWidth(0, 30)
        self.ID_TBL.setColumnWidth(1, 120)
        self.ID_TBL.setSortingEnabled(True)
        horizontal_header_view = self.ID_TBL.horizontalHeader()
        horizontal_header_view.setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)

        self.fill_table_BTN = QtWidgets.QPushButton('Refresh')
        self.fill_table_BTN.setIcon(self.rs_refresh_icon)
        self.fill_table_BTN.setStyleSheet(
            "font: italic; color:rgb(150,150,150);")

        self.rsMatteParam_BTN = agUI.ToolkitQPushButton('Matte parameter')
        self.rsMatteParam_LNE = agUI.ToolkitQLineEdit()
        self.rsMatteParam_LNE.setMaximumWidth(120)
        self.rsMatteParam_LNE.setMaximumWidth(300)
        self.rsMatteParam_LNE.setPlaceholderText('Name your node')

        self.create_ID_AOVs_LNE = agUI.ToolkitQLineEdit()
        self.create_ID_AOVs_LNE \
            .setPlaceholderText('Shot nomenclature')
        self.create_ID_AOVs_LNE.setMinimumWidth(120)
        self.create_ID_AOVs_LNE.setMaximumWidth(300)
        self.create_ID_AOV_BTN = agUI.ToolkitQPushButton('ID AOVs')
        self.create_ID_AOV_values_CBX = QtWidgets.QComboBox()
        ID_values = config.get_id_values()
        for index, each in enumerate(ID_values):
            self.create_ID_AOV_values_CBX.addItem(
                "RGB: {0} {1} {2}".format(*each["values"]))
            self.create_ID_AOV_values_CBX.setItemData(
                index, each, QtCore.Qt.UserRole)
        self.create_ID_AOV_values_CBX.setStyleSheet('''
            background-color: rgb(30,30,30);
            font: italic "Sans Serif";
            color:rgb(150,150,150);
        ''')

        self.ID_main_V_LYT = QtWidgets.QVBoxLayout()
        id_form_LYT = QtWidgets.QFormLayout()
        create_matte_param_LYT = QtWidgets.QHBoxLayout()

        id_assign_select_LYT = QtWidgets.QHBoxLayout()
        id_assign_select_LYT.addWidget(self.id_LNE)
        id_assign_select_LYT.addWidget(self.assign_id_to_selected_BTN)
        id_assign_select_LYT.addStretch()
        id_assign_select_LYT.addWidget(self.fill_table_BTN)
        id_form_LYT.addRow('ID:', id_assign_select_LYT)
        self.ID_main_V_LYT.addLayout(id_form_LYT)
        self.ID_main_V_LYT.addWidget(self.ID_TBL)

        create_matte_param_LYT.addWidget(self.rsMatteParam_LNE)
        create_matte_param_LYT.addWidget(self.rsMatteParam_BTN)
        create_matte_param_LYT.addStretch()
        self.ID_main_V_LYT.addLayout(create_matte_param_LYT)

        create_ID_AOV_LYT = QtWidgets.QHBoxLayout()
        create_ID_AOV_LYT.addWidget(self.create_ID_AOVs_LNE)
        create_ID_AOV_LYT.addWidget(self.create_ID_AOV_values_CBX)
        create_ID_AOV_LYT.addWidget(self.create_ID_AOV_BTN)

        self.ID_main_V_LYT.addLayout(create_ID_AOV_LYT)

    def create_layers_tab(self):
        shaders_list = [
            'RedshiftSprite', 'surfaceShader',
            'RedshiftMaterial', 'RedshiftSkin',
            'lambert', 'blinn', 'RedshiftHair']

        shader_layer_GRP = agUI.ToolkitQGroupBox("Shader override layer: ")
        self.render_layer_name_LNE = agUI.ToolkitQLineEdit('Name')
        self.render_layer_type_CBX = agUI.ToolkitQComboBox(shaders_list)
        self.sprite_layer_base_CBX = agUI.ToolkitQComboBox(shaders_list[1: -1])
        self.sprite_with_LBL = QtWidgets.QLabel('    with:')
        self.create_render_layer_BTN = agUI.ToolkitQPushButton('Create')

        layers_naming_H_LYT = QtWidgets.QHBoxLayout()

        layers_type_V_LYT = QtWidgets.QVBoxLayout()
        layers_type_V_LYT.addWidget(self.render_layer_type_CBX)
        layers_type_V_LYT.addWidget(self.sprite_with_LBL)
        layers_type_V_LYT.addWidget(self.sprite_layer_base_CBX)

        layers_naming_H_LYT.addWidget(self.render_layer_name_LNE)
        layers_naming_H_LYT.addLayout(layers_type_V_LYT)
        layers_naming_H_LYT.addWidget(self.create_render_layer_BTN)

        shader_layer_GRP.setLayout(layers_naming_H_LYT)

        self.layers_main_V_LYT = QtWidgets.QVBoxLayout()
        self.layers_main_V_LYT.addStretch()
        self.layers_main_V_LYT.addWidget(shader_layer_GRP)
        self.layers_main_V_LYT.addStretch()

    def create_agnostics(self):
        self.console = agUI.ToolkitQConsole()
        self.close_BTN = QtWidgets.QPushButton('Close')

        self.footer_H_LYT = QtWidgets.QHBoxLayout()
        self.footer_H_LYT.addStretch()
        self.footer_H_LYT.addWidget(agUI.ToolkitQCredits())
        self.footer_H_LYT.addStretch()
        self.footer_H_LYT.addWidget(self.close_BTN)

    def create_layouts(self):
        main_LYT = QtWidgets.QVBoxLayout(self)

        main_LYT.addWidget(self.rs_TAB)
        self.rs_ID_tab_LYT.addLayout(self.ID_main_V_LYT)
        self.rs_layers_tab_LYT.addLayout(self.layers_main_V_LYT)

        main_LYT.addWidget(self.console)
        main_LYT.addLayout(self.footer_H_LYT)

    def create_connections(self):
        self.set_change_table_connection(True)
        self.assign_id_to_selected_BTN.clicked.connect(
            self.assign_id_to_selected)
        self.id_LNE.s_key_pressed.connect(self.select_by_id)
        self.id_LNE.enter_key_pressed.connect(self.assign_id_to_selected)
        self.ID_TBL.enter_pressed.connect(self.on_changed_cell)
        self.fill_table_BTN.clicked.connect(
            self.fill_table)
        self.create_ID_AOV_BTN.clicked.connect(self.create_ID_AOVs)
        self.rsMatteParam_BTN.clicked.connect(self.create_matte_params)

        self.render_layer_type_CBX.activated[str].connect(
            self.change_shader_override_type)
        self.create_render_layer_BTN.clicked.connect(
            self.create_shader_override_render_layer)

        self.close_BTN.clicked.connect(self.close)

    # _________________________________________________________

    def keyPressEvent(self, event):
        super(GUI, self).keyPressEvent(event)
        event.accept()

    def showEvent(self, event):
        super(GUI, self).showEvent(event)
        self.fill_table()

    def set_change_table_connection(self, is_enabled):
        if is_enabled:
            self.ID_TBL.cellChanged.connect(self.on_changed_cell)
        else:
            self.ID_TBL.cellChanged.disconnect(self.on_changed_cell)

    def fill_table(self):
        self.set_change_table_connection(False)
        self.ID_TBL.setRowCount(0)
        meshes = pm.ls(type='mesh')

        for i, mesh in enumerate(meshes):
            name = mesh.longName()
            id_val = mesh.rsObjectId.get()
            self.ID_TBL.insertRow(i)

            item_name = QtWidgets.QTableWidgetItem(name)

            item_name.setFlags(
                QtCore.Qt.ItemIsEnabled |
                QtCore.Qt.ItemIsSelectable)

            item_id = QtWidgets.QTableWidgetItem(str(id_val))
            item_id.setTextAlignment(
                QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            item_id.setFlags(
                QtCore.Qt.ItemIsEnabled |
                QtCore.Qt.ItemIsSelectable |
                QtCore.Qt.ItemIsEditable)
            item_id.setData(QtCore.Qt.UserRole, id_val)

            self.ID_TBL.setItem(i, 0, item_id)
            self.ID_TBL.setItem(i, 1, item_name)

        self.set_change_table_connection(True)

    def on_changed_cell(self):
        self.set_change_table_connection(False)
        item = self.ID_TBL.currentItem()
        row_id = self.ID_TBL.item(item.row(), 0).text()
        new_id = None

        if not row_id.strip().isdigit():
            new_id = 0
            self.console.log(
                'You didn\'t provide a valid ID number', 'error')
        else:
            new_id = int(row_id)

        if len(self.ID_TBL.selectedItems()) > 0:
            self.change_selected_cells_id(new_id)

        self.console.log('ID changed', 'success')
        self.rs_ids_instance.update_id_map_and_set()
        self.set_change_table_connection(True)

    def change_selected_cells_id(self, new_id):
        names_in_selection = []

        for each in self.ID_TBL.selectedItems():
            item = self.ID_TBL.item(each.row(), each.column())
            names_in_selection.append(self.ID_TBL.item(each.row(), 1).text())
            item.setData(QtCore.Qt.UserRole, new_id)
            item.setText(str(new_id))
        meshes = pm.ls(names_in_selection, type="mesh")
        self.rs_ids_instance.assign_id(meshes, new_id)

    def select_by_id(self):
        self.rs_ids_instance.update_id_map_and_set()
        current_id = int(self.id_LNE.text())

        if current_id in self.rs_ids_instance.scene_ids:
            self.rs_ids_instance.select_by_ids(current_id)
            self.console.log('Objects selected')
        else:
            self.console.log(
                'That ID hasn\'t been assigned in the scene yet', 'warning')

    def assign_id_to_selected(self):
        id_value = int(self.id_LNE.text())
        list_of_transform = pm.ls(sl=True, type='transform')
        list_of_shapes = []

        for transform in list_of_transform:
            shapes = transform.listRelatives(allDescendents=True, type="mesh")
            for shape in shapes:
                list_of_shapes.append(shape)

        if len(list_of_shapes) == 0:
            self.console.log("No objects selected", "warning")
            return
        self.rs_ids_instance.assign_id(list_of_shapes, id_value)
        self.console.log(
            'ID assigned to selected objects!', 'success')
        self.fill_table()

    def select_list_ids(self):
        items = self.ID_LST.selectedItems()
        selected_items = []
        for each in items:
            selected_items.append(each.text())

    def create_matte_params(self):
        name = self.rsMatteParam_LNE.text().strip()

        if name == '':
            name = 'default'

        nomenclature = 'matteParams_{}_AOV'.format(name)

        list_of_nodes = pm.ls(sl=True, type='transform')

        if len(list_of_nodes) != 0:
            self.rs_matteParams.send_nodes_inside_matteParam(
                nomenclature, list_of_nodes)
            self.console.log(
                "Matte param node created with name: \"{}\"".format(nomenclature), "success")
        else:
            self.console.log(
                "You didn't select any object", "error")

    def create_ID_AOVs(self):
        stripped_text = self.create_ID_AOVs_LNE.text().strip()
        nomenclature = "ID_{}_AOV".format(stripped_text)
        if stripped_text != '':
            self.rs_ids_instance.create_aovs(
                stripped_text,
                self.create_ID_AOV_values_CBX.currentData(QtCore.Qt.UserRole)["values"])
            self.console.log(
                'ID AOV created with name: \"{}\"'.format(nomenclature), 'success')
        else:
            self.console.log(
                'Please set a name your ID AOVs', 'warning')

    def change_shader_override_type(self, shader_type):
        if shader_type == 'RedshiftSprite':
            self.sprite_with_LBL.setVisible(True)
            self.sprite_layer_base_CBX.setVisible(True)
        else:
            self.sprite_with_LBL.setVisible(False)
            self.sprite_layer_base_CBX.setVisible(False)

    def create_shader_override_render_layer(self):
        shader_type = self.render_layer_type_CBX.currentText()
        selected = pm.ls(sl=True, type='transform')
        name = self.render_layer_name_LNE.text().encode("ascii", "replace")
        layer = None

        if name == '':
            self.console.log(
                'You have to provide a valid layer name.', 'error')
            return

        if len(selected) == 0:
            selected = None

        if shader_type == 'RedshiftSprite':
            sprite_base_shader = self.sprite_layer_base_CBX.currentText()
            layer = layers.create_redshift_shader_override_layer(
                name, sprite_base_shader, list_of_objects=selected, sprite=True)
        else:
            layer = layers.create_redshift_shader_override_layer(
                name, shader_type, list_of_objects=selected, sprite=False)

        self.console.log(
            'Shader override layer created: {}_RYR.'.format(name), 'success')
