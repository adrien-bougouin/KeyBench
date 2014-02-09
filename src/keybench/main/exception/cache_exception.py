class KBCacheException(Exception):
  """An Exception triggered when an error occurres while managing objects within
  cache.
  """

  def __init__(self, cache_directory, identifier, message):
    """
    Args:
      cache_directory: The C{string} path of the directory where cached_objects
        are stored.
      identifier: The C{string} identifier of the managed C{object}.
      message: A C{string} message describing the occurred exception.
    """

    super(KBCacheException, self).__init__()

    self._message = "Error while storing '%s' within %s: %s"%(identifier,
                                                              cache_directory,
                                                              message)

  def __str__(self):
    return self._message

