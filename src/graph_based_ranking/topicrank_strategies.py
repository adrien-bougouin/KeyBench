#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import math
from textrank_strategies import TextRankStrategyI
from util import term_clustering

ID_TAG = "id"

class CompleteGraphStrategy(TextRankStrategyI):
  """
  """

  def reset(self, tokens, context):
    """
    """

    ##### Data structures ######################################################
    tokens = []             # filled
    token_ids = {}          # filled
    indexed_sentences = []  # unfilled
    indexed_token_ids = {}  # filled
    computed_weights = {}   # filled

    ##### Fill the data structures #############################################
    sentence_inc = 0
    for i, s in enumerate(context):
      s = s.lower()

      for wt in s.split():
        tag = wt.rsplit(self.tag_separator(), 1)[1]

        if self.accepted_tags().count(tag) > 0:
          w_id = self.identifier(wt)

          if tokens.count(wt) <= 0:
            tokens.append(wt)
            if not token_ids.has_key(w_id):
              token_ids[w_id] = []
            token_ids[w_id].append(wt)

          if not indexed_token_ids.has_key(w_id):
            indexed_token_ids[w_id] = []
          indexed_token_ids[w_id].append(i + sentence_inc)

          # add the word as key of computed_weights
          if not computed_weights.has_key(w_id):
            computed_weights[w_id] = {}

        sentence_inc += len(s.split())

    ##### Reset ################################################################
    self.set_tokens(tokens)
    self.set_context(context)
    self.set_token_ids(token_ids)
    self.set_indexed_sentences(indexed_sentences)
    self.set_indexed_token_ids(indexed_token_ids)
    self.set_computed_weights(computed_weights)

  def recomendation(self, in_token_id, out_token_id):
    """
    Computes the recomendation score beetween two groups of tokens (using the
    tokens' identifier). The recomendation score is used to link two node in the
    graph. The weight of the created edge is equal to the recomendation score.

    @param  in_token_id:  The identifier of the source token.
    @type   in_token_id:  C{string}
    @param  out_token_id: The identifier of the target token.
    @type   out_token_id: C{string}

    @return:  The weight the the edge two create by recomendation.
    @rtype:   C{float}
    """

    weight = 0.0

    if not self.computed_weights()[in_token_id].has_key(out_token_id):
      for i in self.indexed_token_ids()[in_token_id]:
        for j in self.indexed_token_ids()[out_token_id]:
          distance = float(abs(i - j))
          
          if distance > 0.0:
            weight += 1.0 / distance
      self.computed_weights()[in_token_id][out_token_id] = weight
      self.computed_weights()[out_token_id][in_token_id] = weight
    else:
      weight = self.computed_weights()[in_token_id][out_token_id]

    return weight

################################################################################

