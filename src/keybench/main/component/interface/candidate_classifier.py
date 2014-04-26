# -*- encoding: utf-8 -*-

import exceptions

from keybench.main.component import component

class KBCandidateClassifierI(component.KBComponent):
  """The abstract component responsible of the classification of the candidates
  of a document.

  The component that classifies the candidates of a C{KBDocument}. In most
  cases, subclasses must not override C{classifyCandidates()}, but only
  C{candidateClassification()}.
  """

  KEYPHRASE     = "__keyphrase__"
  NON_KEYPHRASE = "__non_keyphrase__"

  def classifyCandidates(self, document):
    """Classifies the candidates of a given document.

    Args:
      document: The C{KBDocument} from which the candidates must be classified.

    Returns:
      The C{map} of C{KBTextualUnit} C{list}s associated to a C{string} class
      (C{KBCandidateClassifierI.KEYPHRASE} or
      C{KBCandidateClassifierI.NON_KEYPHRASE}).
    """

    classified_candidates = None

    # - can the component do lazy loading?
    # - does the document already exist?
    if self.isLazy() \
       and self.exists(document):
      # lazy loading
      classified_candidates = self.load(document)
    # classify candidates
    else:
      ## candidate classification ##############################################
      self.logDebug("Classifying candidates of %s..."%(document.name))
      classified_candidates = self._candidateClassification(document)
      ## serialization #########################################################
      self.logDebug("Saving classified candidates of %s..."%(document.name))
      self.store(document, classified_candidates)

    return classified_candidates

  def _candidateClassification(self, document):
    """Classifies the candidates of a given document.

    Args:
      document: The C{KBDocument} from which the candidates must be classified.

    Returns:
      The C{map} of C{KBTextualUnit} C{list}s associated to a C{string} class
      (C{KBCandidateClassifierI.KEYPHRASE} or
      C{KBCandidateClassifierI.NON_KEYPHRASE}).
    """

    raise exceptions.NotImplementedError()

