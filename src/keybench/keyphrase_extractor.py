#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from multiprocessing import Pool
from os import listdir
from os import path

##### Multi-processing #########################################################

def keyphrase_extraction_pool_worker(arguments):
  """
  Remote keyphrase extraction. it extracts keyphrases for one file.

  @param  arguments: Sequences of arguments to send to the keyphrase extraction
                     component (filenamen filepath, pre_processor,
                     candidate_extractor, candidate_clusterer, ranker,
                     selector).
  @type   arguments: C{list(list(object))}
  """

  filename, filepath, pp, ce, cc, r, s = arguments

  # pre-processing
  pre_processed_text = pp.pre_process_file(filepath)
  # candidate extraction
  candidates = ce.extract_candidates(filepath, pre_processed_text)
  # candidate clustering
  clusters = cc.cluster_candidates(filepath, pre_processed_text, candidates)
  # ranking
  ranked_candidates = r.rank(filepath, pre_processed_text, candidates, clusters)
  # selection
  extracted_keyphrases = s.select(filepath,
                                  pre_processed_text,
                                  ranked_candidates,
                                  clusters)

  return (filename, extracted_keyphrases)

################################################################################

class KeyphraseExtractor(object):
  """
  Configuration of the keyphrase extraction system. The workflow is composed of
  six steps:
    1. Document pre-processing
    2. Candidate extraction
    3. Candidate clustering
    4. Candidate ranking
    5. Keyphrase selection among the ranked candidates
    6. Keyphrase evaluation
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
                                  extraction.
    @type   candidate_extractor:  C{CandidateExtractorC}
    @param  candidate_clusterer:  The component responsible of the candidate
                                  clustering.
    @type   candidate_clusterer:  C{CandidateClustererC}
    @param  ranker:               The component responsible of the candidate
                                  ranking.
    @type   ranker:               C{RankerC}
    @param  selector:             The component responsible of the keyphrase
                                  selection.
    @type   selector:             C{SelectorC}
    @param  evaluator:            The component responsible of the keyphrase
                                  evaluation.
    @type   evaluator:            C{EvaluatorC}
    """

    super(KeyphraseExtractor, self).__init__()

    self.set_input_directory(input_directory)
    self.set_input_extension(input_extension)
    self.set_pre_processor(pre_processor)
    self.set_candidate_extractor(candidate_extractor)
    self.set_candidate_clusterer(candidate_clusterer)
    self.set_ranker(ranker)
    self.set_selector(selector)
    self.set_evaluator(evaluator)

  def input_directory(self):
    """
    Getter of the directory path where the cached data are stored.

    @return:  The directory path where the cached data are stored.
    @rtype:   C{string}
    """

    return self._input_directory

  def set_input_directory(self, input_directory):
    """
    Setter of the directory path where the cached data are stored.

    @param  input_extension: The new directory path where the cached data are
                             stored.
    @type   input_extension: C{string}
    """

    self._input_directory = input_directory

  def input_extension(self):
    """
    Getter of the extension of the processed files.

    @return:  The extension of the processed files.
    @rtype:   C{string}
    """

    return self._input_extension

  def set_input_extension(self, input_extension):
    """
    Setter of the extension of the processed files.

    @param  input_extension: The new extension of the processed files.
    @type   input_extension: C{string}
    """

    self._input_extension = input_extension

  def pre_processor(self):
    """
    Getter of the component responsible of the document pre-processing.

    @return:  The component responsible of the document pre-processing.
    @rtype:   C{PreProcessorC}
    """

    return self._pre_processor

  def set_pre_processor(self, pre_processor):
    """
    Setter of the component responsible of the document pre-processing.

    @param  pre_processor: The new component responsible of the document
                           pre-processing.
    @type   pre_processor: C{PreProcessorC}
    """

    self._pre_processor = pre_processor

  def candidate_extractor(self):
    """
    Getter of the component responsible of the candidate extraction.

    @return:  The component responsible of the candidate extraction.
    @rtype:   C{CandidateExtractorC}
    """

    return self._candidate_extractor

  def set_candidate_extractor(self, candidate_extractor):
    """
    Setter of the component responsible of the candidate extraction.

    @param  candidate_extractor: The new component responsible of the candidate
                                 extraction.
    @type   candidate_extractor: C{CandidateExtractorC}
    """

    self._candidate_extractor = candidate_extractor

  def candidate_clusterer(self):
    """
    Getter of the component responsible of the candidate clustering.

    @return:  The component responsible of the candidate clustering.
    @rtype:   C{CandidateClustererC}
    """

    return self._candidate_clusterer

  def set_candidate_clusterer(self, candidate_clusterer):
    """
    Setter of the component responsible of the candidate clustering.

    @param  candidate_clusterer: The new component responsible of the candidate
                                 clustering.
    @type   candidate_clusterer: C{CandidateClustererC}
    """

    self._candidate_clusterer = candidate_clusterer

  def ranker(self):
    """
    Getter of the component responsible of the candidate ranking.

    @return:  The component responsible of the candidate ranking.
    @rtype:   C{RankerC}
    """

    return self._ranker

  def set_ranker(self, ranker):
    """
    Setter of the component responsible of the candidate ranking.

    @param  ranker: The new component responsible of the candidate ranking.
    @type   ranker: C{RankerC}
    """

    self._ranker = ranker

  def selector(self):
    """
    Getter of the component responsible of the keyphrase selection.

    @return:  The component responsible of the keyphrase selection.
    @rtype:   C{SelectorC}
    """

    return self._selector

  def set_selector(self, selector):
    """
    Setter of the component responsible of the keyphrase selection.

    @param  selector: The new component responsible of the keyphrase selection.
    @type   selector: C{SelectorC}
    """

    self._selector = selector

  def evaluator(self):
    """
    Getter of the component responsible of the evaluation.

    @return:  The component responsible of the evaluation.
    @rtype:   C{EvaluatorC}
    """

    return self._evaluator

  def set_evaluator(self, evaluator):
    """
    Setter of the component responsible of the evaluation.

    @param  evaluator: The new component responsible of the evaluation.
    @type   evaluator: C{EvaluatorC}
    """

    self._evaluator = evaluator

  def extract_keyphrases(self):
    """
    Execution of the keyphrase extraction workflow.
    """

    ext = self.input_extension()
    working_pool = Pool(8)
    pool_args = []
    pool_results = []
    extracted_keyphrases = {}

    ##### Analysis of all the input files ######################################
    for filename in listdir(self.input_directory()):
      if filename.rfind(ext) >= 0 \
         and len(filename) - filename.rfind(ext) == len(ext):
        filepath = path.join(self.input_directory(), filename)

        pool_args.append((filename,
                          filepath,
                          self.pre_processor(),
                          self.candidate_extractor(),
                          self.candidate_clusterer(),
                          self.ranker(),
                          self.selector()))
    pool_results = working_pool.map(keyphrase_extraction_pool_worker, pool_args)
    #for args in pool_args:
    #  pool_results.append(keyphrase_extraction_pool_worker(args))

    ##### Evaluation of the extracted keyphrases ###############################
    for filename, keyphrases in pool_results:
      extracted_keyphrases[filename] = keyphrases
    self.evaluator().evaluate(extracted_keyphrases.items())

