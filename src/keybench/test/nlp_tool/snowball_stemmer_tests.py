import unittest

from keybench.main.nlp_tool import implementation as nlp_tool

class SnowballStemmerTests(unittest.TestCase):

  def setUp(self):
    self._stemmer = nlp_tool.SnowballStemmer("english")

  def tearDown(self):
    self._stemmer = None

  def testStemming(self):
    plural_word = "words"
    stemmed_word = "word"

    self.failUnless(self._stemmer.stem(plural_word) == stemmed_word)

