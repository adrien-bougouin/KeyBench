from keybench.main import exception

class KBNLPResourceFactoryI(object):
  """The configuration of the NLP resources to use for each language.

  The abstract factory providing the usefull Natural Language Processing
  resources (e.g. list of stop words, Part-of-Speech tagset) for specific
  languages.
  """

  class POSTagKey:
    """Part-of-Speech names.

    Part-of-Speech keys to use with the C{dict} returned by
    C{KBNLPResourceFactory.posTags()}.

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

  def stopLists(self):
    """Provides a list of stop words.

    Returns:
      The C{list} of C{string} words to use as stop words.
    """

    raise exception.KBConfigurationException(self, "Uncomplete NLP resource configuration!")

  def posTags(self):
    """Provides the tagset to use.

    Returns:
      The C{dict} of tags (C{list} of C{string} tags) associated to a
      grammatical class (see C{KBNLPResourceFactoryI.POSTagKey}).
    """

    raise exception.KBConfigurationException(self, "Uncomplete NLP resource configuration!")

