import codecs
import unittest
import shutil

import os
from os import path

from keybench.main import model
from keybench.main.component import implementation as component_implementation

class KBCorpusTests(unittest.TestCase):

  def setUp(self):
    self._corpus = model.KBCorpus("test-corpus",
                                  "test_corpus",
                                  "train",
                                  "test",
                                  path.join("reference", "train"),
                                  path.join("reference", "test"),
                                  "fr",
                                  "utf-8",
                                  ".txt",
                                  ".key",
                                  True,
                                  False,
                                  False,
                                  False,
                                  False)

    # create corpus directory
    os.makedirs(path.join("test_corpus", "train"))
    os.makedirs(path.join("test_corpus", "test"))
    os.makedirs(path.join("test_corpus", "reference", "train"))
    os.makedirs(path.join("test_corpus", "reference", "test"))
    # add documents
    codecs.open(path.join("test_corpus",
                          "train",
                          "doc1.txt"),
                          "a",
                          "utf-8").close()
    codecs.open(path.join("test_corpus",
                          "train",
                          "doc2.txt"),
                          "a",
                          "utf-8").close()
    codecs.open(path.join("test_corpus",
                          "test",
                          "doc3.txt"),
                          "a",
                          "utf-8").close()
    codecs.open(path.join("test_corpus",
                          "test",
                          "doc4.txt"),
                          "a",
                          "utf-8").close()
    # add keyphrases
    with codecs.open(path.join("test_corpus",
                               "reference",
                               "train",
                               "doc1.key"),
                               "a",
                               "utf-8") as f:
      f.write("key11\nkey12")
    with codecs.open(path.join("test_corpus",
                               "reference",
                               "train",
                               "doc2.key"),
                               "a",
                               "utf-8") as f:
      f.write("key21\nkey22")
    with codecs.open(path.join("test_corpus",
                               "reference",
                               "test",
                               "doc3.key"),
                               "a",
                               "utf-8") as f:
      f.write("key31\nkey32")
    with codecs.open(path.join("test_corpus",
                               "reference",
                               "test",
                               "doc4.key"),
                               "a",
                               "utf-8") as f:
      f.write("key41\nkey42")
    # add tricky files
    codecs.open(path.join("test_corpus",
                          "train",
                          "dummy1.key"),
                          "a",
                          "utf-8").close()
    codecs.open(path.join("test_corpus",
                          "test",
                          "dummy2.key"),
                          "a",
                          "utf-8").close()
    codecs.open(path.join("test_corpus",
                          "reference",
                          "train",
                          "dummy1.txt"),
                          "a",
                          "utf-8").close()
    codecs.open(path.join("test_corpus",
                          "reference",
                          "test",
                          "dummy2.txt"),
                          "a",
                          "utf-8").close()

  def tearDown(self):
    self._corpus = None
    shutil.rmtree("test_corpus")
    if path.exists(".test_tmp"):
      shutil.rmtree(".test_tmp")

  def testInitialization(self):
    self.failUnless(self._corpus.name == "test-corpus")
    self.failUnless(self._corpus.directory == "test_corpus")
    self.failUnless(self._corpus.train_subdirectory == "train")
    self.failUnless(self._corpus.test_subdirectory == "test")
    self.failUnless(self._corpus.train_reference_subdirectory == path.join("reference", "train"))
    self.failUnless(self._corpus.test_reference_subdirectory == path.join("reference", "test"))
    self.failUnless(self._corpus.language == "fr")
    self.failUnless(self._corpus.encoding == "utf-8")
    self.failUnless(self._corpus.file_extension == ".txt")
    self.failUnless(self._corpus.reference_extension == ".key")
    self.failUnless(self._corpus.normalized_references == True)
    self.failUnless(self._corpus.tokenized_references == False)
    self.failUnless(self._corpus.stemmed_references == False)
    self.failUnless(self._corpus.lemmatized_references == False)
    self.failUnless(self._corpus.pos_tagged_references == False)

    train_directory = path.join(self._corpus.directory,
                                self._corpus.train_subdirectory)
    test_directory = path.join(self._corpus.directory,
                               self._corpus.test_subdirectory)
    train_reference_directory = path.join(self._corpus.directory,
                                          self._corpus.train_reference_subdirectory)
    test_reference_directory = path.join(self._corpus.directory,
                                         self._corpus.test_reference_subdirectory)

    self.failUnless(self._corpus.train_directory == train_directory)
    self.failUnless(self._corpus.test_directory == test_directory)
    self.failUnless(self._corpus.train_reference_directory == train_reference_directory)
    self.failUnless(self._corpus.test_reference_directory == test_reference_directory)

  def testEqual(self):
    corpus1 = model.KBCorpus("test-corpus",
                             "test_corpus",
                             "train",
                             "test",
                             path.join("reference", "train"),
                             path.join("reference", "test"),
                             "fr",
                             "utf-8",
                             ".txt",
                             ".key",
                             True,
                             False,
                             False,
                             False,
                             False)
    corpus2 = model.KBCorpus("test-corpus",
                             "test_corpus",
                             "train",
                             "test",
                             path.join("reference", "train"),
                             path.join("reference", "test"),
                             "fr",
                             "utf-8",
                             ".txt",
                             ".key",
                             False,
                             False,
                             False,
                             False,
                             False)
    corpus3 = model.KBCorpus("test-corpus2",
                             "test_corpus2",
                             "train",
                             "test",
                             path.join("reference", "train"),
                             path.join("reference", "test"),
                             "fr",
                             "utf-8",
                             ".txt",
                             ".key",
                             True,
                             False,
                             False,
                             False,
                             False)

    self.failUnless(self._corpus == corpus1)
    self.failIf(self._corpus == corpus2)
    self.failIf(self._corpus == corpus3)

  def testNotEqual(self):
    corpus1 = model.KBCorpus("test-corpus",
                             "test_corpus",
                             "train",
                             "test",
                             path.join("reference", "train"),
                             path.join("reference", "test"),
                             "fr",
                             "utf-8",
                             ".txt",
                             ".key",
                             True,
                             False,
                             False,
                             False,
                             False)
    corpus2 = model.KBCorpus("test-corpus",
                             "test_corpus",
                             "train",
                             "test",
                             path.join("reference", "train"),
                             path.join("reference", "test"),
                             "fr",
                             "utf-8",
                             ".txt",
                             ".key",
                             False,
                             False,
                             False,
                             False,
                             False)
    corpus3 = model.KBCorpus("test-corpus2",
                             "test_corpus2",
                             "train",
                             "test",
                             path.join("reference", "train"),
                             path.join("reference", "test"),
                             "fr",
                             "utf-8",
                             ".txt",
                             ".key",
                             True,
                             False,
                             False,
                             False,
                             False)

    self.failIf(self._corpus != corpus1)
    self.failUnless(self._corpus != corpus2)
    self.failUnless(self._corpus != corpus3)

  def testDocumentExtraction(self):
    document_builder = component_implementation.PlainTextDocumentBuilder("name",
                                                                         "run_name",
                                                                         False,
                                                                         False,
                                                                         False,
                                                                         ".test_tmp")

    self.failUnless(self._corpus.trainDocuments(document_builder).keys() == ["doc2",
                                                                             "doc1"])
    self.failUnless(self._corpus.testDocuments(document_builder).keys() == ["doc3",
                                                                            "doc4"])
    self.failUnless(self._corpus.trainReferences() == {
      "doc1": ["key11", "key12"],
      "doc2": ["key21", "key22"]
    })
    self.failUnless(self._corpus.testReferences() == {
      "doc3": ["key31", "key32"],
      "doc4": ["key41", "key42"]
    })

