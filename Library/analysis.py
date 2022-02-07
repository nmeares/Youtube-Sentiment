import spacy
import pandas as pd
from spacy.lang.en.stop_words import STOP_WORDS
from textblob import TextBlob

# TODO: improve scalability (async / multithreading)


class sentiment():
    '''Sentiment Analysis Object
    '''
    # TODO: check if instance is series and if so then used vectorised functions and apply

    def __init__(self, text):
        self.text = text
        self.nlp = spacy.load('en_core_web_sm')
        if isinstance(self.text, (str, list)):
            self.text_list = [self.text] if not isinstance(self.text, list) else self.text
            self.docs = [self.nlp(text) for text in self.text_list]
            self.tokens = [self._tokenise(doc) for doc in self.docs]
        # Allow for faster vectorisation if a pandas series is passed
        elif isinstance(self.text, pd.Series):
            self.tokens = self.text.str.split().astype(str)
        else:
            raise TypeError("Object only supports str, list or pd.Series!")

    def _tokenise(self, string: str) -> list:  # TODO: use str.split if pd.series
        token_list = []
        for token in string:
            token_list.append(token.text)
        return token_list

    def _dropwords(self, tokens: list) -> list:
        dropped = []
        for word in tokens:
            lex = self.nlp.vocab[word]
            if lex.is_stop == False:
                dropped.append(word)
        return dropped

    def _polarity(self, nlp_text) -> int:
        string = " ".join(self._dropwords(nlp_text))
        blob = TextBlob(string)

        if blob.sentiment.polarity > 0:
            sentiment = 1
        elif blob.sentiment.polarity == 0:
            sentiment = 0
        elif blob.sentiment.polarity < 0:
            sentiment = -1
        return sentiment

    def polarity(self) -> list:
        '''Generate polarity from text

        1 : Positive sentiment
        0 : Neutral sentiment
        -1 : Negative sentiment

        Returns
        -------
        list
            List of polarity integers
        '''
        if isinstance(self.tokens, list):
            result = map(self._polarity, self.tokens)
        elif isinstance(self.tokens, pd.Series):
            result = self.tokens.apply(self._polarity)
        return list(result)
