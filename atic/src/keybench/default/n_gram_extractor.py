#!/usr/bin/env python
# -*- encoding utf-8 -*-

from keybench.candidate_extractor import CandidateExtractorC
from keybench.default.util import n_grams
from keybench.default.util import n_to_m_grams

class NGramExtractor(CandidateExtractorC):
  """
  Component performing candidate terms extraction. It extracts 1..n-grams.
  Component performing keyphrase candidate extraction. It extracts n-grams for
  n in {1..4}.
  """

  def __init__(self, name, is_lazy, lazy_directory, debug, n):
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
    @param  n:              The maximum size of a candidate term
    @type   n:              C{int}
    """

    super(NGramExtractor, self).__init__(name, is_lazy, lazy_directory, debug)

    self.set_n(n)

  def n(self):
    """
    Getter of the maximum n-gram size.

    @return:  The maximum size of the extracted n-grams.
    @rtype:   C{int}
    """

    return self._n

  def set_n(self, n):
    """
    Setter of the maximum n-gram size.

    @param  n: The new maximum size of the extracted n-grams.
    @type   n: C{int}
    """

    self._n = n

  def candidate_extraction(self, pre_processed_file):
    """
    Extracts the candidates from a pre-processed file.

    @param    pre_processed_file: The pre-processed analysed file.
    @type     pre_processed_file: C{PreProcessedFile}

    @return:  A list of candidates.
    @rtype:   C{list(string)}
    """

    candidates = []

    for sentence in pre_processed_file.full_text():
      words = sentence.split()
      
      for term in n_to_m_grams(words, 1, self.n()):
        if self.filtering(term, pre_processed_file.tag_separator()):
          candidates.append(term)

    return candidates

  def filtering(self, term, tag_separator):
    """
    Indicates if a candidate can be concidered as a keyphrase candidate or not.

    @param    candidate:      The POS tagged candidate.
    @type     candidate:      C{string}
    @param    tag_separator:  The character used to separate a words from its
                              tag.
    @type     tag_separator:  C{string}

    @return:  True if the candidate is a keyphrase candidate, else False.
    @rtype:   C{bool}
    """

    return True

