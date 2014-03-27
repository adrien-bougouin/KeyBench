import shutil
import unittest

from os import path

from keybench.main import component
from keybench.main import exception
from keybench.main import model

class KBComponentTests(unittest.TestCase):

  def setUp(self):
    self._rcomp = component.KBComponent("SharedCompName",
                                        "TestRun",
                                        True,
                                        True,
                                        True,
                                        "cache_root")
    self._scomp = component.KBComponent("SingleCompName",
                                        "TestRun",
                                        False,
                                        False,
                                        True,
                                        "cache_root")

  def tearDown(self):
    self._rcomp = None
    self._scomp = None

    if path.exists("cache_root"):
      shutil.rmtree("cache_root")

  def testInitialization(self):
    self.failUnless(self._rcomp.name == "SharedCompName")
    self.failUnless(self._rcomp.run_name == "TestRun")
    self.failUnless(self._rcomp.isLazy() == True)
    self.failUnless(self._rcomp._debug_mode == True)
    self.failUnless(self._rcomp._cache_manager.cache_directory
                    == path.join("cache_root", "shared", self._rcomp.name))

    self.failUnless(self._scomp.name == "SingleCompName")
    self.failUnless(self._scomp.run_name == "TestRun")
    self.failUnless(self._scomp.isLazy() == False)
    self.failUnless(self._scomp._debug_mode == True)
    self.failUnless(self._scomp._cache_manager.cache_directory
                    == path.join("cache_root",
                                 self._scomp.run_name,
                                 self._scomp.name))

  def testEqual(self):
    rcomp1 = component.KBComponent("SharedCompName",
                                   "TestRun",
                                   True,
                                   True,
                                   True,
                                   "cache_root")
    rcomp2 = component.KBComponent("SingleCompName",
                                   "TestRun",
                                   True,
                                   True,
                                   True,
                                   "cache_root")
    scomp1 = component.KBComponent("SingleCompName",
                                   "TestRun",
                                   False,
                                   False,
                                   True,
                                   "cache_root")
    scomp2 = component.KBComponent("SharedCompName",
                                   "TestRun",
                                   False,
                                   True,
                                   True,
                                   "cache_root")

    self.failUnless(self._rcomp == rcomp1)
    self.failIf(self._rcomp == rcomp2)
    self.failIf(self._rcomp == scomp2)

    self.failUnless(self._scomp == scomp1)
    self.failIf(self._scomp == scomp2)
    self.failIf(self._scomp == rcomp2)

  def testNotEqual(self):
    rcomp1 = component.KBComponent("SharedCompName",
                                   "TestRun",
                                   True,
                                   True,
                                   True,
                                   "cache_root")
    rcomp2 = component.KBComponent("SingleCompName",
                                   "TestRun",
                                   True,
                                   True,
                                   True,
                                   "cache_root")
    scomp1 = component.KBComponent("SingleCompName",
                                   "TestRun",
                                   False,
                                   False,
                                   True,
                                   "cache_root")
    scomp2 = component.KBComponent("SharedCompName",
                                   "TestRun",
                                   False,
                                   True,
                                   True,
                                   "cache_root")

    self.failIf(self._rcomp != rcomp1)
    self.failUnless(self._rcomp != rcomp2)
    self.failUnless(self._rcomp != scomp2)

    self.failIf(self._scomp != scomp1)
    self.failUnless(self._scomp != scomp2)
    self.failUnless(self._scomp != rcomp2)

  def testStoringIdentification(self):
    doc = model.KBDocument("Test-Corpus",
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
                           [["ADV", "VB", "DET", "PONCT"]],
                           [["N", "N", "NUM", "PONCT"],
                           ["N", "N", "NUM", "PONCT"]],
                           [["N", "N", "NUM", "PONCT"],
                           ["N", "N", "NUM", "PONCT"]])
    obj = [1, 2, 3]

    self._rcomp.store(doc, obj)
    self._scomp.store(doc, obj)

    self.failUnless(self._rcomp.exists(doc))
    self.failUnless(self._rcomp._cache_manager.exists("test_corpus_1337"))

    self.failUnless(self._scomp.exists(doc))
    self.failUnless(self._scomp._cache_manager.exists("test_corpus_1337"))

  def testNoLazyLoading(self):
    doc = model.KBDocument("Test-Corpus",
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
                           [["ADV", "VB", "DET", "PONCT"]],
                           [["N", "N", "NUM", "PONCT"],
                           ["N", "N", "NUM", "PONCT"]],
                           [["N", "N", "NUM", "PONCT"],
                           ["N", "N", "NUM", "PONCT"]])

    with self.assertRaises(exception.KBLazyComponentException):
      self._scomp.load(doc)

