import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from textblob import TextBlob

# TODO: improve scalability (async / multithreading)
class sentiment():
    '''Sentiment Analysis Object
    '''

    def __init__(self, text: list):
        self.text_list = [text] if not isinstance(text, list) else text
        self.nlp = spacy.load('en_core_web_sm')
        self.docs = [self.nlp(text) for text in self.text_list]

    def _tokenise(self, string: str) -> list:
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

    def _filtered(self, nlp_text) -> list:
        tokens = self._tokenise(nlp_text)
        return self._dropwords(tokens)

    def _polarity(self, nlp_text) -> int:
        string = " ".join(self._filtered(nlp_text))
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
        result = map(self._polarity, self.docs)
        return list(result)
