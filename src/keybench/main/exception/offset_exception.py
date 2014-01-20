
class KBOffsetException(Exception):
  """Exception triggered when an unexpected offset is found for a given textual
  unit within a given document.
  """

  def __init__(self, offset, textual_unit, document, message):
    """
    Args:
      offset: The offset value (C{int)}) for which the exception occurred.
      textual_unit: The C{string} representation of the textual unit for which
        the exception occurred.
      document: The C{string} identifier of the document for which the exception
        occurred.
      message: A C{string} message describing the occurred exception.
    """

    super(KBOffsetException, self).__init__()

    self._message = "Error with offset %d of '%s' from '%s': %s"%(offset,
                                                                 textual_unit,
                                                                 document,
                                                                 message)

  def __str__(self):
    return self._message

