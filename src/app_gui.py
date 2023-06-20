"""
-------
APP GUI
-------

* Handles GUI with PyQt.
* This file should be run to start the application.
* Generates the report as an html file.

"""

from PyQt5 import QtCore, QtWidgets, uic
import sys
import os

from Window import *
from files_analyser import *
import report_generator


#class AppGui(QtWidgets.QWidget):
class AppGui(QtWidgets.QWidget, Ui_Window):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        #super().__init__()

        #uic.loadUi("Window.ui", self)

        title = "Code Metrics" + " V" + VERSION
        #_translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(QtCore.QCoreApplication.translate("Window", title))
        #self.setWindowIcon(QtGui.QIcon('app_icon.ico'))

        self.browse_btn.clicked.connect(self.browse)
        self.skipDir_checkBox.toggled.connect(self.skipDir_toggled)
        self.skipDir_disabled = True
        self.dirFiltEntry.setDisabled(True)
        #self.exportToHtml_checkBox.toggled.connect(self.exportToHtml_toggled)
        self.report_btn.clicked.connect(self.response)

    def browse(self):

        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder_path: self.path_entry.setText(folder_path)

    def skipDir_toggled(self):

        if self.skipDir_checkBox.isChecked():
            self.skipDir_disabled = False
            self.dirFiltEntry.setDisabled(False)
        else:
            self.skipDir_disabled = True
            self.dirFiltEntry.setDisabled(True)

    def response(self):

        path = self.path_entry.text()
        filters = self.filters_entry.text()

        if not(path):
            err_str = "Provide folder path"
            self.resultConsole.setText("\n" + err_str)
            if self.exportToHtml_checkBox.isChecked():
                report_generator.generate_error_report(err_str)
        elif not(validate_path(path)):
            err_str = "Invalid folder path"
            self.resultConsole.setText("\n" + err_str)
            if self.exportToHtml_checkBox.isChecked():
                report_generator.generate_error_report(err_str)
        elif not(filters):
            err_str = "Provide filters"
            self.resultConsole.setText("\n" + err_str)
            if self.exportToHtml_checkBox.isChecked():
                report_generator.generate_error_report(err_str)

        else:
            data = fetch_metrics(path, filters, self.skipDir_disabled, self.dirFiltEntry.text())
            result = fetch_str_result(data)

            #self.path_var.set("")
            #self.filters_var.set("")

            self.resultConsole.setText(result)
            if self.exportToHtml_checkBox.isChecked():
                report_generator.generate_report(data)


# Handling high resolution displays
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

# Constants
VERSION = "4.0.0"

app = QtWidgets.QApplication(sys.argv)
ui = AppGui()

base_dir = os.path.dirname(__file__)
app.setWindowIcon(QtGui.QIcon(os.path.join(base_dir, 'app_icon.ico')))

try:
    from ctypes import windll  # Only exists on Windows.
    app_id = 'Madhavakumar.CodeMetrics.4.00'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
except ImportError:
    pass


if __name__ == "__main__":
    print("\n\
NOT MEANT TO BE RUN\n\
\n\
This is just the module for GUI.\n\
Run 'code_metrics.py' to start the application.\n\
")

