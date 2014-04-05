import unittest

from keybench.main.nlp_tool import implementation
from keybench.main.nlp_tool import interface

class FrenchLeFFFLemmatizerTests(unittest.TestCase):

  def setUp(self):
    self._lemmatizer = implementation.FrenchLeFFFLemmatizer()

  def tearDown(self):
    self._lemmatizer = None

  def testLemmatization(self):
    word = u"mots"
    word_lemma = u"mot"
    verb1 = u"r\xe9sous"
    verb_lemma1 = u"r\xe9soudre"
    verb2 = u"suis"
    verb_lemma2 = u"\xeatre"

    self.failUnless(self._lemmatizer.lemmatize(word,
                                               interface.KBPOSTaggerI.POSTagKey.NOUN) == word_lemma)
    self.failUnless(self._lemmatizer.lemmatize(verb1,
                                               interface.KBPOSTaggerI.POSTagKey.VERB) == verb_lemma1)
    self.failUnless(self._lemmatizer.lemmatize(verb2,
                                               interface.KBPOSTaggerI.POSTagKey.VERB) == verb_lemma2)

