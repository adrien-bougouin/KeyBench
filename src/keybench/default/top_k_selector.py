#!/usr/bin/env python
# -*- encoding utf-8 -*-

from keybench.selector import SelectorC

class TopKSelector(SelectorC):
  """
  Component performing selection of the k-best keyphrases among the ranked
  candidates.
  """

  def __init__(self, name, is_lazy, lazy_directory, debug, k):
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
    @param  k:              The number of best candidates to select.
    @type   k:              C{int}
    """

    super(TopKSelector, self).__init__(name, is_lazy, lazy_directory, debug)

    self.set_k(k)

  def k(self):
    """
    Getter of the number of candidates to select.

    @return:  The number of candidates to select as keyphrases.
    @rtype:   C{int}
    """

    return self._k

  def set_k(self, k):
    """
    Setter of the number of candidates to select.

    @param  k: The new number of candidates to select as keyphrases.
    @type   k: C{int}
    """

    self._k = k

  def selection(self, pre_processed_file, ranked_candidates, clusters):
    """
    Selects the keyphrases among the ordered and weighted candidates.

    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}
    @param    ranked_candidates:  The list of the file's ranked candidates and
                                  their weight.
    @type     ranked_candidates:  C{list(tuple(string, float))}
    @param    clusters:           The clustered candidates.
    @type     clusters:           C{list(list(string))}

    @return:  A list of weihgted keyphrases.
    @rtype:   C{list(tuple(string, float))}
    """

    limit = min(ranked_candidates, self._k)

    return ranked_candidates[:limit]

