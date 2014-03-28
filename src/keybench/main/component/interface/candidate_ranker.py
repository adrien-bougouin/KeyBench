import exceptions

from keybench.main.component import component # avoid recursive import

class KBCandidateRankerI(component.KBComponent):
  """The abstract component responsible of the ranking of the candidates of a
  document.

  The component that ranks the candidates of a C{KBDocument}. In most cases,
  subclasses must not override C{rankCandidates()}, but only
  C{candidateRanking()}.
  """

  def rankCandidates(self, document):
    """Ranks the candidates of a given document.

    Args:
      document: The C{KBDocument} from which the candidates must be ranked.

    Returns:
      The ordered C{list} of C{KBTextualUnit} candidates and their C{int} score
      (C{tuple}).
    """

    ranked_candidates = None

    # - can the component do lazy loading?
    # - does the document already exist?
    if self.isLazy() \
       and self.exists(document):
      # lazy loading
      ranked_candidates = self.load(document)
    # rank candidates
    else:
      ## candidate ranking #####################################################
      self.logDebug("Ranking candidates of %s..."%(document.name))
      ranked_candidates = self._candidateRanking(document)
      ## serialization #########################################################
      self.logDebug("Saving ranked candidates of %s..."%(document.name))
      self.store(document, ranked_candidates)

    return ranked_candidates

  def _candidateRanking(self, document):
    """Ranks the candidates of a given document.

    Args:
      document: The C{KBDocument} from which the candidates must be ranked.

    Returns:
      The ordered C{list} of C{KBTextualUnit} candidates and their C{int} score
      (C{tuple}).
    """

    raise exceptions.NotImplementedError()

