# -*- encoding: utf-8 -*-

import codecs
import math
import networkx
import pickle

from keybench import RankerC
from keybench.default import util as keybench_util
from util import semeval2010
from util import duc2001

topicrankpp_graphs = {}
topicrankpp_stemmed_keyphrases = {}

def create_domain_graph(reference_filepath, encoding):
  graph = networkx.DiGraph()
  reference_file = codecs.open(reference_filepath, "r", encoding)

  #-- parse training reference and initialize graph nodes ----------------------
  train_references = {}
  for line in reference_file.readlines():
    line = line.strip()

    if line != "":
      document = line.split("\t", 1)[0]
      keyphrases = line.split("\t", 1)[1].split(";")

      train_references[document] = []

      for keyphrase in keyphrases:
        keyphrase = keyphrase.strip()

        if keyphrase != "":
          train_references[document].append(keyphrase)

          if not graph.has_node(keyphrase):
            graph.add_node(keyphrase, {"type": "keyphrase"})

  reference_file.close()

  #-- document counts of keyphrase pairs ---------------------------------------
  keyphrase_counts = {}
  pair_counts = {}
  nb_documents = 0.0

  for document in train_references:
    document_keyphrases = []

    nb_documents += 1.0

    for keyphrase1 in train_references[document]:
      # keyphrase count
      if keyphrase1 not in document_keyphrases:
        document_keyphrases.append(keyphrase1)

        if keyphrase1 not in keyphrase_counts:
          keyphrase_counts[keyphrase1] = 0.0
        keyphrase_counts[keyphrase1] += 1.0

      # pair count
      associated_keyphrases = []
      for keyphrase2 in train_references[document]:
        if keyphrase1 != keyphrase2:
          if keyphrase2 not in associated_keyphrases:
            associated_keyphrases.append(keyphrase2)

            if keyphrase1 not in pair_counts:
              pair_counts[keyphrase1] = {}
            if keyphrase2 not in pair_counts[keyphrase1]:
              pair_counts[keyphrase1][keyphrase2] = 0.0
            pair_counts[keyphrase1][keyphrase2] += 1.0

  #-- add graph edges ----------------------------------------------------------
  for keyphrase1 in pair_counts:
    for keyphrase2 in pair_counts[keyphrase1]:
      graph.add_edge(keyphrase1, keyphrase2, {"type": "intra", "weight": pair_counts[keyphrase1][keyphrase2] / nb_documents})

  return graph

def add_topicrankpp_graph(key,
                          domain_graph,
                          stemmer):
  # GRAPHS AND MODELS
  topicrankpp_graphs[key] = domain_graph

  # STEMMED KEYPHRASES
  topicrankpp_stemmed_keyphrases[key] = [" ".join(stemmer.stem(w) for w in node.split(" ")) for node in topicrankpp_graphs[key].nodes()]

def word_overlap_similarity(candidate, keyphrase):
    """
    """

    words1 = candidate.split()
    words2 = keyphrase.split()

    intersection = set(words1) & set(words2)
    union = set(words1) | set(words2)

    return (float(len(intersection)) / float(len(union)))

