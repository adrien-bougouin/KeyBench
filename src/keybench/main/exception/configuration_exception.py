class KBConfigurationException(Exception):
  """An exception triggered when the required components do not fit the
  configuration.
  """

  def __init__(self, configuration, message):
    """
    Args:
      configuration: The C{KBComponentFactory} (configuration) for which the
        exception occurred.
      message: A C{string} message describing the occurred exception.
    """

    super(KBConfigurationException, self).__init__()

    self._message = "Error with configurate \\%s\\: %s"%(configuration, message)

  def __str__(self):
    return self._message

