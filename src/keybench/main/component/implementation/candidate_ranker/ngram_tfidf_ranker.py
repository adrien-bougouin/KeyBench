# -*- encoding: utf-8 -*-

import math

from os import path

from keybench.main import core
from keybench.main.component import implementation
from keybench.main.component import interface

class NGramTFIDFRanker(interface.KBCandidateRankerI):
  """N-gram based candidate ranker.

  Attributes:
    n: The maximum size of n-grams. If None, the size of the greatest sentence
      is used.
  """

  def __init__(self,
               name,
               run_name,
               shared,
               lazy_mode,
               debug_mode,
               root_cache,
               n=None):
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
      n: The maximum size of n-grams (defaut=None). If None, the size of the
        greatest sentence is used.
    """

    super(NGRamTFIDFRanker, self).__init__(self,
                                           name,
                                           run_name,
                                           shared,
                                           lazy_mode,
                                           debug_mode,
                                           root_cache)

    self._n = n
    self._idfs = {} # use lazy_loading

  @property
  def n(self):
    return self._n

  def _learnDFs(self, corpus_name):
    """Learns document frequencies (DFs) of n-grams extracted from the train
    documents of a given corpus.

    This method may have unwanted behavior in case of concurrent access. One
    should not make this component a shared component. Also, one should not
    process documents of a same corpus in parallel.

    Args:
      corpus_name: The name of the corpus to use for the learning.
    """

    if corpus_name not in self._dfs:
      component_factory = core.KBBenchmark.singleton().run_configurations[self._run_name]
      corpus_builder = component_factory.corpusBuilders()[corpus_name]
      n = self._n
      self._dfs[corpus_name] = {}
      #-------------------------------------------------------------------------
      if n == None:
        n = 0

        for filepath, corpus_name2, name, language, encoding in corpus.train_document_information:
          document = document_builder.buildDocument(filepath,
                                                    corpus_name2,
                                                    name,
                                                    language,
                                                    encoding)

          for sentence in document.full_text_sentence_tokens:
            n = max(n, len(sentence))
      #-------------------------------------------------------------------------
      n_gram_extractor = implementation.candidate_extractor.NGramExtractor("%s_s_%s"%(self._name,
                                                                                      "n_gram_extractor"),
                                                                           self._run_name,
                                                                           False,
                                                                           self._lazy_mode,
                                                                           self._debug_mode,
                                                                           path.join(self._root_cache,
                                                                                     "n_gram_extractor"),
                                                                           n)
      corpus = corpus_builder.buildCorpus()
      train_document_information = corpus.train_document_information
      nb_documents = float(len(train_document_information))

      # process every train document
      for filepath, corpus_name2, name, language, encoding in train_document_information:
        document = document_builder.buildDocument(filepath,
                                                  corpus_name2,
                                                  name,
                                                  language,
                                                  encoding)
        # extract every n-grams from the document
        candidates = n_gram_extractor.extractCandidates(document)

        # learn DFs
        for candidate in candidates:
          if candidate.identifier not in self._dfs[corpus_name]:
            dfs[corpus_name][candidate.identifier] = 0.0
          dfs[corpus_name][candidate.identifier] += 1.0

  def _candidateRanking(self, document):
    """Ranks the candidates of a given document.

    Args:
      document: The C{KBDocument} from which the candidates must be ranked.

    Returns:
      The ordered C{list} of C{KBTextualUnit} candidates and their C{int} score
      (C{tuple}).
    """

    tf_idfs = []
    component_factory = core.KBBenchmark.singleton().run_configurations[self._run_name]
    candidate_extractor = component_factory.candidateExtractor(document.language)
    candidates = candidate_extractor.extractCandidates(document)

    # lazy loading of the IDFs learnt from the train corpus
    if document.corpus_name not in self._dfs:
      self._learnDFs(document.corpus_name)

    for candidate in candidates:
      tf = candidate.numberOfOccurrences()
      df = 1.0
      if candidate.identifier in self._dfs[document.corpus_name]:
        df += self._idfs[document.corpus_name][candidate.identifier]
      idf = -math.log(1.0 / df, 2)
      tf_idf = tf * idf

      tf_idfs.append((candidate, tf_idf))

    return sorted(tf_idfs,
                  key=lambda (candidate, tfidf): (tfidf, self._candidateIdentifier(candidate)),
                  reverse=True)

