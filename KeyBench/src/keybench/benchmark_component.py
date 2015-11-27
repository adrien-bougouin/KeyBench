#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
import pickle
from os import makedirs
from os import path

class BenchmarkComponent(object):
  """
  Core component of all the keyphrase extraction system. A benchmark component
  can be run in lazy mode, i.e. the previously computed datas will be loaded
  instead of being computed again (data are stored with C{pickle}).
  """

  def __init__(self, name, is_lazy, lazy_directory, debug=False):
    """
    Constructor of the component.

    @param  name:           The name of the component.
    @type   name:           C{string}
    @param  is_lazy:        True if the component must load previous data, False
                            if data must be computed tought they have already
                            been computed.
    @type   is_lazy:        C{bool}
    @param  lazy_directory: The directory used to store previously computed
                            data.
    @type   lazy_directory: C{string}
    @param  debug:          True if the component is in debug mode, else False.
                            When the component is in debug mode, it will output
                            each step of its processing.
    @type   debug:          C{bool}
    """

    super(BenchmarkComponent, self).__init__()

    self._name = name
    self._lazy_directory = path.join(lazy_directory, name)
    self._string_directory = path.join(self.lazy_directory(), "string")
    self._is_lazy = is_lazy
    self._debug = debug

    # create the directory if it does not exist
    if not path.exists(self.lazy_directory()):
      makedirs(self.lazy_directory())
    if not path.exists(self.string_directory()):
      makedirs(self.string_directory())

  def name(self):
    """
    Getter of the name of the component.

    @return:  The name of the component.
    @rtype:   C{string}
    """

    return self._name

  def is_lazy(self):
    """
    Getter of the lazyness property of the component.

    @return:  True if the component uses lazy loading, else False.
    @rtype:   C{bool}
    """

    return self._is_lazy

  def lazy_directory(self):
    """
    Getter of the directory path where the component stores the previously
    computed data.

    @return:  The path of the cache directory of the component.
    @rtype:   C{string}
    """

    return self._lazy_directory

  def string_directory(self):
    """
    Getter of the directory path where the component stores the stringified
    previously computed data.

    @return:  The path of the string version of the component's cache
              directory.
    @rtype:   C{string}
    """

    return self._string_directory

  def debug(self):
    """
    Getter of the debug mode of the document.

    @return:  True if the component is in debug mode, else False.
    @rtype:   C{bool}
    """

    return self._debug

  def set_debug(self, debug):
    """
    """

    self._debug = debug

  def is_cached(self, filename):
    """
    Indicate if a given file exists in the cache directory.

    @param    filename: The name of the file to check.
    @type     filename: C{string}

    @return:  True if the file is already in cache, else False.
    @rtype:   C{bool}
    """

    filepath = path.join(self.lazy_directory(), filename)

    return path.exists(filepath)

  def log(self, message):
    """
    Output a message in a common way for all components of the benchmark system.

    @param  message: The message to display.
    @type   message: C{string}
    """

    if self.debug():
      print "%s >> %s"%(self.name(), message)

  def load(self, filename):
    """
    Load an already stored file.

    @param    filename: The name of the file to load.
    @type     filename: C{string}

    @return:  The object representing the file.
    @rtype:   C{object}
    """

    filepath = path.join(self.lazy_directory(), filename)
    cached_file = open(filepath, "r")
    cached_object = pickle.load(cached_file)

    cached_file.close()

    return cached_object

  def store(self, filename, obj):
    """
    Stores the object, representing an analysed file, into the cache (for future
    lazy loading).

    @param  filename: The name of the file.
    @type   filename: C{string}
    @param  obj:      The object which represents the file.
    @type   obj:      C{object}
    """

    filepath = path.join(self.lazy_directory(), filename)
    cache_file = open(filepath, "w")

    pickle.dump(obj, cache_file)
    cache_file.close()

  def store_string(self, filename, string_obj):
    """
    Stores the object, representing an analysed file, as a string into the
    cache.

    @param  filename:   The name of the file.
    @type   filename:   C{string}
    @param  string_obj: The string object which represents the file.
    @type   string_obj: C{object}
    """

    filepath = path.join(self.string_directory(), filename)
    string_file = codecs.open(filepath, "w", "utf-8")

    string_file.write(string_obj)
    string_file.close()

