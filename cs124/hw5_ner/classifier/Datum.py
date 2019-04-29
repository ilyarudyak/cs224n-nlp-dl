class Datum:
    def __init__(self, word, label):
        self.word = word
        self.label = label
        self.guessLabel = ''
        self.previousLabel = ''
        self.features = []

    def __str__(self):
        return "Datum{" + \
               "word='" + self.word + '\'' + \
               ", label='" + self.label + '\'' + \
               ", guessLabel='" + self.guessLabel + '\'' + \
               ", previousLabel='" + self.previousLabel + '\'' + \
               '}'
