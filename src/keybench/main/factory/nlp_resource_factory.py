from keybench.main import exception

class KBNLPResourceFactory(object):
  """The configuration of the NLP resources to use for each language.

  The abstract factory providing the usefull Natural Language Processing
  resources (e.g. list of stop words, Part-of-Speech tagset) for specific
  languages.

  Attributes:
    stop_lists: The C{list}s of stop words, associated to one specific language
      (C{map} of C{string} language name keys and C{list} of C{string} values).
    pos_tags: The C{list}s of POS tags, associated to one specific language
      (C{map} of C{string} language name keys and C{map} of C{string}
      grammatical class and C{list} of C{string} values as values).
  """

  class POSTagKey:
    """Part-of-Speech names.

    Part-of-Speech keys to use with C{KBNLPResourceFactory.pos_tags}.

    Attributes:
      NOUN_KEY: Key used for noun tags.
      ADJECTIVE_KEY: Key used for adjective tags.
      VERB_KEY: Key used for verb tags.
      ADVERB_KEY: Key used for adverb tags.
      PREPOSITION_KEY: Key used for preposition tags.
      DETERMINER_KEY: Key used for determiner tags.
    """

    NOUN_KEY        = "__noun__"
    ADJECTIVE_KEY   = "__adjective__"
    VERB_KEY        = "__verb__"
    ADVERB_KEY      = "__adverb__"
    PREPOSITION_KEY = "__preposition__"
    DETERMINER_KEY  = "__determiner__"

  def __init__(self):
    super(KBNLPResourceFactory, self).__init__()

    self._stop_lists = None
    self._pos_tags = None

  def __eq__(self, other):
    return self._stop_lists == other._stop_lists \
           and self._pos_tags == other._pos_tags

  def __ne__(self, other):
    return not self.__eq__(other)

  def __str__(self):
    return "%s:%s; %s:%s"%(
             self._stop_lists.__class__.__name__,
             str(self._stop_lists),
             self._pos_tags.__class__.__name__,
             str(self._pos_tags)
           )

  @property
  def stop_lists(self):
    if self._stop_lists == None:
      raise exception.KBConfigurationException(self,
                                               "Uncomplete NLP resource configuration!")
    return self._stop_lists

  @stop_lists.setter
  def stop_lists(self, value):
    self._stop_lists = value

  @property
  def pos_tags(self):
    if self._pos_tags == None:
      raise exception.KBConfigurationException(self,
                                               "Uncomplete NLP resource configuration!")
    return self._pos_tags

  @pos_tags.setter
  def pos_tags(self, value):
    self._pos_tags = value

