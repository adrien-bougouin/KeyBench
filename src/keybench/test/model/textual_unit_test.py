import unittest

from keybench.main import model
from keybench.main import exception

class KBTextualUnitTests(unittest.TestCase):

  def setUp(self):
    self.tu = model.KBTextualUnit("fr",      # language
                                  "test",    # normalized form
                                  ["test"],  # tokens
                                  ["test"],  # lemmas
                                  ["test"],  # stems
                                  ["N"])     # POS tags

  def tearDown(self):
    self.tu = None

  def testInitialization(self):
    self.failUnless(self.tu.language == "fr")
    self.failUnless(self.tu.normalized_form == "test")
    self.failUnless(self.tu.tokens == ["test"])
    self.failUnless(self.tu.lemmas == ["test"])
    self.failUnless(self.tu.stems == ["test"])
    self.failUnless(self.tu.pos_tags == ["N"])

  def testAddOccurrence(self):
    self.tu.addOccurrence("Test",           # seen form
                          "test_document",  # document in which it appears
                          10)               # offset
    self.tu.addOccurrence("Test",                 # seen form
                          "second_test_document", # document in which it appears
                          3)                      # offset
    self.tu.addOccurrence("test",           # seen form
                          "test_document",  # document in which it appears
                          42)               # offset
    self.tu.addOccurrence("Test",           # seen form
                          "test_document",  # document in which it appears
                          37)               # offset
    self.failUnless(self.tu.offsets("test_document") == [10, 42, 37])
    self.failUnless(self.tu.offsets("second_test_document") == [3])
    self.failUnless(self.tu.seen_forms("test_document") == [("Test", [10, 37]),
                                                            ("test", [42])])
    self.failUnless(self.tu.seen_forms("second_test_document") == [("Test",
                                                                    [3])])

    self.failUnless(self.tu.numberOfOccurrences("test_document") == 3)
    self.failUnless(self.tu.numberOfOccurrences("second_test_document") == 1)
    self.failUnless(self.tu.numberOfDocuments() == 2)

  def testAddExistingOccurrence(self):
    self.tu.addOccurrence("Test",           # seen form
                          "test_document",  # document in which it appears
                          10)               # offset
    # same offsets are not allowed for the same textual unit
    with self.assertRaises(exception.KBOffsetException):
      self.tu.addOccurrence("Test", "test_document", 10)

