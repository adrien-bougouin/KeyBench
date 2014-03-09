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

  def testModification(self):
    self._config.document_builders = "Dummy document builder"
    self._config.corpus_builders = "Dummy corpus builder"
    self._config.candidate_extractor = "Dummy candidate extractor"
    self._config.candidate_clusterer = "Dummy candidate clusterer"
    self._config.candidate_ranker = "Dummy candidate ranker"
    self._config.candidate_classifier = "Dummy  candidate classifier"
    self._config.keyphrase_extractor = "Dummy keyphrase extractor"
    self._config.keyphrase_consumers = "Dummy keyphrase consumers"

    self.failUnless(self._config.document_builders == "Dummy document builder")
    self.failUnless(self._config.corpus_builders == "Dummy corpus builder")
    self.failUnless(self._config.candidate_extractor == "Dummy candidate extractor")
    self.failUnless(self._config.candidate_clusterer == "Dummy candidate clusterer")
    self.failUnless(self._config.candidate_ranker == "Dummy candidate ranker")
    self.failUnless(self._config.candidate_classifier == "Dummy  candidate classifier")
    self.failUnless(self._config.keyphrase_extractor == "Dummy keyphrase extractor")
    self.failUnless(self._config.keyphrase_consumers == "Dummy keyphrase consumers")

