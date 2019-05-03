# Third-party libraries
from PyQt5 import QtWidgets, QtGui


class NLPResultForm(QtWidgets.QMdiSubWindow):
    def __init__(self, result, header, **kwargs):
        super(NLPResultForm, self).__init__(**kwargs)

        self.setWindowTitle(header)
        self.setMinimumWidth(700)

        # Main widget and BoxLayout settings
        form = QtWidgets.QWidget()
        form_layout = QtWidgets.QVBoxLayout()
        form.setLayout(form_layout)
        self.setWidget(form)

        result_layout = QtWidgets.QVBoxLayout()

        result_label = QtWidgets.QLabel(f"Výsledek NLP analýzy: {header}", self)
        result_label.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        result_layout.addWidget(result_label)

        result_edit = QtWidgets.QTextEdit(self)
        result_edit.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        result_edit.setText(result)
        result_layout.addWidget(result_edit)

        form_layout.addStretch()
        form_layout.addLayout(result_layout)
        form_layout.addStretch()
