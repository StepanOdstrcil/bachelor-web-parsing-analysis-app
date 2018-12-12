# Basic libraries

# App libraries
from .nlp_result import *
# Third-party libraries
import spacy as s
import gensim
from spacy.lang.en import English
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer


class NLPService:
    """
    Class for fetching NLP results or classes that works with partial results of NLP and provides another methods
    """
    def __init__(self, text=None):
        self._text = text

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
        spacy_nlp = s.load("en_core_web_sm")
        spacy_doc = spacy_nlp(self._text)
        return tuple([NamedEntity(entity.label_, entity.text) for entity in spacy_doc.ents])

    # GENSIM - Topic Modeling, Text summarization

    def get_topic_modeling_and_summarization(self):
        """
        Gets an class for topic modeling and text summarization methods
        :return: Gensim class that has methods for topic modeling and text summarization
        """
        text_data = self._prepare_text_for_lda()

        text_data_dictionary = gensim.corpora.Dictionary(text_data)
        corpus = [text_data_dictionary.doc2bow(text) for text in text_data]

        return Gensim(text_data_dictionary, corpus,
                      gensim.models.ldamodel.LdaModel, gensim.summarization.summarize_corpus)

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

    # def _get_word_root(self, word):
    #     return WordNetLemmatizer().lemmatize(word)
