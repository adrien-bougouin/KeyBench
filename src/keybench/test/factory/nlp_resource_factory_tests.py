import unittest

from keybench.main import exception
from keybench.main import factory

class KBNLPResourceFactoryTests(unittest.TestCase):

  def setUp(self):
    self._config = factory.KBNLPResourceFactory()

  def tearDown(self):
    self._config = None

  def testInitialization(self):
    with self.assertRaises(exception.KBConfigurationException):
      self._config.stop_lists
    with self.assertRaises(exception.KBConfigurationException):
      self._config.pos_tags

  def testEqual(self):
    config1 = factory.KBNLPResourceFactory()
    config2 = factory.KBNLPResourceFactory()

    config2.stop_lists = {}

    self.failUnless(self._config == config1)
    self.failIf(self._config == config2)

  def testNotEqual(self):
    config1 = factory.KBNLPResourceFactory()
    config2 = factory.KBNLPResourceFactory()

    config2.stop_lists = {}

    self.failIf(self._config != config1)
    self.failUnless(self._config != config2)

  def testModification(self):
    self._config.stop_lists = {}
    self._config.pos_tags = {}

    self.failUnless(self._config.stop_lists == {})
    self.failUnless(self._config.pos_tags == {})

