#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import math
import sys
from keybench import CandidateClustererC
from util import hierarchical_clustering

################################################################################
# HierarchicalClusterer

class HierarchicalClusterer(CandidateClustererC):
  """
  """

  def __init__(self, name, is_lazy, lazy_directory, stemmer):
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
    TODO stemmer
    TODO stemmer
    """

    super(HierarchicalClusterer, self).__init__(name,
                                                is_lazy,
                                                lazy_directory)

    self._stemmer = stemmer

  def candidate_clustering(self, pre_processed_file, candidates):
    """
    """

    clusters = hierarchical_clustering(candidates,
                                       pre_processed_file.tag_separator(),
                                       self._stemmer)

    return clusters

