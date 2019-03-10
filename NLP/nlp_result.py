import gensim


class NamedEntity:
    """
    Class that encapsulate named entity recognition result
    """
    def __init__(self, label, text):
        self._label = label
        self._text = text

    def __repr__(self):
        return f"{self._label} - {self._text}"

    def __hash__(self):
        return self.__repr__().__hash__()

    def __eq__(self, other):
        if type(other) != NamedEntity:
            return False

        return self.__hash__() == other.__hash__()


class Gensim:
    """
    Class for working with text for Topic modeling and Text summarization
    """
    def __init__(self, text, text_data):
        self._text = text
        self._text_data_dictionary = gensim.corpora.Dictionary(text_data)
        self._corpus = [self._text_data_dictionary.doc2bow(text) for text in text_data]

    def get_topics(self, number_topic=5, number_words=4):
        """
        Gets topics of text
        :param number_topic: Number of topic
        :param number_words: Number of words in result
        :return: Topic modeling
        """
        lda_model = gensim.models.ldamodel.LdaModel(self._corpus, num_topics=number_topic,
                                                    id2word=self._text_data_dictionary, passes=15)
        lda_model.save('model5.gensim')

        return lda_model.print_topics(num_words=number_words)

    def get_summarization(self):
        """
        Gets text summarization
        :return: Summarized text
        """
        return gensim.summarization.summarize(self._text)
