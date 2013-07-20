#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from benchmark_component import BenchmarkComponent
from exceptions import NotImplementedError
from os import path

class SelectorC(BenchmarkComponent):
  """
  Component responsible of the selection of the candidate keyphrases.
  """

  def __init__(self, name, is_lazy, lazy_directory):
    """
    """

    super(SelectorC, self).__init__(name,
                                    is_lazy,
                                    path.join(lazy_directory, "selections"))

  def select(self,
             filepath,
             pre_processed_file,
             ranked_candidates,
             clusters):
    """
    Selects the keyphrases among weighted terms.

    @param    filepath:           The path of the analysed file.
    @type     filepath:           C{string}
    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}
    @param    ranked_candidates:  The list of the file's ranked candidates and
                                  their weight.
    @type     ranked_candidates:  C{list of (string, float)}
    TODO clusters
    TODO clusters

    @return:  A list of keyphrases.
    @rtype:   C{list of string}
    """

    lazy_filename = path.split(filepath)[1] + ".key"
    keyphrases = []

    if super(SelectorC, self).is_lazy() \
       and super(SelectorC, self).is_cached(lazy_filename):
      keyphrases = super(SelectorC, self).load(lazy_filename)
    else:
      # selection
      super(SelectorC,
            self).log("Selecting the keyphrases among %s's terms..."%filepath)
      weighted_keyphrases = self.selection(pre_processed_file,
                                           ranked_candidates, clusters)

      # remove weights
      keyphrases = []
      for k, w in weighted_keyphrases:
        keyphrases.append(k)

      # serialization
      super(SelectorC,
            self).log("Puting %s's keyphrases into cache..."%filepath)
      super(SelectorC,
            self).store(lazy_filename, keyphrases)

      # save string representation
      super(SelectorC,
            self).log("Saving the readable list of %s's keyphrases..."%filepath)
      string_rep = ""
      for k in keyphrases:
        if string_rep != "":
          string_rep += "\n"
        string_rep += k
      super(SelectorC, self).store_string(lazy_filename, string_rep)

    return keyphrases

  def selection(self, pre_processed_file, ranked_candidates, clusters):
    """
    Selects the keyphrases among weighted terms.

    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}
    @param    ranked_candidates:  The list of the file's ranked candidates and
                                  their weight.
    @type     ranked_candidates:  C{list of (string, float)}
    TODO clusters
    TODO clusters

    @return:  A list of weihgted keyphrases.
    @rtype:   C{list of (string, float)}
    """

    raise NotImplementedError()

