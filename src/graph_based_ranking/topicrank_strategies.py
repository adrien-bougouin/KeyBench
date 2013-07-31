#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import math
from textrank_strategies import TextRankStrategy
from util import term_clustering

ID_TAG = "id"

class CompleteGraphStrategy(TextRankStrategy):
  """
  Strategy to use with the TextRank graph-based ranking algorithm. This strategy
  creates a complete graph and change the weigh computation of links.
  """

  def reset(self, tokens, context):
    """
    Reinitializes the data structures according to the new given tokens and
    context (it is safer to use this method than each setters one by one).

    @param  tokens:   The new tokens to work with.
    @type   tokens:   C{list(string)}
    @param  context:  The context from which the new tokens are extracted (list
                      of POS tagged sentences).
    @type   context:  C{list(string)}
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

class TopicRankStrategy(TextRankStrategy):
  """
  Strategy to use with the TextRank graph-based ranking algorithm. This strategy
  is a decorator of the C{TextRankStrategy} to add candidate clustering support
  for methods which use words instead of candidates [1][2]. In fact, it replaces
  the candidates by one word identifiers, so the decorated strategy can work
  normally.

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

    @param  strategy: The strategy modified to allow candidate clusters ranking.
    @type   strategy: C{TextRankStrategy}
    @param  stemmer:  Stemmer needed for the term clustering.
    @type   stemmer:  C{nltk.stem.StemmerI}
    """

    self.set_strategy(strategy)
    super(TopicRankStrategy, self).__init__(strategy.window(),
                                            strategy.tag_separator(),
                                            [ID_TAG])

    self.set_stemmer(stemmer)
    self.set_clusters([])
    self.set_reverted_token_ids(None)

    self.strategy().set_accepted_tags([ID_TAG])

  def window(self):
    """
    Getter of the size of the window to use for the co-occurrences between
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
    Getter of the POS tag separator.

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
    Getter of the POS tagged of the working words (only the words with the
    given POS tags are ranked).

    @return:  The POS tagged used to filter the words to rank.
    @rtype:   C{list(string)}
    """

    return self.strategy().accepted_tags()

  def set_accepted_tags(self, accepted_tags):
    """
    Setter of the POS tagged of the working words (only the words with the
    given POS tags are ranked).

    @return:  The new POS tagged to use to filter the words to rank.
    @rtype:   C{list(string)}
    """

    self._accepted_tags = accepted_tags
    self.strategy().set_accepted_tags(accepted_tags)

  def indexed_sentences(self):
    """
    Getter of the indexed sentences. Each element of the list represent a
    sentence containing the tokens' id associated with its position(s) in the
    sentence.

    @return:  The indexed sentences.
    @rtype:   C{list(dict(string, list(int)))}
    """

    return self.strategy().indexed_sentences()

  def set_indexed_sentences(self, indexed_sentences):
    """
    Setter of the indexed sentences. Each element of the list represent a
    sentence containing the tokens' id associated with its position(s) in the
    sentence.

    @param  indexed_sentences:  The new indexed sentences.
    @type   indexed_sentences:  C{list(dict(string, list(int)))}
    """

    self.strategy().set_indexed_sentences(indexed_sentences)

  def indexed_token_ids(self):
    """
    Getter of the indexed token ids. A list of sentence index is associated to
    each token ids when one of the token represented by the id appeares in the
    sentences.

    @return:  The indexed token ids.
    @rtype:   C{dict(string, list(int))}
    """

    return self.strategy().indexed_token_ids()

  def set_indexed_token_ids(self, indexed_token_ids):
    """
    Setter of the indexed token ids. A list of sentence index is associated to
    each token ids when one of the token represented by the id appeares in the
    sentences.

    @param  indexed_token_ids:  The new indexed token ids.
    @type   indexed_token_ids:  C{dict(string, list(int))}
    """

    self.strategy().set_indexed_token_ids(indexed_token_ids)

  def computed_weights(self):
    """
    Getter of the already computed recomendations.

    @return:  The already computed recomendations.
    @rtype:   C{dict(string, dict(string, float))}
    """

    return self.strategy().computed_weights()

  def set_computed_weights(self, computed_weights):
    """
    Setter of the already computed recomendations.

    @param  computed_weights: The new already computed recomendations.
    @type   computed_weights: C{dict(string, dict(string, float))}
    """

    self.strategy().set_computed_weights(computed_weights)

  def strategy(self):
    """
    Getter of the decorated strategy.

    @return:  The decorated strategy.
    @rtype:   C{TextRankStrategy}
    """

    return self._strategy

  def set_strategy(self, strategy):
    """
    Setter of the decorated strategy.

    @return:  The new decorated strategy.
    @rtype:   C{TextRankStrategy}
    """

    self._strategy = strategy

  def stemmer(self):
    """
    Getter of the stemmer used for the term clustering.

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

  def clusters(self):
    """
    Getter of the Strategies clusters.

    @return:  The clusters of the strategy.
    @rtype:   C{list(list(string))}
    """

    return self._clusters

  def set_clusters(self, clusters):
    """
    Setter of the Strategies clusters.

    @param  clusters: The new clusters of the strategy.
    @type   clusters: C{list(list(string))}
    """

    self._clusters = clusters

  def reverted_token_ids(self):
    """
    Getter of the reverted version of the _token_ids attribute.

    @return:  The reverted version of the _token_ids attribute.
    @rtype:   C{dict(string, string)}
    """

    return self._reverted_token_ids

  def set_reverted_token_ids(self, reverted_token_ids):
    """
    Setter of the reverted vertion of the _token_ids attribute.

    @return:  The new reverted version of the _token_ids attribute.
    @rtype:   C{dict(string, string)}
    """

    self._reverted_token_ids = reverted_token_ids

  def identifier(self, token):
    """
    Gives the corresponding identifier of a token. By default, there is a unique
    identifier for each token (hash of the stringified token).

    @param  token: The token to get the identifier of.
    @type   token: C{string}

    @return:  The identifier of the given token.
    @rtype:   C{string}
    """

    return self.reverted_token_ids()[token]

  def reset(self, tokens, context):
    """
    Reinitializes the data structures according to the new given tokens and
    context (it is safer to use this method than each setters one by one).

    @param  tokens:   The new tokens to work with.
    @type   tokens:   C{list(string)}
    @param  context:  The context from which the new tokens are extracted (list
                      of POS tagged sentences).
    @type   context:  C{list(string)}
    """

    ##### Strategy's context adaptation ########################################

    modified_context = []
    token_ids = {}
    reverted_token_ids = {}

    # modify the context for the decorated strategy
    # FIXME the replacement may remove some tokens because of overlapping from
    #       different clusters
    for i, sentence in enumerate(context):
      modified_sentence = sentence

      # replacement, starting with the smaller clusters
      for index, cluster_tokens in sorted(enumerate(self.clusters()),
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
    for index, cluster_tokens in enumerate(self.clusters()):
      strategy_token = "%d%s%s"%(index,
                                 self.tag_separator(),
                                 ID_TAG)
      identifier = self.strategy().identifier(strategy_token)
      token_ids[identifier] = cluster_tokens

      for token in cluster_tokens:
        reverted_token_ids[token] = identifier

    ##### Reset ################################################################

    # the PyRank algorithms sees the right datas but the strategy works on
    # modified ones
    self.set_tokens(tokens)
    self.set_context(context)
    self.set_token_ids(token_ids)
    self.set_reverted_token_ids(reverted_token_ids)

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

