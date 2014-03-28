import exceptions

from keybench.main.component import component

class KBCandidateClustererI(component.KBComponent):
  """The abstract component responsible of the clustering of the candidates of a
  document.

  The component that clusters the candidates of a C{KBDocument}. In most cases,
  subclasses must not override C{clusterCandidates()}, but only
  C{candidateClustering()}.
  """

  def extractCandidates(self, document):
    """Clusters the candidates of a given document.

    Args:
      document: The C{KBDocument} from which the candidates must be clustered.

    Returns:
      The C{list} of C{KBTextualUnitCluster}s).
    """

    clusters = None

    # - can the component do lazy loading?
    # - does the document already exist?
    if self.isLazy() \
       and self.exists(document):
      # lazy loading
      clusters = self.load(document)
    # cluster candidates
    else:
      ## candidate clustering ##################################################
      self.logDebug("Clustering candidates of %s..."%(document.name))
      clusters = self._candidateClustering(document)
      ## serialization #########################################################
      self.logDebug("Saving candidate clusters of %s..."%(document.name))
      self.store(document, clusters)

    return clusters

  def _candidateClustering(self, document):
    """Clusters the candidates of a given document.

    Args:
      document: The C{KBDocument} from which the candidates must be clustered.

    Returns:
      The C{list} of C{KBTextualUnitCluster}s).
    """

    raise exceptions.NotImplementedError()

