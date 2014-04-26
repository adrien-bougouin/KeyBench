# -*- encoding: utf-8 -*-

import string
import time

from os import path

from keybench.main import core
from keybench.main import exception

class KBComponent(object):
  """The base class of a component.

  The base class of a KeyBench component. It provides methods to easilly access
  cache objects through the C{KBCacheManager}. A component can only work on one
  run. If two components have the same name, they can share the cached data if
  they are defined to be shared.

  Attributes:
    name: The C{string} name of the component.
    run_name: The C{string} name of the run for which the component is affected
      to.
  """

  def __init__(self,
               name,
               run_name,
               shared,
               lazy_mode,
               debug_mode,
               root_cache):
    """Constructor.

    Args:
      name: The C{string} name of the component.
      run_name: The C{string} name of the run for which the component is
        affected to.
      shared: True if the component shares informations with equivalent
        components (same name).
      lazy_mode: True if the component load precomputed data. False, otherwise.
      debug_mode: True if the component can log debug messages. False,
        otherwise.
      root_cache: The root of the cache directory where the cached objects must
        be stored.
    """

    super(KBComponent, self).__init__()

    self._name = name
    self._run_name = run_name
    cache_directory = root_cache
    if shared:
      cache_directory = path.join(cache_directory, "shared", name)
    else:
      cache_directory = path.join(cache_directory, run_name, name)
    self._cache_manager = core.KBCacheManager(cache_directory)
    self._lazy_mode = lazy_mode
    self._debug_mode = debug_mode

  def __eq__(self, other):
    return self._name == other._name \
           and self._run_name == other._run_name \
           and self._cache_manager == other._cache_manager \
           and self._lazy_mode == other._lazy_mode \
           and self._debug_mode == other._debug_mode

  def __ne__(self, other):
    return not self.__eq__(other)

  def __documentIdentifier(self, document):
    """Creates a unique cache identifier for the document.

    Args:
      document: The C{KBDocument} to identify.

    Returns:
      The unique C{string} identifier that represents the given C{document}.
    """

    valid_chars = "_%s%s" % (string.ascii_letters, string.digits)
    raw_identifier = "%s_%s"%(document.corpus_name.lower(),
                              document.name.lower())
    identifier = ""

    for char in raw_identifier:
      if char in valid_chars:
        identifier += char
      else:
        identifier += "_"

    return identifier

  @property
  def name(self):
    return self._name

  @property
  def run_name(self):
    return self._run_name

  def isLazy(self):
    """Says if the component is lazy.

    Says if the component is lazy. A lazy component can load cached data.

    Returns:
      True if the the component is lazy. False, otherwise.
    """

    return self._lazy_mode

  def logDebug(self, message):
    """Prints a debug message.

    Prints a debug message if the component has been configured has been told to
    be in C{debug_mode}.
    """

    if self._debug_mode:
      print "[%s] %s:%s (%s) >> %s"%(time.strftime("%x %X"),
                                     self._name,
                                     self.__class__.__name__,
                                     self._run_name,
                                     message)

  def exists(self, document):
    """Checks if an object as been cached, by the component, for a given
    document.

    Args:
      document: The document to check.

    Returns:
      True if an C{object} is cached for the given C{document}. False,
      otherwise.
    """

    return self._cache_manager.exists(self.__documentIdentifier(document))

  def store(self, document, obj):
    """Puts an object into cache.

    Stores an object within the cache directory using an identifier computed for
    the given document (associated to the object to put into cache).

    Args:
      document: The document associated with the object to put into cache.
      obj: The C{object} to store into the C{cache_directory}.
    """

    self._cache_manager.store(self.__documentIdentifier(document), obj)

  def storeString(self, document, obj, parser, encoding):
    """Puts an object into cache.

    Stores an object within the cache directory using an identifier computed for
    the given document (associated to the object to put into cache). The
    object is converted as a string.

    Args:
      document: The document associated with the object to put into cache.
      obj: The C{object} to store into the C{cache_directory}.
      parser: The C{CacheParserI} parser to use for the C{string} convertion.
      encoding: The C{string} encoding of the stringified C{object}.
    """

    self._cache_manager.storeString(self.__documentIdentifier(document),
                                    obj,
                                    parser,
                                    encoding)

  def load(self, document):
    """Gives an object stored in cache.

    Gives an object stored within the C{cache_directory}.

    Args:
      document: The document associated with the object to load.

    Returns:
      The C{object} stored for the given C{document}.

    Raises:
      KBLazyComponentException: An exception occurred when there is the
        component is has been set to be lazy.
    """

    if self._lazy_mode:
      return self._cache_manager.load(self.__documentIdentifier(document))
    else:
      raise exception.KBLazyComponentException(self._name,
                                               self.__class__.__name__,
                                               self._run_name,
                                               "Not lazy, but loading is required!")

  def loadFromString(self, document, parser, encoding):
    """Gives an object stored in cache.

    Gives an object stored within the C{cache_directory}. The object is stored
    as a string representation.

    Args:
      document: The document associated with the object to load.
      parser: The C{CacheParserI} parser to use to create an C{object}
        represented by a C{string}.
      encoding: The C{string} encoding of the stringified C{object}.

    Returns:
      The C{object} stored for the given C{document}.

    Raises:
      KBLazyComponentException: An exception occurred when there is the
        component is has been set to be lazy.
    """

    if self._lazy_mode:
      return self._cache_manager.loadFromString(self.__documentIdentifier(document),
                                                parser,
                                                encoding)
    else:
      raise exception.KBLazyComponentException(self._name,
                                               self.__class__.__name__,
                                               self._run_name,
                                               "Not lazy, but loading is required!")

