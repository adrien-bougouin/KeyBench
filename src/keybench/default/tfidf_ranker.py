#!/usr/bin/env python
# -*- encoding utf-8 -*-

import math
from keybench.ranker import RankerC
from keybench.default.util import document_frequencies
from keybench.default.util import inverse_document_frequencies

class TFIDFRanker(RankerC):
  """
  Component performing keyphrase candidate ranking based on the TF-IDF weight of
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

    @param  name:                         The name of the component.
    @type   name:                         C{string}
    @param  is_lazy:                      True if the component must load
                                          previous data, False if data must be
                                          computed tought they have already been
                                          computed.
    @type   is_lazy:                      C{bool}
    @param  lazy_directory:               The directory used to store previously
                                          computed data.
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
    @param  scoring_function:             Function that gives a score to a
                                          candidate according to its words.
    @type   scoring_function:             C{function(expression, word_weights,
                                          tag_separator): float}
    """

    super(TFIDFRanker, self).__init__(name, is_lazy, lazy_directory, debug)

    self.set_inverse_document_frequencies(inverse_document_frequencies)
    self.set_scoring_function(scoring_function)

  def inverse_document_frequencies(self):
    """
    Getter of the inverse document frequencies of the words.

    @return:  The inverse of the number of documents (in a particular corpus) in
              which the words appear.
    @rtype:   C{dict(string, float)}
    """

    return self._inverse_document_frequencies

  def set_inverse_document_frequencies(self, inverse_document_frequencies):
    """
    Setter of the inverse document frequencies of the words.

    @param  inverse_document_frequencies: The new inverse of the number of
                                          documents (in a particular corpus) in
                                          which the words appear.
    @type   inverse_document_frequencies: C{dict(string, float)}
    """

    self._inverse_document_frequencies = inverse_document_frequencies

  def scoring_function(self):
    """
    Getter of the function used to compute the scores of the multi-word
    expression, based on the single words TF-IDF weight.

    @return:  The function that gives a score to a candidate according to its
              words.
    @rtype:   C{function(expression, word_weights, tag_separator): float}
    """

    return self._scoring_function

  def set_scoring_function(self, scoring_function):
    """
    Setter of the function used to compute the scores of the multi-word
    expression, based on the single words TF-IDF weight.

    @param  scoring_function: The new function that gives a score to a candidate
                              according to its words.
    @type   scoring_function: C{function(expression, word_weights,
                              tag_separator): float}
    """

    self._scoring_function = scoring_function

  def weighting(self, pre_processed_file, candidates, clusters):
    """
    Takes a pre-processed text (list of POS-tagged sentences) and give a weight
    to its keyphrase candidates.

    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}
    @param    candidates:         The keyphrase candidates.
    @type     candidates:         C{list(string)}
    @param    clusters:           The clustered candidates.
    @type     clusters:           C{list(list(string))}

    @return:  A dictionary of terms as key and weight as value.
    @rtype:   C{dict(string, float)}
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
          idf = self.inverse_document_frequencies()[w]
          weighted_words[w] = tf * math.log10(idf)

    # compute the candidate scores
    for c in candidates:
      weighted_candidates[c] = self._scoring_function(c,
                                                      weighted_words,
                                                      pre_processed_file.tag_separator())

    return weighted_candidates

  def ordering(self, weights, clusters):
    """
    Takes the weighted candidates of the analysed text and ordered them such as
    the first ones have the highest weight.

    @param    weights:  A dictionary of weighted candidates.
    @type     weights:  C{dict(string, float)}
    @param    clusters: The clustered candidates.
    @type     clusters: C{list(list(string))}

    @return:  A ordered list of weighted terms.
    @rtype:   C{list(tuple(string, float))}
    """

    return sorted(weights.items(), key=lambda row: row[1], reverse=True)

