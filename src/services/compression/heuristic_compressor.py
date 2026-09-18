import string
import copy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import SnowballStemmer

from src.models.chat_models import Source
from src.services.compression.identity_compressor import IdentityCompressor

class HeuristicCompressor(IdentityCompressor):

    def __init__(self):
        self.snowball_stemmer = SnowballStemmer(language='german')
        self.stopwords = set(stopwords.words('german'))

    def _create_set(self, text: str) -> set[str]:
        # tokenize
        tokens = word_tokenize(text, language='german')

        # normalize
        tokens = [t.lower() for t in tokens if t not in string.punctuation]

        # stopword removal
        tokens = set(tokens).difference(self.stopwords)

        # stemming
        tokens = set([self.snowball_stemmer.stem(t) for t in tokens])

        return tokens


    def compress(self, query: str, context: list[Source]) -> list[Source]:

        compressed_context = copy.deepcopy(context)

        query_set = self._create_set(query)

        for c in compressed_context:
            selected_sents = []

            for sentence in sent_tokenize(c.document, language="german"):
                sent_set = self._create_set(sentence)
                intersection = query_set.intersection(sent_set)

                if len(intersection) > 0:
                    selected_sents.append(sentence)

            if selected_sents:
                c.document = " ".join(selected_sents)

        return compressed_context
