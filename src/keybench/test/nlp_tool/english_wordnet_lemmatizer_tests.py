import unittest

from keybench.main.nlp_tool import implementation
from keybench.main.nlp_tool import interface

class EnglishWordNetLemmatizerTests(unittest.TestCase):

  def setUp(self):
    self._lemmatizer = implementation.EnglishWordNetLemmatizer()

  def tearDown(self):
    self._lemmatizer = None

  def testLemmatization(self):
    word = "words"
    word_lemma = "word"
    verb1 = "solving"
    verb_lemma1 = "solve"
    verb2 = "was"
    verb_lemma2 = "be"

    self.failUnless(self._lemmatizer.lemmatize(word,
                                               interface.KBPOSTaggerI.POSTagKey.NOUN) == word_lemma)
    self.failUnless(self._lemmatizer.lemmatize(verb1,
                                               interface.KBPOSTaggerI.POSTagKey.VERB) == verb_lemma1)
    self.failUnless(self._lemmatizer.lemmatize(verb2,
                                               interface.KBPOSTaggerI.POSTagKey.VERB) == verb_lemma2)

