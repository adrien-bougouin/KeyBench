from keybench.main import core
from keybench.main import model

class KBCorpusBuilder(object):
  """The component responsible of the creation of a corpus representation.

  The component that creates a C{KBCorpus} from a file.
  """

  def __init__(self,
               name,
               directory,
               train_subdirectory,
               test_subdicrectory,
               train_reference_subdirectory,
               test_reference_subdirectory,
               language,
               encoding,
               file_extension,
               reference_extension,
               normalized_references,
               tokenized_references,
               stemmed_referecences,
               lemmatized_references,
               pos_tagged_references):
    """Constructor.

    Args:
      name: The name (identifier) of the corpus.
        directory: The C{string} path of the directory containing the corpus'
        materials.
      train_subdirectory: The C{strin} path (relative to the copus' directory)
        of the directory containing the training documents.
      test_subdirectory: The C{strin} path (relative to the copus' directory) of
        the directory containing the test documents.
      train_reference_subdirectory: The C{strin} path (relative to the copus'
        directory) of the directory containing the references associated to the
        training documents.
      test_reference_subdirectory: The C{strin} path (relative to the copus'
        directory) of the directory containing the references associated to the
        test documents.
      language: The C{string} name of the corpus' language. 
      encoding: The C{string} name of the corpus' encoding.
      file_extension: The C{string} extention of the corpus' files (including
        the '.').
      reference_extension: The C{string} extention of the corpus' references
        (including the '.').
      normalized_references: C{True} if the reference keyphrases are normalized.
        Otherwise, C{False}.
      tokenized_references: C{True} if the reference keyphrases are tokenized.
        Otherwise, C{False}.
      stemmed_references: C{True} if the reference keyphrases are stemmed.
        Otherwise, C{False}.
      lemmatized_references: C{True} if the reference keyphrases are lemmatized.
        Otherwise, C{False}.
      pos_tagged_references: C{True} if the reference keyphrases are POS tagged.
        Otherwise, C{False}.
    """

    super(KBCorpusBuilder, self).__init__()

    self._name = name
    self._directory = directory
    self._train_subdirectory = train_subdirectory
    self._test_subdicrectory = test_subdicrectory
    self._train_reference_subdirectory = train_reference_subdirectory
    self._test_reference_subdirectory = test_reference_subdirectory
    self._language = language
    self._encoding = encoding
    self._file_extension = file_extension
    self._reference_extension = reference_extension
    self._normalized_references = normalized_references
    self._tokenized_references = tokenized_references
    self._stemmed_referecences = stemmed_referecences
    self._lemmatized_references = lemmatized_references
    self._pos_tagged_references = pos_tagged_references

  def buildCorpus(self):
    """Builds the corpus.

    Builds the corpus based on arguments sent at the initialization.

    Returns:
      The C{KBCorpus} representation.
    """

    return model.KBCorpus(self._name,
                          self._directory,
                          self._train_subdirectory,
                          self._test_subdicrectory,
                          self._train_reference_subdirectory,
                          self._test_reference_subdirectory,
                          self._language,
                          self._encoding,
                          self._file_extension,
                          self._reference_extension,
                          self._normalized_references,
                          self._tokenized_references,
                          self._stemmed_referecences,
                          self._lemmatized_references,
                          self._pos_tagged_references)

