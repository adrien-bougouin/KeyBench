import exceptions

class KBPOSTaggerI(object):
  """Interface of a tokenized sentence POS tagger.

  Attributes:
    tagset: The C{dict} of tags (C{list} of C{string} tags) associated to a
      grammatical class (see C{KBPOSTaggerI.POSTagKey}).
  """

  ##############################################################################
  class POSTagKey:
    """Part-of-Speech names.

    Part-of-Speech names to use as tagset keys. Those names are generic and
    meant to match multiple tags.

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
  ##############################################################################

  def __init__(self):
    super(KBPOSTaggerI, self).__init__()

    self._tagset = {}

  @property
  def tagset(self):
    return self._tagset

  def tag(self, tokenized_sentences):
    """POS tags tokenized sentences.

    Args:
      tokenized_sentences: The C{list} of tokenized sentences (C{list}s of
        C{string} words).

    Returns:
      The C{list} of sentences' POS tags. POS tags of one sentence is a C{list}
      of C{string} tags.
    """

    raise exceptions.NotImplementedError()

