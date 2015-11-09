# -*- encoding: utf-8 -*-

from keybench.main.factory.interface import nlp_tool_factory
from keybench.main.nlp_tool.implementation.normalizer import lowercase_normalizer
from keybench.main.nlp_tool.implementation.tokenizer import french_bonsai_tokenizer
from keybench.main.nlp_tool.implementation.stemmer import snowball_stemmer
from keybench.main.nlp_tool.implementation.lemmatizer import french_lefff_lemmatizer
from keybench.main.nlp_tool.implementation.pos_tagger import melt_pos_tagger

class FrenchNLPToolFactory(object):
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

    return lowercase_normalizer.LowercaseNormalizer()

  def tokenizer(self, language):
    """Provides the tokenizer to use for a given language.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Returns:
      The C{KBTokenizerI} to use for the given C{language}.
    """

    return french_bonsai_tokenizer.FrenchBonsaiTokenizer("utf-8")

  def stemmer(self, language):
    """Provides the stemmer to use for a given language.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Returns:
      The C{KBStemmerI} to use for the given C{language}.
    """

    return snowball_stemmer.SnowballStemmer("french")

  def lemmatizer(self, language):
    """Provides the lemmatizer to use for a given language.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Returns:
      The C{KBlemmatizerI} to use for the given C{language}.
    """

    return french_lefff_lemmatizer.FrenchLeFFFLemmatizer()

  def posTagger(self, language):
    """Provides the POS tagger to use for a given language.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Returns:
      The C{KBPOSTaggerI} to use for the given C{language}.
    """

    return melt_pos_tagger.MEltPOSTagger("french", "utf-8")

