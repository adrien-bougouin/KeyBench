import exceptions

class KBLemmatizerI(object):
  """Interface of a word lemmatizer.
  """

  def lemmatize(self, normalized_word, tag):
    """Lemmatizes a normalized word.

    Args:
      normalized_word: The C{string} word to lemmatize. It must be lemmatized
        first.
      tag: The C{string} POS tag of the C{normalized_word} (see
        C{keybench.main.nlp_tool.interface.KBPOSTaggerI.POSKey}).

    Returns:
      The C{string} lemmatized C{normalized_word}.
    """

    raise exceptions.NotImplementedError()

