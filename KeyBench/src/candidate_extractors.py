#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
import re
from keybench import CandidateExtractorC
from keybench.default import NGramExtractor
from keybench.default.util import n_to_m_grams
from multiprocessing import Pool
from nltk import Tree
from nltk.chunk.regexp import RegexpParser
from os import path
from os import listdir

################################################################################
# NPChunkExtractor
# STFilteredNGramExtractor
# PatternMatchingExtractor
# CLARIT96Extractor
# FromTerminologyExtractor
# POSSequenceExtractor
# POSBoundaryBasedCandidateExtractor
# ExpandedCoreWordExtractor

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

            if self.filtering(candidate, pre_processed_file.tag_separator()):
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

#    for wt in term.split():
#      w = wt.rsplit(tag_separator, 1)[0]
#
#      if len(w) <= 2: # FIXME semeval trick
#        return False

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

    for i, tagged_word in enumerate(tagged_words):
      word = tagged_word.lower().rsplit(tag_separator, 1)[0]

      # only candidate with first and last words not included into the stop word
      # list are accepted
      if i == 0 or i == (len(tagged_words) - 1):
        if self.stop_words().count(word) > 0:
          return False

      # FIXME semeval trick
#      if len(word) <= 2:
#        return False

    return True

################################################################################

class PatternMatchingExtractor(CandidateExtractorC):
  """
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               debug,
               patterns):
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
    TODO patterns
    TODO patterns
    """

    super(PatternMatchingExtractor, self).__init__(name,
                                                   is_lazy,
                                                   lazy_directory,
                                                   debug)

    self.set_patterns(patterns)

  def patterns(self):
    """
    """

    return self._patterns

  def set_patterns(self, patterns):
    """
    """

    self._patterns = patterns

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

    sentences = pre_processed_file.full_text()
    candidates = []

    for sentence in sentences:
      # pattern matching
      for pattern in self.patterns():
        for match in re.finditer(pattern, sentence):
          candidate = match.group(0).strip()
          accepted = True
          
          if candidate != "":
            for wt in candidate.split():
              w = wt.rsplit(pre_processed_file.tag_separator(), 1)[0]

              if len(w) <= 2: # FIXME semeval trick
                accepted = False

            if accepted:
              candidates.append(candidate)

    return candidates

################################################################################

CLARIT96_LEXATOM_TAG = "lexatom"
CLARIT96_INNER_GROUP_SEPARATOR = "__CLARIT'96_GROUP__"

##### Multi-processing #########################################################

def noun_phrase_extraction_pool_worker(arguments):
  """
  """

  filename, train_directory, pre_processor, candidate_extractor = arguments
  filepath = path.join(train_directory, filename)
  pre_processed_file = pre_processor.pre_process_file(filepath)

  return candidate_extractor.extract_candidates(filepath, pre_processed_file)

def train_clarit(train_directory,
                 file_extension,
                 pre_processor,
                 candidate_extractor): # must be a noun phrase extractor
  working_pool = Pool()
  pool_args = []
  nps = []

  for filename in listdir(train_directory):
    if filename.rfind(file_extension) >= 0 \
       and len(filename) - filename.rfind(file_extension) == len(file_extension):
      pool_args.append((filename,
                        train_directory,
                        pre_processor,
                        candidate_extractor))

  noun_phrase_sets = working_pool.map(noun_phrase_extraction_pool_worker,
                                      pool_args)

  for noun_phrases in noun_phrase_sets:
    for noun_phrase in noun_phrases:
      nps.append(noun_phrase)


  return nps

################################################################################

