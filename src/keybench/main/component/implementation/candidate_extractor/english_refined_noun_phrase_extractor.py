# -*- encoding: utf-8 -*-

import re

from nltk.corpus import wordnet

from keybench.main import core
from keybench.main import model
from keybench.main.component.implementation.candidate_extractor import pos_sequence_based_candidate_extractor as interface
from keybench.main.nlp_tool import interface as nlp_tool_interface

class EnglishRefinedNounPhraseExtractor(interface.POSSequenceBasedCandidateExtractor):
  """English pattern matching candidate extractor that filters useless
  adjectives.

  Candidate extractor providing only textual units that match the POS tag
  pattern C{A?N+}. When the adjective is not derived from a noun, only the
  modified noun is extracted.
  """

  def __init__(self,
               name,
               run_name,
               shared,
               lazy_mode,
               debug_mode,
               root_cache,
               noun_tags=None,
               adjective_tags=None):
    """Constructor.

    Args:
      name: The C{string} name of the component.
      run_name: The C{string} name of the run for which the component is
        affected to.
      shared: True if the component shares informations with equivalent
        components (same name).
      lazy_mode: True if the component load precomputed data. False, otherwise.
      debug_mode: True if the component can log debug messages. False,
        otherwise.
      root_cache: The root of the cache directory where the cached objects must
        be stored.
      noun_tags: The C{list} of the C{string} pos tags used to detect nouns. If
        the list is not defined, the C{noun_tags} are set to the noun tags in
        the C{POSTagger}'s tagset (with the key
        C{keybench.main.nlp_tool.interface.KBPOSTaggerI.POSKey.NOUN}).
      adjective_tags: The C{list} of the C{string} pos tags used to detect
        adjectives. If the list is not defined, the C{adjective_tags} are set to
        the adjective tags in the C{POSTagger}'s tagset (with the key
        C{keybench.main.nlp_tool.interface.KBPOSTaggerI.POSKey.ADJECTIVE}).
    """

    if noun_tags == None:
      tool_factory = core.KBBenchmark.singleton().run_tools[run_name]
      pos_tagger = tool_factory.posTagger(document.language)

      noun_tags = pos_tagger.tagset()[nlp_tool_interface.KBPOSTaggerI.POSTagKey.NOUN]
    if adjective_tags == None:
      tool_factory = core.KBBenchmark.singleton().run_tools[run_name]
      pos_tagger = tool_factory.posTagger(document.language)

      adjective_tags = pos_tagger.tagset()[nlp_tool_interface.KBPOSTaggerI.POSTagKey.ADJECTIVE]

    pos_regexp = r"(%s)?(%s)+"%("|".join(self._adjective_tags),
                                "|".join(self._noun_tags))

    super(EnglishRefinedNounPhraseExtractor, self).__init__(name,
                                                           run_name,
                                                           shared,
                                                           lazy_mode,
                                                           debug_mode,
                                                           root_cache,
                                                           pos_regexp)

    self._noun_tags = noun_tags
    self._adjective_tags = adjective_tags

  def _candidateExtraction(self, document):
    """Extracts the candidates of a given document.

    Args:
      document: The C{KBDocument} from which the candidates must be extracted.

    Returns:
      The C{list} of extracted, and filtered, candidates (C{KBTextualUnit}s).
    """

    candidates = super(EnglishRefinedNounPhraseExtractor,
                       self)._candidateExtraction(document)

    for index, candidate in enumerate(candidates):
      # WARNING works only for A?N+ (one adjective at the left)
      # check if the adjective must be filtered out or not
      if not self.i_check_adjective(candidate):
        candidate_normalized_tokens = candidate.normalized_tokens[1:]
        # create a new candidate without the adjective
        candidate_normalized_form = " ".join(candidate_normalized_tokens)
        candidate_normalized_lemmas = candidate.normalized_lemmas[1:]
        candidate_normalized_stems = candidate.normalized_stems[1:]
        candidate_pos_tags = candidate.pos_tags[1:]
        new_candidate = model.KBTextualUnit(document.corpus_name,
                                            document.language,
                                            candidate_normalized_form,
                                            candidate_normalized_tokens,
                                            candidate_normalized_lemmas,
                                            candidate_normalized_stems,
                                            candidate_pos_tags)

        # add all the occurrences
        seen_forms = candidate.seen_forms
        for seen_form in seen_forms:
          new_seen_form =" ".join(seen_form.split(" ")[1:]) # FIXME tokenized form, not seen form :{

          for sentence_offset, inner_sentence_offsets in seen_forms[seen_form].items():
            for inner_sentence_offset in inner_sentence_offsets:
              new_candidate.addOccurrence(new_seen_form,
                                          sentence_offset,
                                          inner_sentence_offset)

        candidates[index] = new_candidate

    return candidates.values()

  def _check_adjective(self, candidate):
    """Check that a given candidate does not contain an useless adjective.

    Check that a given candidate does not contain an useless adjective. A
    candidate is alright if it contains no adjective or only an useful
    adjective. An useful adjective is either derived from a noun or use more
    than once with the same noun sequence.

    Args:
      candidate: The C{KBTextualUnit} to check.

    Returns:
      True if the given C{candidate} is alright, False if the it contains an
      useless adjective.
    """

    # http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.380.8821&rep=rep1&type=pdf
    adjr_suffixes = [
      u"al",
      u"ant",
      u"ary",
      u"ic",
      u"ous",
      u"ive"
    ]

    # WARNING works only for A?N+ (one adjective at the left)
    # check if the adjective must be filtered out or not
    if candidate.pos_tags[0] not in self._adjective_tags \
       or candidate.numberOfOccurrences() > 1:
      return True
    for synset in wordnet.synsets(candidate.normalized_tokens[0]):
      if synset.name.find(".a.") != -1:
        for lemma in synset.lemmas:
          if len(lemma.pertainyms()) > 0:
            return True
    for suffix in adjr_suffixes:
      if candidate.normalized_tokens[0][-len(suffix):] == suffix:
        return True

    return False

