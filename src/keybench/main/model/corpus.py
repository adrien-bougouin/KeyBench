# -*- encoding: utf-8 -*-

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
      C{keybench.main.language_support.KBLanguage}). 
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
   train_document_information: The information of the train documents required
    to be able to get their C{KBDocument} representation (C{list} of
    C{tuple(<filepath>, <corpus_name>, <name>, <language>, <encoding>)}).
   test_document_information: The information of the test documents required
    to be able to get their C{KBDocument} representation (C{list} of
    C{tuple(<filepath>, <corpus_name>, <name>, <language>, <encoding>)}).
   train_references: The C{map} of C{list} of C{string} keyphrases associated to
    each train document (referenced by its C{string} name).
   test_references: The C{map} of C{list} of C{string} keyphrases associated to
    each test document (referenced by its C{string} name).
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
               pos_tagged_references,
               train_document_information,
               test_document_information,
               train_references,
               test_references):

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
    self._train_document_information = train_document_information
    self._test_document_information = test_document_information
    self._train_references = train_references
    self._test_references = test_references

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
           and self._pos_tagged_references == other._pos_tagged_references \
           and self._train_document_information == other._train_document_information \
           and self._test_document_information == other._test_document_information \
           and self._train_references == other._train_references \
           and self._test_references == other._test_references

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
  def train_document_information(self):
    return self._train_document_information

  @property
  def test_document_information(self):
    return self._test_document_information

  @property
  def train_references(self):
    return self._train_references

  @property
  def test_references(self):
    return self._test_references

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

