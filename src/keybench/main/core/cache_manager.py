# -*- encoding: utf-8 -*-

import codecs
import os
import pickle

from exceptions import NotImplementedError
from os import path

from keybench.main import exception

class KBCacheManager(object):
  """A tool to manage object into cache.

  A tool that stores objects into a cache directory. Objects can be stored using
  either C{pickle} or a string parser (C{CacheParserI}).

  Attributes:
    cache_directory: The C{string} path to the directory where the cached
      objects must be stored.
  """
  
  ##############################################################################
  class CacheParserI(object):
    """An C{object} to C{string} and C{string} to C{object} converter.
    """

    def toString(self, obj):
      """Represents a given object as a string.

      Args:
        obj: The C{object} to convert as a C{string}.
      """

      raise NotImplementedError()

    def fromString(self, obj_string):
      """Parses a string to produce the represented object.

      Args:
        obj_string: The C{string} representation of an C{object}.

      Returns:
        The C{object} represented by the C{obj_string} C{string}.
      """

      raise NotImplementedError()
  ##############################################################################

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
    """Checks if an object as been cached using a given identifier.

    Args:
      identifier: A unique C{string} used to identify a cached C{object}.

    Returns:
      True if an C{object} is cached using the C{identifier}. False, otherwise.
    """

    return path.exists(path.join(self._cache_directory, identifier))

  def store(self, identifier, obj):
    """Puts an object into cache.

    Stores an object within the cache directory using a given identifier.

    Args:
      identifier: The C{string} identifier representing the C{object} to store.
      obj: The C{object} to store into the C{cache_directory}.
    """

    filepath = path.join(self._cache_directory, identifier)

    with open(filepath, "w") as cache_file:
      pickle.dump(obj, cache_file)

  def storeString(self, identifier, obj, encoding, parser=None):
    """Puts an object into cache.

    Stores an object within the cache directory using a given identifier. The
    object is converted as a string.

    Args:
      identifier: The C{string} identifier representing the C{object} to store.
      obj: The C{object} to store into the C{cache_directory}.
      encoding: The C{string} encoding of the stringified C{object}.
      parser: The C{CacheParserI} parser to use for the C{string} convertion
        (default=None => the object is a string).
    """

    filepath = path.join(self._cache_directory, identifier)

    with codecs.open(filepath, "w", encoding) as cache_file:
      if parser == None:
        cache_file.write(obj)
      else:
        cache_file.write(parser.toString(obj))

  def load(self, identifier):
    """Gives an object stored in cache.

    Gives an object stored within the C{cache_directory}.

    Args:
      identifier: The C{string} identifier representing the C{object} to load.

    Returns:
      The C{object} stored for the given C{identifier}.

    Raises:
      KBCacheException: An exception occurred when there is no C{object} stored
        for the given C{identifier}.
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

  def loadFromString(self, identifier, encoding, parser=None):
    """Gives an object stored in cache.

    Gives an object stored within the C{cache_directory}. The object is stored
    as a string representation.

    Args:
      identifier: The C{string} identifier representing the C{object} to load.
      encoding: The C{string} encoding of the stringified C{object}.
      parser: The C{CacheParserI} parser to use to create an C{object}
        represented by a C{string} (default=None => the object is a string).

    Returns:
      The C{object} stored for the given C{identifier}.

    Raises:
      KBCacheException: An exception occurred when there is no C{object} stored
        for the given C{identifier}.
    """

    if self.exists(identifier):
      filepath = path.join(self._cache_directory, identifier)
      cached_object = None

      with codecs.open(filepath, "r", encoding) as cached_file:
        if parser == None:
          cached_object = cached_file.read()
        else:
          cached_object = parser.fromString(cached_file.read())

      return cached_object
    else:
      raise exception.KBCacheException(self._cache_directory,
                                       identifier,
                                       "Identifier does not exists!")

