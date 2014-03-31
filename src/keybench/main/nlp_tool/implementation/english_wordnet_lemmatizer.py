from nltk.stem import wordnet

from keybench.main.nlp_tool import interface

class EnglishWordNetLemmatizer(interface.KBLemmatizerI):
  """WordNet lemmatizer for English.
  """

  def __init__(self):
    super(EnglishWordNetLemmatizer, self).__init__()

    self._lemmatizer = wordnet.WordNetLemmatizer()

  def lemmatize(self, word, tag):
    """lemmatizes a word.

    Args:
      word: The C{string} word to lemmatize.
      tag: The C{string} POS tag of the C{word} (see
        C{keybench.main.nlp_tool.interface.KBPOSTaggerI.POSKey}).

    Returns:
      The C{string} lemmatized C{word}.
    """

    pos = "n"

    if tag == interface.KBPOSTaggerI.POSTagKey.ADJECTIVE:
      pos = "a"
    elif tag == interface.KBPOSTaggerI.POSTagKey.VERB:
      pos = "v"
    elif tag == interface.KBPOSTaggerI.POSTagKey.ADVERB:
      pos = "r"

    return self._lemmatizer.lemmatize(word, pos)

