import unittest

from keybench.main import exception
from keybench.main import factory

class KBComponentFactoryTests(unittest.TestCase):

  def setUp(self):
    self._config = factory.KBComponentFactory()

  def tearDown(self):
    self._config = None

  def testInitialization(self):
    with self.assertRaises(exception.KBConfigurationException):
      self._config.document_builders
    with self.assertRaises(exception.KBConfigurationException):
      self._config.corpus_builders
    with self.assertRaises(exception.KBConfigurationException):
      self._config.candidate_extractor
    with self.assertRaises(exception.KBConfigurationException):
      self._config.candidate_clusterer
    with self.assertRaises(exception.KBConfigurationException):
      self._config.candidate_ranker
    with self.assertRaises(exception.KBConfigurationException):
      self._config.candidate_classifier
    with self.assertRaises(exception.KBConfigurationException):
      self._config.keyphrase_extractor
    with self.assertRaises(exception.KBConfigurationException):
      self._config.keyphrase_consumers

  def testEqual(self):
    config1 = factory.KBComponentFactory()
    config2 = factory.KBComponentFactory()

    config2.document_builders = {}

    self.failUnless(self._config == config1)
    self.failIf(self._config == config2)

  def testNotEqual(self):
    config1 = factory.KBComponentFactory()
    config2 = factory.KBComponentFactory()

    config2.document_builders = {}

    self.failIf(self._config != config1)
    self.failUnless(self._config != config2)

  # TODO complete after component interface creation
  def testRightCongifurationCreation(self):
    self.failUnless(False)

  # TODO should after component interface creation
  def testWrongCongifurationCreation(self):
    with self.assertRaises(exception.KBConfigurationException):
      self._config.document_builders = "Wrong document builder"
    with self.assertRaises(exception.KBConfigurationException):
     self._config.document_builders = {"Wrong document builder": "Told you!"}
    with self.assertRaises(exception.KBConfigurationException):
      self._config.corpus_builders = "Wrong corpus builder"
    with self.assertRaises(exception.KBConfigurationException):
      self._config.corpus_builders = ["Wrong corpus builder"]
    with self.assertRaises(exception.KBConfigurationException):
      self._config.candidate_extractor = "Wrong candidate extractor"
    with self.assertRaises(exception.KBConfigurationException):
      self._config.candidate_clusterer = "Wrong candidate clusterer"
    with self.assertRaises(exception.KBConfigurationException):
      self._config.candidate_ranker = "Wrong candidate ranker"
    with self.assertRaises(exception.KBConfigurationException):
      self._config.candidate_classifier = "Wrong  candidate classifier"
    with self.assertRaises(exception.KBConfigurationException):
      self._config.keyphrase_extractor = "Wrong keyphrase extractor"
    with self.assertRaises(exception.KBConfigurationException):
      self._config.keyphrase_consumers = "Wrong keyphrase consumers"
    with self.assertRaises(exception.KBConfigurationException):
      self._config.keyphrase_consumers = ["Wrong keyphrase consumers"]

