#!/usr/bin/env python
# -*- encoding utf-8 -*-

import codecs
import math
import pickle
from graph_based_ranking import TextRank
from graph_based_ranking import TopicRankStrategy
from keybench import RankerC
from multiprocessing import Pool
from os import listdir
from os import path
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import MinMaxScaler
#from nltk.classify.weka import WekaClassifier

################################################################################
# TextRankRanker
# KEARanker

# TODO remove
def pos_tagged_term_stemming(pos_tagged_candidate, tag_separator, stemmer):
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
    stem += stemmer.stem(w)

  return stem

# TODO include into the keybench processing
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

  centroid = None
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

################################################################################

class ORDERING_CRITERIA:
  POSITION  = 0
  FREQUENCY = 1
  CENTROID  = 2

class TextRankRanker(RankerC):
  """
  Component performing candidate terms ranking based on the TextRank score of
  their words.
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               debug,
               strategy,
               scoring_function,
               ordering_criteria=ORDERING_CRITERIA.POSITION):
    """
    Constructor of the component.

    @param  name:               The name of the component.
    @type   name:               C{string}
    @param  is_lazy:            True if the component must load previous data,
                                False if data must be computed tought they have
                                already been computed.
    @type   is_lazy:            C{bool}
    @param  lazy_directory:     The directory used to store previously computed
                                data.
    @type   lazy_directory:     C{string}
    @param  debug:              True if the component is in debug mode, else
                                False. When the component is in debug mode, it
                                will output each step of its processing.
    @type   debug:              C{bool}
    @param  strategy:           The strategy used to specialized the graph
                                construction and usage.
    @type   strategy:           C{TextRankStrategy}
    @param  scoring_function:   Function used to compute the scores of the
                                textual units, when the give candidates to
                                weight are not single words.
    @type   scoring_function:   C{function(expression, word_weights): float}
    @param  ordering_criteria:  The criteria to use to order the cluster.
                                - Position: the first appearing candidate, in
                                the document, is ranked first.
                                - Frequency: the most frequent candidate, in the
                                document, is ranked first.
                                - Centroid: The centroid of the cluster is
                                ranked first.
    @type   ordering_criteria: C{ORDERING_CRITERIA}
    """

    super(TextRankRanker, self).__init__(name, is_lazy, lazy_directory, debug)

    self._strategy = strategy
    self._textrank = TextRank(strategy,
                              scoring_function,
                              0.0001,
                              0.85,
                              1000000)
    self._ordering_criteria = ordering_criteria

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
    Takes the weighted terms of the analysed text and ordered them.

    @param    weights:  A dictionary of weighted candidates.
    @type     weights:  C{dict(string, float)}
    @param    clusters: The clustered candidates.
    @type     clusters: C{list(list(string))}

    @return:  A ordered list of weighted terms.
    @rtype:   C{list(tuple(string, float))}
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
    Orders the elements of a cluster, based on a given criteria.

    @param    cluster: The cluster to re-order.
    @type     cluster: C{list(string)}

    @return:  The re-ordered cluster. 
    @rtype:   C{list{string}}
    """

    text = self._textrank.strategy().context()
    sentence_length_accumulator = 0
    first_positions = {}
    frequency = {}

    ##### centroid calculation #################################################
    fake_pos_tagged_cluster = []
    for term in cluster:
      tagged = ""

      for w in term.split():
        if tagged != "":
          tagged += " "
        tagged += w + self._textrank.strategy().tag_separator() + "fk"
      fake_pos_tagged_cluster.append(tagged)
    tagged_centroid = cluster_centroid(fake_pos_tagged_cluster,
                                       self._textrank.strategy().tag_separator(),
                                       self._textrank.strategy().stemmer())
    centroid = ""
    for i, term in enumerate(fake_pos_tagged_cluster):
      if term == tagged_centroid:
        centroid = cluster[i]

    ##### first position and frequency calculation #############################
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

    if self._ordering_criteria == ORDERING_CRITERIA.POSITION:
      return sorted(cluster, key=lambda (t): (first_positions[t],
                                              -1 * len(t.split())))
    else:
      if self._ordering_criteria == ORDERING_CRITERIA.FREQUENCY:
        return sorted(cluster, key=lambda (t): (frequency[t],
                                                -1 * len(t.split())))
      else:
        return sorted(cluster, key=lambda (t): (t != centroid,
                                                -1 * len(t.split())))

################################################################################

