# -*- encoding: utf-8 -*-

from keybench.main.factory.state_of_the_art import tfidf_component_factory
from keybench.main.component.implementation.document_builder import plain_text_document_builder
from keybench.main.component.implementation.corpus_builder import corpus_builder

class TestRunFactory(tfidf_component_factory.TFIDFComponentFactory):
  def __init__(self):
    super(TestRunFactory, self).__init__("test_run", True, True, "./cache_test")

  def documentBuilder(self, corpus_name):
    """Provides the component that can build documents for a given corpus.

    Args:
      corpus_name: The C{string} name of the corpus of the documents that must
        be built.

    Returns:
      The C{KBDocumentBuilderI} that can parse file and build documents
      belonging to the given C{corpus_name}.
    """

    return plain_text_document_builder.PlainTextDocumentBuilder(
      "test_document_builder",
      self._run_name,
      True,
      self._lazy_mode,
      self._debug_mode,
      self._root_cache
    )

  def corpusBuilders(self):
    """Provides a list of corpus builders.

    Provides a list of corpus builders. This list determines every corpus to be
    treated in the run.

    Returns:
      The C{map} of C{KBCorpusBuilder} of the run.
    """

    return {
      "test_run": corpus_builder.KBCorpusBuilder(
        "test_corpus_builder",
        self._run_name,
        True,
        self._lazy_mode,
        self._debug_mode,
        self._root_cache,
        "test_corpus",
        "./test_corpus",
        "train",
        "test",
        "train_ref",
        "test_ref",
        "french", # FIXME use language_support
        "utf-8",
        ".txt",
        ".key",
        False,
        False,
        False,
        False,
        False
      )
    }
    

  def keyphraseConsumers(self, language):
    """Provides a list of keyphrase consumers.

    Args:
      language: The C{string} name of the language to treat (see
        C{keybench.main.language_support.KBLanguage}).

    Provides a list of keyphrase consumers. It can be keyphrase extraction
    evaluators, keyphrase indexing systems, word cloud generators, etc.

    Returns:
      The C{list} of C{KBKeyphraseConsumerI} of the run.
    """

    return []

