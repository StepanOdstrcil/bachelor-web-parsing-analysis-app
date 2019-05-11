# Basic libraries

# App libraries
from .nlp_result import *
# Third-party libraries
import spacy as s
import gensim
from spacy.lang.en import English
import nltk
from nltk.corpus import wordnet as wn
import scattertext as st
import textacy
import textacy.keyterms
from nltk.stem.wordnet import WordNetLemmatizer
from textacy.similarity import word_movers


class NLPService:
    """
    Class for fetching NLP results or classes that works with partial results of NLP and provides another methods
    """
    def __init__(self, text=None):
        self._text = text

    _WORD_MODEL_NAME = "en_core_web_sm"  # en_core_web_md

    # -----------------
    # Properties
    # -----------------

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    # -----------------
    # Public methods
    # -----------------

    # SPACY - Named Entity Recognition

    def get_named_entity_recognition(self):
        """
        Gets named entity recognition in tuple
        :return: Tuple filled with SpacyEntity class that has 'label' and its 'text'
        """
        spacy_nlp = s.load(self._WORD_MODEL_NAME)
        spacy_doc = spacy_nlp(self._text)
        return tuple(set([NamedEntity(entity.label_, entity.text)
                          for entity in spacy_doc.ents
                          if entity.label_ != "GPE"]))

    def get_scatter_text_html(self):
        """
        Gets scatter text html used for visualization
        :return: Html text used for visualisation
        """
        spacy_nlp = s.load(self._WORD_MODEL_NAME)
        # convention_df = st.SampleCorpora.ConventionData2012.get_data()
        # corpus = st.CorpusFromPandas(convention_df, category_col='party', text_col='text', nlp=spacy_nlp).build()
        # return st.produce_scattertext_explorer(corpus, category='democrat', category_name='Democratic',
        #                                        not_category_name='Republican', width_in_pixels=1000,
        #                                        metadata=convention_df['speaker'])
        return "TODO"

    @staticmethod
    def get_textacy_doc(text):
        """
        Gets document of textacy library
        :param text: Text of which textacy doc to get
        :return: Textacy doc
        """
        en = textacy.load_spacy(NLPService._WORD_MODEL_NAME, disable=('parser',))
        processed_text = textacy.preprocess_text(text, lowercase=True, no_punct=True)

        return textacy.Doc(processed_text, lang=en)

    def get_textacy_analysis(self):
        """
        Gets basic textacy analysis from textacy doc
        :return: String full of analysis from textacy doc
        """
        doc = self.get_textacy_doc(self.text)

        section_delimeter = "------\n"
        result_text = []

        result_text.append("N Grams")
        result_text.append(", ".join([str(ngram) for ngram in textacy.extract.ngrams(doc, 3, filter_stops=True,
                                                                                     filter_punct=True,
                                                                                     filter_nums=False)]))
        result_text.append(section_delimeter)

        result_text.append("Named entities")
        result_text.append(", ".join([str(named_entity) for named_entity
                                      in textacy.extract.named_entities(doc, drop_determiners=True)]))
        result_text.append(section_delimeter)

        result_text.append("Pos regex matches")
        pattern = textacy.constants.POS_REGEX_PATTERNS['en']['NP']
        result_text.append(", ".join([str(regex_match) for regex_match
                                      in textacy.extract.pos_regex_matches(doc, pattern)]))
        result_text.append(section_delimeter)

        result_text.append("Key terms")
        result_text.append("\n".join([f"{textrank[0]} - {textrank[1]}" for textrank
                                      in textacy.keyterms.textrank(doc, normalize='lemma', n_keyterms=10)]))
        result_text.append("\n")
        result_text.append("\n".join([f"{sgrank[0]} - {sgrank[1]}" for sgrank
                                      in textacy.keyterms.sgrank(doc, ngrams=(1, 2, 3, 4),
                                                                 normalize='lower', n_keyterms=0.1)]))
        result_text.append(section_delimeter)

        # print("Basic counts and various readability statistics")
        # result_text.append("Basic counts and various readability statistics")
        # ts = textacy.TextStats(doc)
        # result_text.append(f"Unique words: {ts.n_unique_words}\n"
        #                    f"Basic counts: {ts.basic_counts}\n"
        #                    f"Readability stats: {ts.readability_stats}")
        # result_text.append(section_delimeter)

        result_text.append("Bag of terms")
        bot = doc.to_bag_of_terms(ngrams=(1, 2, 3), named_entities=True, weighting='count', as_strings=True)
        result_text.append("\n".join([f"{term[0]} - {term[1]}" for term
                                      in sorted(bot.items(), key=lambda x: x[1], reverse=True)[:15]]))
        result_text.append(section_delimeter)

        return "\n".join(result_text)

    @staticmethod
    def get_textacy_word_movers(text_1, text_2):
        doc_1 = NLPService.get_textacy_doc(text_1)
        doc_2 = NLPService.get_textacy_doc(text_2)

        word_mover = word_movers(doc_1, doc_2, metric="cosine")

        return word_mover

    # GENSIM - Topic Modeling, Text summarization

    def get_topic_modeling_and_summarization(self):
        """
        Gets an class for topic modeling and text summarization methods
        :return: Gensim class that has methods for topic modeling and text summarization
        """
        text_data = self._prepare_text_for_lda()

        return Gensim(self.text, text_data)

    # -----------------
    # Private methods
    # -----------------

    def _prepare_text_for_lda(self):
        """
        Prepares text for Latent Dirichlet Allocation
        :return: Tokens of the previously defined text
        """
        nltk.download('stopwords')
        stop_words = set(nltk.corpus.stopwords.words('english'))

        nltk.download('wordnet')
        tokens = self._tokenize()
        tokens = [token for token in tokens if len(token) > 4]
        tokens = [token for token in tokens if token not in stop_words]
        tokens = [self._get_lemma(token) for token in tokens]

        # Divide tokens for individual lists into one list
        number_parts = int(len(tokens) / 10)
        token_list = []
        for i in range(0, len(tokens) + 1, number_parts):
            token_list.append(tokens[i:i + number_parts])
        if len(tokens) % 10:
            token_list.append(tokens[number_parts * 10:])

        return token_list

    def _tokenize(self):
        """
        Create Latent Dirichlet Allocation tokens
        :return: List of tokens of Latent Dirichlet Allocation
        """
        parser = English()
        tokens = parser(self.text)

        lda_tokens = []
        for token in tokens:
            if token.orth_.isspace():
                continue
            elif token.like_url:
                lda_tokens.append("URL")
            elif token.orth_.startswith("@"):
                lda_tokens.append("SCREEN_NAME")
            else:
                lda_tokens.append(token.lower_)
        return lda_tokens

    @staticmethod
    def _get_lemma(word):
        """
        Gets meaning of word.
        Don't forget to use "nltk.download('wordnet')" before using this method
        :param word: Word of which meaning to get
        :return: Meaning of the word
        """
        lemma = wn.morphy(word)
        if lemma is None:
            return word
        else:
            return lemma
