from keybench.main import exception

class KBComponentFactory(object):
  """The configuration of a run.

  The abstract factory providing the components to use for one specific
  keyphrase extraction run.

  Attributes:
    document_builder: The C{KBDocumentBuilderI} components responsible of the
      creation of C{KBDocument}s, associated to one specific corpus.
    corpus_builders: The C{KBDocumentBuilder} components responsible of the
      creation of specific corpora.
    candidate_extractor: The C{KBCandidateExtractorI} component responsible of
      the extraction of C{KBTextualUnit} candidates.
    candidate_clusterer: The C{KBCandidateClustererI} component responsible of
      the clustering of C{KBTextualUnit} candidates.
    candidate_ranker: The C{KBCandidateRankerI} component responsible of
      the ranking of C{KBTextualUnit} candidates.
    candidate_classifier: The C{KBCandidateClassifierI} component responsible of
      the classification of C{KBTextualUnit} candidates.
    keyphrase_extractor: The C{KBKeyphraseExtractorI} component responsible of
      the extraction of keyphrases among C{KBTextualUnit} candidates.
    keyphrase_consumers: The C{KBKeyphraseConsumer} componets that makes usage
      of the extracted C{KBTextualUnit} keyphrases.
  """

  def __init__(self):
    super(KBComponentFactory, self).__init__()

    self._document_builders = None
    self._corpus_builders = None
    self._candidate_extractor = None
    self._candidate_clusterer = None
    self._candidate_ranker = None
    self._candidate_classifier = None
    self._keyphrase_extractor = None
    self._keyphrase_consumers = None

  def __eq__(self, other):
    return self._document_builders == other._document_builders \
           and self._corpus_builders == other._corpus_builders \
           and self._candidate_extractor == other._candidate_extractor \
           and self._candidate_clusterer == other._candidate_clusterer \
           and self._candidate_ranker == other._candidate_ranker \
           and self._candidate_classifier == other._candidate_classifier \
           and self._keyphrase_extractor == other._candidate_extractor \
           and self._keyphrase_consumers == other._keyphrase_consumers

  def __ne__(self, other):
    return not self.__eq__(other)

  def __str__(self):
    return "%s:%s; %s:%s; %s:%s; %s:%s; %s:%s; %s:%s; %s:%s; %s:%s"%(
             self._document_builders.__class__.__name__,
             str(self._document_builders),
             self._corpus_builders.__class__.__name__,
             str(self._corpus_builders),
             self._candidate_extractor.__class__.__name__,
             str(self._candidate_extractor),
             self._candidate_clusterer.__class__.__name__,
             str(self._candidate_clusterer),
             self._candidate_ranker.__class__.__name__,
             str(self._candidate_ranker),
             self._candidate_classifier.__class__.__name__,
             str(self._candidate_classifier),
             self._keyphrase_extractor.__class__.__name__,
             str(self._keyphrase_extractor),
             self._keyphrase_consumers.__class__.__name__,
             str(self._keyphrase_consumers),
           )

  @property
  def document_builders(self):
    if self._document_builders == None:
      raise exception.KBConfigurationException(self,
                                               "Uncomplete configuration!")
    return self._document_builders

  @document_builders.setter
  def document_builders(self, value):
    if value.__class__.__name__ != "dict":
      raise exception.KBConfigurationException(self,
                                               "Putting %s instead of %s!"%(
                                                 value.__class__.__name__,
                                                 "dict"
                                               ))
    self._document_builders = value

  @property
  def corpus_builders(self):
    if self._corpus_builders == None:
      raise exception.KBConfigurationException(self,
                                               "Uncomplete configuration!")
    return self._corpus_builders

  @corpus_builders.setter
  def corpus_builders(self, value):
    if value.__class__.__name__ != "list":
      raise exception.KBConfigurationException(self,
                                               "Putting %s instead of %s!"%(
                                                 value.__class__.__name__,
                                                 "list"
                                               ))
    self._corpus_builders = value

  @property
  def candidate_extractor(self):
    if self._candidate_extractor == None:
      raise exception.KBConfigurationException(self,
                                               "Uncomplete configuration!")
    return self._candidate_extractor

  @candidate_extractor.setter
  def candidate_extractor(self, value):
    self._candidate_extractor = value

  @property
  def candidate_clusterer(self):
    if self._candidate_clusterer == None:
      raise exception.KBConfigurationException(self,
                                               "Uncomplete configuration!")
    return self._candidate_clusterer

  @candidate_clusterer.setter
  def candidate_clusterer(self, value):
    self._candidate_clusterer = value

  @property
  def candidate_ranker(self):
    if self._candidate_ranker == None:
      raise exception.KBConfigurationException(self,
                                               "Uncomplete configuration!")
    return self._candidate_ranker

  @candidate_ranker.setter
  def candidate_ranker(self, value):
    self._candidate_ranker = value

  @property
  def candidate_classifier(self):
    if self._candidate_classifier == None:
      raise exception.KBConfigurationException(self,
                                               "Uncomplete configuration!")
    return self._candidate_classifier

  @candidate_classifier.setter
  def candidate_classifier(self, value):
    self._candidate_classifier = value

  @property
  def keyphrase_extractor(self):
    if self._keyphrase_extractor == None:
      raise exception.KBConfigurationException(self,
                                               "Uncomplete configuration!")
    return self._keyphrase_extractor

  @keyphrase_extractor.setter
  def keyphrase_extractor(self, value):
    self._keyphrase_extractor = value

  @property
  def keyphrase_consumers(self):
    if self._keyphrase_consumers == None:
      raise exception.KBConfigurationException(self,
                                               "Uncomplete configuration!")
    return self._keyphrase_consumers

  @keyphrase_consumers.setter
  def keyphrase_consumers(self, value):
    if value.__class__.__name__ != "list":
      raise exception.KBConfigurationException(self,
                                               "Putting %s instead of %s!"%(
                                                 value.__class__.__name__,
                                                 "list"
                                               ))
    self._keyphrase_consumers = value

