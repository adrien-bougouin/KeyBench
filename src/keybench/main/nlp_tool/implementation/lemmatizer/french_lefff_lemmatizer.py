import codecs

from nltk.stem import wordnet
from os import path

from keybench.main.nlp_tool import interface

KEYBENCH_DIRECTORY = path.join(path.dirname(__file__), "..",  "..", "..", "..")
THIRD_PARTY_TOOL_DIRECTORY = path.join(KEYBENCH_DIRECTORY, "third_party_tools")
LEFFF_DIRECTORY = path.join(THIRD_PARTY_TOOL_DIRECTORY, "lemmatizer", "lefff")
LEFFF_LEMMA_FILEPATH = path.join(LEFFF_DIRECTORY, "lefff_lemmas.tsv")

class FrenchLeFFFLemmatizer(interface.KBLemmatizerI):
  """LeFFF lemmatizer for French.
  
  French lemmatizer that uses the LeFFF linguistic resource.
  """

  def __init__(self):
    super(FrenchLeFFFLemmatizer, self).__init__()

    self._lemmas = {}

    # parse the lefff lemma file
    lemma_file = codecs.open(LEFFF_LEMMA_FILEPATH, "r", "utf-8")

    is_reading_header = True
    for word_pos_lemma in lemma_file.read().splitlines():
      if not is_reading_header and word_pos_lemma != "":
        word, pos, lemma = word_pos_lemma.split("\t")

        if word not in self._lemmas:
          self._lemmas[word] = {}
        if pos not in self._lemmas[word]:
          self._lemmas[word][pos] = []
        self._lemmas[word][pos].append(lemma)
      elif word_pos_lemma == "# END OF TERMS AND CONDITIONS":
        is_reading_header = False

    lemma_file.close()

  @property
  def lemmas(self):
    return self._lemmas

  def lemmatize(self, normalized_word, tag, dedicated_tag=None):
    """Lemmatizes a normalized word.

    Args:
      normalized_word: The C{string} word to lemmatize. It must be normalized
        first
      tag: The C{string} POS tag of the C{normalized_word} (see
        C{keybench.main.nlp_tool.interface.KBPOSTaggerI.POSKey}).
      dedicated_tag: The C{string} pos tag return by the C{KBPOSTagger}. This
        C{dedicated_tag} is optionnal and can be used by lemmatizers made to
        work with a specific C{KBPOSTagger}.

    Returns:
      The C{string} lemmatized C{normalized_word}.
    """

    if tag == interface.KBPOSTaggerI.POSTagKey.NOUN:
      pos = "nc"
    elif tag == interface.KBPOSTaggerI.POSTagKey.PROPER_NOUN:
      pos = "np"
    elif tag == interface.KBPOSTaggerI.POSTagKey.ADJECTIVE:
      pos = "adj"
    elif tag == interface.KBPOSTaggerI.POSTagKey.VERB:
      pos = "v"
    elif tag == interface.KBPOSTaggerI.POSTagKey.ADVERB:
      pos = "adv"
    elif tag == interface.KBPOSTaggerI.POSTagKey.COORDINATION:
      pos = "coo"
    elif tag == interface.KBPOSTaggerI.POSTagKey.PREPOSITION:
      pos = "prep"
    else:
      return normalized_word

    try:
      # FIXME
      # same ambiguity resolution than the nltk.stem.wordnet.WordNetLemmatizer
      return min(self._lemmas[normalized_word][pos], key=len)
    except:
      return normalized_word

