class KBLazyComponentException(Exception):
  """An Exception triggered when an error occurres while loading cached objects
  with a non-lazy component.
  """

  def __init__(self, component_name, component_class, run_name, message):
    """
    Args:
      component_name: The C{string} name of the component responsible for the
        triggered exception.
      component_class: The name of the component's class.
      run_name: The C{string} name of the run while the exception occurred.
      message: A C{string} message describing the occurred exception.
    """

    super(KBLazyComponentException, self).__init__()

    self._message = "Error while loading data from %s:%s (%s): %s"%(component_name,
                                                                    component_class,
                                                                    run_name,
                                                                    message)

  def __str__(self):
    return self._message

