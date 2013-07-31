#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from keybench import CandidateExtractorC
from keybench.default import NGramExtractor
from nltk import Tree
from nltk.chunk.regexp import RegexpChunkParser
from nltk.chunk.regexp import RegexpParser

################################################################################
# LongestNounPhraseExtractor
# STFilteredNGramExtractor
# POSFilteredNGramExtractor
# NPChunkExtractor
################################################################################

class LongestNounPhraseExtractor(CandidateExtractorC):
  """
  Component performing candidate terms extraction. It extracts 1..n-grams.
  """

  def __init__(self, name, is_lazy, lazy_directory, debug, noun_tags, adjective_tags):
    """
    Constructor of the component.

    @param  name:           The name of the pre-processor.
    @type   name:           C{string}
    @param  is_lazy:        True if the component can load previous datas, false
                            if everything must be computed tought it has already
                            been computed.
    @type   is_lazy:        C{boolean}
    @param  lazy_directory: The directory used for caching.
    @type   lazy_directory: C{string}
    @param  debug:          True if the component is in debug mode, else False.
                            When the component is in debug mode, it will output
                            each step of its processing.
    @type   debug:          C{bool}
    @param  noun_tags:      The list of the noun tags of the POS tagger.
    @type   noun_tags:      C{list of string}
    @param  adjective_tags: The list of adjective tags of the POS tagger.
    @type   adjective_tags: Clist of string}
    """

    super(LongestNounPhraseExtractor, self).__init__(name,
                                                     is_lazy,
                                                     lazy_directory,
                                                     debug)

    self._noun_tags = noun_tags
    self._adjective_tags = adjective_tags

  def candidate_extraction(self, pre_processed_file):
    """
    Extract the candidate terms (wanna be keyphrases) from a pre-processed file.

    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}

    @return:  A list of terms.
    @rtype:   C{list of string}
    """

    filters = list(set(self._noun_tags) | set(self._adjective_tags))
    candidates = []

    for pos_tagged_sentence in pre_processed_file.full_text():
      candidate = ""

      for tagged_word in pos_tagged_sentence.split():
        word = tagged_word.rsplit(pre_processed_file.tag_separator(), 1)[0]
        tag = tagged_word.rsplit(pre_processed_file.tag_separator(), 1)[1]

        if filters.count(tag) > 0:# and len(word) > 2 : # FIXME make a choice
          if candidate != "":
            candidate += " "
          candidate += tagged_word
        else:
          if candidate != "":
            candidates.append(candidate)

            candidate = ""

    return list(set(candidates))

################################################################################

class STFilteredNGramExtractor(NGramExtractor):
  """
  Component performing candidate terms extraction. It extracts 1..n-grams.
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

    @param  name:           The name of the pre-processor.
    @type   name:           C{string}
    @param  is_lazy:        True if the component can load previous datas, false
                            if everything must be computed tought it has already
                            been computed.
    @type   is_lazy:        C{boolean}
    @param  lazy_directory: The directory used for caching.
    @type   lazy_directory: C{string}
    @param  n:              The maximum size of a candidate term
    @type   n:              C{int}
    @param  stop_words:
    @type   stop_words:
    """

    super(STFilteredNGramExtractor, self).__init__(name,
                                                   is_lazy,
                                                   lazy_directory,
                                                   debug,
                                                   n)

    self._stop_words = stop_words

  def filtering(self, term, tag_separator):
    """
    Says if a term can be concidered as a candidate term. It only accepts terms
    with nouns and adjectives.

    @param    candidate:      The POS tagged candidate.
    @type     candidate:      C{string}
    @param    tag_separator:  The character used to separate a words from its
                              tag.
    @type     tag_separator:  C{string}

    @return:  True if the terme is a candidate term, else False.
    @rtype:   C{bool}
    """

    tagged_words = term.split()

    for tagged_word in tagged_words:
      word = tagged_word.lower().rsplit(tag_separator, 1)[0]

      if self._stop_words.count(word) > 0:
        return False

    return True

