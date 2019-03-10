# Basic libraries
import sys
# App libraries
from .MainForm import MainForm
# Third-party libraries
from PyQt5 import QtWidgets


class App(QtWidgets.QApplication):
    def __init__(self):
        super(App, self).__init__(sys.argv)

    def build(self):
        self.main_form = MainForm()

        self.main_form.setup()

        sys.exit(self.exec_())
