import unittest

from keybench.main import exception
from keybench.main import model

class KBTextualUnitTests(unittest.TestCase):

  def setUp(self):
    self._tu = model.KBTextualUnit("test-corpus", # corpus name
                                   "fr",          # language
                                   "test",        # normalized form
                                   ["test"],      # tokens
                                   ["test"],      # lemmas
                                   ["test"],      # stems
                                   ["N"])         # POS tags

  def tearDown(self):
    self._tu = None

  def testInitialization(self):
    self.failUnless(self._tu.corpus_name == "test-corpus")
    self.failUnless(self._tu.language == "fr")
    self.failUnless(self._tu.normalized_form == "test")
    self.failUnless(self._tu.tokens == ["test"])
    self.failUnless(self._tu.lemmas == ["test"])
    self.failUnless(self._tu.stems == ["test"])
    self.failUnless(self._tu.pos_tags == ["N"])

  def testEqual(self):
    tu1 = model.KBTextualUnit("test-corpus",  # corpus name
                              "fr",           # language
                              "test",         # normalized form
                              ["test"],       # tokens
                              ["test"],       # lemmas
                              ["test"],       # stems
                              ["N"])          # POS tags
    tu2 = model.KBTextualUnit("test-corpus",  # corpus name
                              "fr",           # language
                              "test2",        # normalized form
                              ["test 2"],     # tokens
                              ["test 2"],     # lemmas
                              ["test 2"],     # stems
                              ["N"])          # POS tags
    tu3 = model.KBTextualUnit("test-corpus2", # corpus name
                              "fr",           # language
                              "test",         # normalized form
                              ["test"],       # tokens
                              ["test"],       # lemmas
                              ["test"],       # stems
                              ["N"])          # POS tags

    self.failUnless(self._tu == tu1)
    self.failIf(self._tu == tu2)
    self.failIf(self._tu == tu3)

  def testNotEqual(self):
    tu1 = model.KBTextualUnit("test-corpus",  # corpus name
                              "fr",           # language
                              "test",         # normalized form
                              ["test"],       # tokens
                              ["test"],       # lemmas
                              ["test"],       # stems
                              ["N"])          # POS tags
    tu2 = model.KBTextualUnit("test-corpus",  # corpus name
                              "fr",           # language
                              "test2",        # normalized form
                              ["test 2"],     # tokens
                              ["test 2"],     # lemmas
                              ["test 2"],     # stems
                              ["N"])          # POS tags
    tu3 = model.KBTextualUnit("test-corpus2", # corpus name
                              "fr",           # language
                              "test",         # normalized form
                              ["test"],       # tokens
                              ["test"],       # lemmas
                              ["test"],       # stems
                              ["N"])          # POS tags

    self.failIf(self._tu != tu1)
    self.failUnless(self._tu != tu2)
    self.failUnless(self._tu != tu3)

  def testAddOccurrence(self):
    self._tu.addOccurrence("Test",          # seen form
                           "test_document", # document in which it appears
                           10)              # offset
    self._tu.addOccurrence("Test",                  # seen form
                           "second_test_document",  # document in which it
                                                    # appears
                           3)                       # offset
    self._tu.addOccurrence("test",          # seen form
                           "test_document", # document in which it appears
                           42)              # offset
    self._tu.addOccurrence("Test",          # seen form
                           "test_document", # document in which it appears
                           37)              # offset
    self.failUnless(self._tu.offsets("test_document") == [10, 42, 37])
    self.failUnless(self._tu.offsets("second_test_document") == [3])
    self.failUnless(self._tu.seen_forms("test_document") == [("Test", [10, 37]),
                                                            ("test", [42])])
    self.failUnless(self._tu.seen_forms("second_test_document") == [("Test",
                                                                     [3])])

    self.failUnless(self._tu.numberOfOccurrences("test_document") == 3)
    self.failUnless(self._tu.numberOfOccurrences("second_test_document") == 1)
    self.failUnless(self._tu.numberOfDocuments() == 2)

  def testAddExistingOccurrence(self):
    self._tu.addOccurrence("Test",          # seen form
                           "test_document", # document in which it appears
                           10)              # offset

    # same offsets are not allowed for the same textual unit
    with self.assertRaises(exception.KBOffsetException):
      self._tu.addOccurrence("Test", "test_document", 10)

