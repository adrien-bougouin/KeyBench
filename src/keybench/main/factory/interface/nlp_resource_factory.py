from keybench.main import exception

class KBNLPResourceFactoryI(object):
  """The configuration of the NLP resources to use for each language.

  The abstract factory providing the usefull Natural Language Processing
  resources (e.g. list of stop words) for specific languages.
  """

  def stopList(self, language):
    """Provides a list of stop words.

    Args:
      language: The C{string} name of the language of the data to treat (see
        C{keybench.main.language_support.KBLanguage.ENGLISH}).

    Returns:
      The C{list} of C{string} words to use as stop words.
    """

    raise exception.KBConfigurationException(self, "Uncomplete NLP resource configuration!")

