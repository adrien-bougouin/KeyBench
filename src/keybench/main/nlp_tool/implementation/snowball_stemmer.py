from nltk.stem import snowball

from keybench.main.nlp_tool import interface

class SnowballStemmer(interface.KBStemmerI):
  """Porter stemmer.

  Porter stemmer using the Snoball algorithm.
  """

  def __init__(self, language):
    """Constructor.

    Args:
      language: The C{string} name of the language to be treated by the stemmer.
    """

    self._stemmer = snowball.SnowballStemmer(language)

  def stem(self, word):
    """Stems a word.

    Args:
      word: The C{string} word to stem.

    Returns:
      The C{string} stemmed C{word}.
    """

    return self._stemmer.stem(word)

