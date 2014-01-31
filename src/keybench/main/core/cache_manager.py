import os
import pickle

from os import path

from keybench.main import exception

class KBCacheManager(object):
  """

  Attributes:
  """

  def __init__(self, cache_directory):
    super(KBCacheManager, self).__init__()

    self._cache_directory = cache_directory

    if not path.exists(self._cache_directory):
      os.makedirs(self._cache_directory)

  def __eq__(self, other):
    return self._cache_directory == other._cache_directory

  def __ne__(self, other):
    return not self.__eq__(other)

  @property
  def cache_directory(self):
    return self._cache_directory

  def exists(self, identifier):
    """
    """

    return path.exists(path.join(self._cache_directory, identifier))

  def store(self, identifier, obj):
    """
    """

    filepath = path.join(self._cache_directory, identifier)

    with open(filepath, "w") as cache_file:
      pickle.dump(obj, cache_file)

  def storeString(self, identifier, obj, parser):
    """
    """

    # TODO
    pass

  # TODO exception
  def load(self, identifier):
    """
    Raises:
    """

    if self.exists(identifier):
      filepath = path.join(self._cache_directory, identifier)
      cached_object = None

      with open(filepath, "r") as cached_file:
        cached_object = pickle.load(cached_file)

      return cached_object
    else:
      raise exception.KBCacheException(self._cache_directory,
                                       identifier,
                                       "Identifier does not exists!")

  # TODO exception
  def loadFromString(self, identifier, parser):
    """
    Raises
    """

    # TODO
    pass

