from collections import defaultdict
from math import log
from nltk import ngrams


class CustomLanguageModel:
    """
    Kneser-Ney smoothing for bigrams.
    """

    def __init__(self, corpus):
        """Initialize your data structures in the constructor."""
        self.d = .75

        self.unigramCounts = defaultdict(int)
        self.bigramCounts = defaultdict(int)
        self.trigramCounts = defaultdict(int)
        self.getNgramCounts(corpus)

        self.contProbs = defaultdict(int)
        self.getContProbs()

        self.lambdas = defaultdict(int)
        self.getLambdas()

        self.knProbs = defaultdict(int)
        self.getKnProbs()

    def getNgramCounts(self, corpus):
        """ Takes a corpus and trains your language model.
        Compute any counts or other corpus statistics in this function.
        """
        for sentence in corpus.corpus:

            correctSentence = sentence.getCorrectSentence()

            trigrams = ngrams(correctSentence, 3)
            for trigram in trigrams:
                self.trigramCounts[trigram] += 1

            bigrams = ngrams(correctSentence, 2)
            for bigram in bigrams:
                self.bigramCounts[bigram] += 1

            unigrams = ngrams(correctSentence, 1)
            for unigram in unigrams:
                self.unigramCounts[unigram[0]] += 1

    def showUnigramCounts(self, ngramCounts, n):
        sortedNgrams = sorted(list(ngramCounts.items()), reverse=True, key=lambda x: x[1])
        return sortedNgrams[0:n]

    def getContProbs(self):
        for w, _ in self.bigramCounts:
            for w0, w1 in self.bigramCounts:
                if w == w1:
                    self.contProbs[w] += 1

            self.contProbs[w] *= self.d / len(self.bigramCounts)

    def getLambdas(self):
        for w, _ in self.bigramCounts:
            count = 0.0
            for w0, w1 in self.bigramCounts:
                if w == w0:
                    count += self.bigramCounts[(w0, w1)]
                    self.lambdas[w] += 1
            self.lambdas[w] /= count

    def getKnProbs(self):
        for bigram in self.bigramCounts:
            wi_1, wi = bigram
            self.knProbs[bigram] += max(self.bigramCounts[bigram] - self.d, 0) / self.unigramCounts[wi_1]
            self.knProbs[bigram] += self.lambdas[wi_1] * self.contProbs[wi]

    def score(self, sentence):
        """ Takes a list of strings as argument and returns the log-probability of the
        sentence using your language model. Use whatever data you computed in train() here.
        """
        score = 0.0
        bigrams = ngrams(sentence, 2)
        for bigram in bigrams:
            if bigram in self.bigramCounts:
                score += log(self.knProbs[bigram])
            else:
                score -= log(len(self.bigramCounts))
        return score
