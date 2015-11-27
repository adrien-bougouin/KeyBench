#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
from keybench.default import PRFEvaluator

################################################################################
# StandardPRFEvaluator
# StandardPRFMEvaluator

################################################################################

class StandardPRFEvaluator(PRFEvaluator):
  """
  Component performing keyphrases evaluation. It provides the three classical
  measures (precision, recall, f1-measure).
  """

  def __init__(self,
               name,
               lazy_directory,
               debug,
               reference_file,
               encoding,
               ref_stemmer=None,
               res_stemmer=None):
    """
    Constructor of the component.

    @param  name:           The name of the component.
    @type   name:           C{string}
    @param  is_lazy:        True if the component must load previous data, False
                            if data must be computed tought they have already
                            been computed.
    @type   is_lazy:        C{bool}
    @param  lazy_directory: The directory used to store previously computed
                            data.
    @type   lazy_directory: C{string}
    @param  debug:          True if the component is in debug mode, else False.
                            When the component is in debug mode, it will output
                            each step of its processing.
    @type   debug:          C{bool}
    @param  encoding:       The encoding of the reference files.
    @type   encoding:       C{string}
    @param  stemmer:        The object used to stem words. If it is not defined,
                            there will be no stemming during the evaluation.
    @type   stemmer:        C{nltk.stem.api.StemmerI}
    """

    super(StandardPRFEvaluator, self).__init__(name,
                                               lazy_directory,
                                               debug,
                                               reference_file,
                                               encoding,
                                               ref_stemmer,
                                               res_stemmer)

  def parse_reference_file(self, reference_file, encoding):
    """
    Extracts the reference keyphrases from a given file.

    @param    reference_file: The path of the file containing all the reference
                              keyphrases of the analysed files.
    @type     reference_file: C{string}
    @param    encoding:       The encoding of the reference files.
    @type     encoding:       C{string}

    @return:  The files associated with their reference keyphrases.
    @rtype:   C{dic(string, list(string))}
    """

    ref_file = codecs.open(reference_file, "r", encoding)
    lines = ref_file.read().split("\n")
    ref_dic = {}

    ref_file.close()

    for line in lines:
      if not line == "":
        filename_and_keyphrases = line.split("\t")
        filename = filename_and_keyphrases[0]
        keyphrases = filename_and_keyphrases[1].lower().split(";")

        # strip keyphrases
        for i, k in enumerate(keyphrases):
          keyphrases[i] = k.strip()

        ref_dic[filename] = keyphrases

    return ref_dic

################################################################################

class StandardPRFMEvaluator(StandardPRFEvaluator):
  """
  Component performing keyphrases evaluation. It provides the four classical
  measures over 4 different number of extracted keyphrases (precision@5,
  recall@5, f1-measure@5, map@5, precision@10, recal@10, f1-measure@10, map@10,
  precision@15, recall@15, f1-measure@15, map@15, precision, recall,
  f1-measure, map).
  """

  def __init__(self,
               name,
               lazy_directory,
               debug,
               reference_file,
               encoding,
               ref_stemmer=None,
               res_stemmer=None,
               tokenize_function=None):
    """
    Constructor of the component.

    @param  name:           The name of the component.
    @type   name:           C{string}
    @param  is_lazy:        True if the component must load previous data, False
                            if data must be computed tought they have already
                            been computed.
    @type   is_lazy:        C{bool}
    @param  lazy_directory: The directory used to store previously computed
                            data.
    @type   lazy_directory: C{string}
    @param  debug:          True if the component is in debug mode, else False.
                            When the component is in debug mode, it will output
                            each step of its processing.
    @type   debug:          C{bool}
    @param  encoding:       The encoding of the reference files.
    @type   encoding:       C{string}
    @param  stemmer:        The object used to stem words. If it is not defined,
                            there will be no stemming during the evaluation.
    @type   stemmer:        C{nltk.stem.api.StemmerI}
    TODO
    TODO
    """

    super(StandardPRFMEvaluator, self).__init__(name,
                                                lazy_directory,
                                                debug,
                                                reference_file,
                                                encoding,
                                                ref_stemmer,
                                                res_stemmer)

    self._tokenize_function = tokenize_function

  def tokenize_keyphrases(self, keyphrases):
    """
    """

    tokenized_keyphrases = []

    if self._tokenize_function != None:
      for keyphrase in keyphrases:
        tokenized_keyphrases.append(self._tokenize_function(keyphrase))
    else:
      tokenized_keyphrases = keyphrases

    return tokenized_keyphrases

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

    # keyphrase tokenization
    ref_k = self.tokenize_keyphrases(ref_keyphrases)

    # stemming if needed
    if self._ref_stemmer:
      ref_k = self.stem_keyphrases(ref_k, self._ref_stemmer)
    else:
      ref_k = ref_keyphrases
    if self._res_stemmer:
      res_k = self.stem_keyphrases(res_keyphrases, self._res_stemmer)
    else:
      res_k = res_keyphrases

    ref_length = len(ref_k)
    res_length = len(res_k)
    nb_matches = []
    precisions = []
    recalls = []
    f1_measures = []
    average_precisions = []
    measures = []

    for i in range(res_length):
      nb_ref, nb_res, nb_match = self.comparison(ref_k,
                                                 res_k[:i + 1])
      p = 0.0
      r = 0.0
      f = 0.0
      a = 0.0

      if nb_res != 0.0:
        p = float(nb_match) / float(nb_res)
      if nb_ref != 0.0:
        r = float(nb_match) / float(nb_ref)
      if not (p + r) == 0.0:
        f = (2.0 * p * r) / (p + r)
      if i > 0:
        a = average_precisions[i - 1]
        if nb_match > nb_matches[i - 1]:
          a += (p / float(ref_length))
      else:
        if nb_match > 0:
          a = (p / float(ref_length))

      nb_matches.append(nb_match)
      precisions.append(p)
      recalls.append(r)
      f1_measures.append(f)
      average_precisions.append(a)

    for size in [5, 10, 15, len(res_k)]:
      if size > 0 and size <= len(precisions):
        precision = precisions[size - 1]
        recall = recalls[size - 1]
        f1_measure = f1_measures[size - 1]
        average_precision = average_precisions[size - 1]

        measures.append(precision)
        measures.append(recall)
        measures.append(f1_measure)
        measures.append(average_precision)
      else:
        if len(precisions) > 0:
          measures.append(precisions[-1])
          measures.append(recalls[-1])
          measures.append(f1_measures[-1])
          measures.append(average_precisions[-1])
        else:
          measures.append(0.0)
          measures.append(0.0)
          measures.append(0.0)
          measures.append(0.0)

    return measures

  def measure_labels(self):
    """
    Gives the labels for the evaluation measures. The labels must be in the same
    order than the measures given by C{single_evaluation()}.

    @return:  The labels of the given measures (returned by
              C{single_evaluation()}).
    @rtype:   C{list of string}
    """

    return [
      "Precision@5",
      "Recall@5",
      "F1-measure@5",
      "MAP@5",
      "Precision@10",
      "Recall@10",
      "F1-measure@10",
      "MAP@10",
      "Precision@15",
      "Recall@15",
      "F1-measure@15",
      "MAP@15",
      "Precision",
      "Recall",
      "F1-measure",
      "MAP"
    ]

