import exceptions

class KBStemmerI(object):
  """Interface of a word stemmer.
  """

  def stem(self, normalized_word):
    """Stems a normalized word.

    Args:
      normalized_word: The C{string} word to stem. It must be normalized first.

    Returns:
      The C{string} stemmed C{normalized_word}.
    """

    raise exceptions.NotImplementedError()

