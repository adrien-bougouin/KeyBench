import multiprocessing

import keybench.main.core.benchmark

def __keyphrase_extraction_thread(arguments):
  """Extracts the keyphrases of a document.

  Args:
    arguments: The C{KBKeyphraseExtractorI} component to use for the keyphrase
      extraction and the C{KBDocument} from which the keyphrases must be
      extracted (C{tuple}).

  Returns:
    The C{string} name of the treated document and its C{list} of extracted
    keyphrases
  """
  keyphrase_extractor, document = arguments

  return (document.name, keyphrase_extractor.extractKeyphrases(document))

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
    """

    benchmark_singleton = benchmark.KBBenchmark.singleton()
    configuration = benchmark_singleton.run_configurations[self._name]
    nb_threads = benchmark_singleton.run_threads[self._name]

    # keyphrase extraction of the corpora taken one by one
    for corpus_builder in configuration.corpusBuilders():
      keyphrases = {}
      corpus = corpus_builder.buildCorpus()
      document_builder = configuration.documentBuilder(corpus.name)
      thread_arguments = []
      extraction_results = []

      # preparation of the keyphrase extraction of the documents
      for document in corpus.testDocuments(document_builder):
        thread_arguments.append((configuration.keyphraseExtractor(), document))

      # sequential keyphrase extraction of the documents
      if nb_threads == 1:
        for arguments in thread_arguments:
          extraction_results.append(__keyphrase_extraction_thread(arguments))
      # multi-threaded keyphrase extraction of the documents
      else:
        thread_pool = multiprocessing.Pool(nb_threads)
        extraction_results = thread_pool.map(__keyphrase_extraction_thread,
                                             thread_arguments)

      # formating result
      for document_name, document_keyphrases in extraction_results:
        keyphrases[document_name] = document_keyphrases

      # consumption of the keyphrases extracted from each documents of the
      # corpus
      for keyphrase_consumer in configuration.keyphraseConsumers():
        keyphrase_consumer.consumeKeyphrases(corpus, keyphrases)

