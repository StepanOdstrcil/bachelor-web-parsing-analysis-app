# Basic libraries
import datetime
# Third-party libraries
from PyQt5 import QtWidgets, QtGui


class NLPResultForm(QtWidgets.QMdiSubWindow):
    def __init__(self, result, raw_text="", processed_text="", header="Result form", **kwargs):
        super(NLPResultForm, self).__init__(**kwargs)

        self._raw_text = raw_text

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

        self.result_edit = QtWidgets.QTextEdit(self)
        self.result_edit.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        self.result_edit.setText(result)
        result_layout.addWidget(self.result_edit)

        processed_text_layout = QtWidgets.QVBoxLayout()

        processed_text_label = QtWidgets.QLabel(f"Zpracovaný text", self)
        processed_text_label.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        processed_text_layout.addWidget(processed_text_label)

        self.processed_text_edit = QtWidgets.QTextEdit(self)
        self.processed_text_edit.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        self.processed_text_edit.setText(processed_text)
        processed_text_layout.addWidget(self.processed_text_edit)

        buttons_layout = QtWidgets.QVBoxLayout()

        save_results = QtWidgets.QPushButton("Uložit výsledky", self)
        save_results.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        save_results.clicked.connect(self._on_save_results)
        buttons_layout.addWidget(save_results)

        form_layout.addStretch()
        form_layout.addLayout(result_layout)
        form_layout.addLayout(processed_text_layout)
        form_layout.addLayout(buttons_layout)
        form_layout.addStretch()

    def _on_save_results(self):
        with open(f"{self.windowTitle()}_{str(datetime.datetime.now()).replace('-', ' ').replace(':', '.')}.txt",
                  "w") as f:
            f.write(f"Výsledek:\n{self.result_edit.toPlainText()}\n-----\n"
                    f"Čistý text:\n{self._raw_text}\n-----\n"
                    f"Zpracovaný text:\n{self.processed_text_edit.toPlainText()}")
