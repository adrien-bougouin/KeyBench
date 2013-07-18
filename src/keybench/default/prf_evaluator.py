#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from keybench.evaluator import EvaluatorC

class PRFEvaluator(EvaluatorC):
  """
  Component performing keyphrases evaluation. It provides the three classical
  measures (precision, recall, f1-measure).
  """

  def __init__(self,
               name,
               lazy_directory,
               reference_file,
               encoding,
               ref_stemmer=None,
               res_stemmer=None):
    """
    Constructor of the component.

    @param  name:           The name of the evaluator.
    @type   name:           C{string}
    @param  lazy_directory: The directory used for caching.
    @type   lazy_directory: C{string}
    @param  reference_file: The path of the file containing all the reference
                            keyphrases of the analysed files.
    @type   reference_file: C{string}
    @param  encoding:       The encoding of the reference files.
    @type   encoding:       C{string}
    @param  stemmer:        The object used to stem words. If it is not defined,
                            there will be no stemming during the evaluation.
    @type   stemmer:        C{nltk.stem.api.StemmerI}
    """

    super(PRFEvaluator, self).__init__(name,
                                       lazy_directory,
                                       reference_file,
                                       encoding)

    self._ref_stemmer = ref_stemmer
    self._res_stemmer = res_stemmer

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

    # stemming if needed
    ref_k = []
    res_k = []
    if self._ref_stemmer:
      ref_k = self.stem_keyphrases(ref_keyphrases, self._ref_stemmer)
    else:
      ref_k = ref_keyphrases
    if self._res_stemmer:
      res_k = self.stem_keyphrases(res_keyphrases, self._res_stemmer)
    else:
      res_k = res_keyphrases

    nb_ref, nb_res, nb_match = self.comparison(ref_k, res_k)
    precision = 0.0
    recall = 0.0
    f1_measure = 0.0

    if nb_res != 0.0:
      precision = float(nb_match) / float(nb_res)
    if nb_ref != 0.0:
      recall = float(nb_match) / float(nb_ref)
    if not (precision + recall) == 0.0:
      f1_measure = (2.0 * precision * recall) / (precision + recall)

    return [precision, recall, f1_measure]

  def measure_labels(self):
    """
    Gives the labels for the evaluation measures. The labels must be in the same
    order than the measures given by C{single_evaluation()}.

    @return:  The labels of the given measures (returned by
              C{single_evaluation()}).
    @rtype:   C{list of string}
    """

    return ["Precision", "Recall", "F1-measure"]

  def comparison(self, ref_keyphrases, res_keyphrases):
    """
    Compares two sets of (stemmed if needed) keyphrases.

    @param    ref_keyphrases: The set of reference keyphrases.
    @type     ref_keyphrases: C{list of string}
    @param    res_keyphrases: The set of extracted keyphrases.
    @type     res_keyphrases: C{list of string}

    @return:  A tuple containing the number of assignated keyphrases, the number
              of extracted keyphrases and the number of correctly assignated
              keyphrases.
    @rtype:   C{tuple of int}
    """

    nb_ref = float(len(ref_keyphrases))
    nb_res = float(len(res_keyphrases))
    nb_match = float(len(set(ref_keyphrases) & set(res_keyphrases)))

    return (nb_ref, nb_res, nb_match)

  def stem_keyphrases(self, keyphrases, stemmer):
    """
    """

    stemmed_keyphrases = []

    for keyphrase in keyphrases:
      stemmed_keyphrases.append(self.stem_sentence(keyphrase, stemmer))

    return stemmed_keyphrases

  def stem_sentence(self, sentence, stemmer):
    """
    Stems the words of a sentence.

    @param    sentence: The sentence to stemmed.
    @type     sentence: C{string}
    TODO stemmer
    TODO stemmer

    @return:  The stemmed sentence.
    @rtype:   C{string}
    """

    previous_stemmed_sentence = sentence
    stemmed_sentence = ""

    for w in sentence.split():
      if stemmed_sentence != "":
        stemmed_sentence += " "
      stemmed_sentence += stemmer.stem(w)

    return stemmed_sentence

