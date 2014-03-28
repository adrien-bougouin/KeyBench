import exceptions

class KBLemmatizerI(object):
  """Interface of a word lemmatizer.
  """

  def lemmatize(self, word):
    """lemmatizes a word.

    Args:
      word: The C{string} word to lemmatize.

    Returns:
      The C{string} lemmatized C{word}.
    """

    raise exceptions.NotImplementedError()