KEYPHRASE     = 0
NOT_KEYPHRASE = 1
#KEYPHRASE     = "keyphrase"
#NOT_KEYPHRASE = "not_keyphrase"

class DiscreteMultinomialNB(MultinomialNB):
  """
  """

  def __init__(self):
    """
    """

    super(DiscreteMultinomialNB, self).__init__(alpha=0.0, fit_prior=False)

    self._discretizer = MinMaxScaler()

  def fit(self, X, y, sample_weight=None, class_prior=None):
    """
    """

    return super(DiscreteMultinomialNB, self).fit(self._discretizer.fit_transform(X, y),
                                                  y,
                                                  sample_weight,
                                                  class_prior)

  def partial_fit(self, X, y, classes=None, sample_weight=None):
    """
    """

    return super(DiscreteMultinomialNB, self).partial_fit(self._discretizer.fit_transform(X, y),
                                                          y,
                                                          classes,
                                                          sample_weight)

  def predict(self, X):
    """
    """

    return super(DiscreteMultinomialNB, self).predict(self._discretizer.transform(X))

  def predict_logproba(self, X):
    """
    """

    return super(DiscreteMultinomialNB, self).predict_log_proba(self._discretizer.transform(X))

  def predict_proba(self, X):
    """
    """

    return super(DiscreteMultinomialNB, self).predict_proba(self._discretizer.transform(X))

  def score(self, X, y):
    """
    """

    return super(DiscreteMultinomialNB, self).score(self._discretizer.transform(X),
                                                    y)

def get_features(candidate, pre_processed_file, tfidf):
  """
  TODO
  """

  untagged_candidate = ""
  sentences = pre_processed_file.full_text()
  total_length = 0.0
  first_position = None

  # untag the candidate
  for word in candidate.split():
    if untagged_candidate != "":
      untagged_candidate += " "
    untagged_candidate += word.rsplit(pre_processed_file.tag_separator(), 1)[0]

  # look for the first position
  for sentence in sentences:
    if first_position == None:
      untagged_sentence = ""

      # untag the sentence
      for word in sentence.split():
        if untagged_sentence != "":
          untagged_sentence += " "
        untagged_sentence += word.rsplit(pre_processed_file.tag_separator(), 1)[0]

      if untagged_sentence.find(untagged_candidate) >= 0:
        first_position = total_length

        for word in untagged_sentence.replace(untagged_candidate, untagged_candidate.replace(" ", "_")).split():
          first_position += 1.0

          if word == untagged_candidate.replace(" ", "_"):
            break

    total_length += float(len(sentence.split()))

  return [(first_position / total_length), tfidf]
#  return {"position": (first_position / total_length), "tf-idf": tfidf}

##### Multi-processing #########################################################

def feature_class_extraction_pool_worker(arguments):
  """
  """

  filename, train_directory, file_extension, ref_extension, ref_tokenization_function, stemmer, pre_processor, candidate_extractor, candidate_clusterer, tfidf_ranker = arguments
  filepath = path.join(train_directory, filename)
  pre_processed_file = pre_processor.pre_process_file(filepath)
  candidates = candidate_extractor.extract_candidates(filepath,
                                                      pre_processed_file)
  clusters = candidate_clusterer.cluster_candidates(filepath,
                                                    pre_processed_file,
                                                    candidates)
  ref_filepath = filepath[:filepath.rfind(file_extension)] + ref_extension
  ref_file = codecs.open(ref_filepath, "r", pre_processed_file.encoding())
  # use weighting to keep the dictionary (but there is no storage for lazy
  # loading)
  tfidfs = tfidf_ranker.weighting(pre_processed_file, candidates, clusters)
  feature_sets = []
  targets = []

  # keyphrase stemming
  stemmed_keyphrases = []
  for keyphrase in ref_file.read().split(";"):
    keyphrase = ref_tokenization_function(keyphrase.strip())
    stemmed_keyphrase = ""

    for word in keyphrase.split():
      if stemmed_keyphrase != "":
        stemmed_keyphrase += " "
      stemmed_keyphrase += stemmer.stem(word)

    stemmed_keyphrases.append(stemmed_keyphrase)

  for candidate in candidates:
    candidate_class = NOT_KEYPHRASE
    stemmed_candidate = ""

    for word in candidate.split():
      if stemmed_candidate != "":
        stemmed_candidate += " "
      stemmed_candidate += stemmer.stem(word.rsplit(pre_processor.tag_separator(), 1)[0])

    for keyphrase in stemmed_keyphrases:
      if stemmed_candidate == stemmed_keyphrase:
        candidate_class = KEYPHRASE

    ref_file.close()

    features = get_features(candidate,
                            pre_processed_file,
                            tfidfs[candidate])
    feature_sets.append(features)
    targets.append(candidate_class)

  return (feature_sets, targets)

