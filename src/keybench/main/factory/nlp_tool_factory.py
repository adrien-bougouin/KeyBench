from keybench.main import exception

class KBNLPToolFactory(object):
  """The configuration of the NLP tools to use for each language.

  The abstract factory providing the components that perform a specific Natural
  Language Processing for specific languages.

  Attributes:
    normalizers: The C{KBNormalizerI} components responsible of the string
      normalization, associated to  one specific language (C{map} of C{string}
      language name keys and C{KBNormalizerI} values).
    tokenizers: The C{KBTokenizerI} components responsible of sentence and word
      tokenization, associated to  one specific language (C{map} of C{string}
      language name keys and C{KBTokenizerI} values).
    stemmers: The C{KBStemmerI} components responsible of phrase and/or word
      stemming, associated to  one specific language (C{map} of C{string}
      language keys and C{KBStemmerI} values).
    lemmatizers: The C{KBLemmatizerI} components responsible of phrase and/or
      word lemmatization, associated to  one specific language (C{map} of
      C{string} language keys and C{KBLemmatizerI} values).
    pos_taggers: The C{KBPOSTaggerI} components responsible of word-tokenized
      sentence POS tagging, associated to  one specific language (C{map} of
      C{string} language keys and C{KBStemmerI} values).
  """

  def __init__(self):
    super(KBNLPToolFactory, self).__init__()

    self._normalizers = None
    self._tokenizers = None
    self._stemmers = None
    self._lemmatizers = None
    self._pos_taggers = None

  def __eq__(self, other):
    return self._normalizers == other._normalizers \
           and self._tokenizers == other._tokenizers \
           and self._stemmers == other._stemmers \
           and self._lemmatizers == other._lemmatizers \
           and self._pos_taggers == other._pos_taggers

  def __ne__(self, other):
    return not self.__eq__(other)

  def __str__(self):
    return "%s:%s; %s:%s; %s:%s; %s:%s; %s:%s"%(
             self._normalizers.__class__.__name__,
             str(self._normalizers),
             self._tokenizers.__class__.__name__,
             str(self._tokenizers),
             self._stemmers.__class__.__name__,
             str(self._stemmers),
             self._lemmatizers.__class__.__name__,
             str(self._lemmatizers),
             self._pos_taggers.__class__.__name__,
             str(self._pos_taggers)
           )

  @property
  def normalizers(self):
    if self._normalizers == None:
      raise exception.KBConfigurationException(self,
                                               "Uncomplete NLP tool configuration!")
    return self._normalizers

  @normalizers.setter
  def normalizers(self, value):
    self._normalizers = value

  @property
  def tokenizers(self):
    if self._tokenizers == None:
      raise exception.KBConfigurationException(self,
                                               "Uncomplete NLP tool configuration!")
    return self._tokenizers

  @tokenizers.setter
  def tokenizers(self, value):
    self._tokenizers = value

  @property
  def stemmers(self):
    if self._stemmers == None:
      raise exception.KBConfigurationException(self,
                                               "Uncomplete NLP tool configuration!")
    return self._stemmers

  @stemmers.setter
  def stemmers(self, value):
    self._stemmers = value

  @property
  def lemmatizers(self):
    if self._lemmatizers == None:
      raise exception.KBConfigurationException(self,
                                               "Uncomplete NLP tool configuration!")
    return self._lemmatizers

  @lemmatizers.setter
  def lemmatizers(self, value):
    self._lemmatizers = value

  @property
  def pos_taggers(self):
    if self._pos_taggers == None:
      raise exception.KBConfigurationException(self,
                                               "Uncomplete NLP tool configuration!")
    return self._pos_taggers

  @pos_taggers.setter
  def pos_taggers(self, value):
    self._pos_taggers = value

