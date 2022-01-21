import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from textblob import TextBlob


class sentiment():
    
    def __init__(self, text: str):
        self.text = text
        self.nlp = spacy.load('en_core_web_sm')
        self.doc = self.nlp(self.text)
        

def tokenise(doc: object):
    token_list = []
    for token in doc:
        token_list.append(doc.text)
    return token_list