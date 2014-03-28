import exceptions

class KBPOSTaggerI(object):
  """Interface of a tokenized sentence POS tagger.
  """

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

