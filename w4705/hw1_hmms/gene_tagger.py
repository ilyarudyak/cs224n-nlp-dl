from count_freqs import Hmm
from collections import defaultdict
import utils


class HmmTagger(object):
    def __init__(self):
        self.hmm = Hmm()
        self.word_count = defaultdict(int)
        self.rare_words = defaultdict(int)
        self.emission_params = defaultdict(int)

    def get_word_count(self, filename):
        self.hmm.train(file(filename))
        for (word, _), count in self.hmm.emission_counts.items():
            self.word_count[word] += count

    def get_rare_words(self):
        for word, count in self.word_count.items():
            if count < utils.RARE_WORD_THRESHOLD:
                self.rare_words[word] = count

    def write_rare_words(self):
        with open(utils.TRAIN_FILE) as in_f:
            with open(utils.TRAIN_FILE_RARE, 'w') as out_f:
                for line in in_f:
                    if line == '\n':
                        out_f.write(line)
                    else:
                        word, tag = line.strip().split()
                        if word in self.rare_words:
                            word = utils.RARE_WORD_SYMBOL
                        out_f.write(utils.format_train_string(word, tag))

    def get_emission_params(self, filename):
        self.hmm.train(file(filename))
        unigrams = self.hmm.ngram_counts[0]
        # print unigrams
        for (word, tag), count in self.hmm.emission_counts.items():
            self.emission_params[(word, tag)] = float(count) / unigrams[(tag,)]

    def write_simple_tag(self):
        """
        - read gene.dev.no.key line by line
        - produce tag for word (see below)
        - write word and tag in file gene.dev.p1.out

        - to produce tag we use argmax e(x|y) over y;
          in other words we compare emission params for 2 possible tags
          and choose tag with the bigger value;
        - if this word is not in train set or it's in rare words set (from train set, NOT dev set)
          we use emission params for _RARE_;
        """
        self.get_word_count(utils.TRAIN_FILE)
        self.get_rare_words()

        self.get_emission_params(utils.TRAIN_FILE_RARE)

        with open(utils.DEV_FILE_NO_KEY) as in_f:
            with open(utils.DEV_FILE_OUT, 'w') as out_f:
                for line in in_f:
                    if line == '\n':
                        out_f.write(line)
                    else:
                        word = line.strip()
                        tag = self.get_simple_tag(word)
                        out_f.write(utils.format_train_string(word, tag))

    def get_simple_tag(self, word):
        if (word not in self.word_count) or (word in self.rare_words):
            tag = utils.O_TAG
        else:
            i_gene_emission = self.emission_params[(word, utils.I_GENE_TAG)]
            o_emission = self.emission_params[(word, utils.O_TAG)]
            if o_emission < i_gene_emission:
                tag = utils.I_GENE_TAG
            else:
                tag = utils.O_TAG
        return tag


if __name__ == '__main__':
    tagger = HmmTagger()

    # write rare words in the file
    # hmm.get_word_count(utils.TRAIN_FILE)
    # hmm.write_rare_words()

    # write output of simple tagger
    tagger.write_simple_tag()
