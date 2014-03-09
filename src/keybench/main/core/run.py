class KBRun(object):
  """The executor of a specific run.

  The executor of a run specified by its C{name}. The configuration
  (C{KBComponentFactory}) of the run can be found from the C{KBBenchmark}
  singleton.

  Attributes:
    name: The C{string} name of the run.
  """

  def __init__(self, name):
    super(KBRun, self).__init__()

    self._name = name

  def __eq__(self, other):
    return self._name == other._name

  def __ne__(self, other):
    return not self.__eq__(other)

  @property
  def name(self):
    return self._name

  def start(self):
    """Executes the run.
    """

    # TODO
    print "Run %s"%(self._name)

