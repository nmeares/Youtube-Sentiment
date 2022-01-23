import asyncio
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from textblob import TextBlob


class sentiment():
    
    def __init__(self, text:list):
        self.text_list = [text] if not isinstance(text, list) else text
        self.nlp = spacy.load('en_core_web_sm')
        self.docs = [self.nlp(text) for text in self.text_list]
        
    async def _tokenise(self, string: str):
        token_list = []
        for token in string:
            token_list.append(token.text)
        return token_list
    
    async def _dropwords(self, tokens: list):
        dropped = []
        for word in tokens:
            lex = self.nlp.vocab[word]
            if lex.is_stop == False:
                dropped.append(word)
        return dropped
    
    async def _filtered(self, nlp_text):
        tokens = self._tokenise(nlp_text)
        return self._dropwords(tokens)
    
    async def _polarity(self, nlp_text):
        string = " ".join(self._filtered(nlp_text))
        blob = await TextBlob(string)
        
        if blob.sentiment.polarity > 0:
            sentiment = 'positive'
        elif blob.sentiment.polarity == 0:
            sentiment = 'neutral'
        elif blob.sentiment.polarity < 0:
            sentiment = 'negative'
        return sentiment
    
    async def _async_polarity(self):
        
        return await asyncio.gather(map(self._polarity, self.docs))
    
    async def polarity(self):
        return asyncio.run(await self._async_polarity())