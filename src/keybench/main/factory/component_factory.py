from keybench.main import exception

class KBComponentFactory(object):
  """
  """

  def __init__(self):
    super(KBComponentFactory, self).__init__()

    self._document_builders = None
    self._corpus_builders = None
    self._candidate_extractor = None
    self._candidate_clusterer = None
    self._candidate_ranker = None
    self._candidate_classifier = None
    self._candidate_extractor = None
    self._keyphrase_consumer = None

  def __eq__(self, other):
    return self._document_builders == other._document_builders \
           and self._corpus_builders == other._corpus_builders \
           and self._candidate_extractor == other._candidate_extractor \
           and self._candidate_clusterer == other._candidate_clusterer \
           and self._candidate_ranker == other._candidate_ranker \
           and self._candidate_classifier == other._candidate_classifier \
           and self._candidate_extractor == other._candidate_extractor \
           and self._keyphrase_consumer == other._keyphrase_consumer

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
             self._candidate_extractor.__class__.__name__,
             str(self._candidate_extractor),
             self._keyphrase_consumer.__class__.__name__,
             str(self._keyphrase_consumer),
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
  def candidate_extractor(self):
    if self._candidate_extractor == None:
      raise exception.KBConfigurationException(self,
                                               "Uncomplete configuration!")
    return self._candidate_extractor

  @candidate_extractor.setter
  def candidate_extractor(self, value):
    self._candidate_extractor = value

  @property
  def keyphrase_consumer(self):
    if self._keyphrase_consumer == None:
      raise exception.KBConfigurationException(self,
                                               "Uncomplete configuration!")
    return self._keyphrase_consumer

  @keyphrase_consumer.setter
  def keyphrase_consumer(self, value):
    self._keyphrase_consumer = value

