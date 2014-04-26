# -*- encoding: utf-8 -*-

import unittest

from keybench.main.nlp_tool.implementation import tokenizer as nlp_tool

class EnglishPunktTokenizerTests(unittest.TestCase):

  def setUp(self):
    self._tokenizer = nlp_tool.EnglishPunktTokenizer()

  def tearDown(self):
    self._tokenizer = None

  def testTokenization(self):
    string_sentences = "This is the first sentence. This is the second one..."
    list_sentences = [
      "This is the first sentence.",
      "This is the second one..."
    ]
    tokenized_sentences = [
      ["This", "is", "the", "first", "sentence", "."],
      ["This", "is", "the", "second", "one", "..."]
    ]

    self.failUnless(self._tokenizer.tokenizeSentences(string_sentences) == list_sentences)
    self.failUnless(self._tokenizer.tokenizeWords(list_sentences) == tokenized_sentences)

