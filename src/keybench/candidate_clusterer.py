#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from benchmark_component import BenchmarkComponent
from exceptions import NotImplementedError
from os import path

class CandidateClustererC(BenchmarkComponent):
  """
  Component responsible of the candidate clustering.
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

    super(CandidateClustererC, self).__init__(name,
                                              is_lazy,
                                              path.join(lazy_directory,
                                                        "clusters"),
                                              debug)

  def cluster_candidates(self, filepath, pre_processed_file, candidates):
    """
    Clusters the candidates that have been extracted from an analysed file.

    @param    filepath:           The path of the analysed file.
    @type     filepath:           C{string}
    @param    pre_processed_file: The pre-processed analysed file.
    @type     pre_processed_file: C{PreProcessedFile}
    @param    candidates:         The candidates to cluster.
    @type     candidates:         C{list(string)}

    @return:  A list of clusters (lists of candidates).
    @rtype:   C{list(list(string))}
    """

    lazy_filename = path.split(filepath)[1] + ".clr"
    clusters = []

    if super(CandidateClustererC, self).is_lazy() \
       and super(CandidateClustererC, self).is_cached(lazy_filename):
      clusters = super(CandidateClustererC, self).load(lazy_filename)
    else:
      # extraction
      super(CandidateClustererC,
            self).log("Clustering candidates of %s..."%filepath)
      clusters = self.candidate_clustering(pre_processed_file, candidates)

      # serialization
      super(CandidateClustererC,
            self).log("Puting %s's clusters into cache..."%filepath)
      super(CandidateClustererC,
            self).store(lazy_filename, clusters)

      # store string representation
      super(CandidateClustererC,
            self).log("Saving the readable list of %s's clusters..."%filepath)
      string_rep = ""
      for c in clusters:
        if string_rep != "":
          string_rep += "\n"
        string_rep += str(c)
      super(CandidateClustererC, self).store_string(lazy_filename, string_rep)

    return clusters

  def candidate_clustering(self, pre_processed_file, candidates):
    """
    Clusters the candidates that have been extracted from an analysed file.

    @param    pre_processed_file: The pre-processed analysed file.
    @type     pre_processed_file: C{PreProcessedFile}
    @param    candidates:         The candidates to cluster.
    @type     candidates:         C{list(string)}

    @return:  A list of clusters (lists of candidates).
    @rtype:   C{list((string))}
    """

    raise NotImplementedError()

