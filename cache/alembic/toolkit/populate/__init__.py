from PySide2 import QtCore, QtWidgets, QtGui
import pymel.core as pm


def with_items(QTableWidget):
    QTableWidget.setRowCount(0)
    selection = pm.ls(sl=True, type="transform")
    for index, node in enumerate(selection):
        QTableWidget.insertRow(index)
        dag_path = node.longName()

        i_node_name = QtWidgets.QTableWidgetItem()
        i_node_name.setText(dag_path.split('|')[-1])
        i_node_name.setFlags(QtCore.Qt.NoItemFlags)

        i_file_name = QtWidgets.QTableWidgetItem()
        i_file_name.setText("DefaultName{0}".format(index))
        i_file_name.setData(
            QtCore.Qt.UserRole,
            "DefaultName{0}".format(index))

        i_root_name = QtWidgets.QTableWidgetItem()
        i_root_name.setText(dag_path)
        i_root_name.setData(
            QtCore.Qt.UserRole, dag_path)
        i_root_name.setFlags(QtCore.Qt.NoItemFlags)

        QTableWidget.setItem(index, 0, i_node_name)
        QTableWidget.setItem(index, 1, i_file_name)
        QTableWidget.setItem(index, 2, i_root_name)


def update_item(QTableWidget, row, column):
    item = QTableWidget.item(row, column)
    item.setData(QtCore.Qt.UserRole, item.text())


def with_shots(QTableWidget):
    QTableWidget.setRowCount(0)
    selection = pm.ls(type="shot")
    result = []
    for index, node in enumerate(selection):
        data = {
            "shot": "",
            "range": {"start": 0, "end": 0},
            "camera": "",
            "widget": None
        }

        QTableWidget.insertRow(index)
        name = node.shotName.get()
        i_shot_name = QtWidgets.QTableWidgetItem(name)
        i_shot_name.setData(
            QtCore.Qt.UserRole, node.name())
        i_shot_name.setFlags(
            QtCore.Qt.NoItemFlags)
        i_shot_name.setTextAlignment(
            QtCore.Qt.AlignVCenter |
            QtCore.Qt.AlignHCenter)

        data["shot"] = node.name()

        start = int(node.getStartTime())
        end = int(node.getEndTime())
        i_range = QtWidgets.QTableWidgetItem(
            "{0} - {1}".format(start, end))
        i_range.setTextAlignment(
            QtCore.Qt.AlignVCenter |
            QtCore.Qt.AlignHCenter)
        i_range.setFlags(
            QtCore.Qt.NoItemFlags)
        data["range"]["start"] = start
        data["range"]["end"] = end

        i_camera = QtWidgets.QTableWidgetItem(
            node.getCurrentCamera())
        i_camera.setTextAlignment(
            QtCore.Qt.AlignVCenter |
            QtCore.Qt.AlignHCenter)
        i_camera.setFlags(
            QtCore.Qt.NoItemFlags)
        data["camera"] = pm.ls(node.getCurrentCamera())[0]

        _export_WGT = QtWidgets.QWidget()
        _export_CBX = QtWidgets.QCheckBox()
        _H_LYT = QtWidgets.QHBoxLayout()
        _H_LYT.addWidget(_export_CBX)
        _H_LYT.setAlignment(QtCore.Qt.AlignHCenter)
        _export_WGT.setLayout(_H_LYT)
        data["widget"] = _export_CBX

        _export_camera_WGT = QtWidgets.QWidget()
        _export_camera_CBX = QtWidgets.QCheckBox()
        _H_camera_LYT = QtWidgets.QHBoxLayout()
        _H_camera_LYT.addWidget(_export_camera_CBX)
        _H_camera_LYT.setAlignment(QtCore.Qt.AlignHCenter)
        _export_camera_WGT.setLayout(_H_camera_LYT)
        data["export_camera_widget"] = _export_camera_CBX

        _export_clip_WGT = QtWidgets.QWidget()
        _export_clip_CBX = QtWidgets.QCheckBox()
        _H_clip_LYT = QtWidgets.QHBoxLayout()
        _H_clip_LYT.addWidget(_export_clip_CBX)
        _H_clip_LYT.setAlignment(QtCore.Qt.AlignHCenter)
        _export_clip_WGT.setLayout(_H_clip_LYT)
        data["export_clip_widget"] = _export_camera_CBX

        QTableWidget.setItem(index, 0, i_shot_name)
        QTableWidget.setItem(index, 1, i_range)
        QTableWidget.setItem(index, 2, i_camera)
        QTableWidget.setCellWidget(index, 3, _export_WGT)
        QTableWidget.setCellWidget(index, 4, _export_camera_WGT)
        QTableWidget.setCellWidget(index, 5, _export_clip_WGT)

        result.append(data)

    return result
