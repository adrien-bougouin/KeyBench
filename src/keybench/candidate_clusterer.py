#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from benchmark_component import BenchmarkComponent
from exceptions import NotImplementedError
from os import path

class CandidateClustererC(BenchmarkComponent):
  """
  """

  def __init__(self, name, is_lazy, lazy_directory):
    """
    Constructor of the component.

    @param  name:           The name of the pre-processor.
    @type   name:           C{string}
    @param  is_lazy:        True if the component can load previous datas, false
                            if everything must be computed tought it has already
                            been computed.
    @type   is_lazy:        C{boolean}
    @param  lazy_directory: The directory used for caching.
    @type   lazy_directory: C{string}
    """

    super(CandidateClustererC, self).__init__(name,
                                              is_lazy,
                                              path.join(lazy_directory,
                                                        "clusters"))

  def cluster_candidates(self, filepath, pre_processed_file, candidates):
    """
    Extract the candidate terms (wanna be keyphrases) from a pre-processed file.

    @param    filepath:           The path of the analysed file.
    @type     filepath:           C{string}
    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}
    TODO CANDIDATES
    TODO CANDIDATES

    @return:  A list of terms.
    @rtype:   C{list of string}
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
    """

    raise NotImplementedError()

