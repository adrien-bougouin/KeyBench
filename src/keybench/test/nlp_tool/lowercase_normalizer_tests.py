import unittest

from keybench.main.nlp_tool.implementation import normalizer as nlp_tool

class LowercaseNormalizerTests(unittest.TestCase):

  def setUp(self):
    self._normalizer = nlp_tool.LowercaseNormalizer()

  def tearDown(self):
    self._normalizer = None

  def testNormalization(self):
    self.failUnless(self._normalizer.normalize("This is not normalized") == "this is not normalized")
    self.failUnless(self._normalizer.normalize("this is normalized") == "this is normalized")

