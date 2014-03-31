import string

from nltk.tag import stanford
from os import path

from keybench.main.nlp_tool import interface
from keybench.main import language_support

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
  (C{keybench.main.language_support.KBLanguage.ENGLISH}) and French
  (C{keybench.main.language_support.KBLanguage.FRENCH}).
  """

  def __init__(self, language, encoding):
    """Constructor.

    Args:
      language: The C{string} name of the language of the data to treat (see
        C{keybench.main.language_support.KBLanguage}).
      encoding: The C{string} encoding of the data to treat.
    """

    super(StanfordPOSTagger, self).__init__()

    language_model = None
    if language == language_support.KBLanguage.ENGLISH:
      language_model = path.join(STANFORD_MODEL_DIRECTORY,
                                 "english-bidirectional-distsim.tagger")
      self._tagset = {
        interface.KBPOSTaggerI.POSTagKey.NOUN:          ["NN", "NNS"],
        interface.KBPOSTaggerI.POSTagKey.PROPER_NOUN:   ["NNP", "NNPS"],
        interface.KBPOSTaggerI.POSTagKey.ADJECTIVE:     ["JJ", "JJR", "JJS"],
        interface.KBPOSTaggerI.POSTagKey.VERB:          ["VB", "VBD", "VBP",
                                                         "VBZ", "VBN", "VBG"],
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
    if language == language_support.KBLanguage.FRENCH:
      language_model = path.join(STANFORD_MODEL_DIRECTORY, "french.tagger")
      self._tagset = {
        interface.KBPOSTaggerI.POSTagKey.NOUN:          ["NC"],
        interface.KBPOSTaggerI.POSTagKey.PROPER_NOUN:   ["NP"],
        interface.KBPOSTaggerI.POSTagKey.ADJECTIVE:     ["A"],
        interface.KBPOSTaggerI.POSTagKey.VERB:          ["V"],
        interface.KBPOSTaggerI.POSTagKey.ADVERB:        ["ADV"],
        interface.KBPOSTaggerI.POSTagKey.PRONOUN:       ["PRO", "CL"],
        interface.KBPOSTaggerI.POSTagKey.PREPOSITION:   ["P"],
        interface.KBPOSTaggerI.POSTagKey.DETERMINER:    ["D"],
        interface.KBPOSTaggerI.POSTagKey.NUMBER:        [],
        interface.KBPOSTaggerI.POSTagKey.FOREIGN_WORD:  ["ET"],
        interface.KBPOSTaggerI.POSTagKey.PUNCTUATION:   ["PONCT"]
      }

    self._pos_tagger = stanford.POSTagger(language_model,
                                          STANFORD_JAR,
                                          encoding)

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
        if word == tag \
           or tag in string.punctuation:
          pos_tagged_sentence.append(self._tagset[interface.KBPOSTaggerI.POSTagKey.PUNCTUATION][0])
        else:
          pos_tagged_sentence.append(tag)

      pos_tagged_sentences.append(pos_tagged_sentence)

    return pos_tagged_sentences

