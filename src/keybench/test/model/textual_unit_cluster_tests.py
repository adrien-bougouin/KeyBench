# -*- encoding: utf-8 -*-

import unittest

from keybench.main import exception
from keybench.main import model

class KBTextualUnitClusterTests(unittest.TestCase):

  def setUp(self):
    self._tuc = model.KBTextualUnitCluster()

  def tearDown(self):
    self._tuc = None

  def testInitialization(self):
    self.failUnless(self._tuc.textual_units == [])
    self.failUnless(self._tuc.centroid == None)

  def testEqual(self):
    tuc1 = model.KBTextualUnitCluster()
    tuc2 = model.KBTextualUnitCluster()
    tuc3 = model.KBTextualUnitCluster()
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

    self._tuc.addTextualUnit(tu1)
    self._tuc.addTextualUnit(tu2)
    self._tuc.centroid = tu2
    tuc1.addTextualUnit(tu1)
    tuc1.addTextualUnit(tu2)
    tuc1.centroid = tu2
    tuc2.addTextualUnit(tu1)
    tuc2.addTextualUnit(tu2)
    tuc2.centroid = tu1
    tuc3.addTextualUnit(tu2)
    tuc3.centroid = tu2

    self.failUnless(self._tuc == tuc1)
    self.failIf(self._tuc == tuc2)
    self.failIf(self._tuc == tuc3)

  def testNotEqual(self):
    tuc1 = model.KBTextualUnitCluster()
    tuc2 = model.KBTextualUnitCluster()
    tuc3 = model.KBTextualUnitCluster()
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

    self._tuc.addTextualUnit(tu1)
    self._tuc.addTextualUnit(tu2)
    self._tuc.centroid = tu2
    tuc1.addTextualUnit(tu1)
    tuc1.addTextualUnit(tu2)
    tuc1.centroid = tu2
    tuc2.addTextualUnit(tu1)
    tuc2.addTextualUnit(tu2)
    tuc2.centroid = tu1
    tuc3.addTextualUnit(tu2)
    tuc3.centroid = tu2

    self.failIf(self._tuc != tuc1)
    self.failUnless(self._tuc != tuc2)
    self.failUnless(self._tuc != tuc3)

  def testAddTextualUnit(self):
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

    self._tuc.addTextualUnit(tu1)
    self._tuc.addTextualUnit(tu2)

    self.failUnless(self._tuc.numberOfTextualUnits() == 2)
    self.failUnless(self._tuc.textual_units == [tu1, tu2])

  def testAddExistingTextualUnit(self):
    tu1 = model.KBTextualUnit("test-corpus",  # corpus name
                              "fr",           # language
                              "test",         # normalized form
                              ["test"],       # tokens
                              ["test"],       # lemmas
                              ["test"],       # stems
                              ["N"])          # POS tags
    tu2 = model.KBTextualUnit("test-corpus",  # corpus name
                              "fr",           # language
                              "test",         # normalized form
                              ["test"],       # tokens
                              ["test"],       # lemmas
                              ["test"],       # stems
                              ["N"])          # POS tags

    self._tuc.addTextualUnit(tu1)

    with self.assertRaises(exception.KBTextualUnitClusterException):
      self._tuc.addTextualUnit(tu2)

  def testSetCentroid(self):
    tu = model.KBTextualUnit("test-corpus",  # corpus name
                             "fr",           # language
                             "test",         # normalized form
                             ["test"],       # tokens
                             ["test"],       # lemmas
                             ["test"],       # stems
                             ["N"])          # POS tags

    self._tuc.addTextualUnit(tu)
    self._tuc.centroid = tu

    self.failUnless(self._tuc.centroid == tu)

  def testSetWrongCentroid(self):
    tu = model.KBTextualUnit("test-corpus",  # corpus name
                             "fr",           # language
                             "test",         # normalized form
                             ["test"],       # tokens
                             ["test"],       # lemmas
                             ["test"],       # stems
                             ["N"])          # POS tags

    with self.assertRaises(exception.KBTextualUnitClusterException):
      self._tuc.centroid = tu

