#!/usr/bin/env python
# -*- encoding: utf-8 -*-

def sum(term, word_weights, tag_separator=None):
  """
  Computes the score of a term, based on its words weight (sum).

  @param    term:           The POS tagged candidate.
  @type     term:           C{string}
  @param    word_weights:   The weights of all the words (POS tags or not).
  @type     word_weights:   C{dict(string, float)} or C{list(tuple((string,
                            float))}
  @param    tag_separator:  The character used to separate a words from its
                            tag.
  @type     tag_separator:  C{string}

  @return:  The calculated score of the given term.
  @rtype:   C{float}
  """

  score = 0.0

  # convert the list into a dict
  if not isinstance(word_weights, dict):
    temp_dic = {}
    for s, f in word_weights:
      temp_dic[s] = f
    word_weights = temp_dic

  for w in term.lower().split():
    w = w

    # remove the tag if needed
    if not word_weights.has_key(w) and tag_separator != None:
      w = w.rsplit(tag_separator, 1)[0]

    # compute score
    if word_weights.has_key(w):
      score += word_weights[w]

  return score

def normalized(term, word_weights, tag_separator=None):
  """
  Computes the score of a term, based on its words weight (normalized sum).

  @param    term:           The POS tagged candidate.
  @type     term:           C{string}
  @param    word_weights:   The weights of all the words (POS tags or not).
  @type     word_weights:   C{dict(string, float)} or C{list(tuple((string,
                            float))}
  @param    tag_separator:  The character used to separate a words from its
                            tag.
  @type     tag_separator:  C{string}

  @return:  The calculated score of the given term.
  @rtype:   C{float}
  """
  score = 0.0
  words = term.lower().split()
  n = len(words)

  # convert the list into a dict
  if not isinstance(word_weights, dict):
    temp_dic = {}
    for s, f in word_weights:
      temp_dic[s] = f
    word_weights = temp_dic

  for i, w in enumerate(words):
    w = w

    # remove the tag if needed
    if not word_weights.has_key(w) and tag_separator != None:
      w = w.rsplit(tag_separator, 1)[0]

    # compute score
    if word_weights.has_key(w):
      score += word_weights[w]

  return (score / (n + 1))

def normalized_left_significance(term, word_weights, tag_separator=None):
  """
  Computes the score of a term, based on its words weight (normalized sum of
  weighted word's weight).

  @param    term:           The POS tagged candidate.
  @type     term:           C{string}
  @param    word_weights:   The weights of all the words (POS tags or not).
  @type     word_weights:   C{dict(string, float)} or C{list(tuple((string,
                            float))}
  @param    tag_separator:  The character used to separate a words from its
                            tag.
  @type     tag_separator:  C{string}

  @return:  The calculated score of the given term.
  @rtype:   C{float}
  """
  score = 0.0
  words = term.lower().split()
  n = len(words)

  # convert the list into a dict
  if not isinstance(word_weights, dict):
    temp_dic = {}
    for s, f in word_weights:
      temp_dic[s] = f
    word_weights = temp_dic

  for i, w in enumerate(words):
    w = w
    a = (i + 1) / n

    # remove the tag if needed
    if not word_weights.has_key(w) and tag_separator != None:
      w = w.rsplit(tag_separator, 1)[0]

    # compute score
    if word_weights.has_key(w):
      score = (a * score) + ((1 - a) * word_weights[w])

  return (score / (n + 1))

def normalized_right_significance(term, word_weights, tag_separator=None):
  """
  Computes the score of a term, based on its words weight (normalized sum of
  weighted word's weight).

  @param    term:           The POS tagged candidate.
  @type     term:           C{string}
  @param    word_weights:   The weights of all the words (POS tags or not).
  @type     word_weights:   C{dict(string, float)} or C{list(tuple((string,
                            float))}
  @param    tag_separator:  The character used to separate a words from its
                            tag.
  @type     tag_separator:  C{string}

  @return:  The calculated score of the given term.
  @rtype:   C{float}
  """
  score = 0.0
  words = term.lower().split()
  n = len(words)

  # convert the list into a dict
  if not isinstance(word_weights, dict):
    temp_dic = {}
    for s, f in word_weights:
      temp_dic[s] = f
    word_weights = temp_dic

  for i, w in enumerate(words):
    w = w
    a = (i + 1) / n

    # remove the tag if needed
    if not word_weights.has_key(w) and tag_separator != None:
      w = w.rsplit(tag_separator, 1)[0]

    # compute score
    if word_weights.has_key(w):
      score = ((1 - a) * score) + (a * word_weights[w])

  return (score / (n + 1))

