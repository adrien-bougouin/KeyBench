#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from benchmark_component import BenchmarkComponent
from exceptions import NotImplementedError
from os import path

class RankerC(BenchmarkComponent):
  """
  Component responsible of the candidates' ranking.
  """

  def __init__(self, name, is_lazy, lazy_directory):
    """
    """

    super(RankerC, self).__init__(name,
                                  is_lazy,
                                  path.join(lazy_directory, "rankings"))

  def rank(self, filepath, pre_processed_file, candidates, clusters):
    """
    Weights and ordered the terms of a pre-processed text.

    @param    filepath:           The path of the analysed file.
    @type     filepath:           C{string}
    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}
    @param    candidates:         The candidates to be keyphrases.
    @type     candidates:         C{list of string}
    TODO clusters
    TODO clusters

    @return:  A list of terms and their weight (no more POS tags).
    @rtype:   C{list of (string, float)}
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
    Takes a pre-processed text (list of POS-tagged sentences) and give a weight
    to its candidates keyphrases.

    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}
    @param    candidates:         The candidates to be keyphrases.
    @type     candidates:         C{list of string}
    TODO clusters
    TODO clusters

    @return:  A dictionary of terms as key and weight as value.
    @rtype:   C{dict: string -> float}
    """

    raise NotImplementedError()

  def ordering(self, weights, clusters):
    """
    Takes the weighted terms of the analysed text and ordered them such as the
    first termes are the one with the best weight.

    @param    weights: A dictionary of weighted terms.
    @type     weights: C{dict: string -> float}
    TODO clusters
    TODO clusters

    @return:  A ordered list of weighted terms.
    @rtype:   C{list of (string, float)}
    """

    raise NotImplementedError()

