from keybench.main import exception

class KBComponentFactoryI(object):
  """The configuration of a run.

  The abstract factory providing the components to use for one specific
  keyphrase extraction run.
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

  def candidateExtractor(self):
    """Provides the component to use for candidate extraction in the run.

    Returns:
      The C{KBCandidateExtractorI} of the run.
    """

    raise exception.KBConfigurationException(self, "Uncomplete configuration!")

  def candidateClusterer(self):
    """Provides the component to use for candidate clustering in the run.

    Returns:
      The C{KBCandidateClustererI} of the run.
    """

    raise exception.KBConfigurationException(self, "Uncomplete configuration!")

  def candidateRanker(self):
    """Provides the component to use for candidate ranking in the run.

    Returns:
      The C{KBCandidateRankerI} of the run.
    """

    raise exception.KBConfigurationException(self, "Uncomplete configuration!")

  def candidateClassifier(self):
    """Provides the component to use for candidate classification in the run.

    Returns:
      The C{KBCandidateClassifierI} of the run.
    """

    raise exception.KBConfigurationException(self, "Uncomplete configuration!")

  def keyphraseExtractor(self):
    """Provides the component to use for keyphrase extraction in the run.

    Returns:
      The C{KBKeyphraseExtractorI} of the run.
    """

    raise exception.KBConfigurationException(self, "Uncomplete configuration!")

  def keyphraseConsumers(self):
    """Provides a list of keyphrase consumers.

    Provides a list of keyphrase consumers. It can be keyphrase extraction
    evaluators, keyphrase indexing systems, word cloud generators, etc.

    Returns:
      The C{list} of C{KBKeyphraseConsumerI} of the run.
    """

    raise exception.KBConfigurationException(self, "Uncomplete configuration!")

