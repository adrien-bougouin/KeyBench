# -*- encoding: utf-8 -*-

from nltk.stem import snowball

from keybench.main.nlp_tool import interface

class SnowballStemmer(interface.KBStemmerI):
  """Porter stemmer.

  Porter stemmer using the Snoball algorithm.
  """

  def __init__(self, language):
    """Constructor.

    Args:
      language: The C{string} name of the language to be treated by the stemmer
        (see C{keybench.main.language_support.KBLanguage}).
    """

    super(SnowballStemmer, self).__init__()

    self._stemmer = snowball.SnowballStemmer(language)

  def stem(self, normalized_word):
    """Stems a normalized word.

    Args:
      normalized_word: The C{string} word to stem. It must be normalized first.

    Returns:
      The C{string} stemmed C{normalized_word}.
    """

    return self._stemmer.stem(normalized_word)

