#!/usr/bin/env python
# -*- encoding utf-8 -*-

from keybench.selector import SelectorC

class WholeSelector(SelectorC):
  """
  Component performing selection of the keyphrases among the ranked candidates.
  The all set of candidates are selected. Candidates are ordered to allow
  further cut-off.
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

    super(WholeSelector, self).__init__(name, is_lazy, lazy_directory, debug)

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

    return ranked_candidates

