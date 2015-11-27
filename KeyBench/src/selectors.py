#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from keybench.selector import SelectorC
from keybench.default import WholeSelector
from keybench.default import TopKSelector

################################################################################
# UnredundantWholeSelector
# UnredundantTopKSelector
# UnredundantTextRankSelector

def stem_and_untag_phrase(phrase, tag_separator, stemmer):
  """
  Transforms the phrase so its words are stemmed and untagged.

  @param    phrase:         The phrase to stem.
  @type     phrase:         C{string}
  @param    tag_separator:  The separator used between a word and its POS tag.
  type      tag_separator:  C{string}
  @param    stemmer:        Stemmer used to stemmed the candidates' words.
  @type     stemmer:        C{nltk.stem.api.StemmerI}
  
  @return:  The stemmed version of the phrase.
  @rtype:   C{string}
  """

  stemmed_phrase = ""

  for tagged_word in phrase.split():
    word = tagged_word.rsplit(tag_separator, 1)[0]

    if stemmed_phrase != "":
      stemmed_phrase += " "
    stemmed_phrase += stemmer.stem(word)

  return stemmed_phrase

def remove_redundancies(weights, tag_separator, stemmer):
  """
  Uses a stemmer to remove redundant weighted candidates. It keeps the one with
  the best scores.

  @param    weights:        The weighted candidates.
  @type     weights:        C{list of (string, float)}
  @param    tag_separator:  The separator used between a word and its POS tag.
  type      tag_separator:  C{string}
  @param    stemmer:        Stemmer used to stemmed the candidates' words.
  @type     stemmer:        C{nltk.stem.api.StemmerI}

  @return:  The non-redundant list of weighted candidates.
  @rtype:   C{list of (string -> float)}
  """

  unredundant = []
  ranked_unredundant = []
  stem_clusters = {}

  # store the weighted candidates according to their stem
  for rank, cw in enumerate(weights):
    candidate, weight = cw
    stem = stem_and_untag_phrase(candidate, tag_separator, stemmer)

    if not stem_clusters.has_key(stem):
      stem_clusters[stem] = []
    stem_clusters[stem].append((candidate, weight, rank))

  # keep the candidate with the better weight for each cluster
  for candidates in stem_clusters.values():
    candidates = sorted(candidates, key=lambda (c, w, r): r)
    candidate, weight, rank = candidates[0]

    ranked_unredundant.append((candidate, weight, rank))

  # reordered the candidates
  ranked_unredundant = sorted(ranked_unredundant, key=lambda (c, w, r): r)
  for candidate, weight, rank in ranked_unredundant:
    unredundant.append((candidate, weight))


  return unredundant

################################################################################

class UnredundantWholeSelector(WholeSelector):
  """
  Component performing selection of the keyphrases among the ranked candidate
  terms. It selects the whole list of candidates, except redundant ones.
  """

  def __init__(self, name, is_lazy, lazy_directory, debug, stemmer):
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
    @param  stemmer:        Stemmer used to remove redundancies in the selected
                            candidates.
    @type   stemmer:        C{nltk.stem.api.StemmerI}
    """

    super(UnredundantWholeSelector, self).__init__(name,
                                                   is_lazy,
                                                   lazy_directory,
                                                   debug)

    self.set_stemmer(stemmer)

  def stemmer(self):
    """
    Getter of the stemmer used to stem words.

    @return:  The stemmer used to stem words.
    @rtype:   C{nltk.stem.api.StemmerI}
    """

    return self._stemmer

  def set_stemmer(self, stemmer):
    """
    Setter of the stemmer used to stem words.

    @param  stemmer: The new stemmer used to stem words.
    @type   stemmer: C{nltk.stem.api.StemmerI}
    """

    self._stemmer = stemmer

  def selection(self, pre_processed_file, ranked_candidates, clusters):
    """
    Selects the keyphrases among weighted terms.

    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}
    @param    ranked_candidates:  The list of the file's ranked candidates and
                                  their weight.
    @type     ranked_candidates:  C{list(tuple(string, float))}
    @param    clusters:           The clustered candidates.
    @type     clusters:           C{list(list(string))}

    @return:  A list of weihgted keyphrases.
    @rtype:   C{list(tuple(string, float))}
    """

    return super(UnredundantWholeSelector,
                 self).selection(pre_processed_file,
                                 remove_redundancies(ranked_candidates,
                                                     pre_processed_file.tag_separator(),
                                                     self.stemmer()),
                                 clusters)

################################################################################

class UnredundantTopKSelector(TopKSelector):
  """
  Component performing selection of the keyphrases among the ranked candidate
  terms. It selects only the k-first unredundant candidates.
  """

  def __init__(self, name, is_lazy, lazy_directory, debug, k, stemmer):
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
    @param  stemmer:        Stemmer used to remove redundancies in the selected
                            candidates.
    @type   stemmer:        C{nltk.stem.api.StemmerI}
    """

    super(UnredundantTopKSelector, self).__init__(name,
                                                  is_lazy,
                                                  lazy_directory,
                                                  debug,
                                                  k)

    self.set_stemmer(stemmer)

  def stemmer(self):
    """
    Getter of the stemmer used to stem words.

    @return:  The stemmer used to stem words.
    @rtype:   C{nltk.stem.api.StemmerI}
    """

    return self._stemmer

  def set_stemmer(self, stemmer):
    """
    Setter of the stemmer used to stem words.

    @param  stemmer: The new stemmer used to stem words.
    @type   stemmer: C{nltk.stem.api.StemmerI}
    """

    self._stemmer = stemmer

  def selection(self, pre_processed_file, ranked_candidates, clusters):
    """
    Selects the keyphrases among weighted terms.

    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}
    @param    ranked_candidates:  The list of the file's ranked candidates and
                                  their weight.
    @type     ranked_candidates:  C{list(tuple(string, float))}
    @param    clusters:           The clustered candidates.
    @type     clusters:           C{list(list(string))}

    @return:  A list of weihgted keyphrases.
    @rtype:   C{list(tuple(string, float))}
    """

    return super(UnredundantTopKSelector,
                 self).selection(pre_processed_file,
                                 remove_redundancies(ranked_candidates,
                                                     pre_processed_file.tag_separator(),
                                                     self.stemmer()),
                                 clusters)

