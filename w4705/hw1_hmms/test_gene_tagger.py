import unittest
from gene_tagger import HmmTagger
import utils


class TestGeneTagger(unittest.TestCase):

    def setUp(self):
        self.tagger = HmmTagger()

    def test_get_word_count(self):
        self.tagger.get_word_count(utils.TRAIN_FILE)

        self.assertEqual(208, self.tagger.word_count['mouse'])
        self.assertEqual(207, self.tagger.word_count['rat'])
        self.assertEqual(173, self.tagger.word_count['rats'])

        self.assertEqual(4, self.tagger.word_count['extracorporeal'])
        self.assertEqual(3, self.tagger.word_count['Beta'])
        self.assertEqual(2, self.tagger.word_count['nucleotidase'])

    def test_get_rare_words(self):
        self.tagger.get_word_count(utils.TRAIN_FILE)
        self.tagger.get_rare_words()

        self.assertTrue('extracorporeal' in self.tagger.rare_words)
        self.assertTrue('Beta' in self.tagger.rare_words)
        self.assertTrue('nucleotidase' in self.tagger.rare_words)

    def test_get_emission_params(self):
        self.tagger.get_emission_params(utils.TRAIN_FILE_RARE)

        self.assertAlmostEqual(float(69) / utils.UNIGRAM_COUNT_GENE,
                               self.tagger.emission_params[('mouse', utils.I_GENE_TAG)])
        self.assertAlmostEqual(float(139) / utils.UNIGRAM_COUNT_O,
                               self.tagger.emission_params[('mouse', utils.O_TAG)])

        self.assertAlmostEqual(float(66) / utils.UNIGRAM_COUNT_GENE,
                               self.tagger.emission_params[('rat', utils.I_GENE_TAG)])
        self.assertAlmostEqual(float(141) / utils.UNIGRAM_COUNT_O,
                               self.tagger.emission_params[('rat', utils.O_TAG)])

    def test_get_simple_tag(self):
        self.tagger.get_word_count(utils.TRAIN_FILE)
        self.tagger.get_rare_words()

        self.tagger.get_emission_params(utils.TRAIN_FILE_RARE)

        self.assertEqual(utils.I_GENE_TAG, self.tagger.get_simple_tag('mouse'))
        self.assertEqual(utils.I_GENE_TAG, self.tagger.get_simple_tag('rat'))
        self.assertEqual(utils.O_TAG, self.tagger.get_simple_tag('rats'))
        self.assertEqual(utils.O_TAG, self.tagger.get_simple_tag(utils.RARE_WORD_SYMBOL))


if __name__ == '__main__':
    unittest.main()