class CLARIT96Extractor(PatternMatchingExtractor):
  """
  TODO supose that patterns extracts noun phrases
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               debug,
               noun_phrase_patterns,
               lexical_atom_patterns,
               special_phrase_patterns,
               impossible_phrase_patterns,
               train_noun_phrases):
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
    TODO train_noun_phrases
    TODO train_noun_phrases
    TODO noun_phrase_patterns
    TODO noun_phrase_patterns
    TODO
    TODO
    TODO
    TODO
    TODO
    TODO
    """

    super(CLARIT96Extractor, self).__init__(name,
                                            is_lazy,
                                            lazy_directory,
                                            debug,
                                            noun_phrase_patterns)

    self.set_lexical_atom_patterns(lexical_atom_patterns)
    self.set_special_phrase_patterns(special_phrase_patterns)
    self.set_impossible_phrase_patterns(impossible_phrase_patterns)
    self.set_train_noun_phrases(train_noun_phrases)

  def lexical_atom_patterns(self):
    """
    """

    return self._lexical_atom_patterns

  def set_lexical_atom_patterns(self, lexical_atom_patterns):
    """
    """

    self._lexical_atom_patterns = lexical_atom_patterns

  def special_phrase_patterns(self):
    """
    """

    return self._special_phrase_patterns

  def set_special_phrase_patterns(self, special_phrase_patterns):
    """
    """

    self._special_phrase_patterns = special_phrase_patterns

  def impossible_phrase_patterns(self):
    """
    """

    return self._impossible_phrase_patterns

  def set_impossible_phrase_patterns(self, impossible_phrase_patterns):
    """
    """

    self._impossible_phrase_patterns = impossible_phrase_patterns

  def train_noun_phrases(self):
    """
    """

    return self._train_noun_phrases

  def set_train_noun_phrases(self, train_noun_phrases):
    """
    """

    self._train_noun_phrases = train_noun_phrases

  def continuous_frequencies(self):
    """
    """

    return self._continuous_frequencies

  def set_continuous_frequencies(self, continuous_frequencies):
    """
    """

    self._continuous_frequencies = continuous_frequencies

  def discontinuous_frequencies(self):
    """
    """

    return self._discontinuous_frequencies

  def set_discontinuous_frequencies(self, discontinuous_frequencies):
    """
    """

    self._discontinuous_frequencies = discontinuous_frequencies

  def is_possible_lexical_atom(self, pair, lexical_atoms, tag_separator):
    """
    """
    phrase1, phrase2 = pair
    # mark lexatoms
    if lexical_atoms.count(phrase1):
      phrase1 = phrase1 + tag_separator + CLARIT96_LEXATOM_TAG
    else:
      phrase1 = phrase1.replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()
    if lexical_atoms.count(phrase2):
      phrase2 = phrase2 + tag_separator + CLARIT96_LEXATOM_TAG
    else:
      phrase2 = phrase2.replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()
    pair_phrase = "%s %s"%(phrase1, phrase2)

    if len(pair_phrase.split()) == 2:
      for pattern in self.lexical_atom_patterns():
        if pattern != "":
          # ensure a match on the whole phrase
          if pattern[0] != "^":
            pattern = "^" + pattern
          if pattern[-1] != "$":
            pattern += "$"

          if re.match(pattern, pair_phrase) != None:
            return True

    return False

  def is_special_pair(self, pair):
    """
    """

    phrase1 = pair[0].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()
    phrase2 = pair[1].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()
    pair_phrase = "%s %s"%(phrase1, phrase2)

    if len(pair_phrase.split()) == 2:
      for pattern in self.special_phrase_patterns():
        if pattern != "":
          # ensure a match on the whole phrase
          if pattern[0] != "^":
            pattern = "^" + pattern
          if pattern[-1] != "$":
            pattern += "$"

          if re.match(pattern, pair_phrase) != None:
            return True

    return False

  def is_impossible_pair(self, pair):
    """
    """

    phrase1 = pair[0].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()
    phrase2 = pair[1].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()
    pair_phrase = "%s %s"%(phrase1, phrase2)

    if len(pair_phrase.split()) == 2:
      for pattern in self.impossible_phrase_patterns():
        if pattern != "":
          # ensure a match on the whole phrase
          if pattern[0] != "^":
            pattern = "^" + pattern
          if pattern[-1] != "$":
            pattern += "$"

          if re.match(pattern, pair_phrase) != None:
            return True

    return False

  def frequency(self, phrase, noun_phrases, lazy_dic):
    """
    """

    if phrase not in lazy_dic:
      phrase_count = 0.0

      for noun_phrase in noun_phrases:
        phrase_count += float(noun_phrase.count(phrase))
      lazy_dic[phrase] = phrase_count

      return phrase_count
    else:
      return lazy_dic[phrase]

  def continuous_frequency(self, pair, noun_phrases, sub_lazy_dic):
    """
    """

    phrase1 = pair[0].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()
    phrase2 = pair[1].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()
    pair_phrase = "%s %s"%(phrase1, phrase2)

    return self.frequency(pair_phrase, noun_phrases, sub_lazy_dic)

  def discontinuous_frequency(self, pair, noun_phrases, lazy_dic):
    """
    """

    if str(pair) not in lazy_dic:
      discontinuous_count = 0.0
      phrase1 = pair[0].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()
      phrase2 = pair[1].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()

      for noun_phrase in noun_phrases:
        discontinuous_count += float(len(re.findall("%s .*? %s"%(re.escape(phrase1),
                                                                 re.escape(phrase2)),
                                                    noun_phrase)))
      lazy_dic[str(pair)] = discontinuous_count

      return discontinuous_count
    else:
      return lazy_dic[str(pair)]

  def left_discontinuous_frequency(self, w, p1, p2, noun_phrases, cf_lazy_dic, df_lazy_dic):
    """
    """

    f_w_p1 = self.continuous_frequency((w, p1), noun_phrases, cf_lazy_dic)
    df_w_p2 = self.discontinuous_frequency((w, p2), noun_phrases, df_lazy_dic)

    return min(f_w_p1, df_w_p2)

  def right_discontinuous_frequency(self, p1, p2, w, noun_phrases, cf_lazy_dic, df_lazy_dic):
    """
    """

    df_p1_w = self.discontinuous_frequency((p1, w), noun_phrases, df_lazy_dic)
    f_p2_w = self.continuous_frequency((p2, w), noun_phrases, cf_lazy_dic)

    return min(df_p1_w, f_p2_w)

  def maximum_left_discontinuous_frequency(self, pair, word_noun_phrases, word_bag, cf_lazy_dic, df_lazy_dic, lazy_dic):
    """
    """

    if str(pair) not in lazy_dic:
      max_ldf = 0.0
      phrase1 = pair[0].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()
      phrase2 = pair[1].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()

      # compute max_lfd
      for word in word_bag:
        if word != phrase1 and word != phrase2:
          ldf = self.left_discontinuous_frequency(word, phrase1, phrase2, word_noun_phrases[word], cf_lazy_dic, df_lazy_dic)

          max_ldf = max(max_ldf, ldf)
      lazy_dic[str(pair)] = max_ldf

      return max_ldf
    else:
      return lazy_dic[str(pair)]

  def maximum_right_discontinuous_frequency(self, pair, word_noun_phrases, word_bag, cf_lazy_dic, df_lazy_dic, lazy_dic):
    """
    """

    if str(pair) not in lazy_dic:
      max_rdf = 0.0
      phrase1 = pair[0].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()
      phrase2 = pair[1].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()

      # compute max_rfd
      for word in word_bag:
        if word != phrase1 and word != phrase2:
          rdf = self.right_discontinuous_frequency(phrase1, phrase2, word, word_noun_phrases[word], cf_lazy_dic, df_lazy_dic)

          max_rdf = max(max_rdf, rdf)
      lazy_dic[str(pair)] = max_rdf

      return max_rdf
    else:
      return lazy_dic[str(pair)]

  def average_left_discontinuous_frequency(self, pair, word_noun_phrases, word_bag, cf_lazy_dic, df_lazy_dic, lazy_dic):
    """
    """

    if str(pair) not in lazy_dic:
      max_ldf = 0.0
      ld = 1.0
      phrase1 = pair[0].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()
      phrase2 = pair[1].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()

      # compute max_lfd
      for word in word_bag:
        if word != phrase1 and word != phrase2:
          ldf = self.left_discontinuous_frequency(word, phrase1, phrase2, word_noun_phrases[word], cf_lazy_dic, df_lazy_dic)

          if ldf != 0.0:
            ld += 1.0

          max_ldf = max(max_ldf, ldf)
      lazy_dic[str(pair)] = max_ldf / ld

      return max_ldf / ld
    else:
      return lazy_dic[str(pair)]

  def average_right_discontinuous_frequency(self, pair, word_noun_phrases, word_bag, cf_lazy_dic, df_lazy_dic, lazy_dic):
    """
    """

    if str(pair) not in lazy_dic:
      max_rdf = 0.0
      rd = 1.0
      phrase1 = pair[0].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()
      phrase2 = pair[1].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()

      # compute max_rfd
      for word in word_bag:
        if word != phrase1 and word != phrase2:
          rdf = self.right_discontinuous_frequency(phrase1, phrase2, word, word_noun_phrases[word], cf_lazy_dic, df_lazy_dic)

          if rdf != 0.0:
            rd += 1.0

          max_rdf = max(max_rdf, rdf)
      lazy_dic[str(pair)] = max_rdf / rd

      return max_rdf / rd
    else:
      return lazy_dic[str(pair)]

  def association(self, pair, noun_phrases, cf_lazy_dic, df_lazy_dic):
    """
    """

    phrase1 = pair[0].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()
    phrase2 = pair[1].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()
    lambda2 = 1000.0 # FIXME this is the default threshold
    frequency1 = self.frequency(phrase1, noun_phrases, cf_lazy_dic)
    frequency2 = self.frequency(phrase2, noun_phrases, cf_lazy_dic)
    frequency12 = self.continuous_frequency(pair, noun_phrases, cf_lazy_dic)

    return (lambda2 / (frequency1 + frequency2 - (2.0 * frequency12) + lambda2))

  def association_score(self, pair, noun_phrases, word_noun_phrases, word_bag, cf_lazy_dic, df_lazy_dic, avg_ldf_lazy_dic, avg_rdf_lazy_dic):
    """
    """

    lambda1 = 5.0 # FIXME this is the default threshold
    avg_ldf = self.average_left_discontinuous_frequency(pair, word_noun_phrases, word_bag, cf_lazy_dic, df_lazy_dic, avg_ldf_lazy_dic)
    avg_rdf = self.average_right_discontinuous_frequency(pair, word_noun_phrases, word_bag, cf_lazy_dic, df_lazy_dic, avg_rdf_lazy_dic)
    f = self.continuous_frequency(pair, noun_phrases, cf_lazy_dic)
    df = self.discontinuous_frequency(pair, noun_phrases, df_lazy_dic)
    a = self.association(pair, noun_phrases, cf_lazy_dic, df_lazy_dic)

    return (((lambda1 + avg_ldf + avg_rdf) / ((lambda1 * f) + df )) * a)

  def locally_dominant_count(self, pair, noun_phrases, word_noun_phrases, word_bag, cf_lazy_dic, df_lazy_dic, avg_ldf_lazy_dic, avg_rdf_lazy_dic, lazy_dic):
    if str(pair) not in lazy_dic:
      dominant_count = 0.0
      phrase1 = pair[0].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()
      phrase2 = pair[1].replace(CLARIT96_INNER_GROUP_SEPARATOR, " ").strip()
      pair_phrase = "%s %s"%(phrase1, phrase2)
      pair_word_bag = list(set(phrase1.split()) | set(phrase2.split()))
      association_score = self.association_score(pair,
                                                 noun_phrases,
                                                 word_noun_phrases,
                                                 word_bag,
                                                 cf_lazy_dic,
                                                 df_lazy_dic,
                                                 avg_ldf_lazy_dic,
                                                 avg_rdf_lazy_dic)

      for noun_phrase in word_noun_phrases[pair_word_bag[0]]: # reduce the amount of phrase to browse
        if noun_phrase.count(pair_phrase) > 0:
          max_score = association_score

          for i, wt in enumerate(noun_phrase.split()[:-1]):
            p = (wt, noun_phrase.split()[i + 1])
            max_score = max(max_score, self.association_score(p,
                                                              noun_phrases,
                                                              word_noun_phrases,
                                                              word_bag,
                                                              cf_lazy_dic,
                                                              df_lazy_dic,
                                                              avg_ldf_lazy_dic,
                                                              avg_rdf_lazy_dic))

            if max_score != association_score:
              break

          if max_score == association_score:
            dominant_count += 1.0
      lazy_dic[str(pair)] = dominant_count

      return dominant_count
    else:
      return lazy_dic[str(pair)]

  def preference_score(self, pair, noun_phrases, word_noun_phrases, word_bag, cf_lazy_dic, df_lazy_dic, avg_ldf_lazy_dic, avg_rdf_lazy_dic, ldc_lazy_dic):
    """
    """

    ldc = self.locally_dominant_count(pair, noun_phrases, word_noun_phrases, word_bag, cf_lazy_dic, df_lazy_dic, avg_ldf_lazy_dic, avg_rdf_lazy_dic, ldc_lazy_dic)
    f = self.continuous_frequency(pair, noun_phrases, cf_lazy_dic)

    return (ldc / f)

  def candidate_extraction(self, pre_processed_file):
    """
    Extracts the candidates from a pre-processed file.

    @param    pre_processed_file: The pre-processed analysed file.
    @type     pre_processed_file: C{PreProcessedFile}

    @return:  A list of candidates.
    @rtype:   C{list(string)}
    """

    noun_phrases = list(self.train_noun_phrases())
    candidates = []
    word_bag = []
    word_noun_phrases = {}
    # 'lazy loading' structures
    continuous_frequencies = {}
    discontinuous_frequencies = {}
    maximum_left_discontinuous_frequencies = {}
    maximum_right_discontinuous_frequencies = {}
    average_left_discontinuous_frequencies = {}
    average_right_discontinuous_frequencies = {}
    locally_dominant_counts = {}

    # extract candidates and add them to the whole noun phrases
    for candidate in super(CLARIT96Extractor, self).candidate_extraction(pre_processed_file):
      noun_phrases.append(candidate)
      candidates.append(candidate)

    # create the bag of words
    for noun_phrase in noun_phrases:
      for word in set(noun_phrase.split()):
        if word not in word_noun_phrases:
          word_noun_phrases[word] = []
        word_noun_phrases[word].append(noun_phrase)
        word_bag.append(word)
    word_bag = list(set(word_bag))

    # add noun phrases' subcompounds
    candidate_set = list(set(candidates))
    for noun_phrase in candidate_set:
      if len(noun_phrase.split()) > 2:
        lexical_atoms = []
        previous_groups = None
        current_groups = []
        s_ips = {}

        while current_groups != previous_groups:
          previous_groups = list(current_groups)
          pairs = []
          possible_groupings = []

          # create pairs
          for i, wt in enumerate(noun_phrase.split()[:-1]):
            pairs.append((wt, noun_phrase.split()[i + 1]))

          # find lexical atoms
          for pair in pairs:
            continuous_frequency = self.continuous_frequency(pair,
                                                             noun_phrases,
                                                             continuous_frequencies)
            discontinuous_frequency = self.discontinuous_frequency(pair,
                                                                   noun_phrases,
                                                                   discontinuous_frequencies)
            max_ldf = self.maximum_left_discontinuous_frequency(pair,
                                                                word_noun_phrases,
                                                                word_bag,
                                                                continuous_frequencies,
                                                                discontinuous_frequencies,
                                                                maximum_left_discontinuous_frequencies)
            max_rdf = self.maximum_right_discontinuous_frequency(pair,
                                                                 word_noun_phrases,
                                                                 word_bag,
                                                                 continuous_frequencies,
                                                                 discontinuous_frequencies,
                                                                 maximum_right_discontinuous_frequencies)
            heuristique_1 = (continuous_frequency > max_ldf) and (continuous_frequency > max_rdf)
            heuristique_2 = (continuous_frequency - discontinuous_frequency) > 0.0 # FIXME must be a threshold

            if self.is_possible_lexical_atom(pair,
                                             lexical_atoms,
                                             pre_processed_file.tag_separator())\
               and heuristique_1\
               and heuristique_2:
              lexical_atoms.append(pair)

          # compute S and PS scores of each pair, keep the possible groupings and
          # order them pairs
          for pair in pairs:
            s = None
            ips = None

            if str(pair) not in s_ips:
              if self.is_impossible_pair(pair):
                s = 100.0
              elif self.is_special_pair(pair):
                s = 10.0
              elif lexical_atoms.count(pair) > 0:
                s = 0.0
              else:
                s = self.association_score(pair,
                                           noun_phrases,
                                           word_noun_phrases,
                                           word_bag,
                                           continuous_frequencies,
                                           discontinuous_frequencies,
                                           average_left_discontinuous_frequencies,
                                           average_right_discontinuous_frequencies)
              ips = 0.0
              ps = self.preference_score(pair,
                                         noun_phrases,
                                         word_noun_phrases,
                                         word_bag,
                                         continuous_frequencies,
                                         discontinuous_frequencies,
                                         average_left_discontinuous_frequencies,
                                         average_right_discontinuous_frequencies,
                                         locally_dominant_counts)
              if ps != 0.0:
                ips = 1.0 / ps

              s_ips[str(pair)] = (s, ips)
            else:
              s, ips = s_ips[str(pair)]

            # filter by PS
            if ips != 0.0:
              if s != 100.0 and (1.0 / ips) >= 0.5: # FIXME this is a test threshold (default is 0.7)
                possible_groupings.append(pair)
          # order by S then PS
          possible_groupings = sorted(possible_groupings,
                                      key=lambda p: s_ips[str(p)])

          # the best pair is now one unit into the processed noun phrase
          # => (a, b) -> a__CLARIT'96_GROUP__b
          if len(possible_groupings) > 0:
            left, right = possible_groupings[0]

            noun_phrase = noun_phrase.replace("%s %s"%(left, right),
                                              "%s%s%s"%(left, CLARIT96_INNER_GROUP_SEPARATOR, right))
            current_groups.append((left, right))
            # the pair is added as a candidate
            candidates.append("%s %s"%(left.replace(CLARIT96_INNER_GROUP_SEPARATOR, " "),
                                       right.replace(CLARIT96_INNER_GROUP_SEPARATOR, " ")))

    return candidates

