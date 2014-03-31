import exceptions

class KBLemmatizerI(object):
  """Interface of a word lemmatizer.
  """

  def lemmatize(self, word, tag):
    """lemmatizes a word.

    Args:
      word: The C{string} word to lemmatize.
      tag: The C{string} POS tag of the C{word} (see
        C{keybench.main.nlp_tool.interface.KBPOSTaggerI.POSKey}).

    Returns:
      The C{string} lemmatized C{word}.
    """

    raise exceptions.NotImplementedError()

