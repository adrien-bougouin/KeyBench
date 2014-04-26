# -*- encoding: utf-8 -*-

import codecs
import os
import string

from datetime import datetime
from os import path

from keybench.main.nlp_tool import interface
from keybench.main import language_support

KEYBENCH_DIRECTORY = path.join(path.dirname(__file__), "..", "..", "..", "..")
THIRD_PARTY_TOOL_DIRECTORY = path.join(KEYBENCH_DIRECTORY, "third_party_tools")
MELT_DIRECTORY = path.join(THIRD_PARTY_TOOL_DIRECTORY,
                           "pos_tagger",
                           "melt")
MELT_MODEL_DIRECTORY = path.join(MELT_DIRECTORY, "data")
MELT_EXEC = path.join(MELT_DIRECTORY, "MElt_tagger.py")

class MEltPOSTagger(interface.KBPOSTaggerI):
  """MElt Part-of-Speech tagger.

  MElt Part-of-Speech tagger. It currently only supports French
  (C{keybench.main.language_support.KBLanguage.FRENCH}) and English
  (C{keybench.main.language_support.KBLanguage.English}).
  """

  def __init__(self, language, encoding):
    """Constructor.

    Args:
      language: The C{string} name of the language of the data to treat (see
        C{keybench.main.language_support.KBLanguage}).
      encoding: The C{string} encoding of the data to treat.
    """

    super(MEltPOSTagger, self).__init__()

    self._melt_command = ""
    self._encoding = encoding

    if language == language_support.KBLanguage.FRENCH:
      model_directory = path.join(MELT_MODEL_DIRECTORY, "fr")
      self._melt_command = "python %s -m %s -d %s -l %s -e %s"%(
                             MELT_EXEC,
                             model_directory,
                             path.join(model_directory, "tag_dict.json"),
                             path.join(model_directory, "lexicon.json"),
                             encoding
                           )
      self._tagset = {
        interface.KBPOSTaggerI.POSTagKey.NOUN:          ["NC"],
        interface.KBPOSTaggerI.POSTagKey.PROPER_NOUN:   ["NPP"],
        interface.KBPOSTaggerI.POSTagKey.ADJECTIVE:     ["ADJ", "ADJWH"],
        interface.KBPOSTaggerI.POSTagKey.VERB:          ["V", "VIMP", "VINF",
                                                         "VS", "VPP", "VPR"],
        interface.KBPOSTaggerI.POSTagKey.ADVERB:        ["ADV", "ADVWH"],
        interface.KBPOSTaggerI.POSTagKey.COORDINATION:  ["CC"],
        interface.KBPOSTaggerI.POSTagKey.PRONOUN:       ["PRO", "PROREL",
                                                         "PROWH", "CLO", "CLR",
                                                         "CLS"],
        interface.KBPOSTaggerI.POSTagKey.PREPOSITION:   ["P"],
        interface.KBPOSTaggerI.POSTagKey.DETERMINER:    ["DET", "DETWH"],
        interface.KBPOSTaggerI.POSTagKey.NUMBER:        [],
        interface.KBPOSTaggerI.POSTagKey.FOREIGN_WORD:  ["ET"],
        interface.KBPOSTaggerI.POSTagKey.PUNCTUATION:   ["PONCT"]
      }
    elif language == language_support.KBLanguage.ENGLISH:
      model_directory = path.join(MELT_MODEL_DIRECTORY, "en")
      self._melt_command = "python %s -m %s -d %s -l %s -e %s"%(
                             MELT_EXEC,
                             model_directory,
                             path.join(model_directory, "tag_dict.json"),
                             path.join(model_directory, "lexicon.json"),
                             encoding
                           )
      self._tagset = {
        interface.KBPOSTaggerI.POSTagKey.NOUN:          ["NN", "NNS"],
        interface.KBPOSTaggerI.POSTagKey.PROPER_NOUN:   ["NNP", "NNPS"],
        interface.KBPOSTaggerI.POSTagKey.ADJECTIVE:     ["JJ", "JJR", "JJS"],
        interface.KBPOSTaggerI.POSTagKey.VERB:          ["VB", "VBD", "VBP",
                                                         "VBZ", "VBN", "VBG"],
        interface.KBPOSTaggerI.POSTagKey.ADVERB:        ["RB", "RBR", "RBS",
                                                         "WRB"],
        interface.KBPOSTaggerI.POSTagKey.COORDINATION:  ["CC"],
        interface.KBPOSTaggerI.POSTagKey.PRONOUN:       ["PRP", "PRP$", "WP",
                                                         "WP$"],
        interface.KBPOSTaggerI.POSTagKey.PREPOSITION:   ["IN"],
        interface.KBPOSTaggerI.POSTagKey.DETERMINER:    ["DT", "WDT"],
        interface.KBPOSTaggerI.POSTagKey.NUMBER:        ["CC"],
        interface.KBPOSTaggerI.POSTagKey.FOREIGN_WORD:  ["FW"],
        interface.KBPOSTaggerI.POSTagKey.PUNCTUATION:   ["PUNCT"]
      }

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
    input_filepath = ".melt_%s_%s_input.tmp"%(
                       hash(str(tokenized_sentences)),
                       hash(datetime.today().ctime())
                     )
    output_filepath = ".melt_%s_%s_output.tmp"%(
                        hash(str(tokenized_sentences)),
                        hash(datetime.today().ctime())
                      )

    # write input
    input_file = codecs.open(input_filepath, "w", self._encoding)

    for tokenized_sentence in tokenized_sentences:
      input_file.write("%s\n"%(" ".join(tokenized_sentence)))
    input_file.close()

    # POS tagging
    os.system("%s %s > %s 2> /dev/null"%(self._melt_command,
                                         input_filepath,
                                         output_filepath))

    # read output (<word>/<tag> <word>/<tag> ...)
    output_file = codecs.open(output_filepath, "r", self._encoding)
    for sentence in output_file.read().splitlines():
      tags = []
      for wt in sentence.split(" "):
        tags.append(wt.rsplit("/", 1)[1])
      pos_tagged_sentences.append(tags)
    output_file.close()

    # remove input and output files
    os.remove(input_filepath)
    os.remove(output_filepath)

    return pos_tagged_sentences

