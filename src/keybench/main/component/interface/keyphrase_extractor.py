# -*- encoding: utf-8 -*-

import exceptions

from keybench.main.component import component

class KBKeyphraseExtractorI(component.KBComponent):
  """The abstract component responsible of the extraction of the keyphrases of a
  document.

  The component that extracts keyphrases from a C{KBDocument}. In most cases,
  subclasses must not override C{extractKeyphrases()}, but only
  C{keyphraseExtraction()}.
  """

  ##############################################################################
  class RedundancyFilterI(object):
    """An interface of a candidate filter.
    """

    def areRedundant(self, textual_unit1, textual_unit2):
      """Checks if two textual units are redundant.

      Args:
        textual_unit1: The first C{KBTextualUnit} to check.
        textual_unit2: The second C{KBTextualUnit} to check.

      Returns:
        True if the C{textual_unit}s are redundant. False, otherwise.
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

    super(KBCandidateExtractorI, self).__init__(name,
                                                run_name,
                                                shared,
                                                lazy_mode,
                                                debug_mode,
                                                root_cache)

    self._redundancy_filters = redundancy_filters

  def extractKeyphrases(self, document):
    """Extracts the keyphrases of a given document.

    Args:
      document: The C{KBDocument} from which the keyphrases must be extracted.

    Returns:
      The C{list} of extracted, and filtered, keyphrases (C{KBTextualUnit}s).
    """

    keyphrases = None

    # - can the component do lazy loading?
    # - does the document already exist?
    if self.isLazy() \
       and self.exists(document):
      # lazy loading
      keyphrases = self.load(document)
    # extract the candidates
    else:
      ## keyphrase extraction ##################################################
      self.logDebug("Extracting keyphrases of %s..."%(document.name))
      keyphrases = self._keyphraseExtraction(document)
      ## candidate filtering ###################################################
      self.logDebug("Filtering keyphrases of %s..."%(document.name))
      index = 0
      while index != len(keyphrases) - 1:
        redundant = False

        for redundancy_filter in self._redundancy_filters:
          for test_keyphrase in keyphrases[index + 1:]:
            if redundancy_filter.areRedundant(keyphrases[index],
                                              test_keyphrase):
              redundant = True
              break

          if redundant == True:
            break

        if redundant == True:
          keyphrases.remove(keyphrases[index])
        else:
          index += 1
      ## serialization #########################################################
      self.logDebug("Saving keyphrases of %s..."%(document.name))
      self.store(document, keyphrases)

    return keyphrases

  def _keyphraseExtraction(self, document):
    """Extracts the keyphrases of a given document.

    Args:
      document: The C{KBDocument} from which the keyphrases must be extracted.

    Returns:
      The C{list} of extracted, and filtered, keyphrases (C{KBTextualUnit}s).
    """

    raise exceptions.NotImplementedError()

