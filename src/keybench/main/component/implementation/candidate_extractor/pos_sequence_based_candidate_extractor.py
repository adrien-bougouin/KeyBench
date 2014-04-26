import re

from keybench.main import core
from keybench.main import model
from keybench.main.component import interface

class POSSequenceBasedCandidateExtractor(interface.KBCandidateExtractorI):
  """Pattern matching candidate extractor.

  Candidate extractor providing only textual units that match given
  Part-of-Speech patterns (e.g. r"JJ?NN+"), using the appropriate tag labels
  (see C{keybench.main.nltp_tool.interface.KBPOSTaggerI.POSTagKey}).
  """

  def __init__(self,
               name,
               run_name,
               shared,
               lazy_mode,
               debug_mode,
               root_cache,
               pos_regexp):
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
    pos_regexp: The regular expression that represents Part-of-Speech patterns.
    """

    super(POSSequenceBasedCandidateExtractor, self).__init__(name,
                                                             run_name,
                                                             shared,
                                                             lazy_mode,
                                                             debug_mode,
                                                             root_cache)

    self._pos_regexp = pos_regexp

  def _candidateExtraction(self, document):
    """Extracts the candidates of a given document.

    Args:
      document: The C{KBDocument} from which the candidates must be extracted.

    Returns:
      The C{list} of extracted, and filtered, candidates (C{KBTextualUnit}s).
    """

    tokenized_sentences = document.full_text_sentence_tokens()
    pos_tagged_sentences = document.full_text_token_pos_tags()
    candidates = {}

    ## NLP tools ###############################################################
    tool_factory = core.KBBenchmark.singleton().run_tools[self._run_name]
    pos_tagger = tool_factory.posTagger(document.language)
    normalizer = tool_factory.normalizer(document.language)
    lemmatizer = tool_factory.lemmatizer(document.language)
    stemmer = tool_factory.stemmer(document.language)
    ############################################################################

    # extract sentences' textual units matching POS tag patterns
    for sentence_offset, tokenized_sentence in enumerate(tokenized_sentences):
      pos_tagged_sentence = pos_tagged_sentences[sentence_offset]
      full_pos_tag_sequence = " ".join(pos_tagged_sentence)
      pos_position_to_inner_sentence_position = {}

      # create the map associating the position a POS tag first character to a
      # token position
      pos_character_position_accumulator = 0
      for inner_sentence_position, pos in pos_tagged_sentence:
        pos_position_to_inner_sentence_position[pos_character_position_accumulator] = inner_sentence_position

        pos_character_position_accumulator += len(pos) + 1 # 1 is for the " "

      # find the textual unit matching the POS tag sequence represented by the
      # regexp
      for match in re.finditer(self._pos_regexp, full_pos_tag_sequence):
        pos_tag_sequence = match.string[match.start():match.end()]
        candidate_pos_tags = pos_tag_sequence.split(" ")
        inner_sentence_offset = pos_position_to_inner_sentence_position[match.start()]
        start = inner_sentence_offset
        end = start + len(candidate_pos_tags)
        candidate = " ".join(tokenized_sentence[start:end])
        candidate_seen_form = candidate # FIXME tokenized form, not seen form :{
        candidate_normalized_form = normalizer.normalize(candidate)
        candidate_normalized_tokens = candidate_normalized_form.split(" ")

        # identify the candidates using the POS tags, so same normalized forms
        # with different POS tags are considered as different candidates
        candidate_id = "%s%s"%(candidate_normalized_form,
                               str(candidate_pos_tags))
        # create the textual unit if no existing candidate matches it
        if candidate_id not in candidates:
          # compute the n-gram's lemmas and stems
          candidate_normalized_lemmas = []
          candidate_normalized_stems = []

          for word_index, word in enumerate(candidate_normalized_tokens):
            pos_tag = candidate_pos_tags[word_index]
            tag_name = pos_tagger.tagName(pos_tag)
            candidate_normalized_lemmas.append(lemmatizer.lemmatize(word,
                                                                    tag_name,
                                                                    pos_tag))
            candidate_normalized_stems.append(stemmer.stem(word))
          candidates[candidate_id] = model.KBTextualUnit(document.corpus_name,
                                                         document.language,
                                                         candidate_normalized_form,
                                                         candidate_normalized_tokens,
                                                         candidate_normalized_lemmas,
                                                         candidate_normalized_stems,
                                                         candidate_pos_tags)
        candidates[candidate_id].addOccurrence(candidate_seen_form,
                                               sentence_offset,
                                               inner_sentence_offset)

    return candidates.values()

