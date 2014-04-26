# -*- encoding: utf-8 -*-

import exceptions

class KBTokenizerI(object):
  """Interface of a sentence and word tokenizer.
  """

  def tokenizeSentences(self, text):
    """Tokenizes a text into sentences.

    Args:
      text: The C{string} text to tokenize.

    Returns:
      The ordered C{list} of every C{string} sentence of the C{text}.
    """

    raise exceptions.NotImplementedError()

  def tokenizeWords(self, sentences):
    """Tokenizes sentences into word lists.

    Args:
      sentences: The C{list} of C{string} sentences to tokenize.

    Returns:
      The ordered C{list} of sentences represented as C{list}s of C{string}
      words.
    """

    raise exceptions.NotImplementedError()

