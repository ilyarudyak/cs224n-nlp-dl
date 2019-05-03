TRAIN_FILE = 'data/gene.train'
TRAIN_FILE_RARE = 'data/gene.train.rare'
DEV_FILE_NO_KEY = 'data/gene.dev.no.key'
DEV_FILE_OUT = 'data/gene.dev.p1.out'

RARE_WORD_THRESHOLD = 5
RARE_WORD_SYMBOL = '_RARE_'

I_GENE_TAG = 'I-GENE'
O_TAG = 'O'

# unigram count in gene.train.rare
# defaultdict(<type 'int'>, {('I-GENE',): 41072, ('O',): 345128})
UNIGRAM_COUNT_GENE = 41072
UNIGRAM_COUNT_O = 345128


def format_train_string(word, tag):
    return '{} {}\n'.format(word, tag)
