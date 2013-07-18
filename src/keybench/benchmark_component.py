#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
import pickle
from os import makedirs
from os import path

class BenchmarkComponent(object):
  """
  Core component of all the keyphrase extractor system's components. This
  component can be run in lazy mode, wich means that the previously computed
  datas will be loaded instead of being computed again.
  """

  def __init__(self, name, is_lazy, lazy_directory):
    """
    Constructor of the component.

    @param  name:           The concrete name of the component.
    @type   name:           C{string}
    @param  is_lazy:        True if the component can load previous datas, false
                            if everything must be computed tought it as already
                            been computed.
    @type   is_lazy:        C{boolean}
    @param  lazy_directory: The directory used for caching.
    @type   lazy_directory: C{string}
    """

    super(BenchmarkComponent, self).__init__()

    self._name = name
    self._is_lazy = is_lazy
    self._lazy_directory = path.join(lazy_directory, name)
    self._string_directory = path.join(self._lazy_directory, "string")

    # create the directory if it does not exist
    if not path.exists(self._lazy_directory):
      makedirs(self._lazy_directory)
    if not path.exists(self._string_directory):
      makedirs(self._string_directory)

  def name(self):
    """
    Gives the name of the component.

    @return:  The name of the component.
    @rtype:   C{string}
    """

    return self._name

  def is_lazy(self):
    """
    Says if the component uses lazy loading or not.

    @return:  True if the component uses lazy loading, else false.
    @rtype:   C{boolean}
    """

    return self._is_lazy

  def lazy_directory(self):
    """
    Gives the directory where the component stores its cached computations.

    @return:  The path of the cache directory of the component.
    @rtype:   C{string}
    """

    return self._lazy_directory

  def is_cached(self, filename):
    """
    Says if a given file exists in the cache directory.

    @param    filename: The name of the file to check.
    @type     filename: C{string}

    @return:  True if the file is already in cache, else False.
    @rtype:   C{boolean}
    """

    filepath = path.join(self._lazy_directory, filename)

    return path.exists(filepath)

  def log(self, message):
    """
    Output a message in a common way for all components of the benchmark system.

    @param  message: The message to display.
    @type   message: C{string}
    """

    print "%s >> %s"%(self._name, message)

  def load(self, filename):
    """
    Load a already stored file representation object.

    @param    filename: The name of the file to load.
    @type     filename: C{string}

    @return:  The representation object of the file.
    @rtype:   C{object}
    """

    filepath = path.join(self._lazy_directory, filename)
    cached_file = open(filepath, "r")
    cached_object = pickle.load(cached_file)

    cached_file.close()

    return cached_object

  def store(self, filename, obj):
    """
    Put the file representation object into the cache (for future lazy loading).

    @param  filename: The name of the file to store in cache.
    @type   filename: C{string}
    @param  obj:      The representation object of the file.
    @type   obj:      C{object}
    """

    filepath = path.join(self._lazy_directory, filename)
    cache_file = open(filepath, "w")

    pickle.dump(obj, cache_file)
    cache_file.close()

  def store_string(self, filename, string_obj):
    """
    Put the representation string into the cache directory.

    @param  filename:   The name of the file to store in cache.
    @type   filename:   C{string}
    @param  string_obj: The representation string to store.
    @type   string_obj: C{object}
    """

    filepath = path.join(self._string_directory, filename)
    string_file = codecs.open(filepath, "w", "utf-8")

    string_file.write(string_obj)
    string_file.close()

