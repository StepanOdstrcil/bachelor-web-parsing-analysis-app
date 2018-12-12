class NamedEntity:
    """
    Class that encapsulate named entity recognition result
    """
    def __init__(self, label, text):
        self._label = label
        self._text = text

    def __repr__(self):
        return f"{self._label} - {self._text}"


class Gensim:
    """
    Class for working with text for Topic modeling and Text summarization
    """
    def __init__(self, text_data_dictionary, corpus, LdaModel, summarize_corpus):
        self._text_data_dictionary = text_data_dictionary
        self._corpus = corpus
        self._LdaModel = LdaModel
        self._summarize_corpus = summarize_corpus

    def get_topics(self, number_topic=5, number_words=4):
        """
        Gets topics of text
        :param number_topic: Number of topic
        :param number_words: Number of words in result
        :return: Topic modeling
        """
        lda_model = self._LdaModel(self._corpus, num_topics=number_topic,
                                   id2word=self._text_data_dictionary, passes=15)
        lda_model.save('model5.gensim')

        return lda_model.print_topics(num_words=number_words)

    def get_summarization(self):
        """
        Gets text summarization
        :return: Summarized text
        """
        return self._summarize_corpus(self._corpus)
