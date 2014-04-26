# -*- encoding: utf-8 -*-

import re

from nltk.tokenize import punkt

from keybench.main.nlp_tool import interface

class EnglishPunktTokenizer(interface.KBTokenizerI):
  """Sentence and word tokenizer.

  Sentence and word tokenizer using the NLTK's C{punkt} module.
  """

  def __init__(self):
    """Constructor.
    """

    super(EnglishPunktTokenizer, self).__init__()

    self._sentence_tokenizer = punkt.PunktSentenceTokenizer()
    self._word_tokenizer = punkt.PunktWordTokenizer()

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

    for sentence in sentences:
      tokenized_sentence = self._word_tokenizer.tokenize(sentence)

      # split the unsplitted "."
      if tokenized_sentence[-1].find(".") == len(tokenized_sentence[-1]) - 1:
        tokenized_last_word = re.sub(r"(\.+)$", r" \1", tokenized_sentence[-1])
        w1 = tokenized_last_word.rsplit(" ", 1)[0]
        w2 = tokenized_last_word.rsplit(" ", 1)[1]

        tokenized_sentence[-1] = w1
        tokenized_sentence.append(w2)

      tokenized_sentences.append(tokenized_sentence)

    return tokenized_sentences

