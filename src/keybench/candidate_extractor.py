#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from benchmark_component import BenchmarkComponent
from exceptions import NotImplementedError
from os import path

class CandidateExtractorC(BenchmarkComponent):
  """
  Component responsible of the term filtering. Only the given candidates can be
  selected as keyphrases.
  """

  def __init__(self, name, is_lazy, lazy_directory):
    """
    """

    super(CandidateExtractorC, self).__init__(name,
                                              is_lazy,
                                              path.join(lazy_directory,
                                                        "candidates"))

  def extract_candidates(self, filepath, pre_processed_file):
    """
    Extract the candidate terms (wanna be keyphrases) from a pre-processed file.

    @param    filepath:           The path of the analysed file.
    @type     filepath:           C{string}
    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}

    @return:  A list of terms.
    @rtype:   C{list of string}
    """

    lazy_filename = path.split(filepath)[1] + ".cdt"
    candidates = []

    if super(CandidateExtractorC, self).is_lazy() \
       and super(CandidateExtractorC, self).is_cached(lazy_filename):
      candidates = super(CandidateExtractorC, self).load(lazy_filename)
    else:
      # extraction
      super(CandidateExtractorC,
            self).log("Extracting candidates of %s..."%filepath)
      candidates = self.candidate_extraction(pre_processed_file)

      # serialization
      super(CandidateExtractorC,
            self).log("Puting %s's candidates into cache..."%filepath)
      super(CandidateExtractorC,
            self).store(lazy_filename, candidates)

      # store string representation
      super(CandidateExtractorC,
            self).log("Saving the readable list of %s's candidates..."%filepath)
      string_rep = ""
      for c in candidates:
        if string_rep != "":
          string_rep += "\n"
        string_rep += c
      super(CandidateExtractorC, self).store_string(lazy_filename, string_rep)

    return candidates

  def candidate_extraction(self, pre_processed_file):
    """
    Extract the candidate terms (wanna be keyphrases) from a pre-processed file.

    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}

    @return:  A list of terms.
    @rtype:   C{list of string}
    """

    raise NotImplementedError()

