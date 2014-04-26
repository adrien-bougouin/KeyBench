# -*- encoding: utf-8 -*-

import codecs
import os

from datetime import datetime
from nltk import data
from os import path

from keybench.main.nlp_tool import interface

KEYBENCH_DIRECTORY = path.join(path.dirname(__file__), "..", "..", "..", "..")
THIRD_PARTY_TOOL_DIRECTORY = path.join(KEYBENCH_DIRECTORY, "third_party_tools")
BONSAI_DIRECTORY = path.join(THIRD_PARTY_TOOL_DIRECTORY,
                             "tokenizer",
                             "bonsai")
BONSAI_EXEC = path.join(BONSAI_DIRECTORY, "bonsai_tokenizer.pl")

class FrenchBonsaiTokenizer(interface.KBTokenizerI):
  """Sentence and word tokenizer.

  Sentence and word tokenizer using the NLTK's C{punkt} module for sentence
  tokenization and the bonsai word tokenizer for word tokenization.
  """

  def __init__(self, encoding):
    """Constructor.
    """

    super(FrenchBonsaiTokenizer, self).__init__()

    self._sentence_tokenizer = data.load('tokenizers/punkt/french.pickle')
    self._encoding = encoding

  def tokenizeSentences(self, text):
    """Tokenizes a text into sentences.

      Args:
        text: The C{string} text to tokenize.

      Returns:
        The ordered C{list} of every C{string} sentence of the C{text}.
    """

    if text != "":
      return self._sentence_tokenizer.tokenize(text)

    return []

  def tokenizeWords(self, sentences):
    """Tokenizes sentences into word lists.

    Args:
      sentences: The C{list} of C{string} sentences to tokenize.

    Returns:
      The ordered C{list} of sentences represented as C{list}s of C{string}
      words.
    """


    tokenized_sentences = []
    input_filepath = ".bonsai_%s_%s_input.tmp"%(
                       hash(str(sentences)),
                       hash(datetime.today().ctime())
                     )
    output_filepath = ".bonsai_%s_%s_output.tmp"%(
                        hash(str(sentences)),
                        hash(datetime.today().ctime())
                      )

    # write input
    input_file = codecs.open(input_filepath, "w", self._encoding)

    for sentence in sentences:
      input_file.write("%s\n"%(sentence))
    input_file.close()

    # POS tagging
    os.system("%s %s > %s"%(BONSAI_EXEC, input_filepath, output_filepath))

    output_file = codecs.open(output_filepath, "r", self._encoding)
    for sentence in output_file.read().splitlines():
      tokenized_sentences.append(sentence.split(" "))
    output_file.close()

    # remove input and output files
    os.remove(input_filepath)
    os.remove(output_filepath)

    return tokenized_sentences

