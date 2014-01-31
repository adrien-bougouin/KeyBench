class KBCacheException(Exception):
  """
  """

  def __init__(self, cache_directory, identifier, message):
    """
    Args:
    """

    super(KBCacheException, self).__init__()

    self._message = "Error while storing '%s' within %s: %s"%(identifier,
                                                              cache_directory,
                                                              message)

  def __str__(self):
    return self._message

