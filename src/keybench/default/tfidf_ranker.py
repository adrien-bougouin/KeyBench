#!/usr/bin/env python
# -*- encoding utf-8 -*-

import math
from keybench.ranker import RankerC
from keybench.default.util import document_frequencies
from keybench.default.util import inverse_document_frequencies

class TFIDFRanker(RankerC):
  """
  Component performing candidate terms ranking based on the TF-IDF weight of
  their words.
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               debug,
               inverse_document_frequencies,
               scoring_function):
    """
    Constructor of the component.

    @param  name:                         The name of the ranker.
    @type   name:                         C{string}
    @param  is_lazy:                      True if the component can load
                                          previous datas, false if everything
                                          must be computed tought it has already
                                          been computed.
    @type   is_lazy:                      C{boolean}
    @param  lazy_directory:               The directory used for caching.
    @type   lazy_directory:               C{string}
    @param  debug:                        True if the component is in debug
                                          mode, else False. When the component
                                          is in debug mode, it will output each
                                          step of its processing.
    @type   debug:                        C{bool}
    @param  inverse_document_frequencies: The inverse document frequencies of
                                          each word that can appear in a
                                          candidate term.
    @type   inverse_document_frequencies: C{dict: string -> float}
    @param  scoring_function:             Function wich gives a score to a
                                          candidate according to its words.
    @type   scoring_function:             C{func(string: term, dict(string ->
                                          float): word_weights, string:
                                          tag_separator) : float}
    """

    super(TFIDFRanker, self).__init__(name, is_lazy, lazy_directory, debug)

    self._inverse_document_frequencies = inverse_document_frequencies
    self._scoring_function = scoring_function

  def weighting(self, pre_processed_file, candidates, clusters):
    """
    Takes a pre-processed text (list of POS-tagged sentences) and give a weight
    to its candidates keyphrases.

    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}
    @param    candidates:         The candidates to be keyphrases.
    @type     candidates:         C{list of string}
    TODO clusters
    TODO clusters

    @return:  A dictionary of terms as key and weight as value.
    @rtype:   C{dict: string -> float}
    """

    word_counts = {}
    weighted_words = {}
    weighted_candidates = {}

    # get the words counts
    for w in pre_processed_file.full_text_words():
      # no tags in the weights
      w = w.lower().rsplit(pre_processed_file.tag_separator(), 1)[0]

      if not word_counts.has_key(w):
        word_counts[w] = 0.0
      word_counts[w] += 1.0

    # compute only the needed words' tf*idf
    for c in candidates:
      for w in c.split():
        # no tags in the weights
        w = w.lower().rsplit(pre_processed_file.tag_separator(), 1)[0]

        if not weighted_words.has_key(w):
          tf = word_counts[w]
          idf = self._inverse_document_frequencies[w]
          weighted_words[w] = tf * math.log10(idf)

    # compute the candidate scores
    for c in candidates:
      weighted_candidates[c] = self._scoring_function(c,
                                                      weighted_words,
                                                      pre_processed_file.tag_separator())

    return weighted_candidates

  def ordering(self, weights, clusters):
    """
    Takes the weighted terms of the analysed text and ordered them such as the
    first termes are the one with the best weight.

    @param    weights: A dictionary of weighted terms.
    @type     weights: C{dict: string -> float}
    TODO clusters
    TODO clusters

    @return:  A ordered list of weighted terms.
    @rtype:   C{list of (string, float)}
    """

    return sorted(weights.items(), key=lambda row: row[1], reverse=True)

