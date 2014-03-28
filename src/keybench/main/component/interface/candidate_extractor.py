import exceptions

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

  def _candidateExtraction(self, document):
    """Extracts the candidates of a given document.

    Args:
      document: The C{KBDocument} from which the candidates must be extracted.

    Returns:
      The C{list} of extracted, and filtered, candidates (C{KBTextualUnit}s).
    """

    raise exceptions.NotImplementedError()

