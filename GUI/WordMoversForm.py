# App libraries
from .NLPResultForm import NLPResultForm
# Third-party libraries
from PyQt5 import QtWidgets, QtGui


class WordMoversForm(QtWidgets.QMdiSubWindow):
    def __init__(self, nlp_service, text_1, **kwargs):
        super(WordMoversForm, self).__init__(**kwargs)

        self._nlp_service = nlp_service

        self.setWindowTitle("Word Movers Window")
        self.setMinimumWidth(700)

        # Main widget and BoxLayout settings
        form = QtWidgets.QWidget()
        form_layout = QtWidgets.QVBoxLayout()
        form.setLayout(form_layout)
        self.setWidget(form)

        main_layout = QtWidgets.QVBoxLayout()

        # Error label
        self._error_label = QtWidgets.QLabel("", self)
        self._error_label.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        self._error_label.setStyleSheet('color: red')
        self._error_label.setWordWrap(True)
        main_layout.addWidget(self._error_label)

        # Text areas
        text_1_label = QtWidgets.QLabel("Jeden text (automaticky převzat z výsledků)", self)
        text_1_label.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        main_layout.addWidget(text_1_label)

        self.text_1_edit = QtWidgets.QTextEdit(self)
        self.text_1_edit.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        self.text_1_edit.setText(text_1)
        main_layout.addWidget(self.text_1_edit)

        text_2_label = QtWidgets.QLabel("Druhý text", self)
        text_2_label.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        main_layout.addWidget(text_2_label)

        self.text_2_edit = QtWidgets.QTextEdit(self)
        self.text_2_edit.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        main_layout.addWidget(self.text_2_edit)

        word_movers_analysis = QtWidgets.QPushButton("Word movers analysis", self)
        word_movers_analysis.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        word_movers_analysis.clicked.connect(self._on_word_movers_analysis)
        main_layout.addWidget(word_movers_analysis)

        form_layout.addStretch()
        form_layout.addLayout(main_layout)
        form_layout.addStretch()

    def _on_word_movers_analysis(self):
        self._error_label.setText("")

        if not (self.text_1_edit.toPlainText() and self.text_2_edit.toPlainText()):
            self._error_label.setText("Jeden/oba texty jsou prázdné.")

        try:
            word_movers_result = self._nlp_service.get_textacy_word_movers(self.text_1_edit.toPlainText(),
                                                                           self.text_2_edit.toPlainText())

            self.word_movers_result_form = NLPResultForm(str(word_movers_result), "Word Movers Result")
            self.word_movers_result_form.show()
        except Exception as ex:
            self._error_label.setText(ex.__str__())
