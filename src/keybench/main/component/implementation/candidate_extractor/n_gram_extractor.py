# -*- encoding: utf-8 -*-

from keybench.main import core
from keybench.main import model
from keybench.main.component import interface

class NGramExtractor(interface.KBCandidateExtractorI):
  """N-gram candidate extractor.

  Attributes:
    n: The maximum size of a candidate (number of words).
  """

  def __init__(self,
               name,
               run_name,
               shared,
               lazy_mode,
               debug_mode,
               root_cache,
               n):
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
      n: The maximum size of a candidate (number of words).
    """

    super(NGramExtractor, self).__init__(name,
                                         run_name,
                                         shared,
                                         lazy_mode,
                                         debug_mode,
                                         root_cache)

    self._n = n

  @property
  def n(self):
    return self._n

  def _candidateExtraction(self, document):
    """Extracts the candidates of a given document.

    Args:
      document: The C{KBDocument} from which the candidates must be extracted.

    Returns:
      The C{list} of extracted, and filtered, candidates (C{KBTextualUnit}s).
    """

    tokenized_sentences = document.full_text_sentence_tokens
    pos_tagged_sentences = document.full_text_token_pos_tags
    candidates = {}

    # extract sentences' n-grams
    for sentence_offset, tokenized_sentence in enumerate(tokenized_sentences):
      pos_tagged_sentence = pos_tagged_sentences[sentence_offset]

      # extract word lists of size up to n
      for n in range(1, self._n + 1):
        for i in range(n, len(tokenized_sentence) + 1):
          start = i - n
          end = i

          super(NGramExtractor, self)._updateCandidateDictionary(candidates,
                                                   document,
                                                   sentence_offset,
                                                   start,
                                                   end)

    return candidates.values()

