from keybench.main import exception

class KBTextualUnitCluster(object):
  """A representation of a cluster of textual units.

  A cluster grouping textual units and their centroid. No duplicate textual
  units are allowed and the centroid must be part of the textual units of the
  cluster.

  Attributes:
    textual_units: The C{list} of cluster's C{KBTextualUnit}s.
    centroid: The C{KBTextualUnit} that is the centroid of the cluster.
  """

  def __init__(self):
    super(KBTextualUnitCluster, self).__init__()

    self._textual_units = []
    self._centroid = None

  def __eq__(self, other):
    return self._textual_units == other._textual_units \
           and self._centroid == other._centroid

  def __ne__(self, other):
    return not self.__eq__(other)

  @property
  def textual_units(self):
    return self._textual_units

  @property
  def centroid(self):
    return self._centroid

  @centroid.setter
  def centroid(self, textual_unit):
    """
    Raises:
      KBTextualUnitClusterException: An exception occurred when the
        C{textual_unit} given as a centroid does not belong to the cluster's
        textual unit.
    """
    if textual_unit in self._textual_units:
      self._centroid = textual_unit
    else:
      raise exception.KBTextualUnitClusterException("Centroid not in the cluster!",
                                                    textual_unit,
                                                    self._textual_units)

  def addTextualUnit(self, textual_unit):
    """Adds a textual unit to the cluster.

    Args:
      textual_unit: The C{KBTextualUnit} to add to the clusters.

    Raises:
      KBTextualUnitCluster: An exception occurred when the C{textual_unit} that
        is given already exists in the cluster.
    """

    if textual_unit not in self._textual_units:
      self._textual_units.append(textual_unit)
    else:
      raise exception.KBTextualUnitClusterException("Textual unit aleady in the cluster!",
                                                    textual_unit,
                                                    self._textual_units)

  def numberOfTextualUnits(self):
    """Gives the size of the cluster.

    Gives the size of the cluster, in terms of number of textual units within
    it.

    Returns:
      The number of textual units that the cluster contains.
    """

    return len(self._textual_units)

