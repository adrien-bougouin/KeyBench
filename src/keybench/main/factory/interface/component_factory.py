# -*- encoding: utf-8 -*-

from keybench.main import exception

class KBComponentFactoryI(object):
  """The configuration of a run.

  The abstract factory providing the components to use for one specific
  keyphrase extraction run. Components for one service (candidate extraction,
  candidate ranking, etc.) may differ for each language. However, it is
  recommended that, despite language specific processing, such components
  provide similar treatment.
  """

  def documentBuilder(self, corpus_name):
    """Provides the component that can build documents for a given corpus.

    Args:
      corpus_name: The C{string} name of the corpus of the documents that must
        be built.

    Returns:
      The C{KBDocumentBuilderI} that can parse file and build documents
      belonging to the given C{corpus_name}.
    """

    raise exception.KBConfigurationException(self, "Uncomplete configuration!")

  def corpusBuilders(self):
    """Provides a list of corpus builders.

    Provides a list of corpus builders. This list determines every corpus to be
    treated in the run.

    Returns:
      The C{list} of C{KBCorpusBuilder} of the run.
    """

    raise exception.KBConfigurationException(self, "Uncomplete configuration!")

  def candidateExtractor(self, language):
    """Provides the component to use for candidate extraction in the run.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Returns:
      The C{KBCandidateExtractorI} of the run.
    """

    raise exception.KBConfigurationException(self, "Uncomplete configuration!")

  def candidateClusterer(self, language):
    """Provides the component to use for candidate clustering in the run.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Returns:
      The C{KBCandidateClustererI} of the run.
    """

    raise exception.KBConfigurationException(self, "Uncomplete configuration!")

  def candidateRanker(self, language):
    """Provides the component to use for candidate ranking in the run.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Returns:
      The C{KBCandidateRankerI} of the run.
    """

    raise exception.KBConfigurationException(self, "Uncomplete configuration!")

  def candidateClassifier(self, language):
    """Provides the component to use for candidate classification in the run.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Returns:
      The C{KBCandidateClassifierI} of the run.
    """

    raise exception.KBConfigurationException(self, "Uncomplete configuration!")

  def keyphraseExtractor(self, language):
    """Provides the component to use for keyphrase extraction in the run.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Returns:
      The C{KBKeyphraseExtractorI} of the run.
    """

    raise exception.KBConfigurationException(self, "Uncomplete configuration!")

  def keyphraseConsumers(self, language):
    """Provides a list of keyphrase consumers.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Provides a list of keyphrase consumers. It can be keyphrase extraction
    evaluators, keyphrase indexing systems, word cloud generators, etc.

    Returns:
      The C{list} of C{KBKeyphraseConsumerI} of the run.
    """

    raise exception.KBConfigurationException(self, "Uncomplete configuration!")