################################################################################

class FromTerminologyExtractor(CandidateExtractorC):
  """
  """

  def __init__(self, name, is_lazy, lazy_directory, debug, terminology_filepath, encoding, tokenize_function):
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
    TODO
    TODO
    TODO
    TODO
    """

    super(FromTerminologyExtractor, self).__init__(name, is_lazy, lazy_directory, debug)

    terminology = {}
    terminology_file = codecs.open(terminology_filepath, "r", encoding)

    for term in terminology_file.read().split("\n"):
      term = term.strip()

      if term != "":
        terminology[tokenize_function(term)] = True

    terminology_file.close()

    self.set_terminology(terminology)

  def terminology(self):
    """
    """

    return self._terminology

  def set_terminology(self, terminology):
    """
    """

    self._terminology = terminology

  def candidate_extraction(self, pre_processed_file):
    """
    Extracts the candidates from a pre-processed file.

    @param    pre_processed_file: The pre-processed analysed file.
    @type     pre_processed_file: C{PreProcessedFile}

    @return:  A list of candidates.
    @rtype:   C{list(string)}
    """

    candidates = []
    sentences = pre_processed_file.full_text()

    for sentence in sentences:
      for candidate in n_to_m_grams(sentence.split(), 1, len(sentence.split())):
        untagged_candidate = ""

        for word in candidate.split():
          if untagged_candidate != "":
            untagged_candidate += " "
          untagged_candidate += word.rsplit(pre_processed_file.tag_separator(), 1)[0]

        if untagged_candidate in self.terminology():
          candidates.append(candidate)

    return candidates

################################################################################

class POSSequenceExtractor(CandidateExtractorC):
  """
  Component performing candidate terms extraction. It extracts NP chunks (based
  on a given rule).
  """

  def __init__(self, name, is_lazy, lazy_directory, debug, pos_sequences, stop_words):
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
    TODO pos_sequences
    TODO pos_sequences
    """

    super(POSSequenceExtractor, self).__init__(name,
                                               is_lazy,
                                               lazy_directory,
                                               debug)

    self.set_stop_words(stop_words)
    self.set_pos_sequences(pos_sequences)

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

  def pos_sequences(self):
    """
    """

    return self._pos_sequences

  def set_pos_sequences(self, pos_sequences):
    """
    """

    self._pos_sequences = pos_sequences

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
      for candidate in n_to_m_grams(sentence.split(), 1, len(sentence.split())):
        tag_sequence = ""

        for wt in candidate.split(" "):
          if tag_sequence != "":
            tag_sequence += " "
          tag_sequence += wt.rsplit(pre_processed_file.tag_separator(), 1)[1]

        if tag_sequence in self.pos_sequences():
          if self.filtering(candidate, pre_processed_file.tag_separator()):
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

    tagged_words = term.split()

    for i, tagged_word in enumerate(tagged_words):
      word = tagged_word.lower().rsplit(tag_separator, 1)[0]

      # only candidate with first and last words not included into the stop word
      # list are accepted
      if i == 0 or i == (len(tagged_words) - 1):
        if self.stop_words().count(word) > 0:
          return False

      # FIXME semeval trick
