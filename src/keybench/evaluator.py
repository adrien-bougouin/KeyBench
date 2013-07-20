#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from benchmark_component import BenchmarkComponent
from exceptions import NotImplementedError
from multiprocessing import Pool
from os import path

def single_evaluation_pool_worker(arguments):
  """
  """

  evaluator, filename, keyphrase_list = arguments

  return (filename,
          evaluator.single_evaluation(evaluator._reference_keyphrases[filename],
                                      keyphrase_list))

class EvaluatorC(BenchmarkComponent):
  """
  Component responsible of the keyphrases evaluation, compared to reference
  keyphrases.
  """

  def __init__(self, name, lazy_directory, reference_file, encoding):
    """
    TODO

    @param  reference_file: The path of the file containing all the reference
                            keyphrases of the analysed files.
    @type   reference_file: C{string}
    @param  encoding:       The encoding of the reference files.
    @type   encoding:       C{string}
    """

    super(EvaluatorC, self).__init__(name,
                                     False,
                                     path.join(lazy_directory, "evaluations"))

    self._reference_keyphrases = self.parse_reference_file(reference_file,
                                                           encoding)

  def evaluate(self, keyphrases):
    """
    Evaluate keyphrases extracted from various files (files and keyphrases are
    associated).

    @param    keyphrases: The files and their associated keyphrases.
    @type     keyphrases: C{list of (string, list of string)}
    """

    working_pool = Pool()
    pool_args = []
    all_measures = []
    average_measures = {}

    for label in self.measure_labels():
      average_measures[label] = 0.0

    super(EvaluatorC, self).log("Evaluating extracted keyphrases...")

    # evaluate the keyphrases
    for filename, keyphrase_list in keyphrases:
      pool_args.append((self, filename, keyphrase_list))
    all_measures = working_pool.map(single_evaluation_pool_worker, pool_args)
    #for args in pool_args:
    #  all_measures.append(single_evaluation_pool_worker(args))

    # compute the average of each measure
    nb_value = len(keyphrases)
    for filename, measures in all_measures:
      for i, measure in enumerate(measures):
        label = self.measure_labels()[i]

        if not average_measures.has_key(label):
          average_measures[label] = 0.0
        average_measures[label] += measure / float(nb_value)

    # save all the measures in one file
    super(EvaluatorC, self).log("Saving the readable list of evaluations...")
    string_rep = ""
    for f, m in all_measures:
      string_rep += "%s: %s\n"%(f, str(m))
    for label in self.measure_labels():
      string_rep += "%s: %f\n"%(label, average_measures[label])
    string_rep = "filename: %s\n%s"%(self.measure_labels(), string_rep)
    super(EvaluatorC, self).store_string("results.evl", string_rep)

  def parse_reference_file(self, reference_file, encoding):
    """
    Extracts the reference keyphrases from a given file.

    @param    reference_file: The path of the file containing all the reference
                              keyphrases of the analysed files.
    @type     reference_file: C{string}
    @param    encoding:       The encoding of the reference files.
    @type     encoding:       C{string}

    @return:  The files associated with their reference keyphrases.
    @rtype:   C{dict: string -> list of string}
    """

    raise NotImplementedError()

  def single_evaluation(self, ref_keyphrases, res_keyphrases):
    """
    Compares two lists of keyphrases and gives comparison mesures.

    @param    ref_keyphrases: The list of keyphrases use as gold standard
                              keyphrases.
    @type     ref_keyphrases: C{list of string}
    @param    res_keyphrases: The list of extracted keyphrases.
    @type     res_keyphrases: C{list of string}

    @return:  One or more measures which results of the comparison of the two
              lists of keyphrases.
    @rtype:   C{list of float}
    """

    raise NotImplementedError()

  def measure_labels(self):
    """
    Gives the labels for the evaluation measures. The labels must be in the same
    order than the measures given by C{single_evaluation()}.

    @return:  The labels of the given measures (returned by
              C{single_evaluation()}).
    @rtype:   C{list of string}
    """

    raise NotImplementedError()

