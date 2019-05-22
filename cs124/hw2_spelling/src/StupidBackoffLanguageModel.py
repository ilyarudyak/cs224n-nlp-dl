from collections import defaultdict
from math import log
from nltk import ngrams


class StupidBackoffLanguageModel:

    def __init__(self, corpus):
        """Initialize your data structures in the constructor."""
        self.unigramCounts = defaultdict(int)
        self.bigramCounts = defaultdict(int)
        self.trigramCounts = defaultdict(int)
        self.totalWords = 0
        self.train(corpus)

    def train(self, corpus):
        """ Takes a corpus and trains your language model.
        Compute any counts or other corpus statistics in this function.
        """
        for sentence in corpus.corpus:

            trigrams = ngrams(sentence.getCorrectSentence(), 3)
            for trigram in trigrams:
                self.bigramCounts[trigram] += 1

            bigrams = ngrams(sentence.getCorrectSentence(), 2)
            for bigram in bigrams:
                self.bigramCounts[bigram] += 1

            for datum in sentence.data:
                token = datum.word
                self.unigramCounts[token] += 1
                self.totalWords += 1

    def score(self, sentence):
        """ Takes a list of strings as argument and returns the log-probability of the
        sentence using your language model. Use whatever data you computed in train() here.
        """
        score = 0.0
        trigrams = ngrams(sentence, 3)
        for trigram in trigrams:
            wi_2, wi_1, wi = trigram
            bigram = (wi_1, wi)
            unigram = wi
            if trigram in self.trigramCounts:
                score += log(self.trigramCounts[trigram])
                score -= log(self.bigramCounts[(wi_2, wi_1)])
            elif bigram in self.bigramCounts:
                score += log(0.4)
                score += log(self.bigramCounts[bigram])
                score -= log(self.unigramCounts[wi_1])
            elif unigram in self.unigramCounts:
                score += log(0.16)
                score += log(self.unigramCounts[unigram])
                score -= log(self.totalWords)
            else:
                score += log(0.064)
                score -= log(self.totalWords)
        return score
