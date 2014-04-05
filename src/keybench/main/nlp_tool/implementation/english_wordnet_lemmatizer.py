from nltk.stem import wordnet

from keybench.main.nlp_tool import interface

class EnglishWordNetLemmatizer(interface.KBLemmatizerI):
  """WordNet lemmatizer for English.
  """

  def __init__(self):
    super(EnglishWordNetLemmatizer, self).__init__()

    self._lemmatizer = wordnet.WordNetLemmatizer()

  def lemmatize(self, normalized_word, tag):
    """Lemmatizes a normalized word.

    Args:
      normalized_word: The C{string} word to lemmatize. It mus be normalized
        first.
      tag: The C{string} POS tag of the C{normalized_word} (see
        C{keybench.main.nlp_tool.interface.KBPOSTaggerI.POSKey}).

    Returns:
      The C{string} lemmatized C{normalized_word}.
    """

    if tag == interface.KBPOSTaggerI.POSTagKey.NOUN:
      pos = "n"
    elif tag == interface.KBPOSTaggerI.POSTagKey.ADJECTIVE:
      pos = "a"
    elif tag == interface.KBPOSTaggerI.POSTagKey.VERB:
      pos = "v"
    elif tag == interface.KBPOSTaggerI.POSTagKey.ADVERB:
      pos = "r"
    else:
      return normalized_word

    return self._lemmatizer.lemmatize(normalized_word, pos)

