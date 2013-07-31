#!/usr/bin/env python
# -*- encoding utf-8 -*-

import math
from keybench import RankerC
from graph_based_ranking import TextRank
from graph_based_ranking import TopicRankStrategy
from util import cluster_centroid

################################################################################
# TextRankRanker

################################################################################

class TextRankRanker(RankerC):
  """
  Component performing candidate terms ranking based on the TextRank qcore of
  their words.
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               debug,
               strategy,
               scoring_function):
    """
    Constructor of the component.

    @param  name:             The name of the ranker.
    @type   name:             C{string}
    @param  is_lazy:          True if the component can load previous datas,
                              false if everything must be computed tought it has
                              already been computed.
    @type   is_lazy:          C{boolean}
    @param  lazy_directory:   The directory used for caching.
    @type   lazy_directory:   C{string}
    @param  debug:            True if the component is in debug mode, else
                              False. When the component is in debug mode, it
                              will output each step of its processing.
    @type   debug:            C{bool}
    @param  strategy:         The strategy to use with the TextRank algorithm.
    @type   strategy:         C{textrank.TextRankStrategy}
    @param  scoring_function: Function wich gives a score to a
                              candidate according to its words.
    @type   scoring_function: C{func(string: term, dict(string ->
                              float): word_weights, string:
                              tag_separator) : float}
    """

    super(TextRankRanker, self).__init__(name, is_lazy, lazy_directory, debug)

    self._strategy = strategy
    self._textrank = TextRank(strategy,
                              scoring_function,
                              0.0001,
                              0.85,
                              1000000)

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

    # sheat to reset clusters for TopicRank
    if isinstance(self._textrank.strategy(), TopicRankStrategy):
      self._strategy.set_clusters(clusters)
    ranking = self._textrank.rank(candidates, pre_processed_file.full_text())
    weighted_candidates = {}

    for candidate, score in ranking:
      weighted_candidates[candidate] = score

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

    ordered_terms = []

    if not isinstance(self._textrank.strategy(), TopicRankStrategy):
      ordered_terms = sorted(weights.items(),
                             key=lambda row: row[1],
                             reverse=True)
    else:
      clusters = self._textrank.strategy().token_ids().values()

      # extraction the best candidate term per cluster
      for cluster in clusters:
        # ordering and untagging of the termes of the clusters
        untagged_cluster = []

        for term in cluster:
          untagged_term = ""

          for wt in term.split():
            w = wt.rsplit(self._textrank.strategy().tag_separator(), 1)[0]

            if untagged_term != "":
              untagged_term += " "
            untagged_term += w

          untagged_cluster.append(untagged_term)
        untagged_cluster = self.cluster_ordering(untagged_cluster)

        # adding the best keyphrase of the cluster
        cluster_keyphrase = untagged_cluster[0]
        cluster_score = weights[untagged_cluster[0]]

        ordered_terms.append((cluster_keyphrase, cluster_score))
      ordered_terms = sorted(ordered_terms,
                             key=lambda (t, s): (s),
                             reverse=True)

    return ordered_terms

  def cluster_ordering(self, cluster):
    """
    """

    text = self._textrank.strategy().context()
    sentence_length_accumulator = 0
    first_positions = {}
    frequency = {}

    #####
    fake_pos_tagged_cluster = []
    for term in cluster:
      tagged = ""

      for w in term.split():
        if tagged != "":
          tagged += " "
        tagged += w + self._textrank.strategy().tag_separator() + "fk"
      fake_pos_tagged_cluster.append(tagged)
    tagged_centroid = cluster_centroid(fake_pos_tagged_cluster, self._textrank.strategy().tag_separator(), self._textrank.strategy().stemmer())
    centroid = ""
    for i, term in enumerate(fake_pos_tagged_cluster):
      if term == tagged_centroid:
        centroid = cluster[i]
    #####

    for sentence in text:
      untagged_sentence = ""

      for wt in sentence.split():
        w = wt.rsplit(self._textrank.strategy().tag_separator(), 1)[0]

        if untagged_sentence != "":
          untagged_sentence += " "
        untagged_sentence += w

      for term in cluster:
        pos = untagged_sentence.find(term)

        if pos >= 0:
          if not first_positions.has_key(term):
            first_positions[term] = sentence_length_accumulator + (pos + 1)

          if not frequency.has_key(term):
            frequency[term] = 0.0
          frequency[term] += 1.0

      sentence_length_accumulator += len(untagged_sentence)

    return sorted(cluster, key=lambda (t): (first_positions[t],
                                            -1 * len(t.split())))
    #return sorted(cluster, key=lambda (t): (frequency[t],
    #                                        -1 * len(t.split())))
    #return sorted(cluster, key=lambda (t): (t != centroid,
    #                                        -1 * len(t.split())))

