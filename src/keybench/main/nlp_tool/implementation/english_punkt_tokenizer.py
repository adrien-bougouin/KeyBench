from nltk.tokenize import punkt

from keybench.main.nlp_tool import interface

class EnglishPunktTokenizer(interface.KBTokenizerI):
  """Sentence and word tokenizer.

  Sentence and word tokenizer using the NLTK's C{punct} module.
  """

  def __init__(self):
    """Constructor.
    """

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
      tokenized_sentences.append(self._word_tokenizer.tokenize(sentence))

    return tokenized_sentences

