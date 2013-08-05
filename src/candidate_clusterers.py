#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import math
import sys
from keybench import CandidateClustererC

################################################################################
# HierarchicalClusterer

################################################################################

class LINKAGE_STRATEGY:
  SINGLE    = 0
  AVERAGE   = 1
  COMPLETE  = 2

class StemOverlapHierarchicalClusterer(CandidateClustererC):
  """
  Component performing a hierarchical clustering of candidates. The clustering
  is based on an overlap similarity computed with stems. The clustering must be
  achieved only when the similarity is greater than or equal to a given
  threshold.
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               debug,
               mode,
               similarity_threshold,
               stemmer):
    """
    Constructor of the component.

    @param  name:                 The name of the component.
    @type   name:                 C{string}
    @param  is_lazy:              True if the component must load previous data,
                                  False if data must be computed tought they
                                  have already been computed.
    @type   is_lazy:              C{bool}
    @param  lazy_directory:       The directory used to store previously
                                  computed data.
    @type   lazy_directory:       C{string}
    @param  debug:                True if the component is in debug mode, else
                                  False. When the component is in debug mode, it
                                  will output each step of its processing.
    @type   debug:                C{bool}
    @param  mode:                 The linkage strategy to use for the
                                  clustering.
                                  - Single: The similarity between two clusters
                                  is equal to the minimum similarity among all
                                  the similarities between every elements of
                                  each cluster.
                                  - Average: The similarity between two clusters
                                  is equal to the average of all the
                                  similarities between every elements of each
                                  cluster.
                                  - Complete: The similarity between two
                                  clusters is equal to the maximum similarity
                                  among all the similarities between every
                                  elements of each cluster.
    @type   mode:                 C{LINKAGE_STRATEGY}
    @param  similarity_threshold: The similarity threshold to respect when
                                  clustering.
    @type   similarity_threshold: C{float}
    @param  stemmer:              The stemmer used to stem words.
    @type   stemmer:              C{nltk.stem.api.StemmerI}
    """

    super(StemOverlapHierarchicalClusterer, self).__init__(name,
                                                           is_lazy,
                                                           lazy_directory,
                                                           debug)

    self.set_mode(mode)
    self.set_similarity_threshold(similarity_threshold)
    self.set_stemmer(stemmer)

  def mode(self):
    """
    Getter of the linkage mode of the clustering.

    @return:  The strategy used during the hierarchical clustering.
    @rtype:   C{LINKAGE_STRATEGY}
    """

    return self._mode

  def set_mode(self, mode):
    """
    Setter of the linkage mode of the clustering.

    @param  mode: The new strategy used during the hierarchical clustering.
    @type   mode: C{LINKAGE_STRATEGY}
    """

    self._mode = mode

  def similarity_threshold(self):
    """
    Getter of the similarity threshold used during the clustering.

    @return:  The similarity threshold used during the clustering.
    @rtype:   C{float}
    """

    return self._similarity_threshold

  def set_similarity_threshold(self, similarity_threshold):
    """
    Setter of the similarity threshold used during the clustering.

    @param  similarity_threshold: The new similarity threshold used during the
                                  clustering.
    @type   similarity_threshold: C{float}
    """

    self._similarity_threshold = similarity_threshold

  def stemmer(self):
    """
    Getter of the stemmer used to stem words.

    @return:  The stemmer used to stem words.
    @rtype:    C{nltk.stem.api.StemmerI}
    """

    return self._stemmer

  def set_stemmer(self, stemmer):
    """
    Setter of the stemmer used to stem words.

    @param: The new stemmer used to stem words.
    @type:  C{nltk.stem.api.StemmerI}
    """

    self._stemmer = stemmer

  def pos_tagged_candidate_stemming(self, pos_tagged_candidate, tag_separator):
    """
    Provides the stemmed version of a POS tagged candidate.

    @param    pos_tagged_candidate: The POS tagged candidate to stem.
    @type     pos_tagged_candidate: C{string}
    @param    tag_separator:        The symbol used to separate a words from its
                                    POS tag.
    @type     tag_separator:        C{string}

    @return:  The stemmed version of the candidate.
    @rtype:   C{string}
    """

    stem = ""

    for wt in pos_tagged_candidate.split():
      w = wt.rsplit(tag_separator, 1)[0]

      if stem != "":
        stem += " "
      stem += self.stemmer().stem(w)

    return stem

  def simple_word_overlap_similarity(self, expression1, expression2):
    """
    Computes the overlap similarity between two single or multi-word
    expressions.

    @param    expression1: The first single or multi-word expression.
    @type     expression1: C{string}
    @param    expression2: The second single or multi-word expression.
    @type     expression2: C{string}

    @return:  The overlap similarity computed between the two expressions.
    @rtype:   C{float}
    """

    words1 = expression1.split()
    words2 = expression2.split()

    intersection = set(words1) & set(words2)
    union = set(words1) | set(words2)

    return (float(len(intersection)) / float(len(union)))

  def candidate_clustering(self, pre_processed_file, candidates):
    """
    Clusters the candidates that have been extracted from an analysed file.

    @param    pre_processed_file: The pre-processed analysed file.
    @type     pre_processed_file: C{PreProcessedFile}
    @param    candidates:         The candidates to cluster.
    @type     candidates:         C{list(string)}

    @return:  A list of clusters (lists of candidates).
    @rtype:   C{list(list(string))}
    """

    nodes = []
    clusters = {}
    lazy_pairs = {}
    lazy_stems = {}
    lazy_t_t_sims = {}
    lazy_max_t_n_sims = {}
    lazy_average_t_n_sims = {}
    lazy_min_t_n_sims = {}

    # fill the structures for the lazy loading and initialize the nodes
    for candidate in candidates:
      stem = self.pos_tagged_candidate_stemming(candidate,
                                                pre_processed_file.tag_separator())
      lazy_stems[candidate] = stem
      lazy_t_t_sims[stem] = {}
      lazy_max_t_n_sims[stem] = {}
      lazy_average_t_n_sims[stem] = {}
      lazy_min_t_n_sims[stem] = {}

      nodes.append([candidate])

    # start the clustering
    stabilized = False
    while not stabilized:
      best_node1 = []
      best_node1_index = 0
      best_node2 = []
      best_node2_index = 0
      best_sim = -1.0

      ##### computing all similarity pairs #####################################
      for node1_index, node1 in enumerate(nodes):
        key1 = hash(str(node1))

        if not lazy_pairs.has_key(key1):
          lazy_pairs[key1] = {}

        for node2_index, node2 in enumerate(nodes[node1_index:]):
          # the given index is not related to the nodes list (fix it)
          node2_index += node1_index

          if node2 != node1:
            key2 = hash(str(node2))
            max_sim_n1_n2 = 0.0
            average_sim_n1_n2 = 0.0
            min_sim_n1_n2 = 1.0

            if not lazy_pairs.has_key(key2):
              lazy_pairs[key2] = {}

            if not lazy_pairs[key1].has_key(key2):
              for candidate1 in node1:
                stem1 = lazy_stems[candidate1]
                max_sim_t1_n2 = 0.0
                average_sim_t1_n2 = 0.0
                min_sim_t1_n2 = 1.0

                if not lazy_max_t_n_sims[stem1].has_key(key2):
                  for candidate2 in node2:
                    stem2 = lazy_stems[candidate2]
                    sim_t1_t2 = 0.0

                    # compute the similarity between stem1 and stem2
                    if not lazy_t_t_sims[stem1].has_key(stem2):
                      sim_t1_t2 = self.simple_word_overlap_similarity(stem1,
                                                                      stem2)
                      lazy_t_t_sims[stem1][stem2] = sim_t1_t2
                      lazy_t_t_sims[stem2][stem1] = sim_t1_t2
                    else:
                      sim_t1_t2 = lazy_t_t_sims[stem1][stem2]
                    max_sim_t1_n2 = max(max_sim_t1_n2, sim_t1_t2)
                    average_sim_t1_n2 += sim_t1_t2
                    min_sim_t1_n2 = min(min_sim_t1_n2, sim_t1_t2)

                  lazy_max_t_n_sims[stem1][key2] = max_sim_t1_n2
                  lazy_average_t_n_sims[stem1][key2] = average_sim_t1_n2
                  lazy_min_t_n_sims[stem1][key2] = min_sim_t1_n2
                else:
                  max_sim_t1_n2 = lazy_max_t_n_sims[stem1][key2]
                  average_sim_t1_n2 += lazy_average_t_n_sims[stem1][key2]
                  min_sim_t1_n2 = lazy_min_t_n_sims[stem1][key2]

                # re-compute similarities between nodes (clusters)
                max_sim_n1_n2 = max(max_sim_n1_n2, max_sim_t1_n2)
                average_sim_n1_n2 += average_sim_t1_n2
                min_sim_n1_n2 = min(min_sim_n1_n2, min_sim_t1_n2)

              average_sim_n1_n2 /= float(len(node1) * len(node2))

              # choice of the effective similarity according to the mode
              if self.mode() == LINKAGE_STRATEGY.SINGLE:
                sim_n1_n2 = min_sim_n1_n2
              else:
                if self.mode() == LINKAGE_STRATEGY.AVERAGE:
                  sim_n1_n2 = average_sim_n1_n2
                else:
                  sim_n1_n2 = max_sim_n1_n2

              lazy_pairs[key1][key2] = sim_n1_n2
              lazy_pairs[key2][key1] = sim_n1_n2
            else:
              sim_n1_n2 = lazy_pairs[key1][key2]

            if sim_n1_n2 > best_sim:
              best_node1 = node1
              best_node1_index = node1_index
              best_node2 = node2
              best_node2_index = node2_index
              best_sim = sim_n1_n2

      ##### selecting the nodes to group #######################################
      if best_sim >= self.similarity_threshold():
        nodes.pop(best_node1_index)
        # the index is decreased after the best_node1 removal
        nodes.pop(best_node2_index - 1)

        for candidate in best_node2:
          best_node1.append(candidate)
        nodes.append(best_node1)
      else:
        stabilized = True

    # reordered so the first nodes are the last created
    nodes.reverse()
    return nodes

#  def cluster_centroid(cluster, tag_separator, stemmer):
#    """
#    Computes the centroid of a cluster according to the overlap similarity between
#    its elements.
#
#    @param    cluster:        The cluster from which obtain the centroid.
#    @type     cluster:        C{list(list(string))}
#    @param    tag_separator:  The symbol used to separate a word from its POS tag.
#    @type     tag_separator:  C{string}
#    @param    stemmer:        The stemmer used to stem words.
#    @type     stemmer:        C{nltk.stem.api.StemmerI}
#
#    @return:  The centroid of the cluster.
#    @rtype:   C{string}
#    """
#
#    centroid = None
#    max_similarity = -1.0
#
#    for term1 in cluster:
#      stem1 = pos_tagged_term_stemming(term1, tag_separator, stemmer)
#      similarity = 0.0
#
#      for term2 in cluster:
#        stem2 = pos_tagged_term_stemming(term2, tag_separator, stemmer)
#
#        try:
#          similarity += simple_word_overlap_similarity(stem1)(stem2)
#        except:
#          similarity += 0.0
#      similarity /= float(len(cluster))
#
#      if similarity > max_similarity:
#        max_similarity = similarity
#        centroid = term1
#
#    return centroid

