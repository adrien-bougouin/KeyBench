from nltk.stem import snowball
from os import path

from keybench.main.nlp_tool import interface
from keybench.main import language

KEYBENCH_DIRECTORY = path.join(path.dirname(__file__), "..", "..", "..")
THIRD_PARTY_TOOL_DIRECTORY = path.join(KEYBENCH_DIRECTORY, "third_party_tools")
STANFORD_DIRECTORY = path.join(THIRD_PARTY_TOOL_DIRECTORY,
                               "pos_tagger",
                               "stanford")
STANFORD_MODEL_DIRECTORY = path.join(STANFORD_DIRECTORY, "models")
STANFORD_JAR = path.join(STANFORD_DIRECTORY, "stanford-postagger.jar")

class StanfordPOSTagger(interface.KBPOSTaggerI):
  """Stanford Part-of-Speech tagger.

  Stanford Part-of-Speech tagger. It currently only supports English
  (C{keybench.main.language.KBLanguage.ENGLISH}).
  """

  def __init__(self, language, encoding):
    """Constructor.

    Args:
      language: The C{string} name of the language of the data to treat (see
        C{keybench.main.language.KBLanguage.ENGLISH}).
      encoding: The C{string} encoding of the data to treat.
    """

    language_model = None
    if language == language.KBLanguage.ENGLISH:
      language_model = path.join(STANFORD_MODEL_DIRECTORY,
                                 "english-bidirectional-distsim.tagger")
      self._tagset = {
        interface.KBPOSTaggerI.POSTagKey.NOUN:          ["NN", "NNS"],
        interface.KBPOSTaggerI.POSTagKey.PROPER_NOUN:   ["NNP", "NNPS"],
        interface.KBPOSTaggerI.POSTagKey.ADJECTIVE:     ["JJ", "JJR", "JJS"],
        interface.KBPOSTaggerI.POSTagKey.VERB:          ["VB", "VBD", "VBG",
                                                         "VBN", "VBP", "VBZ"],
        interface.KBPOSTaggerI.POSTagKey.ADVERB:        ["RB", "RBR", "RBS",
                                                         "WRB"],
        interface.KBPOSTaggerI.POSTagKey.PRONOUN:       ["PRP", "PRP$", "WP",
                                                         "WP$"],
        interface.KBPOSTaggerI.POSTagKey.PREPOSITION:   ["IN"],
        interface.KBPOSTaggerI.POSTagKey.DETERMINER:    ["DT", "WDT"],
        interface.KBPOSTaggerI.POSTagKey.NUMBER:        ["CC"],
        interface.KBPOSTaggerI.POSTagKey.FOREIGN_WORD:  ["FW"],
        interface.KBPOSTaggerI.POSTagKey.PUNCTUATION:   ["PUNCT"]
      }

    self._pos_tagger = POSTagger(language_model, STANFORD_JAR, encoding)

  def tag(self, tokenized_sentences):
    """POS tags tokenized sentences.

    Args:
      tokenized_sentences: The C{list} of tokenized sentences (C{list}s of
      C{string} words).

    Returns:
      The C{list} of sentences' POS tags. POS tags of one sentence is a C{list}
      of C{string} tags.
    """

    pos_tagged_sentences = []

    for word_tag_sentence in self._pos_tagger.batch_tag(tokenized_sentences):
      pos_tagged_sentence = []

      for word, tag in word_tag_sentence:
        if word == tag:
          pos_tagged_sentence.append("PUNCT")
        else:
          pos_tagged_sentence.append(tag)

      pos_tagged_sentences.append(pos_tagged_sentence)

    return pos_tagged_sentences