class TopicRankPPRanker(RankerC):
  """
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               debug,
               graphs_and_models_key,
               stemmer,
               lambda_k=0.5, # 0.5 = equi-probability
               lambda_t=0.5, # 0.5 = equi-probability
               nb_controlled_keyphrases=float("inf"),
               convergence_threshold=0.001,
               # TODO test multiple values
               max_iterations=1000000):
    """
    """

    super(TopicRankPPRanker, self).__init__(name,
                                            is_lazy,
                                            lazy_directory,
                                            debug)

    self._graphs_and_models_key = graphs_and_models_key
    self._stemmer = stemmer
    self._nb_controlled_keyphrases = nb_controlled_keyphrases
    self._convergence_threshold = convergence_threshold
    self._lambda_k = lambda_k
    self._lambda_t = lambda_t
    self._max_iterations = max_iterations

  def weighting(self, pre_processed_file, candidates, clusters):
    """
    Takes a pre-processed text (list of POS-tagged sentences) and gives a weight
    to its candidates keyphrases.

    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}
    @param    candidates:         The keyphrase candidates.
    @type     candidates:         C{list(string)}
    @param    clusters:           The clustered candidates.
    @type     clusters:           C{list(list(string))}

    @return:  A dictionary of terms as key and weight as value.
    @rtype:   C{dict(string, float)}
    """
    sentences = pre_processed_file.full_text()
    nb_sentences = float(len(sentences))
    topic_indexing = {}
    # initialize the graph with the domain graph (interconnected keyphrases)
    self_graphs_and_models_key = self._graphs_and_models_key
    graph = networkx.DiGraph(topicrankpp_graphs[self_graphs_and_models_key])
    reference_keyphrases = list(graph.nodes())

    # index topics with sentence appearances
    for sentence_index, sentence in enumerate(sentences):
      ngrams = keybench_util.n_to_m_grams(sentence.split(" "), 1, len(sentence.split(" ")))

      for topic_id, topic in enumerate(clusters):
        if len(set(topic) & set(ngrams)) > 0:
          if topic_id not in topic_indexing:
            topic_indexing[topic_id] = []
          topic_indexing[topic_id].append(sentence_index)

    #-- graph creation ---------------------------------------------------------
    # add document information within the domain graph
    for topic_id_1 in topic_indexing:
      count_1 = float(len(topic_indexing[topic_id_1]))
      p_1 = count_1 / nb_sentences

      # document connections
      for topic_id_2 in topic_indexing:
        if topic_id_1 != topic_id_2:
          pair_count_1_2 = float(len(set(topic_indexing[topic_id_1]) & set(topic_indexing[topic_id_2])))
          weight = pair_count_1_2 / nb_sentences

          if weight != 0.0:
            if not graph.has_node(topic_id_1):
              graph.add_node(topic_id_1, {"type": "topic"})
            if not graph.has_node(topic_id_2):
              graph.add_node(topic_id_2, {"type": "topic"})

            graph.add_edge(topic_id_1,
                           topic_id_2,
                           {"type": "intra", "weight": weight})

      # domain connections
      for keyphrase in reference_keyphrases:
        stemmed_keyphrase = " ".join(self._stemmer.stem(w) for w in keyphrase.split(" "))
        weight_topic_to_keyphrase = 0.0
        weight_keyphrase_to_topic = 0.0

        for tagged_candidate in clusters[topic_id_1]:
          candidate = " ".join(wt.rsplit(pre_processed_file.tag_separator(), 1)[0] for wt in tagged_candidate.split(" "))

          stemmed_candidate = " ".join(self._stemmer.stem(w) for w in candidate.split(" "))
          stem_overlap_similarity = word_overlap_similarity(stemmed_candidate,
                                                            stemmed_keyphrase)

          if stemmed_candidate == stemmed_keyphrase:
            weight_topic_to_keyphrase = 1.0
            weight_keyphrase_to_topic = 1.0

        if weight_topic_to_keyphrase != 0.0:
        # FIXME not generic, should be tested earlier
        #if weight_topic_to_keyphrase > 0.25:
          if not graph.has_node(topic_id_1):
            graph.add_node(topic_id_1, {"type": "topic"})
          if not graph.has_node(keyphrase):
            graph.add_node(keyphrase, {"type": "keyphrase"})

          graph.add_edge(topic_id_1,
                         keyphrase,
                         {"type": "extra", "weight": weight_topic_to_keyphrase})
        if weight_keyphrase_to_topic != 0.0:
        # FIXME not generic, should be tested earlier
        #if weight_keyphrase_to_topic > 0.25:
          if not graph.has_node(topic_id_1):
            graph.add_node(topic_id_1, {"type": "topic"})
          if not graph.has_node(keyphrase):
            graph.add_node(keyphrase, {"type": "keyphrase"})

          graph.add_edge(keyphrase,
                         topic_id_1,
                         {"type": "extra", "weight": weight_keyphrase_to_topic})
    #output_file = open("output.pickle", "w")
    #pickle.dump(graph, output_file)
    #output_file.close()

    #-- random walk ------------------------------------------------------------
    stabilized = False
    nb_iterations = 0
    in_edge_indexing = {}
    out_edge_indexing = {}
    out_sum_indexing = {}
    scores = {}

    # in and out edge indexing for faster processing
    for node in graph.nodes():
      if node not in in_edge_indexing:
        in_edge_indexing[node] = {"intra": [], "extra": []}
      if node not in out_edge_indexing:
        out_edge_indexing[node] = {"intra": [], "extra": []}

      for source, target, data in graph.in_edges(node, data=True):
        in_edge_indexing[node][data["type"]].append((source, data["weight"]))
      for source, target, data in graph.out_edges(node, data=True):
        out_edge_indexing[node][data["type"]].append((target, data["weight"]))

    # initialization
    for node, data in graph.nodes(data=True):
      scores[node] = 1.0

      out_sum_indexing[node] = {}
      for edge_type in out_edge_indexing[node]:
        if edge_type not in out_sum_indexing[node]:
          out_sum_indexing[node][edge_type] = 0.0

        for target, weight in out_edge_indexing[node][edge_type]:
          out_sum_indexing[node][edge_type] += weight

    while not stabilized and nb_iterations < self._max_iterations:
      stabilized = True
      previous_scores = scores.copy()

      for node, data in graph.nodes(data=True):
        previous_score = previous_scores[node]
        new_score = 0.0

        intra_recommendation_sum = 0.0
        extra_recommendation_sum = 0.0

        # compute the intra-recommendation
        for source, weight1 in in_edge_indexing[node]["intra"]:
          out_sum = out_sum_indexing[source]["intra"]

          intra_recommendation_sum += (weight1 * previous_scores[source]) \
                                      / out_sum
        # compute the extra-recommendation
        for source, weight1 in in_edge_indexing[node]["extra"]:
          out_sum = out_sum_indexing[source]["extra"]

          extra_recommendation_sum += (weight1 * previous_scores[source]) \
                                      / out_sum

        lambda_value = -1.0
        if data["type"] == "topic":
          lambda_value = self._lambda_t
        else:
          lambda_value = self._lambda_k
        if lambda_value == -1:
          print "<<<<<<<<<<<<<<<<<<< WHAT IS THE FUCK!!! >>>>>>>>>>>>>>>>>>>>>>"
        new_score = ((1.0 - lambda_value) * extra_recommendation_sum) \
                    + (lambda_value * intra_recommendation_sum)

        # look for convergence
        if math.fabs(new_score - previous_score) > self._convergence_threshold:
          stabilized = False

        scores[node] = new_score

      nb_iterations += 1

    ##-- determine the minimum depth from a domain keyphrase to a topic --------
    generalization_degree = {}
    generalization_fifo = []

    # TODO REMOVE
    #max_degree = 0
    for node, data in graph.nodes(data=True):
      if data["type"] == "keyphrase":
        if out_sum_indexing[node]["extra"] > 0.0:
          generalization_degree[node] = 1.0

          generalization_fifo.insert(0, node)
        else:
          generalization_degree[node] = float("inf")
    while len(generalization_fifo) > 0:
      keyphrase = generalization_fifo.pop()
      keyphrase_degree = generalization_degree[keyphrase]

      for next_keyphrase, weight in out_edge_indexing[keyphrase]["intra"]:
        next_keyphrase_degree = generalization_degree[next_keyphrase]

        if next_keyphrase_degree == float("inf"):
          generalization_fifo.insert(0, next_keyphrase)
        generalization_degree[next_keyphrase] = min(next_keyphrase_degree,
                                                    keyphrase_degree + 1.0)
        # TODO remove
        #max_degree = max(max_degree, generalization_degree[next_keyphrase])
    # TODO remove
    #cpt = 0
    #for k, d in generalization_degree.items():
    #  if d == float("inf"):
    #    cpt += 1
    #print "## %d infinite degrees (max_degree=%d) #########"%(cpt, max_degree)

    ##-- post-processing -------------------------------------------------------
    ranking_results = {}
    tagged_text = " ".join(pre_processed_file.full_text_words())
    untagged_text = " ".join(wt.rsplit(pre_processed_file.tag_separator(), 1)[0] for wt in pre_processed_file.full_text_words())
    sorted_nodes = []
    if self._nb_controlled_keyphrases != float("inf"):
      # keyphrases first
      sorted_nodes = sorted(graph.nodes(data=True),
                            key=lambda (n, d): (len(d["type"]), scores[n]),
                            reverse=True)
    else:
      # best score first, then keyphrases first
      sorted_nodes = sorted(graph.nodes(data=True),
                            key=lambda (n, d): (scores[n], len(d["type"])),
                            reverse=True)
    best_score = max(scores[n] for n, d in sorted_nodes)
    nb_added_controlled_keyphrases = 0
    # TODO use for percentage of assignment count
    #printed = False

    # - treat keyphrases first
    # - add the best score to every keyphrase so that candidates are always
    #   ranked below
    for node, node_data in sorted_nodes:
      # TODO use for percentage of assignment count
      #if len(ranking_results) == 10 and printed == False:
      #  print nb_added_controlled_keyphrases
      #  printed = True
      # add reference keyphrases if it has a score above 0.0 and if it is not in
      # the document
      if node_data["type"] == "keyphrase" \
         and nb_added_controlled_keyphrases < self._nb_controlled_keyphrases \
         and scores[node] > 0.0 \
         and generalization_degree[node] < float("inf"):
        ranking_results[node] = scores[node]
        nb_added_controlled_keyphrases += 1

        if self._nb_controlled_keyphrases != float("inf"):
          ranking_results[node] += best_score
      # put only a few candidates per topic
      elif node_data["type"] == "topic":
        cluster = sorted(clusters[node],
                         key=lambda c: len(c.split(" ")),
                         reverse=True)
        topic_reference_keyphrases = []
        best_candidate = ""
        best_first_position = float("inf")

        # find the first occuring candidate (prioritize reference keyphrases)
        for candidate in cluster:
          untagged_candidate = " ".join(wt.rsplit(pre_processed_file.tag_separator(), 1)[0] for wt in candidate.split(" "))
          stemmed_candidate = " ".join(self._stemmer.stem(w) for w in untagged_candidate.split(" "))
          first_position = tagged_text.find(candidate)

          # choose the first occuring reference keyphrases or the first occuring
          # candidate (not already extracted)
          if stemmed_candidate in topic_reference_keyphrases \
             or (len(topic_reference_keyphrases) == 0 \
                 and untagged_candidate not in ranking_results): 
            if first_position < best_first_position \
               and untagged_candidate not in ranking_results: # exclude already
                                                              # extracted
                                                              # keyphrases
              best_candidate = candidate
              best_first_position = first_position

        if best_candidate != "":
          ranking_results[best_candidate] = scores[node]

    return ranking_results

  def ordering(self, weights, clusters):
    """
    Takes the weighted terms of the analysed text and ordered them.

    @param    weights:  A dictionary of weighted candidates.
    @type     weights:  C{dict(string, float)}
    @param    clusters: The clustered candidates.
    @type     clusters: C{list(list(string))}

    @return:  A ordered list of weighted terms.
    @rtype:   C{list(tuple(string, float))}
    """

    return sorted(weights.items(), key=lambda row: row[1], reverse=True)

