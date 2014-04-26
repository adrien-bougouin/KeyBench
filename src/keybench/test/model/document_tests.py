# -*- encoding: utf-8 -*-

import unittest

from keybench.main import model

class KBDocumentTests(unittest.TestCase):

  def setUp(self):
    self._doc = model.KBDocument("test-corpus",
                                 "a/file/path",
                                 "1337",
                                 "fr",
                                 "utf-8",
                                 "Here is the title.",
                                 "Abstract sentence 1. Abstract sentence 2.",
                                 "Content sentence 1. Content sentence 2.",
                                 ["Here is the title."],
                                 ["Abstract sentence 1.",
                                  "Abstract sentence 2."],
                                 ["Content sentence 1.",
                                  "Content sentence 2."],
                                 [["Here", "is", "the", "title", "."]],
                                 [["Abstract", "sentence", "1", "."],
                                  ["Abstract", "sentence", "2", "."]],
                                 [["Content", "sentence", "1", "."],
                                  ["Content", "sentence", "2", "."]],
                                 [["here", "is", "the", "title", "."]],
                                 [["abstract", "sentence", "1", "."],
                                  ["abstract", "sentence", "2", "."]],
                                 [["content", "sentence", "1", "."],
                                  ["content", "sentence", "2", "."]],
                                 [["here", "be", "the", "title", "."]],
                                 [["abstract", "sentence", "1", "."],
                                  ["abstract", "sentence", "2", "."]],
                                 [["content", "sentence", "1", "."],
                                  ["content", "sentence", "2", "."]],
                                 [["here", "is", "the", "title", "."]],
                                 [["abstract", "sentence", "1", "."],
                                  ["abstract", "sentence", "2", "."]],
                                 [["content", "sentence", "1", "."],
                                  ["content", "sentence", "2", "."]],
                                 [["ADV", "VB", "DET", "PONCT"]],
                                 [["N", "N", "NUM", "PONCT"],
                                  ["N", "N", "NUM", "PONCT"]],
                                 [["N", "N", "NUM", "PONCT"],
                                  ["N", "N", "NUM", "PONCT"]])

  def tearDown(self):
    self._doc = None

  def testInitialization(self):
    self.failUnless(self._doc.corpus_name == "test-corpus")
    self.failUnless(self._doc.filepath == "a/file/path")
    self.failUnless(self._doc.name == "1337")
    self.failUnless(self._doc.language == "fr")
    self.failUnless(self._doc.encoding == "utf-8")
    self.failUnless(self._doc.title == "Here is the title.")
    self.failUnless(self._doc.abstract == "Abstract sentence 1. Abstract sentence 2.")
    self.failUnless(self._doc.content == "Content sentence 1. Content sentence 2.")
    self.failUnless(self._doc.title_sentences == ["Here is the title."])
    self.failUnless(self._doc.abstract_sentences == ["Abstract sentence 1.",
                                                     "Abstract sentence 2."])
    self.failUnless(self._doc.content_sentences == ["Content sentence 1.",
                                                    "Content sentence 2."])
    self.failUnless(self._doc.title_sentence_tokens == [["Here", "is", "the", "title", "."]])
    self.failUnless(self._doc.abstract_sentence_tokens == [["Abstract", "sentence", "1", "."],
                                                           ["Abstract", "sentence", "2", "."]])
    self.failUnless(self._doc.content_sentence_tokens == [["Content", "sentence", "1", "."],
                                                          ["Content", "sentence", "2", "."]])
    self.failUnless(self._doc.title_normalized_tokens == [["here", "is", "the", "title", "."]])
    self.failUnless(self._doc.abstract_normalized_tokens == [["abstract", "sentence", "1", "."],
                                                             ["abstract", "sentence", "2", "."]])
    self.failUnless(self._doc.content_normalized_tokens == [["content", "sentence", "1", "."],
                                                            ["content", "sentence", "2", "."]])
    self.failUnless(self._doc.title_token_lemmas == [["here", "be", "the", "title", "."]])
    self.failUnless(self._doc.abstract_token_lemmas == [["abstract", "sentence", "1", "."],
                                                        ["abstract", "sentence", "2", "."]])
    self.failUnless(self._doc.content_token_lemmas == [["content", "sentence", "1", "."],
                                                       ["content", "sentence", "2", "."]])
    self.failUnless(self._doc.title_token_stems == [["here", "is", "the", "title", "."]])
    self.failUnless(self._doc.abstract_token_stems == [["abstract", "sentence", "1", "."],
                                                       ["abstract", "sentence", "2", "."]])
    self.failUnless(self._doc.content_token_stems == [["content", "sentence", "1", "."],
                                                      ["content", "sentence", "2", "."]])
    self.failUnless(self._doc.title_token_pos_tags == [["ADV", "VB", "DET", "PONCT"]])
    self.failUnless(self._doc.abstract_token_pos_tags == [["N", "N", "NUM", "PONCT"],
                                                          ["N", "N", "NUM", "PONCT"]])
    self.failUnless(self._doc.content_token_pos_tags == [["N", "N", "NUM", "PONCT"],
                                                         ["N", "N", "NUM", "PONCT"]])
    self.failUnless(self._doc.full_text == "%s %s %s"%("Here is the title.",
                                                       "Abstract sentence 1. Abstract sentence 2.",
                                                       "Content sentence 1. Content sentence 2."))
    self.failUnless(self._doc.full_text_sentences == ["Here is the title.",
                                                      "Abstract sentence 1.",
                                                      "Abstract sentence 2.",
                                                      "Content sentence 1.",
                                                      "Content sentence 2."])
    self.failUnless(self._doc.full_text_sentence_tokens == [["Here", "is", "the", "title", "."],
                                                            ["Abstract", "sentence", "1", "."],
                                                            ["Abstract", "sentence", "2", "."],
                                                            ["Content", "sentence", "1", "."],
                                                            ["Content", "sentence", "2", "."]])
    self.failUnless(self._doc.full_text_normalized_tokens == [["here", "is", "the", "title", "."],
                                                              ["abstract", "sentence", "1", "."],
                                                              ["abstract", "sentence", "2", "."],
                                                              ["content", "sentence", "1", "."],
                                                              ["content", "sentence", "2", "."]])
    self.failUnless(self._doc.full_text_token_lemmas == [["here", "be", "the", "title", "."],
                                                         ["abstract", "sentence", "1", "."],
                                                         ["abstract", "sentence", "2", "."],
                                                         ["content", "sentence", "1", "."],
                                                         ["content", "sentence", "2", "."]])
    self.failUnless(self._doc.full_text_token_stems == [["here", "is", "the", "title", "."],
                                                        ["abstract", "sentence", "1", "."],
                                                        ["abstract", "sentence", "2", "."],
                                                        ["content", "sentence", "1", "."],
                                                        ["content", "sentence", "2", "."]])
    self.failUnless(self._doc.full_text_token_pos_tags == [["ADV", "VB", "DET", "PONCT"],
                                                           ["N", "N", "NUM", "PONCT"],
                                                           ["N", "N", "NUM", "PONCT"],
                                                           ["N", "N", "NUM", "PONCT"],
                                                           ["N", "N", "NUM", "PONCT"]])

  def testEqual(self):
    doc1 = model.KBDocument("test-corpus",
                            "a/file/path",
                            "1337",
                            "fr",
                            "utf-8",
                            "Here is the title.",
                            "Abstract sentence 1. Abstract sentence 2.",
                            "Content sentence 1. Content sentence 2.",
                            ["Here is the title."],
                            ["Abstract sentence 1.",
                             "Abstract sentence 2."],
                            ["Content sentence 1.",
                             "Content sentence 2."],
                            [["Here", "is", "the", "title", "."]],
                            [["Abstract", "sentence", "1", "."],
                             ["Abstract", "sentence", "2", "."]],
                            [["Content", "sentence", "1", "."],
                             ["Content", "sentence", "2", "."]],
                            [["here", "is", "the", "title", "."]],
                            [["abstract", "sentence", "1", "."],
                             ["abstract", "sentence", "2", "."]],
                            [["content", "sentence", "1", "."],
                             ["content", "sentence", "2", "."]],
                            [["here", "be", "the", "title", "."]],
                            [["abstract", "sentence", "1", "."],
                             ["abstract", "sentence", "2", "."]],
                            [["content", "sentence", "1", "."],
                             ["content", "sentence", "2", "."]],
                            [["here", "is", "the", "title", "."]],
                            [["abstract", "sentence", "1", "."],
                             ["abstract", "sentence", "2", "."]],
                            [["content", "sentence", "1", "."],
                             ["content", "sentence", "2", "."]],
                            [["ADV", "VB", "DET", "PONCT"]],
                            [["N", "N", "NUM", "PONCT"],
                             ["N", "N", "NUM", "PONCT"]],
                            [["N", "N", "NUM", "PONCT"],
                             ["N", "N", "NUM", "PONCT"]])
    doc2 = model.KBDocument("test-corpus",
                            "a/file/path",
                            "1338",
                            "fr",
                            "utf-8",
                            "Here is the title.",
                            "Abstract sentence 1. Abstract sentence 2.",
                            "Content sentence 1. Content sentence 2.",
                            ["Here is the title."],
                            ["Abstract sentence 1.",
                             "Abstract sentence 2."],
                            ["Content sentence 1.",
                             "Content sentence 2."],
                            [["Here", "is", "the", "title", "."]],
                            [["Abstract", "sentence", "1", "."],
                             ["Abstract", "sentence", "2", "."]],
                            [["Content", "sentence", "1", "."],
                             ["Content", "sentence", "2", "."]],
                            [["here", "is", "the", "title", "."]],
                            [["abstract", "sentence", "1", "."],
                             ["abstract", "sentence", "2", "."]],
                            [["content", "sentence", "1", "."],
                             ["content", "sentence", "2", "."]],
                            [["here", "be", "the", "title", "."]],
                            [["abstract", "sentence", "1", "."],
                             ["abstract", "sentence", "2", "."]],
                            [["content", "sentence", "1", "."],
                             ["content", "sentence", "2", "."]],
                            [["here", "is", "the", "title", "."]],
                            [["abstract", "sentence", "1", "."],
                             ["abstract", "sentence", "2", "."]],
                            [["content", "sentence", "1", "."],
                             ["content", "sentence", "2", "."]],
                            [["ADV", "VB", "DET", "PONCT"]],
                            [["N", "N", "NUM", "PONCT"],
                             ["N", "N", "NUM", "PONCT"]],
                            [["N", "N", "NUM", "PONCT"],
                             ["N", "N", "NUM", "PONCT"]])

    self.failUnless(self._doc == doc1)
    self.failIf(self._doc == doc2)

  def testNotEqual(self):
    doc1 = model.KBDocument("test-corpus",
                            "a/file/path",
                            "1337",
                            "fr",
                            "utf-8",
                            "Here is the title.",
                            "Abstract sentence 1. Abstract sentence 2.",
                            "Content sentence 1. Content sentence 2.",
                            ["Here is the title."],
                            ["Abstract sentence 1.",
                             "Abstract sentence 2."],
                            ["Content sentence 1.",
                             "Content sentence 2."],
                            [["Here", "is", "the", "title", "."]],
                            [["Abstract", "sentence", "1", "."],
                             ["Abstract", "sentence", "2", "."]],
                            [["Content", "sentence", "1", "."],
                             ["Content", "sentence", "2", "."]],
                            [["here", "is", "the", "title", "."]],
                            [["abstract", "sentence", "1", "."],
                             ["abstract", "sentence", "2", "."]],
                            [["content", "sentence", "1", "."],
                             ["content", "sentence", "2", "."]],
                            [["here", "be", "the", "title", "."]],
                            [["abstract", "sentence", "1", "."],
                             ["abstract", "sentence", "2", "."]],
                            [["content", "sentence", "1", "."],
                             ["content", "sentence", "2", "."]],
                            [["here", "is", "the", "title", "."]],
                            [["abstract", "sentence", "1", "."],
                             ["abstract", "sentence", "2", "."]],
                            [["content", "sentence", "1", "."],
                             ["content", "sentence", "2", "."]],
                            [["ADV", "VB", "DET", "PONCT"]],
                            [["N", "N", "NUM", "PONCT"],
                             ["N", "N", "NUM", "PONCT"]],
                            [["N", "N", "NUM", "PONCT"],
                             ["N", "N", "NUM", "PONCT"]])
    doc2 = model.KBDocument("test-corpus",
                            "a/file/path",
                            "1338",
                            "fr",
                            "utf-8",
                            "Here is the title.",
                            "Abstract sentence 1. Abstract sentence 2.",
                            "Content sentence 1. Content sentence 2.",
                            ["Here is the title."],
                            ["Abstract sentence 1.",
                             "Abstract sentence 2."],
                            ["Content sentence 1.",
                             "Content sentence 2."],
                            [["Here", "is", "the", "title", "."]],
                            [["Abstract", "sentence", "1", "."],
                             ["Abstract", "sentence", "2", "."]],
                            [["Content", "sentence", "1", "."],
                             ["Content", "sentence", "2", "."]],
                            [["here", "is", "the", "title", "."]],
                            [["abstract", "sentence", "1", "."],
                             ["abstract", "sentence", "2", "."]],
                            [["content", "sentence", "1", "."],
                             ["content", "sentence", "2", "."]],
                            [["here", "be", "the", "title", "."]],
                            [["abstract", "sentence", "1", "."],
                             ["abstract", "sentence", "2", "."]],
                            [["content", "sentence", "1", "."],
                             ["content", "sentence", "2", "."]],
                            [["here", "is", "the", "title", "."]],
                            [["abstract", "sentence", "1", "."],
                             ["abstract", "sentence", "2", "."]],
                            [["content", "sentence", "1", "."],
                             ["content", "sentence", "2", "."]],
                            [["ADV", "VB", "DET", "PONCT"]],
                            [["N", "N", "NUM", "PONCT"],
                             ["N", "N", "NUM", "PONCT"]],
                            [["N", "N", "NUM", "PONCT"],
                             ["N", "N", "NUM", "PONCT"]])

    self.failIf(self._doc != doc1)
    self.failUnless(self._doc != doc2)

