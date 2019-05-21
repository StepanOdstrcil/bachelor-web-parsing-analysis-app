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
from sklearn.metrics import pairwise_distances
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyemd import emd
from sklearn.manifold import MDS
import collections
from nltk.stem.wordnet import WordNetLemmatizer
from textacy.similarity import word_movers, extract, compat


class NLPService:
    """
    Class for fetching NLP results or classes that works with partial results of NLP and provides another methods
    """
    def __init__(self, text=None):
        self._text = text

    _WORD_MODEL_NAME = "en_core_web_md"
    COLORING = ('b', 'r', 'g', 'k', 'y')

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
    def get_word_movers(text_1, text_2):
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

    @staticmethod
    def show_word_movers_plot(text_1, text_2):
        """
        Show word movers matplotlib's plot.
        :param text_1: First text
        :param text_2: Second text
        """
        doc_1, _ = NLPService.get_textacy_doc(text_1)
        doc_2, _ = NLPService.get_textacy_doc(text_2)

        word_idxs = dict()
        word_vecs = []
        word_nams = []
        nums_vecs = 0

        concatenated = [extract.words(doc_1), extract.words(doc_2)]
        for document in range(len(concatenated)):
            for word in concatenated[document]:
                if word.has_vector and word_idxs.setdefault(word.orth, nums_vecs) == nums_vecs:
                    word_vecs.append(word.vector)
                    word_nams.append({'word': str(word), 'class': document})
                    nums_vecs += 1
        distance_mat = pairwise_distances(word_vecs, metric="cosine").astype(np.double)
        distance_mat /= distance_mat.max()

        # Create DataFrame
        w = [w.get('word') for w in word_nams]
        c = [w.get('class') for w in word_nams]
        df = pd.DataFrame(data=distance_mat, index=w, columns=w)

        writer = pd.ExcelWriter('output_raw_sim.xlsx')
        df.to_excel(writer, 'Sheet1')
        writer.save()

        mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
        pos = mds.fit_transform(df.values)

        xvals = pos[:, 0]
        yvals = pos[:, 1]

        classes = c if c else [0] * len(xvals)
        colors = NLPService.COLORING
        values = list(zip(xvals, yvals, classes, df.columns))

        for x, y, cls, name in values:
            plt.scatter(x, y, c=colors[cls])
            plt.text(x, y, name, fontsize=9)

        # closest = find_closest_words(values)
        closest = NLPService.find_closest_words(values, classes=classes, focused_class=0)
        for close_points in closest:
            x = [close_points[0][0], close_points[1][0]]
            y = [close_points[0][1], close_points[1][1]]
            plt.plot(x, y, 'k', alpha=0.5)
        plt.show()

    @staticmethod
    def find_closest_words(coordinates, classes=None, focused_class=None):
        if classes is not None and focused_class is not None:
            closest = []
            sources = []
            targets = []
            for i in range(len(coordinates)):
                if classes[i] == focused_class:
                    sources.append(coordinates[i])
                else:
                    targets.append(coordinates[i])

            for s in sources:
                dist = [np.linalg.norm(np.array([s[0], s[1]]) - np.array([t[0], t[1]])) for t in targets]
                dist = np.array(dist)
                if np.min(dist) == 0.0:
                    idx = np.where(dist == np.partition(dist, 2)[2])[0]
                else:
                    idx = np.argmin(dist)
                closest.append(((s[0], s[1]), (targets[idx][0], targets[idx][1])))
            return closest
        else:
            x_y_coord = [np.array([c[0], c[1]]) for c in coordinates]
            distances = pairwise_distances(x_y_coord, metric='euclidean').astype(np.double)
            indices = [np.where(row == np.partition(row, 2)[2])[0] for row in distances]
            closest = [(x_y_coord[int(i)], x_y_coord[int(indices[i])]) for i in range(len(indices))]
            return closest

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
