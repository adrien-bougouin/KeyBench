#!/usr/bin/env python
# -*- encoding: utf-8 -*-

def n_grams(tokens, n):
  """
  Extracts n-grams from a list of tokens.

  @param    tokens: The tokens list to transform into n-grams list.
  @type     tokens: C{list(string)}
  @param    n:      The number of tokens to put in each n-gram.
  @type     n:      C{int}

  @return:  A list of n-grams generated from the list of tokens.
  @type:    C{list(string)}
  """

  result = []

  for i in range(n - 1, len(tokens)):
    dec = n - 1
    n_gram = ""
    
    while dec >= 0:
      n_gram += tokens[i - dec]
      if dec > 0:
        n_gram += " "
      dec -= 1
    result.append(n_gram)

  return result

def n_to_m_grams(tokens, n, m):
  """
  Constructs a list of N-grams for N = n..m.

  @param    tokens: The tokenized text to represent with n-grams.
  @type     tokens: C{list(string)}
  @param    n:      The minimum length of a n-gram.
  @type     n:      C{int}
  @param    m:      The maximum length of a n-gram.
  @type     m:      C{int}

  @return:  A list n..m-grams generated from the list of tokens.
  @rtype:   C{list(string)}
  """
  keyphrases = []

  for k in range(n, m + 1):
    keyphrases = list(set(keyphrases) | set(n_grams(tokens, k)))

  return keyphrases

