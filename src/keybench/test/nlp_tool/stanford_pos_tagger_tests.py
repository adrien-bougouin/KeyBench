import unittest

from keybench.main.nlp_tool.implementation import pos_tagger as nlp_tool

class StanfordPOSTaggerTests(unittest.TestCase):

  def setUp(self):
    self._tagger = nlp_tool.StanfordPOSTagger("english", "utf-8")

  def tearDown(self):
    self._tagger = None

  def testTagging(self):
    tokenized_sentences = [
      ["This", "is", "the", "first", "sentence", "."],
      ["This", "is", "the", "second", "one", "..."]
    ]
    # these are Stanford POS tags, not especially correct ones
    pos_tags = [
      ["DT", "VBZ", "DT", "JJ", "NN", "PUNCT"],
      ["DT", "VBZ", "DT", "JJ", "CD", "PUNCT"]
    ]

    self.failUnless(self._tagger.tag(tokenized_sentences) == pos_tags)

