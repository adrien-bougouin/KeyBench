class KBTextualUnitClusterException(Exception):
  """Exception triggered when an error occurres while modifying a cluster of
  textual units.
  """

  def __init__(self, textual_unit, cluster_elements, message):
    """
    Args:
      textual_unit: The C{KBTextualUnit} for which the exception occurred.
      cluster_elements: The cluster (as a C{list} of C{KBTextualUnit}s) for
        which the exception occurred.
      message: A C{string} message describing the occurred exception.
    """

    super(KBTextualUnitClusterException, self).__init__()

    self._message = "Error with '%s' of cluster %s: %s"%(textual_unit,
                                                         str(cluster_elements),
                                                         message)

  def __str__(self):
    return self._message

