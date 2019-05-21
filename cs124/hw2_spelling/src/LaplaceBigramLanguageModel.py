from collections import defaultdict
from math import log
from nltk import ngrams


class LaplaceBigramLanguageModel:

    def __init__(self, corpus):
        """Initialize your data structures in the constructor."""
        self.unigramCounts = defaultdict(int)
        self.bigramCounts = defaultdict(int)
        self.train(corpus)
        self.uniqueBigrams = len(self.bigramCounts)

    def train(self, corpus):
        """ Takes a corpus and trains your language model.
        Compute any counts or other corpus statistics in this function.
        """
        for sentence in corpus.corpus:

          bigrams = ngrams(sentence.getCorrectSentence(), 2)
          for bigram in bigrams:
            self.bigramCounts[bigram] += 1

          for datum in sentence.data:
            token = datum.word
            self.unigramCounts[token] = self.unigramCounts[token] + 1

    def score(self, sentence):
        """ Takes a list of strings as argument and returns the log-probability of the
        sentence using your language model. Use whatever data you computed in train() here.
        """
        score = 0.0
        bigrams = ngrams(sentence, 2)
        for bigram in bigrams:
          score += log(self.bigramCounts[bigram] + 1)
          score -= log(self.unigramCounts[bigram[0]] + self.uniqueBigrams)
        return score
