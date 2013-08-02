#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class LINKAGE_STRATEGY:
  SINGLE    = 0
  AVERAGE   = 1
  COMPLETE  = 2

def simple_word_overlap_similarity(stemmed_term1, stemmed_term2):
  """
  Computes the overlap similarity between two stemmed terms.

  @param    stemmed_term_1: The first term.
  @type     stemmed_term_1: C{string}
  @param    stemmed_term_2: The second term.
  @type     stemmed_term_2: C{string}

  @return:  The overlap similarity computed between the two terms.
  @rtype:   C{float}
  """

  stems1 = stemmed_term1.split()
  stems2 = stemmed_term2.split()

  intersection = set(stems1) & set(stems2)
  union = set(stems1) | set(stems2)

  return (float(len(intersection)) / float(len(union)))

def pos_tagged_term_stemming(pos_tagged_term, tag_separator, stemmer):
  """
  Provides the stemmed version of a POS tagged term.

  @param    pos_tagged_term:  The POS tagged term to stem.
  @type     pos_tagged_term:  C{string}
  @param    tag_separator:    The symbol use to separate a word from its POS
                              tag.
  @type     tag_separator:    C{string}
  @param    stemmer:          The stemmer use to stemmed the words.
  @type     stemmer:          C{nltk.stem.api.StemmerI

  @return:  The stemmed version of the term.
  @rtype:   C{string}
  """

  stem = ""

  for wt in pos_tagged_term.split():
    w = wt.rsplit(tag_separator, 1)[0]

    if stem != "":
      stem += " "
    stem += stemmer.stem(w)

  return stem

def hierarchical_clustering(mode,
                            threshold,
                            pos_tagged_terms,
                            tag_separator,
                            stemmer):
  """
  @param    mode:             The linkage strategy to use for the clustering.
                              - Single: The similarity between two clusters is
                              equal to the minimum similarity among all the
                              similarities between every elements of each
                              cluster.
                              - Average: The similarity between two clusters is
                              equal to the average of all the similarities
                              between every elements of each cluster.
                              - Complete: The similarity between two clusters is
                              equal to the maximum similarity among all the
                              similarities between every elements of each
                              cluster.
  @type     mode:             C{LINKAGE_STRATEGY}
  @param    threshold:        The similarity threshold to respect when
                              clustering.
  @type     threshold:        C{float}
  @param    pos_tagged_terms: The list of POS tagged terms.
  @type     pos_tagged_terms: C{list(string)}
  @param    tag_separator:    The symbol used to separate a word from its POS
                              tag.
  @type     tag_separator:    C{string}
  @param    stemmer:          The stemmer used to stem words.
  @type     stemmer:          C{nltk.stem.api.StemmerI}

  @return:
  @rtype:
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
  for term in pos_tagged_terms:
    stem = pos_tagged_term_stemming(term, tag_separator, stemmer)
    lazy_stems[term] = stem
    lazy_t_t_sims[stem] = {}
    lazy_max_t_n_sims[stem] = {}
    lazy_average_t_n_sims[stem] = {}
    lazy_min_t_n_sims[stem] = {}

    nodes.append([term])

  # start the clustering
  stabilized = False
  while not stabilized:
    best_node1 = []
    best_node1_index = 0
    best_node2 = []
    best_node2_index = 0
    best_sim = -1.0

    ##### computing all similarity pairs #######################################
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
            for term1 in node1:
              stem1 = lazy_stems[term1]
              max_sim_t1_n2 = 0.0
              average_sim_t1_n2 = 0.0
              min_sim_t1_n2 = 1.0

              if not lazy_max_t_n_sims[stem1].has_key(key2):
                for term2 in node2:
                  stem2 = lazy_stems[term2]
                  sim_t1_t2 = 0.0

                  # compute the similarity between stem1 and stem2
                  if not lazy_t_t_sims[stem1].has_key(stem2):
                    sim_t1_t2 = simple_word_overlap_similarity(stem1, stem2)
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
            if mode == LINKAGE_STRATEGY.SINGLE:
              sim_n1_n2 = min_sim_n1_n2
            else:
              if mode == LINKAGE_STRATEGY.AVERAGE:
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

    ##### selecting the nodes to group #########################################
    if best_sim >= threshold:
      nodes.pop(best_node1_index)
      # the index is decreased after the best_node1 removal
      nodes.pop(best_node2_index - 1)

      for term in best_node2:
        best_node1.append(term)
      nodes.append(best_node1)
    else:
      stabilized = True

  # reordered so the first nodes are the last created
  nodes.reverse()
  return nodes

def cluster_centroid(cluster, tag_separator, stemmer):
  """
  Computes the centroid of a cluster according to the overlap similarity between
  its elements.

  @param    cluster:        The cluster from which obtain the centroid.
  @type     cluster:        C{list(list(string))}
  @param    tag_separator:  The symbol used to separate a word from its POS tag.
  @type     tag_separator:  C{string}
  @param    stemmer:        The stemmer used to stem words.
  @type     stemmer:        C{nltk.stem.api.StemmerI}

  @return:  The centroid of the cluster.
  @rtype:   C{string}
  """

  max_similarity = -1.0

  for term1 in cluster:
    stem1 = pos_tagged_term_stemming(term1, tag_separator, stemmer)
    similarity = 0.0

    for term2 in cluster:
      stem2 = pos_tagged_term_stemming(term2, tag_separator, stemmer)

      try:
        similarity += simple_word_overlap_similarity(stem1)(stem2)
      except:
        similarity += 0.0
    similarity /= float(len(cluster))

    if similarity > max_similarity:
      max_similarity = similarity
      centroid = term1

  return centroid

