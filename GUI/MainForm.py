# Basic libraries
from functools import wraps
# App libraries
from NLP.nlp_service import NLPService
from WebParsing.web_parser import WebParser
from .NLPResultForm import NLPResultForm
from .WordMoversForm import WordMoversForm
# Third-party libraries
from PyQt5 import QtWidgets, QtGui, QtCore


class MainForm(QtWidgets.QMainWindow):

    # -----------------
    # Decorators
    # -----------------

    def check_argument(fn):
        @wraps(fn)
        def check_argument_wrapper(self):
            if self.argument != "":
                return fn(self)

            raise Exception("Argument není validní!")

        return check_argument_wrapper

    def check_url_changed(fn):
        @wraps(fn)
        def check_url_wrapper(self):
            if self.is_url_new:
                self.load_web_page()

            return fn(self)

        return check_url_wrapper

    def check_url_valid(fn):
        @wraps(fn)
        def check_url_valid_wrapper(self):
            if self.is_url_valid():
                return fn(self)

            raise Exception("Url není validní!")

        return check_url_valid_wrapper

    def reset_error_message(fn):
        @wraps(fn)
        def reset_error_message_wrapper(self):
            self._error_label.setText("")
            return fn(self)

        return reset_error_message_wrapper

    def catch_exception(fn):
        @wraps(fn)
        def catch_exception_wrapper(self):
            try:
                return fn(self)
            except Exception as ex:
                self._error_label.setText(ex.__str__())

        return catch_exception_wrapper

    # -----------------
    # Initializations
    # -----------------

    def __init__(self, **kwargs):
        super(MainForm, self).__init__(**kwargs)

        # Web parser and NLP service init
        self._web_parser = WebParser()
        self._nlp_service = NLPService()
        # Init of inner properties
        self._last_url = ""

        # Window initialization
        self.setWindowTitle("Parsování a analýza webových stránek")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setMinimumWidth(1400)

        # Main widget and BoxLayout settings
        form = QtWidgets.QWidget()
        form_layout = QtWidgets.QHBoxLayout()
        form.setLayout(form_layout)
        self.setCentralWidget(form)

        left_side_layout = QtWidgets.QVBoxLayout()
        right_side_layout = QtWidgets.QVBoxLayout()

        form_layout.addLayout(left_side_layout)
        form_layout.addLayout(right_side_layout)

        # ------ Set controls ------
        web_url_layout = QtWidgets.QVBoxLayout()

        # Error label
        self._error_label = QtWidgets.QLabel("", self)
        self._error_label.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        self._error_label.setStyleSheet('color: red')
        self._error_label.setWordWrap(True)
        web_url_layout.addWidget(self._error_label)

        # Url + Argument
        url_label = QtWidgets.QLabel("Adresa webové stránky", self)
        url_label.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        web_url_layout.addWidget(url_label)

        self.url_edit = QtWidgets.QLineEdit(self)
        self.url_edit.setText("https://cs.wikipedia.org/wiki/Hlavn%C3%AD_strana")
        self.url_edit.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        web_url_layout.addWidget(self.url_edit)

        argument_label = QtWidgets.QLabel("Argument", self)
        argument_label.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        web_url_layout.addWidget(argument_label)

        self.argument_edit = QtWidgets.QLineEdit(self)
        self.argument_edit.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        web_url_layout.addWidget(self.argument_edit)

        # -- Buttons --
        buttons_layout = QtWidgets.QHBoxLayout()

        # Common functions - buttons
        common_buttons_layout = QtWidgets.QVBoxLayout()
        # common_buttons_layout.addStretch()
        common_buttons_layout.setAlignment(QtCore.Qt.AlignTop)

        common_buttons_label = QtWidgets.QLabel("Obecné funkce", self)
        common_buttons_label.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        common_buttons_layout.addWidget(common_buttons_label)

        cb_get_tags = QtWidgets.QPushButton("Vypsat tagy", self)
        cb_get_tags.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        cb_get_tags.clicked.connect(self._on_get_all_tags)
        common_buttons_layout.addWidget(cb_get_tags)

        # Web parsing - buttons
        web_parsing_layout = QtWidgets.QVBoxLayout()
        # web_parsing_layout.addStretch()
        web_parsing_layout.setAlignment(QtCore.Qt.AlignTop)

        web_parsing_label = QtWidgets.QLabel("Parsování webu", self)
        web_parsing_label.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        web_parsing_layout.addWidget(web_parsing_label)

        wp_get_all_text = QtWidgets.QPushButton("Vypsat text", self)
        wp_get_all_text.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        wp_get_all_text.clicked.connect(self._on_get_all_text)
        web_parsing_layout.addWidget(wp_get_all_text)

        wp_get_items_by_tag = QtWidgets.QPushButton("Text dle tagu", self)
        wp_get_items_by_tag.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        wp_get_items_by_tag.clicked.connect(self._on_get_items_by_tag)
        web_parsing_layout.addWidget(wp_get_items_by_tag)
        wp_get_items_by_tag_arg_lab = QtWidgets.QLabel("Argument: tag", self)
        web_parsing_layout.addWidget(wp_get_items_by_tag_arg_lab)

        wp_get_items_by_class = QtWidgets.QPushButton("Text dle třídy", self)
        wp_get_items_by_class.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        wp_get_items_by_class.clicked.connect(self._on_get_items_by_class)
        web_parsing_layout.addWidget(wp_get_items_by_class)
        wp_get_items_by_class_arg_lab = QtWidgets.QLabel("Argument: třída", self)
        web_parsing_layout.addWidget(wp_get_items_by_class_arg_lab)

        wp_get_all_links = QtWidgets.QPushButton("Získat všechny odkazy", self)
        wp_get_all_links.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        wp_get_all_links.clicked.connect(self._on_get_all_links)
        web_parsing_layout.addWidget(wp_get_all_links)

        wp_get_all_emails = QtWidgets.QPushButton("Získat všechny emaily", self)
        wp_get_all_emails.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        wp_get_all_emails.clicked.connect(self._on_get_all_emails)
        web_parsing_layout.addWidget(wp_get_all_emails)

        wp_get_all_following_links = QtWidgets.QPushButton("Získat odkazy do úrovně", self)
        wp_get_all_following_links.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        wp_get_all_following_links.clicked.connect(self._on_get_all_following_links)
        web_parsing_layout.addWidget(wp_get_all_following_links)
        wp_get_all_following_links_arg_lab = QtWidgets.QLabel("Argument: úroveň", self)
        web_parsing_layout.addWidget(wp_get_all_following_links_arg_lab)

        # Web analysis - buttons
        web_analysis_layout = QtWidgets.QVBoxLayout()
        # web_analysis_layout.addStretch()
        web_analysis_layout.setAlignment(QtCore.Qt.AlignTop)

        web_analysis_label = QtWidgets.QLabel("Analýza webu", self)
        web_analysis_label.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        web_analysis_layout.addWidget(web_analysis_label)
        web_analysis_label_arg_lab = QtWidgets.QLabel("Vstup pro všechna tlačítka: 'Výsledky'\n"
                                                      "Otevře se nové okno s NLP výsledkem", self)
        web_analysis_layout.addWidget(web_analysis_label_arg_lab)

        wa_named_entity_recognition = QtWidgets.QPushButton("Rozpoznání entit", self)
        wa_named_entity_recognition.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        wa_named_entity_recognition.clicked.connect(self._on_named_entity_recognition)
        web_analysis_layout.addWidget(wa_named_entity_recognition)

        wa_topic_modeling = QtWidgets.QPushButton("Témata", self)
        wa_topic_modeling.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        wa_topic_modeling.clicked.connect(self._on_wa_topic_modeling)
        web_analysis_layout.addWidget(wa_topic_modeling)

        wa_text_summarization = QtWidgets.QPushButton("Sumarizace textu", self)
        wa_text_summarization.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        wa_text_summarization.clicked.connect(self._on_wa_text_summarization)
        web_analysis_layout.addWidget(wa_text_summarization)

        # wa_scatter_text = QtWidgets.QPushButton("Scatter text", self)
        # wa_scatter_text.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        # wa_scatter_text.clicked.connect(self._on_wa_scatter_text)
        # web_analysis_layout.addWidget(wa_scatter_text)

        wa_textacy_button = QtWidgets.QPushButton("N Gramy", self)
        wa_textacy_button.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        wa_textacy_button.clicked.connect(self._on_wa_textacy_n_grams)
        web_analysis_layout.addWidget(wa_textacy_button)

        wa_textacy_button = QtWidgets.QPushButton("Rozpoznávání entit", self)
        wa_textacy_button.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        wa_textacy_button.clicked.connect(self._on_wa_textacy_named_entity)
        web_analysis_layout.addWidget(wa_textacy_button)

        wa_textacy_button = QtWidgets.QPushButton("Klíčová slova", self)
        wa_textacy_button.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        wa_textacy_button.clicked.connect(self._on_wa_textacy_key_terms)
        web_analysis_layout.addWidget(wa_textacy_button)

        wa_textacy_button = QtWidgets.QPushButton("Analýza dle regexu", self)
        wa_textacy_button.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        wa_textacy_button.clicked.connect(self._on_wa_textacy_pos_regex)
        web_analysis_layout.addWidget(wa_textacy_button)

        wa_textacy_button = QtWidgets.QPushButton("Termíny", self)
        wa_textacy_button.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        wa_textacy_button.clicked.connect(self._on_wa_textacy_bag_of_terms)
        web_analysis_layout.addWidget(wa_textacy_button)

        wa_textacy_word_movers = QtWidgets.QPushButton("Podobnost textu s druhým", self)
        wa_textacy_word_movers.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        wa_textacy_word_movers.clicked.connect(self._on_wa_textacy_word_movers)
        web_analysis_layout.addWidget(wa_textacy_word_movers)

        # Results
        result_layout = QtWidgets.QVBoxLayout()

        result_label = QtWidgets.QLabel("Výsledky (čistý text)", self)
        result_label.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        result_layout.addWidget(result_label)

        self.result_edit = QtWidgets.QTextEdit(self)
        self.result_edit.setFont(QtGui.QFont("Courier New", 14, QtGui.QFont.Black))
        self.result_edit.setMinimumHeight(500)
        result_layout.addWidget(self.result_edit)

        # Layout set
        buttons_layout.addStretch()
        buttons_layout.addLayout(common_buttons_layout)
        buttons_layout.addLayout(web_parsing_layout)
        buttons_layout.addLayout(web_analysis_layout)
        buttons_layout.addStretch()

        left_side_layout.addStretch()
        left_side_layout.addLayout(web_url_layout)
        left_side_layout.addLayout(buttons_layout)
        left_side_layout.addStretch()

        right_side_layout.addStretch()
        right_side_layout.addLayout(result_layout)
        right_side_layout.addStretch()

        self.show()

    def load_web_page(self):
        if self.url != "":
            self._web_parser.load_page(self.url)

    # -----------------
    # Public methods
    # -----------------

    def is_url_valid(self):
        return self._web_parser.is_url_valid(self.url)

    # -----------------
    # Properties
    # -----------------

    @property
    def url(self):
        return self.url_edit.text()

    @property
    def argument(self):
        return self.argument_edit.text()

    @property
    def result(self):
        return self.result_edit.toPlainText()

    @property
    def is_url_new(self):
        return self.url != self._last_url

    # -----------------
    # Private methods
    # -----------------

    def _set_result(self, result_text):
        self.result_edit.setText(result_text)

    # -----------------
    # Event handlers
    # -----------------

    # Common

    @catch_exception
    @reset_error_message
    @check_url_valid
    @check_url_changed
    def _on_get_all_tags(self):
        all_tags = self._web_parser.get_all_tags()
        self._set_result("\n".join(all_tags))

    # Web parsing

    @catch_exception
    @reset_error_message
    @check_url_valid
    @check_url_changed
    def _on_get_all_text(self):
        text = self._web_parser.get_all_text()
        self._set_result(text)

    @catch_exception
    @reset_error_message
    @check_url_valid
    @check_argument
    @check_url_changed
    def _on_get_items_by_tag(self):
        items_by_tag = self._web_parser.get_items_by_tag(self.argument)
        self._set_result("\n".join(items_by_tag))

    @catch_exception
    @reset_error_message
    @check_url_valid
    @check_argument
    @check_url_changed
    def _on_get_items_by_class(self):
        items_by_class = self._web_parser.get_items_by_tag(self.argument)
        self._set_result("\n".join(items_by_class))

    @catch_exception
    @reset_error_message
    @check_url_valid
    @check_url_changed
    def _on_get_all_links(self):
        links = self._web_parser.get_all_links()
        self._set_result("\n".join(links))

    @catch_exception
    @reset_error_message
    @check_url_valid
    @check_url_changed
    def _on_get_all_emails(self):
        emails = self._web_parser.get_all_emails()
        self._set_result("\n".join(emails))

    @catch_exception
    @reset_error_message
    @check_url_valid
    @check_argument
    @check_url_changed
    def _on_get_all_following_links(self):
        following_links = self._web_parser.get_all_following_links(int(self.argument))
        self._set_result("\n".join(following_links))

    # NLP

    @catch_exception
    @reset_error_message
    @check_url_valid
    @check_url_changed
    def _on_named_entity_recognition(self):
        self._nlp_service.text = self.result
        named_entities = self._nlp_service.get_named_entity_recognition()

        self.named_entity_form = NLPResultForm("\n".join([ne.__repr__() for ne in named_entities]),
                                               raw_text=self.result, header="Rozpoznání entit")
        self.named_entity_form.show()

    @catch_exception
    @reset_error_message
    @check_url_valid
    @check_url_changed
    def _on_wa_topic_modeling(self):
        self._nlp_service.text = self.result
        gensim, processed_text = self._nlp_service.get_topic_modeling_and_summarization()
        topics = [f"{topic[0]} - {topic[1]}" for topic in gensim.get_topics()]

        self.topic_modeling_form = NLPResultForm("\n".join(topics), self.result, processed_text, "Témata")
        self.topic_modeling_form.show()

    @catch_exception
    @reset_error_message
    @check_url_valid
    @check_url_changed
    def _on_wa_text_summarization(self):
        self._nlp_service.text = self.result
        gensim, processed_text = self._nlp_service.get_topic_modeling_and_summarization()
        summarization = gensim.get_summarization()

        self.text_summarization_form = NLPResultForm(summarization, self.result, processed_text, "Sumarizace textu")
        self.text_summarization_form.show()

    # @catch_exception
    # @reset_error_message
    # @check_url_valid
    # @check_url_changed
    # def _on_wa_scatter_text(self):
    #     self._nlp_service.text = self.result
    #     html = self._nlp_service.get_scatter_text_html()
    #     open("scatter_text_result.html", 'wb').write(html.encode('utf-8'))

    @catch_exception
    @reset_error_message
    @check_url_valid
    @check_url_changed
    def _on_wa_textacy_n_grams(self):
        self._nlp_service.text = self.result

        n_grams, processed_text = self._nlp_service.get_n_grams()

        self.textacy_n_grams_form = NLPResultForm(n_grams, self.result, processed_text, "N Gramy")
        self.textacy_n_grams_form.show()

    @catch_exception
    @reset_error_message
    @check_url_valid
    @check_url_changed
    def _on_wa_textacy_named_entity(self):
        self._nlp_service.text = self.result

        named_entity, processed_text = self._nlp_service.get_named_entity()

        self.textacy_named_entity_form = NLPResultForm(named_entity, self.result, processed_text, "Rozpoznávání entit")
        self.textacy_named_entity_form.show()

    @catch_exception
    @reset_error_message
    @check_url_valid
    @check_url_changed
    def _on_wa_textacy_key_terms(self):
        self._nlp_service.text = self.result

        key_terms, processed_text = self._nlp_service.get_key_terms()

        self.textacy_key_terms_form = NLPResultForm(key_terms, self.result, processed_text, "Klíčová slova")
        self.textacy_key_terms_form.show()

    @catch_exception
    @reset_error_message
    @check_url_valid
    @check_url_changed
    def _on_wa_textacy_pos_regex(self):
        self._nlp_service.text = self.result

        pos_regex, processed_text = self._nlp_service.get_pos_regex()

        self.textacy_pos_regex_form = NLPResultForm(pos_regex, self.result, processed_text, "Analýza dle regexu")
        self.textacy_pos_regex_form.show()

    @catch_exception
    @reset_error_message
    @check_url_valid
    @check_url_changed
    def _on_wa_textacy_bag_of_terms(self):
        self._nlp_service.text = self.result

        bag_of_terms, processed_text = self._nlp_service.get_bag_of_terms()

        self.textacy_bag_of_terms_form = NLPResultForm(bag_of_terms, self.result, processed_text, "Termíny")
        self.textacy_bag_of_terms_form.show()

    @catch_exception
    @reset_error_message
    @check_url_valid
    @check_url_changed
    def _on_wa_textacy_word_movers(self):
        self.textacy_word_movers_window = WordMoversForm(self._nlp_service, self.result)
        self.textacy_word_movers_window.show()
