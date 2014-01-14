#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class TextRankStrategy(object):
  """
  Strategy to use with the TextRank graph-based ranking algorithm [1]. It allows
  to define a new graph construction, to define a new link weighting and to
  modify the PageRank formula [2].

  [1] Rada Mihalcea and Paul Tarau. 2004. TextRank: Bringing Order Into Texts.
      In Dekang Lin and Dekai Wu, editors, Proceedings of the 2004 Conference on
      Empirical Methods in Natural Language Processing, pages 404–411,
      Barcelona, Spain, July. Association for Computational Linguistics.
  [2] Sergey Brin and Lawrence Page. 1998. The Anatomy of a Large-Scale
      Hypertextual Web Search Engine. Computer Networks and ISDN Systems,
      30(1):107-117.
  """

  def __init__(self, window, tag_separator, accepted_tags):
    """
    Constructor.

    @param  window:         The window of words used to find word co-occurences.
    @type   window:         C{int}
    @param  tag_separator:  The character that separate the words and their POS
                            tag.
    @type   tag_separator:  C{string}
    @param  accepted_tags:  The POS tags of the words to use as nodes of in the
                            graph.
    @type   accepted_tags:  C{list(string)}
    """

    super(TextRankStrategy, self).__init__()

    self.set_tokens([])
    self.set_context(None)
    self.set_token_ids({})
    self.set_window(window)
    self.set_tag_separator(tag_separator)
    self.set_accepted_tags(accepted_tags)
    self.set_indexed_sentences([])  # position of each token in each sentence
    self.set_indexed_token_ids({})  # sentence indexes in which words appear
    self.set_computed_weights({})   # lazy loading to avoid recomputation

  def tokens(self):
    """
    Getter of the tokens the strategy is working on.

    @return:  The current tokens that can be analysed by the strategy.
    @rtype:   C{list(string)}
    """

    return self._tokens

  def set_tokens(self, tokens):
    """
    setter of the tokens the strategy is working on.

    @param  tokens: The new tokens to work on.
    @type   tokens: C{list(string)}
    """

    self._tokens = tokens

  def context(self):
    """
    Getter of the context which can give clues, about the tokens
    relationships, to the strategy.

    @return:  The context used by the strategy.
    @rtype:   C{string}
    """

    return self._context

  def set_context(self, context):
    """
    Setter of the context that can be used by the strategy to get clues about
    the tokens relationships.

    @param  context: The new context to use.
    @type   context:  C{string}
    """

    self._context = context

  def token_ids(self):
    """
    Getter of tokens, organized by an identifier which can play the role of a
    cluster identifier.

    @return:  The tokens used by the strategy, organized by identifier.
    @rtype:   C{dict(string, string)}
    """

    return self._token_ids

  def set_token_ids(self, token_ids):
    """
    Setter of the identifiers of the tokens the strategy is working on.

    @param  token_ids:  The new identifiers for the tokens the strategy is
                        working on.
    @type   token_ids:  C{dict(string, string)}
    """

    self._token_ids = token_ids

  def window(self):
    """
    Getter of the size of the window to use for the co-occurrences between
    words.

    @return:  The co-occrurrence window's size.
    @rtype:   C{int}
    """

    return self._window

  def set_window(self, window):
    """
    Setter of the size of the window to use for the co-occurrences between
    words.

    @param  window: The new co-occrurrence window's size.
    @type   window: C{int}
    """

    self._window = window

  def tag_separator(self):
    """
    Getter of the POS tag separator.

    @return:  The tag used to devide a word and its POS tag
              (<words><separator><tag>).
    @rtype:   C{string}
    """

    return self._tag_separator

  def set_tag_separator(self, tag_separator):
    """
    Setter of the POS tag separator.

    @param  tag_separator:  The new tag to use to devide a word and its POS tag
                            (<words><separator><tag>).
    @type   tag_separator:  C{string}
    """

    self._tag_separator = tag_separator

  def accepted_tags(self):
    """
    Getter of the POS tagged of the working words (only the words with the
    given POS tags are ranked).

    @return:  The POS tagged used to filter the words to rank.
    @rtype:   C{list(string)}
    """

    return self._accepted_tags

  def set_accepted_tags(self, accepted_tags):
    """
    Setter of the POS tagged of the working words (only the words with the
    given POS tags are ranked).

    @return:  The new POS tagged to use to filter the words to rank.
    @rtype:   C{list(string)}
    """

    self._accepted_tags = accepted_tags

  def indexed_sentences(self):
    """
    Getter of the indexed sentences. Each element of the list represent a
    sentence containing the tokens' id associated with its position(s) in the
    sentence.

    @return:  The indexed sentences.
    @rtype:   C{list(dict(string, list(int)))}
    """

    return self._indexed_sentences

  def set_indexed_sentences(self, indexed_sentences):
    """
    Setter of the indexed sentences. Each element of the list represent a
    sentence containing the tokens' id associated with its position(s) in the
    sentence.

    @param  indexed_sentences:  The new indexed sentences.
    @type   indexed_sentences:  C{list(dict(string, list(int)))}
    """

    self._indexed_sentences = indexed_sentences

  def indexed_token_ids(self):
    """
    Getter of the indexed token ids. A list of sentence index is associated to
    each token ids when one of the token represented by the id appeares in the
    sentences.

    @return:  The indexed token ids.
    @rtype:   C{dict(string, list(int))}
    """

    return self._indexed_token_ids

  def set_indexed_token_ids(self, indexed_token_ids):
    """
    Setter of the indexed token ids. A list of sentence index is associated to
    each token ids when one of the token represented by the id appeares in the
    sentences.

    @param  indexed_token_ids:  The new indexed token ids.
    @type   indexed_token_ids:  C{dict(string, list(int))}
    """

    self._indexed_token_ids = indexed_token_ids

  def computed_weights(self):
    """
    Getter of the already computed recomendations.

    @return:  The already computed recomendations.
    @rtype:   C{dict(string, dict(string, float))}
    """

    return self._computed_weights

  def set_computed_weights(self, computed_weights):
    """
    Setter of the already computed recomendations.

    @param  computed_weights: The new already computed recomendations.
    @type   computed_weights: C{dict(string, dict(string, float))}
    """

    self._computed_weights = computed_weights

  def identifier(self, token):
    """
    Gives the corresponding identifier of a token. By default, there is a unique
    identifier for each token (hash of the stringified token).

    @param  token: The token to get the identifier of.
    @type   token: C{string}

    @return:  The identifier of the given token.
    @rtype:   C{string}
    """

    untagged_token = ""

    for wt in token.split():
      w = wt.rsplit(self._tag_separator, 1)[0]

      if untagged_token != "":
        untagged_token += " "
      untagged_token += w

    return untagged_token

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
    tokens = []
    token_ids = {}
    indexed_sentences = []
    indexed_token_ids = {}
    computed_weights = {}

    ##### Fill the data structures #############################################
    for i, s in enumerate(context):
      indexes = {} # indicates the position(s) of the words in the sentence
      s = s.lower()

      for j, wt in enumerate(s.split()):
        tag = wt.rsplit(self.tag_separator(), 1)[1]

        if self.accepted_tags().count(tag) > 0:
          w_id = self.identifier(wt)

          if tokens.count(wt) <= 0:
            tokens.append(wt)
            if not token_ids.has_key(w_id):
              token_ids[w_id] = []
            token_ids[w_id].append(wt)

          # fill the words_index and the sentences structures
          if not indexes.has_key(w_id):
            indexes[w_id] = []

            if not indexed_token_ids.has_key(w_id):
              indexed_token_ids[w_id] = []
            indexed_token_ids[w_id].append(i)
          indexes[w_id].append(j)

          # add the word as key of computed_weights
          if not computed_weights.has_key(w_id):
            computed_weights[w_id] = {}

      indexed_sentences.append(indexes)

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
        s = self.indexed_sentences()[i]
        if s.has_key(out_token_id):
          for j in s[in_token_id]:
            for k in s[out_token_id]:
              if abs(j - k) < self._window:
                weight = 1.0
                break
            if weight > 0.0:
              break
          if weight > 0.0:
            break
      self.computed_weights()[in_token_id][out_token_id] = weight
      self.computed_weights()[out_token_id][in_token_id] = weight
    else:
      weight = self.computed_weights()[in_token_id][out_token_id]

    return weight

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

    return 1.0

################################################################################

class SingleRankStrategy(TextRankStrategy):
  """
  SingleRank [1] strategy to use with the PyRank algorithm (the tokens must be
  POS tagged). The constructed graph is weighted and undirected.

  [1] Wan, X. et Xiao, J. (2008). Single Document Keyphrase Extraction Using
      Neighborhood Knowledge. In Proceedings of Association for the Advancement
      of Artificial Intelligence, pages 855–860.
  """

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
        s = self.indexed_sentences()[i]
        if s.has_key(out_token_id):
          for j in s[in_token_id]:
            for k in s[out_token_id]:
              if abs(j - k) < self._window:
                weight += 1.0
      self.computed_weights()[in_token_id][out_token_id] = weight
      self.computed_weights()[out_token_id][in_token_id] = weight
    else:
      weight = self.computed_weights()[in_token_id][out_token_id]

    return weight

