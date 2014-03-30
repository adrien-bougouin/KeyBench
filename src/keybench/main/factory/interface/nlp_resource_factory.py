from keybench.main import exception

class KBNLPResourceFactoryI(object):
  """The configuration of the NLP resources to use for each language.

  The abstract factory providing the usefull Natural Language Processing
  resources (e.g. list of stop words) for specific languages.
  """

  def stopLists(self):
    """Provides a list of stop words.

    Returns:
      The C{list} of C{string} words to use as stop words.
    """

    raise exception.KBConfigurationException(self, "Uncomplete NLP resource configuration!")

