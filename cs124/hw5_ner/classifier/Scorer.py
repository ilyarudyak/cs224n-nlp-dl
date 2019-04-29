import csv
from Datum import Datum

class Scorer(object):

    @staticmethod
    def score(data):

        trueEntities = set()
        guessEntities = set()

        prevLabel = 'O'
        start = 0
        for i in range(len(data)):
            label = data[i].label
            if label == 'PERSON' and prevLabel == 'O':
                start = i
            elif label == 'O' and prevLabel == 'PERSON':
                trueEntities.add((start, i))
            prevLabel = label

        prevLabel = 'O'
        for i in range(len(data)):
            label = data[i].guessLabel
            if label == 'PERSON' and prevLabel == 'O':
                start = i
            elif label == 'O' and prevLabel == 'PERSON':
                guessEntities.add((start, i))
            prevLabel = label

        print trueEntities, guessEntities

        intersection = trueEntities.intersection(guessEntities)
        tp = len(intersection)

        prec = float(tp) / len(guessEntities)
        recall = float(tp) / len(trueEntities)
        f = (2 * prec * recall) / (prec + recall)

        return prec, recall, f

    @staticmethod
    def readFile(in_file):
        data, prevLabel = [], ''
        with open(in_file) as in_f:
            f_tsv = csv.reader(in_f, delimiter='\t', escapechar='\\')
            for row in f_tsv:
                # counter += 1
                try:
                    word, label, guessLabel = row
                    datum = Datum(word, label)
                    datum.guessLabel = guessLabel
                    datum.previousLabel = prevLabel
                    prevLabel = label
                    data.append(datum)
                except:
                    print row
        return data

    @staticmethod
    def analyzeData(data):
        """
        error1
        PERSON O
        PERSON O

        error2
        PERSON O
        PERSON PERSON

        error3
        PERSON PERSON
        PERSON O
        """
        count_error1, count_error2, count_error3 = 0, 0, 0
        datum_prev = data[0]
        for i in range(1, len(data)):
            datum = data[i]
            if datum_prev.label == 'PERSON' and datum_prev.guessLabel == 'O' and \
                    datum.label == 'PERSON' and datum.guessLabel == 'O':
                count_error1 += 1
            elif datum_prev.label == 'PERSON' and datum_prev.guessLabel == 'O' and \
                    datum.label == 'PERSON' and datum.guessLabel == 'PERSON':
                count_error2 += 1
            elif datum_prev.label == 'PERSON' and datum_prev.guessLabel == 'PERSON' and \
                    datum.label == 'PERSON' and datum.guessLabel == 'O':
                count_error3 += 1
            datum_prev = datum

        print count_error1, count_error2, count_error3

    @staticmethod
    def printData(data, n):
        for datum in data[:n]:
            print datum


if __name__ == '__main__':
    in_file = 'debug_small.txt'
    data = Scorer.readFile(in_file)
    print Scorer.score(data)