################################################################################

class POSFilteredNGramExtractor(NGramExtractor):
  """
  Component performing candidate terms extraction. It extracts 1..n-grams.
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

    @param  name:           The name of the pre-processor.
    @type   name:           C{string}
    @param  is_lazy:        True if the component can load previous datas, false
                            if everything must be computed tought it has already
                            been computed.
    @type   is_lazy:        C{boolean}
    @param  lazy_directory: The directory used for caching.
    @type   lazy_directory: C{string}
    @param  n:              The maximum size of a candidate term
    @type   n:              C{int}
    @param  noun_tags:      The list of the noun tags of the POS tagger.
    @type   noun_tags:      C{list of string}
    @param  adjective_tags: The list of adjective tags of the POS tagger.
    @type   adjective_tags: Clist of string}
    """

    super(POSFilteredNGramExtractor, self).__init__(name,
                                               is_lazy,
                                               lazy_directory,
                                               debug,
                                               n)

    self._noun_tags = noun_tags
    self._adjective_tags = adjective_tags

  def filtering(self, term, tag_separator):
    """
    Says if a term can be concidered as a candidate term. It only accepts terms
    with nouns and adjectives.

    @param    candidate:      The POS tagged candidate.
    @type     candidate:      C{string}
    @param    tag_separator:  The character used to separate a words from its
                              tag.
    @type     tag_separator:  C{string}

    @return:  True if the terme is a candidate term, else False.
    @rtype:   C{bool}
    """

    filters = []
    tagged_words = term.split()

    for t in self._noun_tags:
      filters.append(t.lower())
    for t in self._adjective_tags:
      filters.append(t.lower())

    for tagged_word in tagged_words:
      tag = tagged_word.lower().rsplit(tag_separator, 1)[1]

      # only nouns and adjectives are accepted
      if not filters.count(tag) > 0:
        return False

      # semeval trick
      if (len(tagged_word) - (len(tag) + 1)) <= 2:
        return False

    return True

################################################################################

class NPChunkExtractor(CandidateExtractorC):
  """
  Component performing candidate terms extraction. It extracts 1..n-grams.
  """

  def __init__(self, name, is_lazy, lazy_directory, debug, rule):
    """
    Constructor of the component.

    @param  name:           The name of the pre-processor.
    @type   name:           C{string}
    @param  is_lazy:        True if the component can load previous datas, false
                            if everything must be computed tought it has already
                            been computed.
    @type   is_lazy:        C{boolean}
    @param  lazy_directory: The directory used for caching.
    @type   lazy_directory: C{string}
    @param  rule:
    @type   rule:
    """

    super(NPChunkExtractor, self).__init__(name, is_lazy, lazy_directory, debug)

    self._np_chunker = RegexpParser("NP: " + rule)

  def candidate_extraction(self, pre_processed_file):
    """
    Extract the candidate terms (wanna be keyphrases) from a pre-processed file.

    @param    pre_processed_file: The pre-processed file.
    @type     pre_processed_file: C{PreProcessedFile}

    @return:  A list of terms.
    @rtype:   C{list of string}
    """

    sentences = pre_processed_file.full_text()
    candidates = []
    
    for sentence in sentences:
      sentence_tree = []

      for wt in sentence.split():
        sentence_tree.append(tuple(wt.rsplit(pre_processed_file.tag_separator(),
                                             1)))
      sentence_tree = self._np_chunker.parse(sentence_tree)

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
    Says if a term can be concidered as a candidate term.

    @param    candidate:      The POS tagged candidate.
    @type     candidate:      C{string}
    @param    tag_separator:  The character used to separate a words from its
                              tag.
    @type     tag_separator:  C{string}

    @return:  True if the term is a candidate term, else False.
    @rtype:   C{bool}
    """

    return True

