import unittest

from keybench.main.nlp_tool.implementation import tokenizer as nlp_tool

class FrenchBonsaiTokenizerTests(unittest.TestCase):

  def setUp(self):
    self._tokenizer = nlp_tool.FrenchBonsaiTokenizer("utf-8")

  def tearDown(self):
    self._tokenizer = None

  def testTokenization(self):
    string_sentences = "Voici la premiere phrase. Et voici la seconde..."
    list_sentences = [
      "Voici la premiere phrase.",
      "Et voici la seconde..."
    ]
    tokenized_sentences = [
      ["Voici", "la", "premiere", "phrase", "."],
      ["Et", "voici", "la", "seconde", "..."]
    ]

    self.failUnless(self._tokenizer.tokenizeSentences(string_sentences) == list_sentences)
    self.failUnless(self._tokenizer.tokenizeWords(list_sentences) == tokenized_sentences)