################################################################################

def train_kea(model_filename,
              train_directory,
              file_extension,
              ref_extension,
              ref_tokenization_function,
              stemmer,
              pre_processor,
              candidate_extractor,
              candidate_clusterer,
              tfidf_ranker):
  """
  TODO
  """

  classifier = DiscreteMultinomialNB()
#  classifier = None
#  classifier_filename = model_filename + "_classifier"

  if not path.exists(model_filename):
#  if not path.exists(model_filename)\
#     or not path.exists(classifier_filename):
    feature_sets = []
    target_sets = []

    working_pool = Pool()
    pool_args = []
    for filename in listdir(train_directory):
      if filename.rfind(file_extension) >= 0 \
         and len(filename) - filename.rfind(file_extension) == len(file_extension):
        pool_args.append((filename,
                          train_directory,
                          file_extension,
                          ref_extension,
                          ref_tokenization_function,
                          stemmer,
                          pre_processor,
                          candidate_extractor,
                          candidate_clusterer,
                          tfidf_ranker))

    feature_sets_and_target_sets = working_pool.map(feature_class_extraction_pool_worker, pool_args)

    for feature_set, target_set in feature_sets_and_target_sets:
      for i, features in enumerate(feature_set):
        feature_sets.append(features)
        target_sets.append(target_set[i])

    # classifier training
    classifier.fit(feature_sets, target_sets)
#    classifier = WekaClassifier.train(model_filename,
#                                      feature_sets,
#                                      "naivebayes",
#                                      ["-D"])
    # serialize the classifier
    classifier_file = open(model_filename, "w")
#    classifier_file = open(classifier_filename, "w")

    pickle.dump(classifier, classifier_file)
    classifier_file.close()
  else:
    # load the serialized classifier
    classifier_file = open(model_filename, "r")
#    classifier_file = open(classifier_filename, "r")
    classifier = pickle.load(classifier_file)

    classifier_file.close()

  return classifier

class KEARanker(RankerC):
  """
  Component used to rank keyphrase candidates using the KEA method [1].

  [1] TODO
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               debug,
               classifier,
               tfidf_ranker):
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
    @param  classifier:     The trained naive bayes classifier to use by KEA.
    @type   classifier:     C{nltk.classify.api.ClassifierI}
    @param  tfidf_ranker:   The KeyBench component responsible of the TF-IDF
                            weighting.
    @type   tfidf_ranker:   C{TFIDFRanker}
    """

    super(KEARanker, self).__init__(name,
                                    is_lazy,
                                    lazy_directory,
                                    debug)

    self.set_classifier(classifier)
    self.set_tfidf_ranker(tfidf_ranker)

  def classifier(self):
    """
    Getter of the naive bayes classifier used by KEA.

    @return:  The naive bayes classifier.
    @rtype:   C{nltk.classify.api.ClassifierI}
    """

    return self._classifier

  def set_classifier(self, classifier):
    """
    Setter of the naive bayes classifier used by KEA.

    @param  classifier: The new naive bayes classifier.
    @type   classifier: C{nltk.classify.api.ClassifierI}
    """

    self._classifier = classifier

  def tfidf_ranker(self):
    """
    TODO
    """

    return self._tfidf_ranker

  def set_tfidf_ranker(self, tfidf_ranker):
    """
    TODO
    """

    self._tfidf_ranker = tfidf_ranker

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

    weighted_candidates = {}
    tfidfs = self.tfidf_ranker().weighting(pre_processed_file,
                                           candidates,
                                           clusters)
    feature_sets = []

    for i, candidate in enumerate(candidates):
      feature_sets.append(get_features(candidate, pre_processed_file, tfidfs[candidate]))

    for i, feature_probabilities in enumerate(self.classifier().predict_proba(feature_sets)):
#    for i, feature_probabilities in enumerate(self.classifier().batch_prob_classify(feature_sets)):
      p_yes = feature_probabilities[KEYPHRASE]
      p_no  = feature_probabilities[NOT_KEYPHRASE]
#      p_yes = feature_probabilities.prob(KEYPHRASE)
#      p_no  = feature_probabilities.prob(NOT_KEYPHRASE)
      weighted_candidates[candidates[i]] = (p_yes / (p_yes + p_no))

    return weighted_candidates

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

