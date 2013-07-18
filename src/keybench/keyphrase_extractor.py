#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from multiprocessing import Pool
from os import listdir
from os import path

def keyphrase_extraction_pool_worker(arguments):
  filename, filepath, pp, ce, cc, r, s = arguments

  # pre-processing
  pre_processed_text = pp.pre_process_file(filepath)
  # candidate extraction
  candidates = ce.extract_candidates(filepath, pre_processed_text)
  clusters = cc.cluster_candidates(filepath, pre_processed_text, candidates)
  # ranking
  ranked_candidates = r.rank(filepath, pre_processed_text, candidates, clusters)
  # selection
  extracted_keyphrases = s.select(filepath,
                                  pre_processed_text,
                                  ranked_candidates,
                                  clusters)

  return (filename, extracted_keyphrases)

class KeyphraseExtractor(object):
  """
  Configuration of the keyphrase extraction system. The workflow is composed of
  five steps:
    1. Document pre-processing
    2. Candidate terms extraction
    3. Candidate terms weighting
    4. Keyphrases selection among the weighted words/terms
    5. Keyphrases evaluation
  """
  
  def __init__(self,
               input_directory,
               input_extension,
               pre_processor,
               candidate_extractor,
               candidate_clusterer,
               ranker,
               selector,
               evaluator):
    """
    Constructor of the keyphrase extraction system.

    @param  input_directory:      The path of the directory containing the files
                                  to analyse.
    @type   input_directory:      C{string}
    @param  input_extension:      The extension of the files to analyse
                                  (example: '.xml').
    @type   input_extension:      C{string}
    @param  pre_processor:        The component responsible of the documents
                                  pre-processing.
    @type   pre_processor:        C{PreProcessorC}
    @param  candidate_extractor:  The component responsible of the candidate
                                  term extraction.
    @type   candidate_extractor:  C{TermExtractorC}
    TODO clusterer
    TODO clusterer
    @param  ranker:               The component responsible of the candidate
                                  terms ranking.
    @type   ranker:               C{RankerC}
    @param  selector:             The component responsible of the keyphrase
                                  selection.
    @type   selector:             C{SelectorC}
    @param  evaluator:            The component responsible of the keyphrase
                                  evaluation.
    @type   evaluator:            C{EvaluatorC}
    """

    super(KeyphraseExtractor, self).__init__()

    self._input_directory = input_directory
    self._input_extension = input_extension
    self._pre_processor = pre_processor
    self._candidate_extractor = candidate_extractor
    self._candidate_clusterer = candidate_clusterer
    self._ranker = ranker
    self._selector = selector
    self._evaluator = evaluator

  def extract_keyphrases(self):
    """
    Execution of the keyphrase extraction workflow.
    """

    ext = self._input_extension
    working_pool = Pool()
    pool_args = []
    pool_results = []
    extracted_keyphrases = {}

    ##### Analysis of all the input files ######################################
    for filename in listdir(self._input_directory):
      if filename.rfind(ext) >= 0 \
         and len(filename) - filename.rfind(ext) == len(ext):
        filepath = path.join(self._input_directory, filename)

        pool_args.append((filename,
                          filepath,
                          self._pre_processor,
                          self._candidate_extractor,
                          self._candidate_clusterer,
                          self._ranker,
                          self._selector))
    #pool_results = working_pool.map(keyphrase_extraction_pool_worker, pool_args)
    for args in pool_args:
      pool_results.append(keyphrase_extraction_pool_worker(args))

    ##### Evaluation of the extracted keyphrases ###############################
    for filename, keyphrases in pool_results:
      extracted_keyphrases[filename] = keyphrases
    self._evaluator.evaluate(extracted_keyphrases.items())

