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

from files_analyser import *
import report_generator

class Ui_Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("Window.ui", self)

        title = "Code Metrics" + " V" + VERSION
        #_translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(QtCore.QCoreApplication.translate("Window", title))
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
VERSION = "3.4.2"

app = QtWidgets.QApplication(sys.argv)
ui = Ui_Window()


if __name__ == "__main__":
    print("\n\
NOT MEANT TO BE RUN\n\
\n\
This is just the module for GUI.\n\
Run 'code_metrics.py' to start the application.\n\
")

