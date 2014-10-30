# -*- encoding: utf-8 -*-

import exceptions

from keybench.main import core
from keybench.main import model
from keybench.main.component import component

class KBCandidateExtractorI(component.KBComponent):
  """The abstract component responsible of the extraction of the candidates of a
  document.

  The component that extracts candidates from a C{KBDocument}. In most cases,
  subclasses must not override C{extractCandidates()}, but only
  C{candidateExtraction()}.
  """

  ##############################################################################
  class CandidateFilterI(object):
    """An interface of a candidate filter.
    """

    def isAccepted(self, textual_unit, candidates, document):
      """Checks if a given textual unit is a suitable candidate.

      Args:
        textual_unit: The C{KBTextualUnit} to check.
        candidates: The C{list} of candidates from which the C{textual_unit}
          belongs to.
        document: The C{KBDocument} from which the candidates are extracted.

      Returns:
        True if the C{textual_unit} is a suitable candidate. False, otherwise.
      """

      raise exceptions.NotImplementedError()
  ##############################################################################

  def __init__(self,
               name,
               run_name,
               shared,
               lazy_mode,
               debug_mode,
               root_cache,
               candidate_filters):
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
      candidate_filters: A C{list} of C{KBCandidateExtractorI.CandidateFilterI}
        to use to filter out some extracted candidates (e.g. hapaxes).
    """

    super(KBCandidateExtractorI, self).__init__(name,
                                                run_name,
                                                shared,
                                                lazy_mode,
                                                debug_mode,
                                                root_cache)

    self._candidate_filters = candidate_filters

  def extractCandidates(self, document):
    """Extracts the candidates of a given document.

    Args:
      document: The C{KBDocument} from which the candidates must be extracted.

    Returns:
      The C{list} of extracted, and filtered, candidates (C{KBTextualUnit}s).
    """

    candidates = None

    # - can the component do lazy loading?
    # - does the document already exist?
    if self.isLazy() \
       and self.exists(document):
      # lazy loading
      candidates = self.load(document)
    # extract the candidates
    else:
      ## candidate extraction ##################################################
      self.logDebug("Extracting candidates of %s..."%(document.name))
      candidates = self._candidateExtraction(document)
      ## candidate filtering ###################################################
      self.logDebug("Filtering candidates of %s..."%(document.name))
      index = 0
      while index != len(candidates):
        accepted = True

        for candidate_filter in self._candidate_filters:
          if not candidate_filter.isAccepted(candidates[index],
                                             candidates,
                                             document):
            accepted = False
            break

        if accepted == False:
          candidates.remove(candidates[index])
        else:
          index += 1
      ## serialization #########################################################
      self.logDebug("Saving candidates of %s..."%(document.name))
      self.store(document, candidates)

    return candidates

  def _updateCandidateDictionary(self,
                                 candiates,
                                 document,
                                 sentence_offset,
                                 starting_token,
                                 ending_token):
    """Adds or update a newly extracted candidate form to a candidate
    dictionary.

    Args:
      candidates: The candidate dictionary to update. Keys are mixtures of
        candidate forms and POS tags.
      document: The C{KBDocument} where the candidate is extracted from.
      sentence_offset: The index of the sentence of the document where the
        candidate is extracted.
      starting_token: The index of the first token of the candidate within the
        sentence it is extracted from.
      ending_token: The index of the last token of the candidate within the
        sentence it is extracted from.
    """

    tool_factory = core.KBBenchmark.singleton().run_tools[self._run_name]
    normalizer = tool_factory.normalizer(document.language)
    #---------------------------------------------------------------------------
    tokenized_sentence = document.full_text_sentence_tokens[sentence_offset]
    pos_tagged_sentence = document.full_text_sentence_pos_tags[sentence_offset]
    #---------------------------------------------------------------------------
    candidate = " ".join(tokenized_sentence[starting_token:ending_token])
    candidate_seen_form = candidate # FIXME tokenized form :{
    candidate_normalized_form = normalizer.normalize(candidate)
    candidate_normalized_tokens = candidate_normalized_form.split(" ")
    candidate_normalized_lemmas = document.full_text_token_lemmas[sentence_offset][starting_token:ending_token]
    candidate_normalized_stems = document.full_text_token_stems[sentence_offset][starting_token:ending_token]
    candidate_pos_tags = pos_tagged_sentence[starting_token:ending_token]

    # identify the candiate with its normalized form and POS tag in order to
    # prevent from having only one candidate for the same form with a diferent
    # POS tagging
    identifier = "%s%s"%(candidate_normalized_form, str(candidate_pos_tags))

    if identifier not in candidates:
      candidates[identifier] = model.KBTextualUnit(document.corpus_name,
                                                   document.language,
                                                   candidate_normalized_form,
                                                   candidate_normalized_tokens,
                                                   candidate_normalized_lemmas,
                                                   candidate_normalized_stems,
                                                   candidate_pos_tags)
    candidates[identifier].addOccurrence(candidate_seen_form,
                                         sentence_offset,
                                         starting_token)

  def _candidateExtraction(self, document):
    """Extracts the candidates of a given document.

    Args:
      document: The C{KBDocument} from which the candidates must be extracted.

    Returns:
      The C{list} of extracted, and filtered, candidates (C{KBTextualUnit}s).
    """

    raise exceptions.NotImplementedError()

