# -*- encoding: utf-8 -*-

import shutil
import unittest

from os import path

from keybench.main import core
from keybench.main import exception

class KBCacheManagerTests(unittest.TestCase):

  ##############################################################################
  class MockStringParser(core.KBCacheManager.CacheParserI):
    def toString(self, obj):
      return obj

    def fromString(self, string):
      return string
  ##############################################################################

  def setUp(self):
    self._cm = core.KBCacheManager("cache_directory")

  def tearDown(self):
    self._cm = None

    if path.exists("cache_directory"):
      shutil.rmtree("cache_directory")
    if path.exists("cache_dir"):
      shutil.rmtree("cache_dir")

  def testInitialization(self):
    self.failUnless(self._cm.cache_directory == "cache_directory")

  def testEqual(self):
    cm1 = core.KBCacheManager("cache_directory")
    cm2 = core.KBCacheManager("cache_dir")

    self.failUnless(self._cm == cm1)
    self.failIf(self._cm == cm2)

  def testNotEqual(self):
    cm1 = core.KBCacheManager("cache_directory")
    cm2 = core.KBCacheManager("cache_dir")

    self.failIf(self._cm != cm1)
    self.failUnless(self._cm != cm2)

  def testStore(self):
    obj = [1, 2, 3]

    self._cm.store("test-object", obj)

    self.failUnless(self._cm.exists("test-object"))
    self.failUnless(self._cm.load("test-object") == obj)

  def testStoreString(self):
    obj = "test object"
    mock_parser = KBCacheManagerTests.MockStringParser()

    self._cm.storeString("test-object", obj, "utf-8", mock_parser)

    self.failUnless(self._cm.exists("test-object"))
    self.failUnless(self._cm.loadFromString("test-object",
                                            "utf-8",
                                            mock_parser) == obj)

  def testDoesNotExist(self):
    mock_parser = KBCacheManagerTests.MockStringParser()

    self.failIf(self._cm.exists("test-object"))

    with self.assertRaises(exception.KBCacheException):
      self._cm.load("test-object")

    with self.assertRaises(exception.KBCacheException):
      self._cm.loadFromString("test-object", "utf-8", mock_parser)

  def testOverride(self):
    obj1 = [1, 2, 3]
    obj2 = "overriden"

    self._cm.store("test-object", obj1)
    self._cm.store("test-object", obj2)

    self.failUnless(self._cm.exists("test-object"))
    self.failIf(self._cm.load("test-object") == obj1)
    self.failUnless(self._cm.load("test-object") == obj2)

  def testOverrideString(self):
    obj1 = "former"
    obj2 = "overriden"
    mock_parser = KBCacheManagerTests.MockStringParser()

    self._cm.storeString("test-object", obj1, "utf-8", mock_parser)
    self._cm.storeString("test-object", obj2, "utf-8", mock_parser)

    self.failUnless(self._cm.exists("test-object"))
    self.failIf(self._cm.loadFromString("test-object",
                                        "utf-8",
                                        mock_parser) == obj1)
    self.failUnless(self._cm.loadFromString("test-object",
                                            "utf-8",
                                            mock_parser) == obj2)

