import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from textblob import TextBlob


class sentiment():
    
    def __init__(self, text: str):
        self.text = text
        self.nlp = spacy.load('en_core_web_sm')
        self.doc = self.nlp(self.text)
        self.tokens = self._tokenise(self.doc)
        self.filtered = self._dropwords(self.tokens)
        self.polarity = self._polarity()
        
    def _tokenise(self, doc: object):
        token_list = []
        for token in doc:
            token_list.append(doc.text)
        return token_list
    
    def _dropwords(self, tokenised_list: list):
        filtered = []
        for word in tokenised_list:
            lex = self.nlp.vocab[word]
            if lex.is_stop == False:
                filtered.append(word)
        return filtered
    
    def _polarity(self):
        string = " ".join(self.filtered)
        blob = TextBlob(string)
        
        if blob.sentiment.polarity > 0:
            sentiment = 'positive'
        elif blob.sentiment.polarity == 0:
            sentiment = 'neutral'
        elif blob.sentiment.polarity < 0:
            sentiment = 'negative'
        return sentiment