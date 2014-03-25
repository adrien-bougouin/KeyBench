import unittest

from keybench.main import exception
from keybench.main import factory

class KBNLPToolFactoryTests(unittest.TestCase):

  def setUp(self):
    self._config = factory.KBNLPToolFactory()

  def tearDown(self):
    self._config = None

  def testInitialization(self):
    with self.assertRaises(exception.KBConfigurationException):
      self._config.normalizers
    with self.assertRaises(exception.KBConfigurationException):
      self._config.tokenizers
    with self.assertRaises(exception.KBConfigurationException):
      self._config.stemmers
    with self.assertRaises(exception.KBConfigurationException):
      self._config.lemmatizers
    with self.assertRaises(exception.KBConfigurationException):
      self._config.pos_taggers

  def testEqual(self):
    config1 = factory.KBNLPToolFactory()
    config2 = factory.KBNLPToolFactory()

    config2.normalizers = {}

    self.failUnless(self._config == config1)
    self.failIf(self._config == config2)

  def testNotEqual(self):
    config1 = factory.KBNLPToolFactory()
    config2 = factory.KBNLPToolFactory()

    config2.normalizers = {}

    self.failIf(self._config != config1)
    self.failUnless(self._config != config2)

  def testModification(self):
    self._config.normalizers = {}
    self._config.tokenizers = {}
    self._config.stemmers = {}
    self._config.lemmatizers = {}
    self._config.pos_taggers = {}

    self.failUnless(self._config.normalizers == {})
    self.failUnless(self._config.tokenizers == {})
    self.failUnless(self._config.stemmers == {})
    self.failUnless(self._config.lemmatizers == {})
    self.failUnless(self._config.pos_taggers == {})