#      if len(word) <= 2:
#        return False

    return True

################################################################################

class POSBoundaryBasedCandidateExtractor(CandidateExtractorC):
  """
  """

  def __init__(self, name, is_lazy, lazy_directory, debug, pos_boundaries):
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
    TODO pos_boundaries {"POS boundary": ["exception", "words", "when", "not", "at", "the", "beging", "or", "end"]}
    TODO pos_boundaries {"POS boundary": ["exception", "words", "when", "not", "at", "the", "beging", "or", "end"]}
    TODO pos_boundaries {"POS boundary": ["exception", "words", "when", "not", "at", "the", "beging", "or", "end"]}
    TODO pos_boundaries {"POS boundary": ["exception", "words", "when", "not", "at", "the", "beging", "or", "end"]}
    """

    super(POSBoundaryBasedCandidateExtractor, self).__init__(name,
                                                             is_lazy,
                                                             lazy_directory,
                                                             debug)

    self._pos_boundaries = pos_boundaries

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
      current_candidate = []
      for wt in sentence.split(" "):
        w = wt.rsplit(pre_processed_file.tag_separator(), 1)[0]
        t = wt.rsplit(pre_processed_file.tag_separator(), 1)[1]

        if t in self._pos_boundaries:
          # do not consider exception cases yet
          if w not in self._pos_boundaries[t]:
            if len(current_candidate) > 0:
              # check exception at the begining
              while current_candidate[0].rsplit(pre_processed_file.tag_separator(), 1)[1] in self._pos_boundaries:
                if len(current_candidate) > 1:
                  current_candidate = current_candidate[1:]
                else:
                  current_candidate = []
                  break
              if len(current_candidate) > 0:
                # check exception at the end
                while current_candidate[-1].rsplit(pre_processed_file.tag_separator(), 1)[1] in self._pos_boundaries:
                  if len(current_candidate) > 1:
                    current_candidate = current_candidate[:-1]
                  else:
                    current_candidate = []
                    break
              if len(current_candidate) > 0:
                candidate = " ".join(current_candidate)
                current_candidate = []
                if self.filtering(candidate, pre_processed_file.tag_separator()):
                  candidates.append(candidate)
          else:
            current_candidate.append(wt)
        else:
          current_candidate.append(wt)

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

      # FIXME semeval trick
#      if len(word) <= 2:
#        return False

    return True

################################################################################

class ExpandedCoreWordExtractor(CandidateExtractorC):
  """
  Component performing candidate terms extraction. It extracts NP chunks (based
  on a given rule).
  """

  def __init__(self, name, is_lazy, lazy_directory, debug, stop_words, verb_tags, stemmer):
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
    """

    super(ExpandedCoreWordExtractor, self).__init__(name, is_lazy, lazy_directory, debug)

    self._stop_words = stop_words
    self._verb_tags = verb_tags
    self._stemmer = stemmer

  def candidate_extraction(self, pre_processed_file):
    """
    Extracts the candidates from a pre-processed file.

    @param    pre_processed_file: The pre-processed analysed file.
    @type     pre_processed_file: C{PreProcessedFile}

    @return:  A list of candidates.
    @rtype:   C{list(string)}
    """

    tagged_sentences = pre_processed_file.full_text()
    stemmed_words = {}
    stem_positions = {}
    candidates = []

    # create reverse indexes
    for sent_pos, tagged_sentence in enumerate(tagged_sentences):
      for pos, tagged_word in enumerate(tagged_sentence.split()):
        if tagged_word not in stemmed_words:
          # only if it is not a stop word
          if self.filtering(tagged_word, pre_processed_file.tag_separator()):
            word = tagged_word.rsplit(pre_processed_file.tag_separator(), 1)[0]
            stemmed_word = self._stemmer.stem(word)
            stemmed_words[tagged_word] = stemmed_word
            if stemmed_word not in stem_positions:
              stem_positions[stemmed_word] = []
            stem_positions[stemmed_word].append((sent_pos, pos))
        else:
          stemmed_word = stemmed_words[tagged_word]
          stem_positions[stemmed_word].append((sent_pos, pos))

    # generate candidates from core words
    core_word_ordering = sorted(stem_positions.items(),
                                key=lambda (c, p): len(p),
                                reverse=True)
    for core_word_stem, positions in core_word_ordering[:50]:
      for sent_pos, pos in positions:
        candidate = tagged_sentences[sent_pos].split()[pos]
        forward_position = pos + 1
        # forward expansion
              # maximum candidate size
              # check index
              # check non stop word
              # frequency requirement
        while len(candidate.split()) < 4 \
              and forward_position < len(tagged_sentences[sent_pos].split()) \
              and tagged_sentences[sent_pos].split()[forward_position] in stemmed_words \
              and len(stem_positions[stemmed_words[tagged_sentences[sent_pos].split()[forward_position]]]) > 1:
          candidate += " " + tagged_sentences[sent_pos].split()[forward_position]
          forward_position += 1
        candidates.append(candidate)

        candidate = tagged_sentences[sent_pos].split()[pos]
        backward_position = pos - 1
        # backward expansion
              # maximum candidate size
              # check index
              # check non stop word
              # frequency requirement
        while len(candidate.split()) < 4 \
              and backward_position >= 0 \
              and tagged_sentences[sent_pos].split()[backward_position] in stemmed_words \
              and len(stem_positions[stemmed_words[tagged_sentences[sent_pos].split()[backward_position]]]) > 1:
          candidate = tagged_sentences[sent_pos].split()[backward_position] + " " + candidate
          backward_position -= 1
        candidates.append(candidate)

    return candidates

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

    for i, tagged_word in enumerate(tagged_words):
      word = tagged_word.lower().rsplit(tag_separator, 1)[0]
      tag = tagged_word.lower().rsplit(tag_separator, 1)[1]

      # only candidate with first and last words not included into the stop word
      # list are accepted
      if i == 0 or i == (len(tagged_words) - 1):
        if self._stop_words.count(word) > 0 \
           or self._verb_tags.count(tag) > 0:
          return False

      # FIXME semeval trick
