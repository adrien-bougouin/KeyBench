# -*- encoding: utf-8 -*-

import multiprocessing

import keybench.main.core.benchmark

def __keyphrase_extraction_thread(arguments):
  """Extracts the keyphrases of a corpus' documents.

  Args:
    arguments: The C{KBKeyphraseExtractorI} component to use for the keyphrase
      extraction and the C{KBCorpus} from which the keyphrases must be
      extracted (C{tuple}).

  Returns:
    The C{KBCorpus} from which the keyphrases are extracted and the C{map} of
    extracted keyphrases (C{list} of C{string} as value) associated to a
    document (C{string name as key}).
  """
  corpus_builder, document_builder, keyphrase_extractor = arguments
  corpus = corpus_builder.buildCorpus()
  keyphrase_documents = {}

  for filepath, corpus_name, name, language, encoding in corpus.test_document_information:
    document = document_builder.buildDocument(filepath,
                                              corpus_name,
                                              name,
                                              language,
                                              encoding)
    document_keyphrases[document.name] = keyphrase_extractor.extractKeyphrases(document)

  return (corpus, document_keyphrases)

################################################################################

class KBRun(object):
  """The executor of a specific run.

  The executor of a run specified by its C{name}. The configuration
  (C{KBComponentFactory}) of the run can be found from the C{KBBenchmark}
  singleton.

  Attributes:
    name: The C{string} name of the run.
  """

  def __init__(self, name):
    super(KBRun, self).__init__()

    self._name = name

  def __eq__(self, other):
    return self._name == other._name

  def __ne__(self, other):
    return not self.__eq__(other)

  @property
  def name(self):
    return self._name

  def start(self):
    """Executes the run.

    Execute the keyphrase extraction run using one thread for each corpus to
    treat during the run.
    """

    benchmark_singleton = benchmark.KBBenchmark.singleton()
    configuration = benchmark_singleton.run_configurations[self._name]
    thread_arguments = []

    # preparation of the keyphrase extract
    for corpus_builder in configuration.corpusBuilders():
      thread_arguments.append((corpus_builder,
                               configuration.documentBuilder(corpus_builder.language),
                               configuration.keyphrase_Extractor(corpus_builder.language)))

    # keyphrase extraction
    if len(thread_arguments) == 1:
      extraction_results = [__keyphrase_extraction_thread(thread_arguments[0])]
    # multi-threaded keyphrase extraction
    else:
      thread_pool = multiprocessing.Pool()
      extraction_results = thread_pool.map(__keyphrase_extraction_thread,
                                           thread_arguments)

    # consumption of the keyphrases extracted from each documents of each
    # corpus
    for corpus, document_keyphrases in extraction_results:
      for keyphrase_consumer in configuration.keyphraseConsumers():
        keyphrase_consumer.consumeKeyphrases(corpus, document_keyphrases)

