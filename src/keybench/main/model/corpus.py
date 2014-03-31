import codecs
import os

from os import path

class KBCorpus(object):
  """A representation of a corpus.

  A read-only representation of a corpus. It contains path information (train
  and test documents, or references), content informations (language, encoding,
  etc.) and others.

  Attributes:
    name: The name (identifier) of the corpus.
    directory: The C{string} path of the directory containing the corpus'
      materials.
    train_subdirectory: The C{strin} path (relative to the copus' directory) of
      the directory containing the training documents.
    test_subdirectory: The C{strin} path (relative to the copus' directory) of
      the directory containing the test documents.
    train_reference_subdirectory: The C{strin} path (relative to the copus'
      directory) of the directory containing the references associated to the
      training documents.
    test_reference_subdirectory: The C{strin} path (relative to the copus'
      directory) of the directory containing the references associated to the
      test documents.
    language: The C{string} name of the corpus' language (see
      C{keybench.main.language.KBLanguage.ENGLISH}). 
    encoding: The C{string} name of the corpus' encoding.
    file_extension: The C{string} extention of the corpus' files (including the
      '.').
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

  def __init__(self,
               name,
               directory,
               train_subdirectory,
               test_subdirectory,
               train_reference_subdirectory,
               test_reference_subdirectory,
               language,
               encoding,
               file_extension,
               reference_extension,
               normalized_references,
               tokenized_references,
               stemmed_references,
               lemmatized_references,
               pos_tagged_references):
    super(KBCorpus, self).__init__()

    self._name = name
    self._directory = directory
    self._train_subdirectory = train_subdirectory
    self._test_subdirectory = test_subdirectory
    self._train_reference_subdirectory = train_reference_subdirectory
    self._test_reference_subdirectory = test_reference_subdirectory
    self._language = language
    self._encoding = encoding
    self._file_extension = file_extension
    self._reference_extension = reference_extension
    self._normalized_references = normalized_references
    self._tokenized_references = tokenized_references
    self._stemmed_references = stemmed_references
    self._lemmatized_references = lemmatized_references
    self._pos_tagged_references = pos_tagged_references

  def __eq__(self, other):
    return self._name == other._name \
           and self._directory == other._directory \
           and self._train_subdirectory == other._train_subdirectory \
           and self._test_subdirectory == other._test_subdirectory \
           and self._train_reference_subdirectory == other._train_reference_subdirectory \
           and self._test_reference_subdirectory == other._test_reference_subdirectory \
           and self._language == other._language \
           and self._encoding == other._encoding \
           and self._file_extension == other._file_extension \
           and self._reference_extension == other._reference_extension \
           and self._normalized_references == other._normalized_references \
           and self._tokenized_references == other._tokenized_references \
           and self._stemmed_references == other._stemmed_references \
           and self._lemmatized_references == other._lemmatized_references \
           and self._pos_tagged_references == other._pos_tagged_references

  def __ne__(self, other):
    return not self.__eq__(other)

  @property
  def name(self):
    return self._name

  @property
  def directory(self):
    return self._directory

  @property
  def train_subdirectory(self):
    return self._train_subdirectory

  @property
  def test_subdirectory(self):
    return self._test_subdirectory

  @property
  def train_reference_subdirectory(self):
    return self._train_reference_subdirectory

  @property
  def test_reference_subdirectory(self):
    return self._test_reference_subdirectory

  @property
  def language(self):
    return self._language

  @property
  def encoding(self):
    return self._encoding

  @property
  def file_extension(self):
    return self._file_extension

  @property
  def reference_extension(self):
    return self._reference_extension

  @property
  def normalized_references(self):
    return self._normalized_references

  @property
  def tokenized_references(self):
    return self._tokenized_references

  @property
  def stemmed_references(self):
    return self._stemmed_references

  @property
  def lemmatized_references(self):
    return self._lemmatized_references

  @property
  def pos_tagged_references(self):
    return self._pos_tagged_references

  @property
  def train_directory(self):
    return path.join(self._directory, self._train_subdirectory)

  @property
  def test_directory(self):
    return path.join(self._directory, self._test_subdirectory)

  @property
  def train_reference_directory(self):
    return path.join(self._directory, self._train_reference_subdirectory)

  @property
  def test_reference_directory(self):
    return path.join(self._directory, self._test_reference_subdirectory)

  def trainDocuments(self, document_builder):
    """Provides every train document of the corpus.

    Args:
      document_builder: The C{KBDocumentBuilderI} component to use for the
        creation of each document.

    Returns:
      The C{list} of C{KBDocument}s in the train directory of the corpus.
    """

    documents = []

    for filename in os.listdir(self.train_directory):
      if filename[-len(self._file_extension):] == self._file_extension:
        document = document_builder(path.join(self.train_directory, filename),
                                    self._name,
                                    filename[:-len(self._file_extension)],
                                    self._language,
                                    self._encoding)

        documents.append(document)

    return documents

  def testDocuments(self, document_builder):
    """Provides every test document of the corpus.

    Args:
      document_builder: The C{KBDocumentBuilderI} component to use for the
        creation of each document.

    Returns:
      The C{list} of C{KBDocument}s in the test directory of the corpus.
    """

    documents = []

    for filename in os.listdir(self.test_directory):
      if filename[-len(self._file_extension):] == self._file_extension:
        document = document_builder(path.join(self.test_directory, filename),
                                    self._name,
                                    filename[:-len(self._file_extension)],
                                    self._language,
                                    self._encoding)

        documents.append(document)

    return documents

  def trainReferences(self):
    """Provides the references for every train document.

    Returns:
      The C{map} of references (C{list} of C{string}) associated to each train
      document (C{string} name as key).
    """

    references = {}

    for filename in os.listdir(self.train_reference_directory):
      if filename[-len(self._reference_extension):] == self._reference_extension:
        filepath = path.join(self.train_reference_directory, filename)
        name = filename[:-len(self._reference_extension)]
        reference_file = codecs.open(filepath, "r", self._encoding)

        references[name] = reference_file.read().splitlines()

        reference_file.close()

    return references

  def testReferences(self):
    """Provides the references for every test document.

    Returns:
      The C{map} of references (C{list} of C{string}) associated to each test
      document (C{string} name as key).
    """

    references = {}

    for filename in os.listdir(self.test_reference_directory):
      if filename[-len(self._reference_extension):] == self._reference_extension:
        filepath = path.join(self.test_reference_directory, filename)
        name = filename[:-len(self._reference_extension)]
        reference_file = codecs.open(filepath, "r", self._encoding)

        references[name] = reference_file.read().splitlines()

        reference_file.close()

    return references

