# -*- encoding: utf-8 -*-

import exceptions

class KBLemmatizerI(object):
  """Interface of a word lemmatizer.
  """

  def lemmatize(self, normalized_word, tag, dedicated_tag=None):
    """Lemmatizes a normalized word.

    Args:
      normalized_word: The C{string} word to lemmatize. It must be lemmatized
        first.
      tag: The C{string} POS tag key of the C{normalized_word} (see
        C{keybench.main.nlp_tool.interface.KBPOSTaggerI.POSKey}).
      dedicated_tag: The C{string} pos tag return by the C{KBPOSTagger}. This
        C{dedicated_tag} is optionnal and can be used by lemmatizers made to
        work with a specific C{KBPOSTagger}.

    Returns:
      The C{string} lemmatized C{normalized_word}.
    """

    raise exceptions.NotImplementedError()