#      if len(word) <= 2:
#        return False

    return True

################################################################################

class NounAndADJRExtractor(CandidateExtractorC):
  """
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               debug,
               patterns,
               adj_tags,
               is_adjr_function):
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
    TODO patterns
    TODO patterns
    """

    super(NounAndADJRExtractor, self).__init__(name,
                                               is_lazy,
                                               lazy_directory,
                                               debug)

    self.set_patterns(patterns)
    self._adj_tags = adj_tags
    self._is_adjr_function = is_adjr_function

  def patterns(self):
    """
    """

    return self._patterns

  def set_patterns(self, patterns):
    """
    """

    self._patterns = patterns

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

    sentences = pre_processed_file.full_text()
    non_filtered_candidate_counts = {}
    candidates = []

    for sentence in sentences:
      # pattern matching
      for pattern in self.patterns():
        for match in re.finditer(pattern, sentence):
          candidate = match.group(0).strip()

          if candidate not in non_filtered_candidate_counts:
            non_filtered_candidate_counts[candidate] = 0
          non_filtered_candidate_counts[candidate] += 1

    # split the component to the non-relational adjectives
    for candidate in non_filtered_candidate_counts:
      #if non_filtered_candidate_counts[candidate] > 1:
      #if non_filtered_candidate_counts[candidate] > 0:
      if candidate.count("/adj") > 0 or candidate.count("/jj") > 0:
        sub_candidate = " ".join(candidate.split()[1:])
        if sub_candidate.count("/adj") > 0 or candidate.count("/jj") > 0:
          sub_candidate = " ".join(candidate.split()[:-1])

          if sub_candidate not in non_filtered_candidate_counts:
            candidates.append(candidate)
          elif non_filtered_candidate_counts[candidate] > non_filtered_candidate_counts[sub_candidate]:
            candidates.append(candidate)
        else:
          candidates.append(candidate)
      else:
        start = 0
        for pos, wt in enumerate(candidate.split()):
          word = wt.rsplit(pre_processed_file.tag_separator(), 1)[0]
          tag = wt.rsplit(pre_processed_file.tag_separator(), 1)[1]

          if tag in self._adj_tags \
             and not self._is_adjr_function(word):
            if pos != 0 and start != (len(candidate.split()) - 1):
              candidates.append(" ".join(candidate.split()[start:pos]))
            start = pos + 1
          elif pos == (len(candidate.split()) - 1):
            candidates.append(" ".join(candidate.split()[start:]))

    return candidates

