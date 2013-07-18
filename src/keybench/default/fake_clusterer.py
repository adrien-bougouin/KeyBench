#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from keybench.candidate_clusterer import CandidateClustererC
from os import path

class FakeClusterer(CandidateClustererC):
  """
  """

  def candidate_clustering(self, pre_processed_file, candidates):
    """
    """

    clusters = []

    for c in candidates:
      clusters.append([c])

    return clusters

