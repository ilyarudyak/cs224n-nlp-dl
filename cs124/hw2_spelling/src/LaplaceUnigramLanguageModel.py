from collections import defaultdict
from math import log


class LaplaceUnigramLanguageModel:

    def __init__(self, corpus):
        """Initialize your data structures in the constructor."""
        self.unigramCounts = defaultdict(int)
        self.totalWords = 0
        self.train(corpus)
        self.uniqueWords = len(self.unigramCounts)

    def train(self, corpus):
        """ Takes a corpus and trains your language model.
        Compute any counts or other corpus statistics in this function.
        """
        for sentence in corpus.corpus:
            for datum in sentence.data:
                token = datum.word
                self.unigramCounts[token] = self.unigramCounts[token] + 1
                self.totalWords += 1

    def score(self, sentence):
        """ Takes a list of strings as argument and returns the log-probability of the
        sentence using your language model. Use whatever data you computed in train() here.
        """
        score = 0.0
        for token in sentence:
            count = self.unigramCounts[token]
            score += log(count + 1)
            score -= log(self.totalWords + self.uniqueWords)
        return score
