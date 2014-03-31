from keybench.main import exception

class KBNLPToolFactoryI(object):
  """The configuration of the NLP tools to use for each language.

  The abstract factory providing the components that perform a specific Natural
  Language Processing for specific languages.
  """

  def normalizer(self, language):
    """Provides the normalizer to use for a given language.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Returns:
      The C{KBNormalizerI} to use for the given C{language}.
    """

    raise exception.KBConfigurationException(self, "Uncomplete NLP tool configuration!")

  def tokenizer(self, language):
    """Provides the tokenizer to use for a given language.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Returns:
      The C{KBTokenizerI} to use for the given C{language}.
    """

    raise exception.KBConfigurationException(self, "Uncomplete NLP tool configuration!")

  def stemmer(self, language):
    """Provides the stemmer to use for a given language.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Returns:
      The C{KBStemmerI} to use for the given C{language}.
    """

    raise exception.KBConfigurationException(self, "Uncomplete NLP tool configuration!")

  def lemmatizer(self, language):
    """Provides the lemmatizer to use for a given language.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Returns:
      The C{KBlemmatizerI} to use for the given C{language}.
    """

    raise exception.KBConfigurationException(self, "Uncomplete NLP tool configuration!")

  def posTagger(self, language):
    """Provides the POS tagger to use for a given language.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Returns:
      The C{KBPOSTaggerI} to use for the given C{language}.
    """

    raise exception.KBConfigurationException(self, "Uncomplete NLP tool configuration!")

