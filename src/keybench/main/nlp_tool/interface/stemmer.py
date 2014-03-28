import exceptions

class KBStemmerI(object):
  """Interface of a word stemmer.
  """

  def stem(self, word):
    """Stems a word.

    Args:
      word: The C{string} word to stem.

    Returns:
      The C{string} stemmed C{word}.
    """

    raise exceptions.NotImplementedError()

