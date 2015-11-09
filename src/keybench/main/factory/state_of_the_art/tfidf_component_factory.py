# -*- encoding: utf-8 -*-

from keybench.main.factory.interface import component_factory
from keybench.main.component.implementation.candidate_extractor import n_gram_extractor
from keybench.main.component.implementation.candidate_ranker import ngram_tfidf_ranker
from keybench.main.component.implementation.keyphrase_extractor import full_keyphrase_extractor

class TFIDFComponentFactory(component_factory.KBComponentFactoryI):
  """Part of the configuration of a TF-IDF run.
  """

  def __init__(self, run_name, lazy_mode, debug_mode, root_cache):
    """ TODO
    """

    super(TFIDFComponentFactory, self).__init__()

    self._run_name = run_name
    self._lazy_mode = lazy_mode
    self._debug_mode = debug_mode
    self._root_cache = root_cache

  def candidateExtractor(self, language):
    """Provides the component to use for candidate extraction in the run.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Returns:
      The C{KBCandidateExtractorI} of the run.
    """

    return n_gram_extractor.NGramExtractor(
      "tfidf_candidate_extractor",
      self._run_name,
      False,
      self._lazy_mode,
      self._debug_mode,
      self._root_cache,
      3
    )

  def candidateClusterer(self, language):
    """Provides the component to use for candidate clustering in the run.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Returns:
      The C{KBCandidateClustererI} of the run.
    """

    return None

  def candidateRanker(self, language):
    """Provides the component to use for candidate ranking in the run.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Returns:
      The C{KBCandidateRankerI} of the run.
    """

    return ngram_tfidf_ranker.NGramTFIDFRanker(
      "tfidf_candidate_ranker",
      self._run_name,
      False,
      self._lazy_mode,
      self._debug_mode,
      self._root_cache,
      3
    )

  def candidateClassifier(self, language):
    """Provides the component to use for candidate classification in the run.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Returns:
      The C{KBCandidateClassifierI} of the run.
    """

    return None

  def keyphraseExtractor(self, language):
    """Provides the component to use for keyphrase extraction in the run.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Returns:
      The C{KBKeyphraseExtractorI} of the run.
    """

    return full_keyphrase_extractor.KBFullKeyphraseExtractor(
      "tfidf_keyphrase_extractor",
      self._run_name,
      False,
      self._lazy_mode,
      self._debug_mode,
      self._root_cache,
      []
    )

