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

    _WORD_MODEL_NAME = "en_core_web_md"

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

    # GENSIM - Topic Modeling, Text summarization

    def get_topic_modeling_and_summarization(self):
        """
        Gets an class for topic modeling and text summarization methods
        :return: Tuple with Gensim class that has methods for topic modeling and text summarization
        and processed text
        """
        text_data = self._prepare_text_for_lda()

        return Gensim(self.text, text_data), "\n".join([",".join(td) for td in text_data])

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
        # spacy_nlp = s.load(self._WORD_MODEL_NAME)
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
        :return: tuple Textacy doc, Processed text
        """
        en = textacy.load_spacy_lang(NLPService._WORD_MODEL_NAME, disable=('parser',))
        processed_text = textacy.preprocess_text(text, lowercase=True, no_punct=True)

        return textacy.make_spacy_doc(processed_text, lang=en), processed_text

    # Base Textacy analysis

    def get_n_grams(self):
        """
        Get N Grams in current text
        :return: Tuple of (Tuple of N Grams, Processed text by this method)
        """
        doc, processed_text = self.get_textacy_doc(self.text)

        return tuple([str(ngram) for ngram
                      in textacy.extract.ngrams(doc, 3, filter_stops=True,
                                                filter_punct=True, filter_nums=False)]), processed_text

    def get_named_entity(self):
        """
        Gets named entity recognition
        :return: Tuple of (Tuple of Named entities, Processed text by this method)
        """
        doc, processed_text = self.get_textacy_doc(self.text)

        return tuple([str(named_entity) for named_entity
                      in textacy.extract.entities(doc, drop_determiners=True)]), processed_text

    def get_key_terms(self):
        """
        Gets key of terms in current text
        :return: Tuple of (Tuple of Key Terms, Processed text by this method)
        """
        doc, processed_text = self.get_textacy_doc(self.text)

        return tuple([f"{textrank[0]} - {textrank[1]}" for textrank
                      in textacy.keyterms.textrank(doc, normalize='lemma', n_keyterms=10)]), processed_text

    def get_pos_regex(self):
        """
        Gets Pos Regex matches in textacy patterns in english
        :return: Tuple of (Tuple of Pos Regex matches, Processed text by this method)
        """
        doc, processed_text = self.get_textacy_doc(self.text)
        pattern = textacy.constants.POS_REGEX_PATTERNS['en']['NP']

        return tuple([str(regex_match) for regex_match
                      in textacy.extract.pos_regex_matches(doc, pattern)]) + ("\n",) +\
               tuple([f"{sgrank[0]} - {sgrank[1]}" for sgrank
                      in textacy.keyterms.sgrank(doc, ngrams=(1, 2, 3, 4), normalize='lower', n_keyterms=0.1)]),\
               processed_text

    def get_bag_of_terms(self):
        """
        Gets bag of terms in current text
        :return: Tuple of (Tuple of Terms, Processed text by this method)
        """
        doc, processed_text = self.get_textacy_doc(self.text)
        bot = doc._.to_bag_of_terms(ngrams=(1, 2, 3), named_entities=True, weighting='count', as_strings=True)

        return tuple([f"{term[0]} - {term[1]}" for term
                      in sorted(bot.items(), key=lambda x: x[1], reverse=True)[:15]]), processed_text

    @staticmethod
    def get_textacy_word_movers(text_1, text_2):
        """
        Gets textacy word movers number from comparing two texts.
        Number between 0.0 to 1.0 where 0 is no similarity and 1 full similarity.
        :param text_1: First text
        :param text_2: Second text
        :return: Returns tuple with result of word movers and both processed texts
        """
        doc_1, preprocess_text_1 = NLPService.get_textacy_doc(text_1)
        doc_2, preprocess_text_2 = NLPService.get_textacy_doc(text_2)

        word_mover = word_movers(doc_1, doc_2, metric="cosine")

        return word_mover, f"Zpracovaný text 1:\n{preprocess_text_1}\n\nZpracovaný text 2:\n{preprocess_text_2}"

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
