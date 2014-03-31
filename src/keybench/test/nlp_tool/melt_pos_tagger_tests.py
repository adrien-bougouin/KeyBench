import unittest

from keybench.main.nlp_tool import implementation as nlp_tool

class MEltPOSTaggerTests(unittest.TestCase):

  def setUp(self):
    self._tagger = nlp_tool.MEltPOSTagger("french", "utf-8")

  def tearDown(self):
    self._tagger = None

  def testTagging(self):
    tokenized_sentences = [
      ["Ceci", "est", "une", "phrase", "."],
      ["Ceci", "est", "une", "seconde", "phrase", "..."]
    ]
    # these are MElt POS tags, not especially correct ones
    pos_tags = [
      ["PRO", "V", "DET", "NC", "PONCT"],
      ["PRO", "V", "DET", "ADJ", "NC", "PONCT"]
    ]

    self.failUnless(self._tagger.tag(tokenized_sentences) == pos_tags)

