import exceptions

class KBNormalizerI(object):
  """Interface of a phrase normalizer.
  """

  def normalize(self, phrase):
    """Normalizes a phrase.

    Args:
      phrase: The C{string} phrase to normalize.

    Returns:
      The C{string} normalized form of the given C{phrase}.
    """

    raise exceptions.NotImplementedError()

