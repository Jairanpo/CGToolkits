from PySide2 import QtCore, QtWidgets, QtGui
import os


# Color definitions:
_WINDOW_STYLE = '''
    font: 10pt; background-color: rgb(40,40,45)
    '''
_BLUE_BTN_STYLE = '''
    QToolTip {color: white; border: 2px solid darkkhaki;
    padding: 5px; border - radius: 3 px; opacity: 200;}
    QPushButton {background-color: rgb(60,70,100)}'''
_DARK_LNE_STYLE = '''
    background:rgb(20,20,20);
    selection-background-color:rgb(250,100,30);'''
_DARK_TBL_STYLE = '''
    QTableWidget {
    background-color: rgb(25,25,25);
    selection-background-color:rgb(45,45,60)}

    QHeaderView{
        color:rgb(150,100,50);
        background-color:rgb(20,20,20)}
    '''
_DARK_TED_STYLE = '''
    QTextEdit {
    font: italic;
    color: rgb(100,100,100);
    background-color: rgb(20,20,20);
    selection-background-color:rgb(30,30,50)}
    '''
_DARK_CBX_STYLE = '''
    background:rgb(20,20,20);
    selection-background-color:rgb(250,100,30);
    '''
# End color definitions.


class ToolkitQDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(ToolkitQDialog, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.setStyleSheet(_WINDOW_STYLE)


class ToolkitQTab(QtWidgets.QTabWidget):
    def __init__(self):
        super(ToolkitQTab, self).__init__()

        self.setStyleSheet('''
                QTabBar::tab{
                background-color:rgb(30,30,30);
                font: bold;
                width:100px;
                }

                QTabBar::tab:selected, QTabBar::tab:hover {
                background: rgb(120,100,60);
                }

                QTabWidget::pane {border-top: 2px solid #C2C7CB;}
                QTabWidget::tab-bar {left: 20px;}
            ''')


class ToolkitQPushButton(QtWidgets.QPushButton):
    def __init__(self, label, tooltip='No tooltip set yet'):
        super(ToolkitQPushButton, self).__init__(label)
        self.setToolTip(tooltip)
        self.setStyleSheet(_BLUE_BTN_STYLE)


class ToolkitQLineEdit(QtWidgets.QLineEdit):
    def __init__(self, placeholder=''):
        super(ToolkitQLineEdit, self).__init__()
        self.setStyleSheet(_DARK_LNE_STYLE)
        self.setPlaceholderText(placeholder)

    s_key_pressed = QtCore.Signal()
    enter_key_pressed = QtCore.Signal()

    def keyPressEvent(self, e):
        super(ToolkitQLineEdit, self).keyPressEvent(e)
        if e.key() == QtCore.Qt.Key_S:
            self.s_key_pressed.emit()
        elif e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
            self.enter_key_pressed.emit()


class ToolkitQTableWidget(QtWidgets.QTableWidget):
    enter_pressed = QtCore.Signal()

    def __init__(self):
        super(ToolkitQTableWidget, self).__init__()
        self.setStyleSheet(_DARK_TBL_STYLE)

    def keyPressEvent(self, e):
        super(ToolkitQTableWidget, self).keyPressEvent(e)
        if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
            self.enter_pressed.emit()


class ToolkitQConsole(QtWidgets.QTextEdit):
    def __init__(self):
        self._colors = {
            "standar": QtGui.QColor(120, 120, 120),
            "success": QtGui.QColor(50, 150, 100),
            "warning": QtGui.QColor(170, 150, 40),
            "error": QtGui.QColor(180, 60, 60)
        }
        super(ToolkitQConsole, self).__init__()
        self.setPlainText("Logs...")
        self.setStyleSheet(_DARK_TED_STYLE)
        self.setMinimumHeight(40)
        self.setMaximumHeight(100)
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                           QtWidgets.QSizePolicy.Minimum)
        self.setReadOnly(True)

    def log(self, message, color="standar"):
        if color == "success":
            self.setText('')
            self.setTextColor(self._colors["success"])
            self.setText('<Success> ' + message)
        elif color == "warning":
            self.setText('')
            self.setTextColor(self._colors["warning"])
            self.setText('<Warning> ' + message)
        elif color == "error":
            self.setText('')
            self.setTextColor(self._colors["error"])
            self.setText('<Error> ' + message)
        else:
            self.setText('')
            self.setTextColor(self._colors["standar"])
            self.setText(message)


class ToolkitQGroupBox(QtWidgets.QGroupBox):
    def __init__(self, label):
        super(ToolkitQGroupBox, self).__init__(label)
        self.setStyleSheet(
            'QGroupBox {border: 1px solid rgb(20,20,20); padding:10%}')


class ToolkitQComboBox(QtWidgets.QComboBox):
    def __init__(self, list_of_items=None):
        super(ToolkitQComboBox, self).__init__()
        self.setStyleSheet(_DARK_CBX_STYLE)

        if list_of_items is not None:
            for each in list_of_items:
                self.addItem(each)


class ToolkitQCredits(QtWidgets.QLabel):
    def __init__(self):
        super(ToolkitQCredits, self).__init__()
        self.setText("Created by Jair Anguiano," +
                     "for support mail me at " +
                     '<a style="color:rgb(95,95,95);"href="jairanpo@gmail.com">' +
                     'jairanpo@gmail.com</a>')

        self.setStyleSheet("color:rgb(90,90,90); font: Italic")


class ToolkitQCloseButton(QtWidgets.QPushButton):
    def __init__(self, text="close"):
        super(ToolkitQCloseButton, self).__init__()
        self.setText(text)
        self.setMinimumWidth(80)
        self.setMaximumWidth(150)


class ToolkitQFooter():
    def __init__(self, window_instance):
        self.credits_LBL = ToolkitQCredits()
        self.close_BTN = ToolkitQCloseButton()
        self.instance = window_instance
        self._layout = None
        self._set_layout()
        self.connections()

    def _set_layout(self):
        _H_LYT = QtWidgets.QHBoxLayout()
        _H_LYT.addWidget(self.credits_LBL)
        _H_LYT.addWidget(self.close_BTN)
        self._layout = _H_LYT

    def getLayout(self):
        return self._layout

    def connections(self):
        self.close_BTN.clicked.connect(self.instance.close)
