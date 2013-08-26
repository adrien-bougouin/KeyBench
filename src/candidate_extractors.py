#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from keybench import CandidateExtractorC
from keybench.default import NGramExtractor
from nltk import Tree
from nltk.chunk.regexp import RegexpParser

################################################################################
# NPChunkExtractor
# STFilteredNGramExtractor
# POSFilteredNGramExtractor
# LongestNounPhraseExtractor

################################################################################

class NPChunkExtractor(CandidateExtractorC):
  """
  Component performing candidate terms extraction. It extracts NP chunks (based
  on a given rule).
  """

  def __init__(self, name, is_lazy, lazy_directory, debug, rule):
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
    @param  rule:           The rule to parse NP chunks. It is expressed with
                            POS tags.
    @type   rule:           C{string}
    """

    super(NPChunkExtractor, self).__init__(name, is_lazy, lazy_directory, debug)

    self.set_np_chunker(RegexpParser("NP: " + rule))

  def np_chunker(self):
    """
    Getter of the chunker used to extract the NP chunks.

    @return: The parser used to identify NP chunks.
    @rtype:  C{nltk.parse.api.ParserI}
    """

    return self._np_chunker

  def set_np_chunker(self, np_chunker):
    """
    Setter of the chunker used to extract the NP chunks.

    @param  np_chunker: The new parser used to identify NP chunks.
    @type   np_chunker: C{nltk.parse.api.ParserI}
    """

    self._np_chunker = np_chunker

  def candidate_extraction(self, pre_processed_file):
    """
    Extracts the candidates from a pre-processed file.

    @param    pre_processed_file: The pre-processed analysed file.
    @type     pre_processed_file: C{PreProcessedFile}

    @return:  A list of candidates.
    @rtype:   C{list(string)}
    """

    sentences = pre_processed_file.full_text()
    candidates = []
    
    for sentence in sentences:
      sentence_tree = []

      for wt in sentence.split():
        sentence_tree.append(tuple(wt.rsplit(pre_processed_file.tag_separator(),
                                             1)))
      sentence_tree = self.np_chunker().parse(sentence_tree)

      for child in sentence_tree:
        if type(child) is Tree:
          if child.node == "NP":
            candidate = ""

            for word, tag in child.leaves():
              if candidate != "":
                candidate += " "
              candidate += word + pre_processed_file.tag_separator() + tag

            candidates.append(candidate)

    return candidates

  def filtering(self, term, tag_separator):
    """
    Indicates if a candidate can be concidered as a keyphrase candidate or not.

    @param    candidate:      The POS tagged candidate.
    @type     candidate:      C{string}
    @param    tag_separator:  The character used to separate a words from its
                              tag.
    @type     tag_separator:  C{string}

    @return:  True if the candidate is a keyphrase candidate, else False.
    @rtype:   C{bool}
    """

    return True

################################################################################

class STFilteredNGramExtractor(NGramExtractor):
  """
  Component performing candidate terms extraction. It extracts 1..n-grams
  filtered by a list of common words (stop words).
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               debug,
               n,
               stop_words):
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
    @param  n:              The maximum size of a candidate term
    @type   n:              C{int}
    @param  stop_words:     The list of stop words (common words).
    @type   stop_words:     C{list(string)}
    """

    super(STFilteredNGramExtractor, self).__init__(name,
                                                   is_lazy,
                                                   lazy_directory,
                                                   debug,
                                                   n)

    self.set_stop_words(stop_words)

  def stop_words(self):
    """
    Getter of the list of stop words.

    @return:  The list of stop words used to filter the n-grams.
    @rtype:   C{list(string)}
    """

    return self._stop_words

  def set_stop_words(self, stop_words):
    """
    Setter of the list of stop words.

    @param  stop_words: The new list of stop words used to filter the n-grams.
    @type   stop_words: C{list(string)}
    """

    self._stop_words = stop_words

  def filtering(self, term, tag_separator):
    """
    Indicates if a candidate can be concidered as a keyphrase candidate or not.

    @warning: This function includes a trick to avoid from extracting variables
              that could be find into SemEval document.

    @param    candidate:      The POS tagged candidate.
    @type     candidate:      C{string}
    @param    tag_separator:  The character used to separate a words from its
                              tag.
    @type     tag_separator:  C{string}

    @return:  True if the candidate is a keyphrase candidate, else False.
    @rtype:   C{bool}
    """

    tagged_words = term.split()

    for tagged_word in tagged_words:
      word = tagged_word.lower().rsplit(tag_separator, 1)[0]

      # only words not included into the stop word list
      if self.stop_words().count(word) > 0:
        return False

      # FIXME semeval trick
      #if len(word) <= 2:
      #  return False

    return True

################################################################################

class POSFilteredNGramExtractor(NGramExtractor):
  """
  Component performing candidate terms extraction. It extracts 1..n-grams
  filtered by POS tags.
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               debug,
               n,
               noun_tags,
               adjective_tags):
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
    @param  n:              The maximum size of a candidate term
    @type   n:              C{int}
    @param  noun_tags:      The list of the noun tags given by the POS tagger.
    @type   noun_tags:      C{list(string)}
    @param  adjective_tags: The list of adjective tags given by the POS tagger.
    @type   adjective_tags: C{list(string)}
    """

    super(POSFilteredNGramExtractor, self).__init__(name,
                                               is_lazy,
                                               lazy_directory,
                                               debug,
                                               n)

    self.set_noun_tags(noun_tags)
    self.set_adjective_tags(adjective_tags)

  def noun_tags(self):
    """
    Getter of the POS tags representing nouns.

    @return:  The list of POS tags representing nouns.
    @rtype:   C{list(string)}
    """

    return self._noun_tags

  def set_noun_tags(self, noun_tags):
    """
    Setter of the POS tags representing nouns.

    @param  noun_tags: The new list of POS tags representing nouns.
    @type   noun_tags: C{list(string)}
    """

    self._noun_tags = noun_tags

  def adjective_tags(self):
    """
    Getter of the POS tags representing adjectives.

    @return:  The list of POS tags representing adjectives.
    @rtype:   C{list(string)}
    """

    return self._adjective_tags

  def set_adjective_tags(self, adjective_tags):
    """
    Setter of the POS tags representing adjectives.

    @param  adjective_tags: The new list of POS tags representing adjectives.
    @type   adjective_tags: C{list(string)}
    """

    self._adjective_tags = adjective_tags

  def filtering(self, term, tag_separator):
    """
    Indicates if a candidate can be concidered as a keyphrase candidate or not.

    @warning: This function includes a trick to avoid from extracting variables
              that could be find into SemEval document.

    @param    candidate:      The POS tagged candidate.
    @type     candidate:      C{string}
    @param    tag_separator:  The character used to separate a words from its
                              tag.
    @type     tag_separator:  C{string}

    @return:  True if the candidate is a keyphrase candidate, else False.
    @rtype:   C{bool}
    """

    filters = []
    tagged_words = term.split()

    for t in self.noun_tags():
      filters.append(t.lower())
    for t in self.adjective_tags():
      filters.append(t.lower())

    for tagged_word in tagged_words:
      tag = tagged_word.lower().rsplit(tag_separator, 1)[1]

      # only nouns and adjectives are accepted
      if not filters.count(tag) > 0:
        return False

      # FIXME semeval trick
      #if (len(tagged_word) - (len(tag) + 1)) <= 2:
      #  return False

    return True

################################################################################

class LongestNounPhraseExtractor(CandidateExtractorC):
  """
  Component performing candidate terms extraction. It extracts noun phrases,
  i.e. the longest sequences of nouns and adjectives.
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               debug,
               noun_tags,
               adjective_tags):
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
    @param  noun_tags:      The list of the noun tags given by the POS tagger.
    @type   noun_tags:      C{list(string)}
    @param  adjective_tags: The list of adjective tags given by the POS tagger.
    @type   adjective_tags: C{list(string)}
    """

    super(LongestNounPhraseExtractor, self).__init__(name,
                                                     is_lazy,
                                                     lazy_directory,
                                                     debug)

    self.set_noun_tags(noun_tags)
    self.set_adjective_tags(adjective_tags)

  def noun_tags(self):
    """
    Getter of the POS tags representing nouns.

    @return:  The list of POS tags representing nouns.
    @rtype:   C{list(string)}
    """

    return self._noun_tags

  def set_noun_tags(self, noun_tags):
    """
    Setter of the POS tags representing nouns.

    @param  noun_tags: The new list of POS tags representing nouns.
    @type   noun_tags: C{list(string)}
    """

    self._noun_tags = noun_tags

  def adjective_tags(self):
    """
    Getter of the POS tags representing adjectives.

    @return:  The list of POS tags representing adjectives.
    @rtype:   C{list(string)}
    """

    return self._adjective_tags

  def set_adjective_tags(self, adjective_tags):
    """
    Setter of the POS tags representing adjectives.

    @param  adjective_tags: The new list of POS tags representing adjectives.
    @type   adjective_tags: C{list(string)}
    """

    self._adjective_tags = adjective_tags

  def candidate_extraction(self, pre_processed_file):
    """
    Extracts the candidates from a pre-processed file.

    @warning: This function includes a trick to avoid from extracting variables
              that could be find into SemEval document.

    @param    pre_processed_file: The pre-processed analysed file.
    @type     pre_processed_file: C{PreProcessedFile}

    @return:  A list of candidates.
    @rtype:   C{list(string)}
    """

    filters = list(set(self.noun_tags()) | set(self.adjective_tags()))
    candidates = []

    for pos_tagged_sentence in pre_processed_file.full_text():
      candidate = ""

      for tagged_word in pos_tagged_sentence.split():
        word = tagged_word.rsplit(pre_processed_file.tag_separator(), 1)[0]
        tag = tagged_word.rsplit(pre_processed_file.tag_separator(), 1)[1]

        if filters.count(tag) > 0:# and len(word) > 2 : # FIXME semeval trick
          if candidate != "":
            candidate += " "
          candidate += tagged_word
        else:
          if candidate != "":
            candidates.append(candidate)

            candidate = ""

    return list(set(candidates))

