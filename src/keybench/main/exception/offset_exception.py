
class KBOffsetException(Exception):
  """Exception triggered when an unexpected offset is found for a given textual
  unit within a given document.
  """

  def __init__(self, message, document, textual_unit, offset):
    """Constructor.

    Args:
      message: A C{string} message describing the occured error.
      document: The C{string} identifier of the document for which the error
        occured.
      textual_unit: The C{string} representation of the textual unit for which
        the error occured.
      offset: The offset value (C{int)}) for which the error occured.
    """

    self._message = "Error with offset %d of '%s' from '%s': %s"%(offset,
                                                                 textual_unit,
                                                                 document,
                                                                 message)

  def __str__(self):
    return self._message