################################################################################

class UnredundantTextRankSelector(SelectorC):
  """
  Component performing selection of the keyphrases among the ranked candidate
  terms. It 'generate' keyphrases based on keywords (the k-first words) [1]. It
  is not exactly a generation, because the generated candidates must be within
  the candidates (single or multi-word expression).

  [1] Rada Mihalcea and Paul Tarau. 2004. TextRank: Bringing Order Into Texts.
      In Dekang Lin and Dekai Wu, editors, Proceedings of the 2004 Conference on
      Empirical Methods in Natural Language Processing, pages 404–411,
      Barcelona, Spain, July. Association for Computational Linguistics.
  """

  def __init__(self, name, is_lazy, lazy_directory, debug, k, stemmer):
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
    @param  stemmer:        Stemmer used to remove redundancies in the selected
                            candidates.
    @type   stemmer:        C{nltk.stem.api.StemmerI}
    """

    super(UnredundantTextRankSelector, self).__init__(name,
                                                      is_lazy,
                                                      lazy_directory,
                                                      debug)

    self.set_k(k)
    self.set_stemmer(stemmer)

  def k(self):
    """
    Getter of the number of keywords to use for the keyphrase generation.

    @return:  The number of keywords used for the keyphrase generation.
    @rtype:   C{int}
    """

    return self._k

  def set_k(self, k):
    """
    Setter of the number of keywords to use for the keyphrase generation.

    @param  k: The new number of keywords used for the keyphrase generation.
    @type   k: C{int}
    """

    self._k = k

  def stemmer(self):
    """
    Getter of the stemmer used to stem words.

    @return:  The stemmer used to stem words.
    @rtype:   C{nltk.stem.api.StemmerI}
    """

    return self._stemmer

  def set_stemmer(self, stemmer):
    """
    Setter of the stemmer used to stem words.

    @param  stemmer: The new stemmer used to stem words.
    @type   stemmer: C{nltk.stem.api.StemmerI}
    """

    self._stemmer = stemmer

  def selection(self, pre_processed_file, ranked_candidates, clusters):
    """
    Selects the keyphrases among weighted terms.

    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}
    @param    ranked_candidates:  The list of the file's ranked candidates and
                                  their weight.
    @type     ranked_candidates:  C{list(tuple(string, float))}
    @param    clusters:           The clustered candidates.
    @type     clusters:           C{list(list(string))}

    @return:  A list of weihgted keyphrases.
    @rtype:   C{list(tuple(string, float))}
    """

    weighted_keywords = {}
    weighted_n_grams = {}
    selected_keyphrases = []
    added = {}

    # get words only and remove redundancy (place n-grams elsewhere)
    nb_keywords = 0
    index = 0
    #####
    #self._k = 0
    #for c, w in ranked_candidates:
    #  if len(c.split()) == 1:
    #    self._k += 1
    #self._k /= 3
    #####
    for c, w in ranked_candidates:
      if len(c.split()) == 1:
        if nb_keywords < self.k():
          weighted_keywords[c] = w
          nb_keywords += 1
      else:
        weighted_n_grams[c] = w

    if len(weighted_n_grams) > 0:
      # add the n-grams containing only keywords (do not extracted sub strings)
      n_grams = sorted(weighted_n_grams.keys(),
                       key=lambda (c): len(c.split()),
                       reverse=True)

      for c in n_grams:
        if not added.has_key(c):
          only_keywords = True
          strings = []

          for w in c.split():
            for string in strings[:]:
              string += " " + w
              strings.append(string)
            strings.append(w)

            if weighted_keywords.keys().count(w) <= 0:
              only_keywords = False

          if only_keywords:
            # avoid from taking a sub string
            for string in strings:
              added[string] = True

            selected_keyphrases.append((c, weighted_n_grams[c]))

    for c, w in weighted_keywords.items():
      if not added.has_key(c):
        selected_keyphrases.append((c, w))

    return remove_redundancies(selected_keyphrases,
                               pre_processed_file.tag_separator(),
                               self.stemmer())

