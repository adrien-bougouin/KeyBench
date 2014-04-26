
class KBOffsetException(Exception):
  """An exception triggered when an unexpected offset is found for a given
    textual unit within a given document.
  """

  def __init__(self,
               sentence_offset,
               inner_sentence_offset,
               textual_unit,
               message):
    """
    Args:
      sentence_offset: The sentence offset value (C{int)}) for which the
        exception occurred.
      inner_sentence_offset: The inner sentence offset value (C{int)}) for which
        the exception occurred.
      textual_unit: The C{string} representation of the textual unit for which
        the exception occurred.
      message: A C{string} message describing the occurred exception.
    """

    super(KBOffsetException, self).__init__()

    self._message = "Error with offset (%d, %d) of '%s': %s"%(
                      sentence_offset,
                      inner_sentence_offset,
                      textual_unit,
                      message
                    )

  def __str__(self):
    return self._message

