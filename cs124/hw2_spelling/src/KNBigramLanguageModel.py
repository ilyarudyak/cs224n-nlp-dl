from collections import defaultdict
from math import log
from nltk import ngrams


class KNBigramLanguageModel:
    """
    Kneser-Ney smoothing for bigrams.
    This class DOES NOT pre compute all probabilities.
    """

    def __init__(self, corpus):
        """Initialize your data structures in the constructor."""
        self.d = .75

        self.unigramCounts = defaultdict(int)
        self.bigramCounts = defaultdict(int)
        self.trigramCounts = defaultdict(int)
        self.getNgramCounts(corpus)

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

    def getFirstTerm(self, bigram):
        wi_1, wi = bigram
        if wi_1 in self.unigramCounts:
            return max(self.bigramCounts[(wi_1, wi)] - self.d, 0) / self.unigramCounts[wi_1]
        else:
            return 0

    def getLambda(self, wi_1):
        count = [self.bigramCounts[(wi_1, w)] for w in self. unigramCounts if self.bigramCounts[(wi_1, w)] > 0]
        if count:
            return self.d * len(count) / sum(count)
        else:
            return 0

    def getContProb(self, wi):
        count = [w for w in self. unigramCounts if self.bigramCounts[(w, wi)] > 0]
        count2 = [bigram for bigram in self.bigramCounts if self.bigramCounts[bigram] > 0]
        return len(count) / len(count2)

    def score(self, sentence):
        """ Takes a list of strings as argument and returns the log-probability of the
        sentence using your language model. Use whatever data you computed in train() here.
        """
        score = 0.0
        bigrams = ngrams(sentence, 2)
        for bigram in bigrams:
            wi_1, wi = bigram
            t1, lambd, p_cont = self.getFirstTerm(bigram), self.getLambda(wi_1), self.getContProb(wi)
            prob = t1 + lambd * p_cont
            if prob:
                score += log(prob)
            else:
                score -= log(len(self.unigramCounts))
        return score
