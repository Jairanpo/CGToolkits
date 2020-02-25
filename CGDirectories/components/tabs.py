import sys
import os

from PySide2 import QtWidgets, QtCore, QtGui
import CGAgnostics.GUI as agUI


class Tabs:

    def __init__(self, parent=""):
        self.parent = parent
        self.V_root_tabs_LYT = None

        self._widgets()
        self._layouts()

    # Public methods:   -----------------------------------------

    @property
    def layout(self):
        return self.V_root_tabs_LYT

    @property
    def campaign(self):
        return self.v_campaign_tab_LYT

    @property
    def project(self):
        return self.v_project_tab_LYT

    @property
    def asset(self):
        return self.V_assets_tab_LYT

    @property
    def shot(self):
        return self.V_shot_tab_LYT

    @property
    def widget(self):
        _WGT = QtWidgets.QWidget()
        _WGT.setLayout(self.layout)
        return _WGT

        # Private methods:  -----------------------------------------

    def _widgets(self):
        self.dir_TAB = agUI.ToolkitQTab()

        self.campaign_WGT = QtWidgets.QWidget()
        self.project_WGT = QtWidgets.QWidget()
        self.assets_WGT = QtWidgets.QWidget()
        self.shot_WGT = QtWidgets.QWidget()

        self.dir_TAB.addTab(self.campaign_WGT, "Campaign")
        self.dir_TAB.addTab(self.project_WGT, "Project")
        self.dir_TAB.addTab(self.assets_WGT, "Asset")
        self.dir_TAB.addTab(self.shot_WGT, "Shot")

        self.dir_TAB.setIconSize(QtCore.QSize(50, 50))

    def _layouts(self):
        _V_LYT = QtWidgets.QHBoxLayout()

        self.v_campaign_tab_LYT = QtWidgets.QVBoxLayout()
        self.campaign_WGT.setLayout(self.v_campaign_tab_LYT)

        self.v_project_tab_LYT = QtWidgets.QVBoxLayout()
        self.project_WGT.setLayout(self.v_project_tab_LYT)

        self.V_assets_tab_LYT = QtWidgets.QVBoxLayout()
        self.assets_WGT.setLayout(self.V_assets_tab_LYT)

        self.V_shot_tab_LYT = QtWidgets.QVBoxLayout()
        self.shot_WGT.setLayout(self.V_shot_tab_LYT)

        _V_LYT.addWidget(self.dir_TAB)

        self.V_root_tabs_LYT = _V_LYT
