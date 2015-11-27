#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import collections
import math

class TextRank(object):
  """
  Implementaton of the TextRank ranking algorithm for Natural Language
  Processing [1]. Only the ranking is implemented, not the keyphrase generation
  based on the keywords. Therefore other methods such as SingleRank [2] can use
  this algorithm. In the case of SingleRank, ascoring function must be defined
  to compute a score to multi-word expressions based on the score of their
  words. To allow the implementation of variants a strategy must be implemented.
  It makes it easy to change the graph construction, change the link weighting
  or to act on the PageRank formula [3].

  [1] Rada Mihalcea and Paul Tarau. 2004. TextRank: Bringing Order Into Texts.
      In Dekang Lin and Dekai Wu, editors, Proceedings of the 2004 Conference on
      Empirical Methods in Natural Language Processing, pages 404–411,
      Barcelona, Spain, July. Association for Computational Linguistics.
  [2] Xiaojun Wan and Jianguo Xiao. 2008. Single Doc ument Keyphrase Extraction
      Using Neighborhood Knowledge. In Proceedings of the 23rd National
      Conference on Artificial Intelligence - Volume 2, pages 855–860. AAAI
      Press.
  [3] Sergey Brin and Lawrence Page. 1998. The Anatomy of a Large-Scale
      Hypertextual Web Search Engine. Computer Networks and ISDN Systems,
      30(1):107-117.
  """

  def __init__(self,
               strategy,
               scoring_function,
               convergence_threshold=0.0001,
               recomendation_weight=0.85,
               max_ranking_iterations=1000000):
    """
    Constructor.

    @param  strategy:               The strategy used to specialized the graph
                                    construction and usage.
    @type   strategy:               C{TextRankStrategy}
    @param  scoring_function:       Function used to compute the scores of the
                                    textual units, when the give candidates to
                                    weight are not single words.
    @type   scoring_function:       C{function(expression, word_weights): float}
    @param  convergence_threshold:  The threshold under which the ranking is
                                    stable.
    @type   convergence_threshold:  C{float}
    @param  recomendation_weight:   The value of the damping factor used in the
                                    PageRank formula.
    @type   recomendation_weight:   C{float}
    @param  max_ranking_iteration:  The number of maximum iteration to do for
                                    the weight computation, in case the ranking
                                    does not reach a stable state.
    @type   max_ranking_iteration:  C{int}
    """

    super(TextRank, self).__init__()

    self.set_strategy(strategy)
    self.set_scoring_function(scoring_function)
    self.set_convergence_threshold(convergence_threshold)
    self.set_recomendation_weight(recomendation_weight)
    self.set_max_ranking_iterations(max_ranking_iterations)

  def strategy(self):
    """
    Getter of the used strategy to create the graph and computes the weights.

    @return:  The strategy used for the graph creation and the score
              computation.
    @rtype:   C{TextRankStrategyI}
    """

    return self._strategy

  def set_strategy(self, strategy):
    """
    Setter of the used strategy to create the graph and computes the weights.

    @param  strategy: The new strategy to use for the graph creation
                      and the scores computation.
    @type   strategy: C{TextRankStrategyI}
    """

    self._strategy = strategy

  def scoring_function(self):
    """
    Accessor to the function used to score a token accoring to scores of another
    granularity tokens.

    @return:  The function used to compute the wright score.
    @rtype:   C{function(token: object, scores: list of (object, float)): float}
    """

    return self._scoring_function

  def set_scoring_function(self, scoring_function):
    """
    Setter to the function used to score a token accoring to scores of another
    granularity tokens.

    @param  scoring_function: The function used to compute the wright score.
    @type   scoring_function: C{function(token: object, scores: list of (object,
                              float)): float}
    """

    self._scoring_function = scoring_function

  def convergence_threshold(self):
    """
    Getter of the convergence threshold for the scores computation.

    @return:  The threshold used to decide weither the computed scores are
              stable or not, according to the previous values.
    @rtype:   C{float}
    """

    return self._convergence_threshold

  def set_convergence_threshold(self, convergence_threshold):
    """
    Setter of the convergence threshold.

    @param  convergence_threshold:  The new threshold used to decide weither the
                                    computed scores of each nodes are stable,
                                    according to the previous value.
    @type   convergence_threshold:  C{float}
    """

    self._convergence_threshold = convergence_threshold

  def recomendation_weight(self):
    """
    Getter of the importance of the recomendation over the random walk.

    @return:  recomendation_weight: The importance value of the recomendation
                                    over the random walk.
    @rtype:   recomendation_weight: C{float}
    """

    return self._recomendation_weight

  def set_recomendation_weight(self, recomendation_weight):
    """
    Setter of the the recomendation importance over the random walk.

    @param  recomendation_weight: The new importance value of the recomendation
                                  over the random walk.
    @type   recomendation_weight: C{float}
    """

    self._recomendation_weight = recomendation_weight

  def max_ranking_iterations(self):
    """
    Getter of the limit number of computation iteration.

    @return:  max_ranking_iterations: The maximum number of iterations to
                                      compute the nodes' score in case that a
                                      stabilization can't be achieved.
    @rtype:   max_ranking_iterations: C{int}
    """

    return self._max_ranking_iterations

  def set_max_ranking_iterations(self, max_ranking_iterations):
    """
    Setter of the limit number of computation iteration.

    @param  max_ranking_iterations: The new maximum number of iterations to
                                    compute the nodes' score in case that a
                                    stabilization can't be achieved.
    @type   max_ranking_iterations: C{int}
    """

    self._max_ranking_iterations = max_ranking_iterations

  def rank(self, tokens, context):
    """
    TextRank graph-based ranking algorithm.

    @param    tokens:   The textual units to rank. They can be different than
                        the tokens used into the graph, but their score must be
                        computed according to the graph tokens.
    @type     tokens:   C{list(string)}
    @param    context:  The text (POS tagged sentences) in wich the given tokens
                        are extracted from.
    @type     context:  C{list(string)}

    @return:  The given tokens associated with there score.
    @rtype:   C{List(tuple(string, float))}
    """

    ##### Strategy reinitialization ############################################
    self.strategy().reset(tokens, context)

    ##### Initialization #######################################################
    token_ids = self.strategy().token_ids()
    in_edges = {}
    weighted_degrees = {}
    scores = {}

    for identifier in token_ids:
      in_edges[identifier] = {}
      weighted_degrees[identifier] = 0.0
      scores[identifier] = 0.0

    ##### Graph creation #######################################################
    for out_token_id in token_ids:
      for in_token_id in token_ids:
        if in_token_id != out_token_id:
          weight = self.strategy().recomendation(in_token_id, out_token_id)

          if weight != 0.0:
            in_edges[out_token_id][in_token_id] = weight
            weighted_degrees[in_token_id] += weight

    ##### Score computation ####################################################
    stabilized = False
    nb_iterations = 0

    while not stabilized and nb_iterations < self.max_ranking_iterations():
      stabilized = True
      previous_scores = scores.copy()

      for identifier in token_ids:
        previous_score = previous_scores[identifier]
        new_score = 0.0
        recomendation_sum = 0.0
        random_walk = self.strategy().random_walk(identifier)

        for in_identifier, recomendation in in_edges[identifier].items():
          recomendation_sum += (recomendation * previous_scores[in_identifier])\
                               / weighted_degrees[in_identifier]

        new_score = ((1 - self.recomendation_weight()) * random_walk)\
                    + (self.recomendation_weight() * recomendation_sum)

        if math.fabs(new_score - previous_score) > self.convergence_threshold():
          stabilized = False

        scores[identifier] = new_score

    ##### Associate scores to tokens according to their identifier #############
    token_scores = []

    for identifier, identifier_tokens in token_ids.items():
      score = scores[identifier]

      for token in identifier_tokens:
        token_scores.append((token, score))

    ##### DEBUG ################################################################
    #print "## nodes' scores (%d) ####################"%len(token_ids)
    #for t, s in token_scores:
    #  print "%s = %f"%(t, s)
    #print "## edges ####################"
    #edges = []
    #for out_node in in_edges:
    #  for in_node, weight in in_edges[out_node].items():
    #    edges.append((in_node, out_node, weight))
    #edges = sorted(edges, key=lambda (i, o, w): (i, o, w))
    #inputs = {}
    #for i, o, w in edges:
    #  if not inputs.has_key(token_ids[o][0]):
    #    print "%s--%s [label=%.0f]"%(token_ids[i][0].replace(" ", "_"), token_ids[o][0].replace(" ", "_"), w)
    #    inputs[token_ids[i][0]] = True
    ############################################################################

    return self.granularity_checking(tokens, context, token_scores)

  def granularity_checking(self, tokens, context, scores):
    """
    Check if the strategy works on the same type of tokens (same granularity).
    If not, the scores of the tokens will be computed using the scoring_function
    with the strategy scored tokens.

    @param  tokens:   The tokens to rank.
    @type   tokens:   C{list(string)}
    @param  context:  The context in which the tokens appeare.
    @type   context:  C{string}
    @param  scores:   The tokens associated with there score.
    @type   scores:   C{list(tuple(string, float))}

    @return:  The correct scores.
    @rtype:   C{list(tuple(string, float))}.
    """

    token_scores = scores
    working_tokens = set(tokens)
    strategy_tokens = set(self.strategy().tokens())

    if strategy_tokens != working_tokens:
      token_scores = []

      for token in tokens:
        score = self.scoring_function()(token, scores)

        token_scores.append((token, score))

    return token_scores

