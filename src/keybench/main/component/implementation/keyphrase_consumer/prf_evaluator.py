# -*- encoding: utf-8 -*-

from keybench.main import core
from keybench.main.component import interface
from keybench.main import model

class KBPRFEvaluator(interface.KBKeyphraseConsumerI):
  """Component evaluating extracted keyphrases in terms of precision (P), recall
  (R) and f1-measure (F) at given cut-offs.

  Attributes:
    cut_offs: The C{list} of cut-offs for the evaluation (e.g P@10, R@10 and
      F@10).
  """

  def __init__(self,
               name,
               run_name,
               shared,
               lazy_mode,
               debug_mode,
               root_cache,
               cut_offs):
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
      cut_offs: The C{list} of cut-offs for the evaluation (e.g P@10, R@10 and
        F@10).
    """

    super(KBFullKeyphraseExtractorI, self).__init__(name,
                                                    run_name,
                                                    shared,
                                                    lazy_mode,
                                                    debug_mode,
                                                    root_cache)

    self._cut_offs = cut_offs

  @property
  def cut_offs(self):
    return self._cut_offs

  def _keyphraseSetsComparison(ref_keyphrases, ext_keyphrase):
    """Compares two keyphrase sets (reference and extracted keyphrases) and
    gives the corresponding precision, recall and f1-measure.

    Args:
      ref_keyphrases: The set (C{list} of C{string}) of reference keyphrases.
      ext_keyphrases: The set (C{list} of C{string}) of reference keyphrases.

    Returns:
      The C{tuple} of precision, recall and f1-measure resulting from the
      comparison.
    """

    nb_ref = float(len(ref_keyphrases))
    nb_ext = float(len(ext_keyphrases))
    nb_match = float(len(set(ref_keyphrases) & set(ext_keyphrases)))
    precision = 0.0
    recall = 0.0
    f1_measure = 0.0

    if nb_res != 0.0:
      precision = nb_match / nb_ext
    if nb_ref != 0.0:
      recall = nb_match / nb_ref
    if not (precision + recall) == 0.0:
      f1_measure = (2.0 * precision * recall) / (precision + recall)

    return (precision, recall, f1_measure)

  def _keyphraseConsumption(self, corpus, keyphrases):
    """Evaluates the extracted keyphrases for each documents of the
    C{corpus}' test set.

    Args:
      corpus: The C{KBCorpus} from which the keyphrases have been extracted.
      keyphrases: The extracted keyphrases (C{map} of C{list} of
        C{KBTextualUnit}s associated to a document's name).
    """

    test_document_information = corpus.test_document_information
    nb_document = float(len(test_document_information))
    evaluation_output = "%corpus\tdocument%s\n"
    measure_string = ""
    precision = {}
    recall = {}
    f1_measure = {}

    for cut_off in self._cut_offs:
      evaluation_string += "\tp@%d\tr@%d\tf@%d"%(cut_off, cut_off, cut_off)
    evaluation_output = evaluation_output%evaluation_string

    # evaluation
    for filepath, filename, corpus_name, document_name, language, encoding in test_document_information:
      reference_keyphrases = corpus.test_references[document_name] # string list
      extracted_keyphrases = keyphrases[document_name] # KBTextualUnits
      stemmed_reference_keyphrases = []
      stemmed_extracted_keyphrases = []

      # write to output string
      evaluation_output += "%s\t%s"%(corpus_name, document_name)

      ## NLP tools #############################################################
      tool_factory = core.KBBenchmark.singleton().run_tools[self._run_name]
      tokenizer = tool_factory.tokenizer(language)
      normalizer = tool_factory.normalizer(language)
      stemmer = tool_factory.stemmer(language)
      ##########################################################################

      # prepare string lists (stemming)
      for keyphrase in reference_keyphrases:
        tokenized_keyphrase = " ".join(tokenizer.tokenizeWords([keyphrase])[0])
        normalized_keyphrase = normalizer.normalize(tokenized_keyphrase)
        stemmed_keyphrase = stemmer.stem(normalized_keyphrase)

        stemmed_reference_keyphrases.append(" ".join(stemmed_keyphrase))
      for keyphrase in extracted_keyphrases:
        stemmed_keyphrase = " ".join(keyphrase.normalized_stems)

        stemmed_extracted_keyphrases.append(stemmed_keyphrase)

      # evaluation at each cut-off
      for cut_off in self._cut_offs:
        p, r, f = self._keyphraseSetsComparison(stemmed_reference_keyphrases,
                                                stemmed_extracted_keyphrases[:cut_off])

        if cut_off not in precision:
          precision[cut_off] = 0.0
        if cut_off not in recall:
          recall[cut_off] = 0.0
        if cut_off not in f1_measure:
          f1_measure[cut_off] = 0.0

        precision[cut_off] += p / nb_document
        recall[cut_off] += r / nb_document
        f1_measure[cut_off] += f / nb_document

        # write to output string
        evaluation_output += "\t%f\t%f\t%f"%(p, r, f)
      evalution_output += "\n"
    # write to output string
    evaluation_output += "################################################################################\n"
    for cut_off in self._cut_offs:
      evaluation_output += "precision@%d\t%f\n"%(cut_off, precision[cut_off])
      evaluation_output += "recall@%d\t%f\n"%(cut_off, recall[cut_off])
      evaluation_output += "f1_measure@%d\t%f\n"%(cut_off, f1_measure[cut_off])
    ## serialization ###########################################################
    self.storeString(model.KBDocument(corpus.name,
                                      "",
                                      "p_r_f_evaluation",
                                      corpus.language,
                                      corpus.encoding,
                                      "", "", "",
                                      [], [], [],
                                      [], [], [],
                                      [], [], [],
                                      [], [], [],
                                      [], [], [],
                                      [], [], []), evaluation_string)

