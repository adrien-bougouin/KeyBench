#!/usr/bin/env python
# -*- encoding utf-8 -*-

from keybench.candidate_extractor import CandidateExtractorC
from keybench.default.util import n_grams
from keybench.default.util import n_to_m_grams

class NGramExtractor(CandidateExtractorC):
  """
  Component performing candidate terms extraction. It extracts 1..n-grams.
  """

  def __init__(self, name, is_lazy, lazy_directory, debug, n):
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
    @param  debug:          True if the component is in debug mode, else False.
                            When the component is in debug mode, it will output
                            each step of its processing.
    @type   debug:          C{bool}
    @param  n:              The maximum size of a candidate term
    @type   n:              C{int}
    """

    super(NGramExtractor, self).__init__(name, is_lazy, lazy_directory, debug)

    self._n = n

  def candidate_extraction(self, pre_processed_file):
    """
    Extract the candidate terms (wanna be keyphrases) from a pre-processed file.

    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}

    @return:  A list of terms.
    @rtype:   C{list of string}
    """

    words = pre_processed_file.full_text_words()
    candidates = []
    
    for term in n_to_m_grams(words, 1, self._n):
      if self.filtering(term, pre_processed_file.tag_separator()):
        candidates.append(term)

    return candidates

  def filtering(self, term, tag_separator):
    """
    Says if a term can be concidered as a candidate term.

    @param    candidate:      The POS tagged candidate.
    @type     candidate:      C{string}
    @param    tag_separator:  The character used to separate a words from its
                              tag.
    @type     tag_separator:  C{string}

    @return:  True if the term is a candidate term, else False.
    @rtype:   C{bool}
    """

    return True

