#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from keybench.candidate_clusterer import CandidateClustererC
from os import path

class FakeClusterer(CandidateClustererC):
  """
  Component performing candidate clustering. It do not really clusters
  candidates. In fact, each candidate represent one cluster.
  """

  def candidate_clustering(self, pre_processed_file, candidates):
    """
    Clusters the candidates that have been extracted from an analysed file.

    @param    pre_processed_file: The pre-processed analysed file.
    @type     pre_processed_file: C{PreProcessedFile}
    @param    candidates:         The candidates to cluster.
    @type     candidates:         C{list(string)}

    @return:  A list of clusters (lists of candidates).
    @rtype:   C{list(list(string))}
    """

    clusters = []

    for c in candidates:
      clusters.append([c])

    return clusters

