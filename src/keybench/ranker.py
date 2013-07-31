#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from benchmark_component import BenchmarkComponent
from exceptions import NotImplementedError
from os import path

class RankerC(BenchmarkComponent):
  """
  Component used to rank keyphrase candidates.
  """

  def __init__(self, name, is_lazy, lazy_directory, debug):
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

    super(RankerC, self).__init__(name,
                                  is_lazy,
                                  path.join(lazy_directory, "rankings"),
                                  debug)

  def rank(self, filepath, pre_processed_file, candidates, clusters):
    """
    Weights and ordered the candidates of a pre-processed text.

    @param    filepath:           The path of the analysed file.
    @type     filepath:           C{string}
    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}
    @param    candidates:         The keyphrase candidates.
    @type     candidates:         C{list(string)}
    @param    clusters:           The clustered candidates.
    @type     clusters:           C{list(list(string))}

    @return:  A list of candidates and their weight (no more POS tags).
    @rtype:   C{list(tuple(string, float))}
    """

    lazy_filename = path.split(filepath)[1] + ".rnk"
    ordered_weights = []

    if super(RankerC, self).is_lazy() \
       and super(RankerC, self).is_cached(lazy_filename):
      ordered_weights = super(RankerC, self).load(lazy_filename)
    else:
      # weighting
      super(RankerC, self).log("Ranking of %s's terms..."%filepath)
      weights = self.weighting(pre_processed_file, candidates, clusters)
      # list cleaning by removing the word tags
      clean_weights = {}
      for t, w in weights.items():
        term = ""
        for wt in t.split():
          if term != "":
            term += " "
          term += wt.rsplit(pre_processed_file.tag_separator(), 1)[0]
        clean_weights[term] = w
      # ordering
      super(RankerC, self).log("Ordering %s's terms..."%filepath)
      ordered_weights = self.ordering(clean_weights, clusters)

      # serialization
      super(RankerC, self).log("Putting %s's terms into cache..."%filepath)
      super(RankerC, self).store(lazy_filename, ordered_weights)

      # save string representation
      super(RankerC,
            self).log("Saving the readable list of %s's terms..."%filepath)
      string_rep = ""
      for c in ordered_weights:
        if string_rep != "":
          string_rep += "\n"
        string_rep += str(c)
      super(RankerC, self).store_string(lazy_filename, string_rep)

    return ordered_weights

  def weighting(self, pre_processed_file, candidates, clusters):
    """
    Takes a pre-processed text (list of POS-tagged sentences) and gives a weight
    to its candidates keyphrases.

    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}
    @param    candidates:         The keyphrase candidates.
    @type     candidates:         C{list(string)}
    @param    clusters:           The clustered candidates.
    @type     clusters:           C{list(list(string))}

    @return:  A dictionary of terms as key and weight as value.
    @rtype:   C{dict(string, float)}
    """

    raise NotImplementedError()

  def ordering(self, weights, clusters):
    """
    Takes the weighted terms of the analysed text and ordered them such as the
    first termes are the one with the best weight.

    @param    weights:  A dictionary of weighted candidates.
    @type     weights:  C{dict(string, float)}
    @param    clusters: The clustered candidates.
    @type     clusters: C{list(list(string))}

    @return:  A ordered list of weighted terms.
    @rtype:   C{list(tuple(string, float))}
    """

    raise NotImplementedError()

