# -*- encoding: utf-8 -*-

from keybench.main import core
from keybench.main.component import interface

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

    # TODO for every test document of the corpus
    for filepath, filename, corpus_name, document_name, language, encoding in corpus.test_document_information:
      reference_keyphrases = corpus.test_references[document_name] # TODO string list (must be stemmed or lemmatized)
      extracted_keyphrases = keyphrases[document_name] # TODO KBTextualUnits (only need to request stemmed or lemmatized version)
      # TODO prepare string lists (stemmed, lemmatized, etc.)
      # TODO for each cut-off
      for cut_off in self._cut_off:
        # TODO compute P, R, and F
        # self._keyphraseComparison(TODO, TODO)
        pass

