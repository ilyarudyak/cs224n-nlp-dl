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

        intersection = trueEntities.intersection(guessEntities)
        tp = len(intersection)

        prec = float(tp) / len(guessEntities)
        recall = float(tp) / len(trueEntities)
        f = (2 * prec * recall) / (prec + recall)

        return prec, recall, f

    @staticmethod
    def readFile(in_file):
        data = []
        with open(in_file) as in_f:
            f_tsv = csv.reader(in_f, delimiter='\t', escapechar='\\')
            for row in f_tsv:
                # counter += 1
                try:
                    word, label, guessLabel = row
                    datum = Datum(word, label)
                    datum.guessLabel = guessLabel
                    data.append(datum)
                except:
                    print row
        return data


if __name__ == '__main__':
    in_file = 'debug_esc.txt'
    data = Scorer.readFile(in_file)
    print Scorer.score(data)

