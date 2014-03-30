from keybench.main.nlp_tool import interface

class LowercaseNormalizer(interface.KBNormalizerI):
  """Phrase normalizer.

  Phrase normalizer that transforms every phraseinto a lowercased phrase.
  """

  def normalize(self, phrase):
    """Normalizes a phrase by making it lowercased.

    Args:
      phrase: The C{string} phrase to normalize.

    Returns:
      The C{string} normalized form of the given C{phrase}.
    """

    return phrase.lower()

