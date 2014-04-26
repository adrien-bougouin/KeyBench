# -*- encoding: utf-8 -*-

from nltk.stem import wordnet

from keybench.main.nlp_tool import interface

class EnglishWordNetLemmatizer(interface.KBLemmatizerI):
  """WordNet lemmatizer for English.
  """

  def __init__(self):
    super(EnglishWordNetLemmatizer, self).__init__()

    self._lemmatizer = wordnet.WordNetLemmatizer()

  def lemmatize(self, normalized_word, tag, dedicated_tag=None):
    """Lemmatizes a normalized word.

    Args:
      normalized_word: The C{string} word to lemmatize. It mus be normalized
        first.
      tag: The C{string} POS tag of the C{normalized_word} (see
        C{keybench.main.nlp_tool.interface.KBPOSTaggerI.POSKey}).
      dedicated_tag: The C{string} pos tag return by the C{KBPOSTagger}. This
        C{dedicated_tag} is optionnal and can be used by lemmatizers made to
        work with a specific C{KBPOSTagger}.

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

