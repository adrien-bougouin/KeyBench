#!/usr/bin/env python
# -*- encoding utf-8 -*-

from keybench.selector import SelectorC

class WholeSelector(SelectorC):
  """
  Component performing selection of the keyphrases among the ranked candidate
  terms.
  """

  def __init__(self, name, is_lazy, lazy_directory):
    """
    Constructor of the component.

    @param  name:           The name of the selector.
    @type   name:           C{string}
    @param  is_lazy:        True if the component can load previous datas, false
                            if everything must be computed tought it has already
                            been computed.
    @type   is_lazy:        C{boolean}
    @param  lazy_directory: The directory used for caching.
    @type   lazy_directory: C{string}
    """

    super(WholeSelector, self).__init__(name, is_lazy, lazy_directory)

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

    @return:  A list of weighted keyphrases.
    @rtype:   C{list of (string, float)}
    """

    return ranked_candidates

