import copy
import string
import logging

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.metrics import jaccard_distance

from models.chat_models import Source
from services.ranking.identity_ranker import IdentityRanker

logger = logging.getLogger(__name__)


class HeuristicRanker(IdentityRanker):

    MIN_LENGTH = 150
    MAX_LENGTH = 800

    def __init__(self, query: str, context: list[Source]):
        logger.info("Using heuristic reranking.")
        self.snowball_stemmer = SnowballStemmer(language='german')

        super().__init__(query, context)
    

    def rank(self) -> list[Source]:
        ranked_context = copy.deepcopy(self.context)

        for c in ranked_context:
            logger.debug("=============================")
            logger.debug("old score: " + str(c.score))

            c.score = (
                0.75 * self._get_retrival_score(c)
                + 0.20 * self._get_query_term_overlap(c)
                + 0.05 * self._get_length_score(c)
                - 0.10 * self._get_duplicate_penalty(c)
            )

            logger.debug("new score: " + str(c.score))
        
        ranked_context.sort(key=lambda source: source.score, reverse=True)
        return ranked_context
    

    def _get_retrival_score(self, source: Source) -> float:
        logger.debug("retrival score: " + str(source.score))
        return source.score
    
    
    def _get_query_term_overlap(self, source: Source) -> float:
        def create_set(text: set) -> set[str]:
            # tokenize
            tokens = word_tokenize(text, language='german')

            # normalize
            tokens = [t.lower() for t in tokens if t not in string.punctuation]

            # stopword removal
            tokens = set(tokens).difference(set(stopwords.words('german')))

            # stemming
            tokens = set([self.snowball_stemmer.stem(t) for t in tokens])

            return tokens

        query_set = create_set(self.query)
        source_set = create_set(source.document)
        
        overlap_set = query_set.intersection(source_set)

        overlap_score = len(overlap_set) / len(query_set)

        logger.debug("overlap score: " + str(overlap_score))
        return overlap_score


    def _get_length_score(self, source: Source) -> float:
        length = len(source.document)
        length_score = 1.0

        if length < HeuristicRanker.MIN_LENGTH:
            length_score = length / HeuristicRanker.MIN_LENGTH

        if length > HeuristicRanker.MAX_LENGTH:
            length_score = max(0.0, 1.0 - ((length - HeuristicRanker.MAX_LENGTH) / HeuristicRanker.MAX_LENGTH))

        logger.debug("length score: " + str(length_score))
        return length_score


    def _get_duplicate_penalty(self, source: Source) -> float:
        max_similarity = 0.0

        for other in self.context:
            if other.document == source.document:
                continue

            other_set = set(word_tokenize(other.document))
            source_set = set(word_tokenize(source.document))

            j_dist = jaccard_distance(other_set, source_set)
            similarity = 1 - j_dist
            max_similarity = max(max_similarity, similarity)

        logger.debug("duplicate penalty: " + str(max_similarity))
        return max_similarity