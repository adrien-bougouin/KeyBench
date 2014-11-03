# -*- encoding: utf-8 -*-

from keybench.main import core
from keybench.main.component import interface

class KBFullKeyphraseExtractor(interface.KBKeyphraseExtractorI):
  """Keyphrase extractor that extracts every candidates.

  Keyphrase extractor that returns every candidates of the documents, in the
  order given by the C{KBCandidateRanker} or the C{KBCandidateClassifier}.
  """

  def __init__(self,
               name,
               run_name,
               shared,
               lazy_mode,
               debug_mode,
               root_cache,
               redundancy_filters):
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
      redundancy_filters: A C{list} of
        C{KBKeyphraseExtractorI.RedundancyFilterI} to use to filter out
        redundant keyphrases.
    """

    super(KBFullKeyphraseExtractorI, self).__init__(name,
                                                    run_name,
                                                    shared,
                                                    lazy_mode,
                                                    debug_mode,
                                                    root_cache,
                                                    redundancy_filters)

  def _keyphraseExtraction(self, document):
    """Extracts the keyphrases of a given document.

    Args:
      document: The C{KBDocument} from which the keyphrases must be extracted.

    Returns:
      The C{list} of extracted, and filtered, keyphrases (C{KBTextualUnit}s).
    """

    component_factory = core.KBBenchmark.singleton().run_configurations[self._run_name]
    # rank the candidates if a candidate ranker is provided
    try:
      candidate_ranker = component_factory.candidateRanker(document.language)

      return candidate_extractor.rankCandidates(document)
    # classify them otherwise
    except:
      candidate_classifier = component_factory.candidateClassifier(document.language)

      return candidate_classifier.classifyCandidates(document)[interface.KBCandidateClassifierI.KEYPHRASE]

