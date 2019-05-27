import sys
import getopt
import os
from math import log

from collections import defaultdict


class NaiveBayes:
    class TrainSplit:
        """Represents a set of training/testing data. self.train is a list of Examples, as is self.test.
        """

        def __init__(self):
            self.train = []
            self.test = []

    class Example:
        """Represents a document with a label. klass is 'pos' or 'neg' by convention.
       words is a list of strings.
        """

        def __init__(self):
            self.klass = ''
            self.words = []

    def __init__(self):
        """NaiveBayes initialization"""
        self.FILTER_STOP_WORDS = False
        self.stopList = set(self.readFile('../data/english.stop'))
        self.numFolds = 10

        self.vocabulary = set()

        self.docsCount = 0
        self.docsPos = 0
        self.docsNeg = 0

        self.wordsPos = defaultdict(int)
        self.wordsNeg = defaultdict(int)

        self.klassPos = 'pos'
        self.klassNeg = 'neg'

        self.priorPos = 0.0
        self.priorNeg = 0.0

        self.condProbsPos = defaultdict(float)
        self.condProbsNeg = defaultdict(float)

    #############################################################################
    # TODO TODO TODO TODO TODO

    def classify(self, words):
        """ TODO
        'words' is a list of words to classify. Return 'pos' or 'neg' classification.
        """
        posLogProb, negLogProb = log(self.priorPos), log(self.priorNeg)
        for word in words:
            posLogProb += log(self.condProbsPos[word])
            negLogProb += log(self.condProbsNeg[word])

        if posLogProb > negLogProb:
            return self.klassPos
        else:
            return self.klassNeg

    def addExample(self, klass, words):
        """
        * TODO
        * Train your model on an example document with label klass ('pos' or 'neg') and
        * words, a list of strings.
        * You should store whatever data structures you use for your classifier
        * in the NaiveBayes class.
        * Returns nothing
        """
        self.docsCount += 1
        if klass == self.klassPos:
            self.docsPos += 1
            self.addWords(words, self.wordsPos)
        else:
            self.docsNeg += 1
            self.addWords(words, self.wordsNeg)

    def addWords(self, words, textDict):
        for word in words:
            self.vocabulary.add(word)
            textDict[word] += 1

    def filterStopWords(self, words):
        """
        * TODO
        * Filters stop words found in self.stopList.
        """
        return words

    # TODO TODO TODO TODO TODO
    #############################################################################

    def readFile(self, fileName):
        """
     * Code for reading a file.  you probably don't want to modify anything here,
     * unless you don't like the way we segment files.
    """
        contents = []
        f = open(fileName)
        for line in f:
            contents.append(line)
        f.close()
        result = self.segmentWords('\n'.join(contents))
        return result

    def segmentWords(self, s):
        """
     * Splits lines on whitespace for file reading
    """
        return s.split()

    def trainSplit(self, trainDir):
        """Takes in a trainDir, returns one TrainSplit with train set."""
        split = self.TrainSplit()
        posTrainFileNames = os.listdir('%s/pos/' % trainDir)
        negTrainFileNames = os.listdir('%s/neg/' % trainDir)
        for fileName in posTrainFileNames:
            example = self.Example()
            example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
            example.klass = 'pos'
            split.train.append(example)
        for fileName in negTrainFileNames:
            example = self.Example()
            example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
            example.klass = 'neg'
            split.train.append(example)
        return split

    def train(self, split):
        for example in split.train:
            words = example.words
            if self.FILTER_STOP_WORDS:
                words = self.filterStopWords(words)
            self.addExample(example.klass, words)
        self.getPriorProbs()
        self.getCondProbs()

    def getPriorProbs(self):
        self.priorPos = float(self.docsPos) / self.docsCount
        self.priorNeg = float(self.docsNeg) / self.docsCount

    def getCondProbs(self):
        posNorm = float(sum([c for c in self.wordsPos.values()]) + len(self.vocabulary))
        negNorm = float(sum([c for c in self.wordsNeg.values()]) + len(self.vocabulary))

        for word in self.vocabulary:
            self.condProbsPos[word] = (self.wordsPos[word] + 1) / posNorm
            self.condProbsNeg[word] = (self.wordsNeg[word] + 1) / negNorm

    def crossValidationSplits(self, trainDir):
        """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
        splits = []
        posTrainFileNames = os.listdir('%s/pos/' % trainDir)
        negTrainFileNames = os.listdir('%s/neg/' % trainDir)
        # for fileName in trainFileNames:
        for fold in range(0, self.numFolds):
            split = self.TrainSplit()
            for fileName in posTrainFileNames:
                example = self.Example()
                example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                example.klass = 'pos'
                if fileName[2] == str(fold):
                    split.test.append(example)
                else:
                    split.train.append(example)
            for fileName in negTrainFileNames:
                example = self.Example()
                example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                example.klass = 'neg'
                if fileName[2] == str(fold):
                    split.test.append(example)
                else:
                    split.train.append(example)
            splits.append(split)
        return splits

    def test(self, split):
        """Returns a list of labels for split.test."""
        labels = []
        for example in split.test:
            words = example.words
            if self.FILTER_STOP_WORDS:
                words = self.filterStopWords(words)
            guess = self.classify(words)
            labels.append(guess)
        return labels

    def buildSplits(self, args):
        """Builds the splits for training/testing"""
        trainData = []
        testData = []
        splits = []
        trainDir = args[0]
        if len(args) == 1:
            print '[INFO]\tPerforming %d-fold cross-validation on data set:\t%s' % (self.numFolds, trainDir)

            posTrainFileNames = os.listdir('%s/pos/' % trainDir)
            negTrainFileNames = os.listdir('%s/neg/' % trainDir)
            for fold in range(0, self.numFolds):
                split = self.TrainSplit()
                for fileName in posTrainFileNames:
                    example = self.Example()
                    example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                    example.klass = 'pos'
                    if fileName[2] == str(fold):
                        split.test.append(example)
                    else:
                        split.train.append(example)
                for fileName in negTrainFileNames:
                    example = self.Example()
                    example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                    example.klass = 'neg'
                    if fileName[2] == str(fold):
                        split.test.append(example)
                    else:
                        split.train.append(example)
                splits.append(split)
        elif len(args) == 2:
            split = self.TrainSplit()
            testDir = args[1]
            print '[INFO]\tTraining on data set:\t%s testing on data set:\t%s' % (trainDir, testDir)
            posTrainFileNames = os.listdir('%s/pos/' % trainDir)
            negTrainFileNames = os.listdir('%s/neg/' % trainDir)
            for fileName in posTrainFileNames:
                example = self.Example()
                example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                example.klass = 'pos'
                split.train.append(example)
            for fileName in negTrainFileNames:
                example = self.Example()
                example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                example.klass = 'neg'
                split.train.append(example)

            posTestFileNames = os.listdir('%s/pos/' % testDir)
            negTestFileNames = os.listdir('%s/neg/' % testDir)
            for fileName in posTestFileNames:
                example = self.Example()
                example.words = self.readFile('%s/pos/%s' % (testDir, fileName))
                example.klass = 'pos'
                split.test.append(example)
            for fileName in negTestFileNames:
                example = self.Example()
                example.words = self.readFile('%s/neg/%s' % (testDir, fileName))
                example.klass = 'neg'
                split.test.append(example)
            splits.append(split)
        return splits


def main():
    nb = NaiveBayes()

    # default parameters: no stop word filtering, and
    # training/testing on ../data/imdb1
    if len(sys.argv) < 2:
        options = [('', '')]
        args = ['../data/imdb1/']
    else:
        (options, args) = getopt.getopt(sys.argv[1:], 'f')
    if ('-f', '') in options:
        nb.FILTER_STOP_WORDS = True

    splits = nb.buildSplits(args)
    avgAccuracy = 0.0
    fold = 0
    for split in splits:
        classifier = NaiveBayes()
        accuracy = 0.0
        for example in split.train:
            words = example.words
            if nb.FILTER_STOP_WORDS:
                words = classifier.filterStopWords(words)
            classifier.addExample(example.klass, words)

        for example in split.test:
            words = example.words
            if nb.FILTER_STOP_WORDS:
                words = classifier.filterStopWords(words)
            guess = classifier.classify(words)
            if example.klass == guess:
                accuracy += 1.0

        accuracy = accuracy / len(split.test)
        avgAccuracy += accuracy
        print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy)
        fold += 1
    avgAccuracy = avgAccuracy / fold
    print '[INFO]\tAccuracy: %f' % avgAccuracy


if __name__ == "__main__":
    main()
