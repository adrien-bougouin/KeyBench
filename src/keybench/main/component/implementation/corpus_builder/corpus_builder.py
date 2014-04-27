# -*- encoding: utf-8 -*-

import os

from os import path

from keybench.main import core
from keybench.main import model
from keybench.main.component import component

class KBCorpusBuilder(component.KBComponent):
  """The component responsible of the creation of a corpus representation.

  The component that creates a C{KBCorpus} from a file.
  """

  def __init__(self,
               name,
               run_name,
               shared,
               lazy_mode,
               debug_mode,
               root_cache,
               corpus_name,
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
      name: The C{string} name of the component.
      run_name: The C{string} name of the run for which the component is
        affected to.
      shared: True if the component shares informations with equivalent
        components (same name).
      lazy_mode: True if the component load precomputed data. False, otherwise.
      debug_mode: True if the component can log debug messages. False,
        otherwise.
      root_cache: The root of the cache directory where the cached objects must
        be stored.

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
      language: The C{string} name of the corpus' language (see
        C{keybench.main.language.KBLanguage.ENGLISH}). 
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

    super(KBCorpusBuilder, self).__init__(name,
                                          run_name,
                                          shared,
                                          lazy_mode,
                                          debug_mode,
                                          root_cache)

    self._corpus_name = corpus_name
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

    self._corpus = None

  def buildCorpus(self):
    """Builds the corpus.

    Builds the corpus based on arguments sent at the initialization.

    Returns:
      The C{KBCorpus} representation.
    """

    # lazy loading of the corpus
    if self._corpus == None:
      ## NLP tools #############################################################
      tool_factory = core.KBBenchmark.singleton().run_tools[self._run_name]
      document_builder = tool_factory.documentBuilder(self._language)
      ##########################################################################

      # build the train documents
      train_documents = {}
      train_directory = path.join(self._directory, self._train_subdirectory)
      for filename in os.listdir(train_directory):
        if filename[-len(self._file_extension):] == self._file_extension:
          document = document_builder.buildDocument(path.join(train_directory,
                                                              filename),
                                                    self._name,
                                                    filename[:-len(self._file_extension)],
                                                    self._language,
                                                    self._encoding)

          train_documents[document.name] = document
      # build the test documents
      test_documents = {}
      test_directory = path.join(self._directory, self._test_subdirectory)
      for filename in os.listdir(test_directory):
        if filename[-len(self._file_extension):] == self._file_extension:
          document = document_builder.buildDocument(path.join(test_directory,
                                                              filename),
                                                    self._name,
                                                    filename[:-len(self._file_extension)],
                                                    self._language,
                                                    self._encoding)

          test_documents[document.name] = document
      # the corpus is kept into memory to avoid creating a distinct instance at
      # each call of buildCorpus(), then increase the memory consumption
      self._corpus = model.KBCorpus(self._corpus_name,
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
                                    self._pos_tagged_references,
                                    train_documents,
                                    test_documents)

    return self._corpus