class TopicRankStrategy(TextRankStrategyI):
  """
  Strategy to use with PyRank. This strategy is a decorator of the
  C{pyrank.nlp.TextRankStrategyI} to add term clustering support for methods
  which use words instead of terms [1][2]. In fact, it replaces the terms by an
  one word identifiers, so the decorated strategy can work normally.

  [1] Mihalcea, R. et Tarau, P (2004). Textrank : Bringing Order Into Texts. In
      Proceedings of the 2004 Conference on Empirical Methods in Natural
      Language Processing.
  [2] Wan, X. et Xiao, J. (2008). Single Document Keyphrase Extraction Using
      Neighborhood Knowledge. In Proceedings of Association for the Advancement
      of Artificial Intelligence, pages 855–860.
  """

  def __init__(self, strategy, stemmer):
    """
    Constructor.

    @param  strategy: The strategy modify to allow term clustering.
    @type   strategy: C{pyrank.nlp.TextRankStrategyI}
    @param  stemmer:  Stemmer needed for the term clustering.
    @type   stemmer:  C{nltk.stem.StemmerI}
    """

    super(TopicRankStrategy, self).__init__(strategy.window(),
                                            strategy.tag_separator(),
                                            [ID_TAG])

    self._clusters = []
    self._strategy = strategy
    self._stemmer = stemmer
    self._reverted_token_ids = None
    self._cluster_frequencies = {}
    self._sentence_frequencies = {}
    self._cluster_sentence_coverages = {}
    self._cluster_first_positions = {}

    self._strategy.set_accepted_tags([ID_TAG])

  def window(self):
    """
    Accessor to the size of the window to use for the co-occurrences between
    words.

    @return:  The co-occrurrence window's size.
    @rtype:   C{int}
    """

    return self.strategy().window()

  def set_window(self, window):
    """
    Setter of the size of the window to use for the co-occurrences between
    words.

    @param  window: The new co-occrurrence window's size.
    @type   window: C{int}
    """

    self._window = window
    self.strategy().set_window(window)

  def tag_separator(self):
    """
    Accessor to the POS tag separator.

    @return:  The tag used to devide a word and its POS tag
              (<words><separator><tag>).
    @rtype:   C{string}
    """

    return self.strategy().tag_separator()

  def set_tag_separator(self, tag_separator):
    """
    Setter of the POS tag separator.

    @param  tag_separator:  The new tag to use to devide a word and its POS tag
                            (<words><separator><tag>).
    @type   tag_separator:  C{string}
    """

    self._tag_separator = tag_separator
    self.strategy().set_tag_separator(tag_separator)

  def accepeted_tags(self):
    """
    Accessor to the POS tagged of the working words (only the words with the
    given POS tags are ranked).

    @return:  The POS tagged used to filter the words to rank.
    @rtype:   C{list of string}
    """

    return self.strategy().accepted_tags()

  def set_accepted_tags(self, accepted_tags):
    """
    Setter of the POS tagged of the working words (only the words with the
    given POS tags are ranked).

    @return:  The new POS tagged to use to filter the words to rank.
    @rtype:   C{list of string}
    """

    self._accepted_tags = accepted_tags
    self.strategy().set_accepted_tags(accepted_tags)

  def indexed_sentences(self):
    """
    Accessor to the indexed sentences. Each element of the list represent a
    sentence containing the tokens' id associated with its position(s) in the
    sentence.

    @return:  The indexed sentences.
    @rtype:   C{list of dict: string -> list of int}
    """

    return self.strategy().indexed_sentences()

  def set_indexed_sentences(self, indexed_sentences):
    """
    Setter of the indexed sentences. Each element of the list represent a
    sentence containing the tokens' id associated with its position(s) in the
    sentence.

    @param  indexed_sentences:  The new indexed sentences.
    @type   indexed_sentences:  C{list of dict: string -> list of int}
    """

    self.strategy().set_indexed_sentences(indexed_sentences)

  def indexed_token_ids(self):
    """
    Accessor to the indexed token ids. A list of sentence index is associated to
    each token ids when one of the token represented by the id appeares in the
    sentences.

    @return:  The indexed token ids.
    @rtype:   C{dict: string -> list of int}
    """

    return self.strategy().indexed_token_ids()

  def set_indexed_token_ids(self, indexed_token_ids):
    """
    Setter of the indexed token ids. A list of sentence index is associated to
    each token ids when one of the token represented by the id appeares in the
    sentences.

    @param  indexed_token_ids:  The new indexed token ids.
    @type   indexed_token_ids:  C{dict: string -> list of int}
    """

    self.strategy().set_indexed_token_ids(indexed_token_ids)

  def computed_weights(self):
    """
    Accessor to the already computed recomendations.

    @return:  The already computed recomendations.
    @rtype:   C{dict: string -> dict: string -> float}
    """

    return self.strategy().computed_weights()

  def set_computed_weights(self, computed_weights):
    """
    Setter of the already computed recomendations.

    @param  computed_weights: The new already computed recomendations.
    @type   computed_weights: C{dict: string -> dict: string -> float}
    """

    self.strategy().set_computed_weights(computed_weights)

  def strategy(self):
    """
    Accessor to the decorated strategy.

    @return:  The decorated strategy.
    @rtype:   C{pyrank.nlp.TextRankStrategyI}
    """

    return self._strategy

  def set_strategy(self, strategy):
    """
    Setter of the decorated strategy.

    @return:  The new decorated strategy.
    @rtype:   C{pyrank.nlp.TextRankStrategyI}
    """

    self._strategy = strategy

  def stemmer(self):
    """
    Accessor to the stemmer used for the term clustering.

    @return:  The use stemmer.
    @rtype:   C{nltk.stem.StemmerI}
    """

    return self._stemmer

  def set_stemmer(self, stemmer):
    """
    Setter of the stemmer to use for the term clustering.

    @return:  The new stemmer to use.
    @rtype:   C{nltk.stem.StemmerI}
    """

    self._stemmer = stemmer

  def reverted_token_ids(self):
    """
    Accessor to the reverted vertion of the _token_ids attribute.

    @return:  The reverted version of the _token_ids attribute.
    @rtype:   C{dict: string -> string}
    """

    return self._reverted_token_ids

  def set_reverted_token_ids(self, reverted_token_ids):
    """
    Setter of the reverted vertion of the _token_ids attribute.

    @return:  The new reverted version of the _token_ids attribute.
    @rtype:   C{dict: string -> string}
    """

    self._reverted_token_ids = reverted_token_ids

  def cluster_frequencies(self):
    """
    Accessor to the document frequency of the clusters.

    @return:  The frequencies associatated to the clusters.
    @rtype:   C{dict: string -> float}
    """

    return self._cluster_frequencies

  def set_cluster_frequencies(self, cluster_frequencies):
    """
    Setter of the document frequency of the clusters.

    @return:  The new frequencies associatated to the clusters.
    @rtype:   C{dict: string -> float}
    """

    self._cluster_frequencies = cluster_frequencies

  def cluster_sentence_frequencies(self):
    """
    Accessor to the document frequency of the clusters.

    @return:  The frequencies associatated to the clusters.
    @rtype:   C{dict: string -> float}
    """

    return self._cluster_sentence_frequencies

  def set_cluster_sentence_frequencies(self, cluster_sentence_frequencies):
    """
    Setter of the document frequency of the clusters.

    @return:  The new frequencies associatated to the clusters.
    @rtype:   C{dict: string -> float}
    """

    self._cluster_sentence_frequencies = cluster_sentence_frequencies

  def cluster_sentence_coverages(self):
    """
    Accessor to the document frequency of the clusters.

    @return:  The frequencies associatated to the clusters.
    @rtype:   C{dict: string -> float}
    """

    return self._cluster_sentence_coverages

  def set_cluster_sentence_coverages(self, cluster_sentence_coverages):
    """
    Setter of the document frequency of the clusters.

    @return:  The new frequencies associatated to the clusters.
    @rtype:   C{dict: string -> float}
    """

    self._cluster_sentence_coverages = cluster_sentence_coverages

  def cluster_first_positions(self):
    """
    Accessor to the document frequency of the clusters.

    @return:  The frequencies associatated to the clusters.
    @rtype:   C{dict: string -> float}
    """

    return self._cluster_first_positions

  def set_cluster_first_positions(self, cluster_first_positions):
    """
    Setter of the document frequency of the clusters.

    @return:  The new frequencies associatated to the clusters.
    @rtype:   C{dict: string -> float}
    """

    self._cluster_first_positions = cluster_first_positions

  def identifier(self, token):
    """
    Gives the corresponding identifier of a token. By default, there is a unique
    identifier for each token (hash of the stringified token).

    @param  token: The token to get the identifier of.
    @type   token: C{object}

    @return:  The identifier of the given token.
    @rtype:   C{string}
    """

    return self.reverted_token_ids()[token]

  def reset(self, tokens, context):
    """
    Reinitializes the data structures according to the new given tokens and
    context (it is safer to use this method than each setters one by one).

    @param  tokens:   The new tokens to work with.
    @type   tokens:   C{list of object}
    @param  context:  The context from which the new tokens are extracted.
    @type   context:  C{object}
    """

    ##### Strategy's context adaptation ########################################

    modified_context = []
    token_ids = {}
    reverted_token_ids = {}
    cluster_frequencies = {}
    cluster_sentence_frequencies = {}
    cluster_sentence_coverages = {}
    cluster_first_positions = {}

    # modify the context for the decorated strategy
    # FIXME the replacement may remove some tokens because of overlapping from
    #       different clusters
    for i, sentence in enumerate(context):
      modified_sentence = sentence

      # replacement, starting with the smaller clusters
      for index, cluster_tokens in sorted(enumerate(self._clusters),
                                          key=lambda (i, c): len(c)):
        # replacement, staring with the bigger terms
        for token in sorted(cluster_tokens,
                            key=lambda t: len(t.split()),
                            reverse=True):
          new_token = "%d%s%s"%(index,
                                self.tag_separator(),
                                ID_TAG)
          modified_sentence = modified_sentence.replace(token, new_token)

      modified_context.append(modified_sentence)

    # the strategy will work on words, but the results will be like a work on
    # terms
    self.strategy().reset(tokens, modified_context)

    # create the correct token ids and reverted_token_ids
    for index, cluster_tokens in enumerate(self._clusters):
      strategy_token = "%d%s%s"%(index,
                                 self.tag_separator(),
                                 ID_TAG)
      identifier = self.strategy().identifier(strategy_token)
      token_ids[identifier] = cluster_tokens

      for token in cluster_tokens:
        reverted_token_ids[token] = identifier

    # compute the clusters' frequencies
    total_count = 0.0
    nb_sentences = len(modified_context)
    positions = {}

    for i, sentence in enumerate(modified_context):
      for index in range(len(self._clusters)):
        strategy_token = "%d%s%s"%(index,
                                   self.tag_separator(),
                                   ID_TAG)
        identifier = self.strategy().identifier(strategy_token)
        count = float(sentence.count(strategy_token))

        if not cluster_frequencies.has_key(identifier):
          cluster_frequencies[identifier] = 0.0
          cluster_sentence_frequencies[identifier] = 0.0
          cluster_sentence_coverages[identifier] = 0.0
          positions[identifier] = []

        cluster_frequencies[identifier] += count
        cluster_sentence_frequencies[identifier] += min(1.0, count)

        if count > 0.0:
          positions[identifier].append(float(i + 1))

        total_count += count

    for identifier, freq in cluster_frequencies.items():
      cluster_frequencies[identifier] = freq / total_count

    for identifier, freq in cluster_sentence_frequencies.items():
      cluster_sentence_frequencies[identifier] = freq / nb_sentences

    nb_sentences = float(len(positions))
    for identifier, cluster_positions in positions.items():
      nb_occurrences = float(len(cluster_positions))

      if nb_occurrences > 0:
        length = float((cluster_positions[-1] - cluster_positions[0]) + 1)
        threshold = math.floor(length / nb_occurrences)
        nb_loss = float(nb_sentences - length)

        if nb_occurrences > 1:
          for i, pos in enumerate(cluster_positions[1:]):
            # because of sub list, i is the index of the previous one
            gap_with_previous = float((pos - cluster_positions[i]) - 1)

            if gap_with_previous > threshold:
              nb_loss += gap_with_previous

        cluster_sentence_coverages[identifier] = 1.0 - (nb_loss / nb_sentences)
        cluster_first_positions[identifier] = 1.0 / cluster_positions[0]
      else:
        cluster_sentence_coverages[identifier] = 0.0
        cluster_first_positions[identifier] = 0.0


    ##### Reset ################################################################

    # the PyRank algorithms sees the right datas but the strategy works on
    # modified ones
    self.set_tokens(tokens)
    self.set_context(context)
    self.set_token_ids(token_ids)
    self.set_reverted_token_ids(reverted_token_ids)
    self.set_cluster_frequencies(cluster_frequencies)
    self.set_cluster_sentence_frequencies(cluster_sentence_frequencies)
    self.set_cluster_sentence_coverages(cluster_sentence_coverages)
    self.set_cluster_first_positions(cluster_first_positions)

  def recomendation(self, in_token_id, out_token_id):
    """
    Computes the recomendation score beetween two groups of tokens (using the
    tokens' identifier). The recomendation score is used to link two node in the
    graph. The weight of the created edge is equal to the recomendation score.

    @param  in_token_id:  The identifier of the source token.
    @type   in_token_id:  C{string}
    @param  out_token_id: The identifier of the target token.
    @type   out_token_id: C{string}

    @return:  The weight the the edge two create by recomendation.
    @rtype:   C{float}
    """

    # FIXME some tokens may have been removed because of overlapping from
    #       different clusters when doing context modification in the reset
    #       function
    if self.strategy().token_ids().has_key(in_token_id) \
       and self.strategy().token_ids().has_key(out_token_id):
      return self.strategy().recomendation(in_token_id, out_token_id)
    else:
      return 0.0

  def random_walk(self, token_id):
    """
    Gives the random walk value for a given group of tokens (using the token's
    identifier). The random walk can be used to simulate cases other than
    recomendation which are positive for the node's access in the graph. By
    default, the random walk is equal to A (no particular effect).

    @param  token_id: The identifier of the tokens to get the random walk of.
    @type   token_id: C{string}

    @return:  The random walk for the given identifier.
    @rtype:   C{float}
    """

    try:
      # TODO
      return self.strategy().random_walk(token_id)
    except:
      return self.strategy().random_walk(token_id)

