#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import codecs
from os import path
from datetime import datetime
from keybench import KeyBenchWorker
from keybench import KeyphraseExtractor
from multiprocessing import Queue
from pre_processors import EnglishPreProcessor
from pre_processors import FrenchPreProcessor
from nltk.stem import PorterStemmer
from nltk.stem.snowball import FrenchStemmer
from util import DEFTFileRep
from util import InspecFileRep
from util import PlainTextFileRep
from util import SemEvalFileRep
from util import WikiNewsFileRep
from candidate_extractors import POSFilteredNGramExtractor
from candidate_extractors import LongestNounPhraseExtractor
from keybench.default import FakeClusterer
from candidate_clusterers import StemOverlapHierarchicalClusterer
from candidate_clusterers import LINKAGE_STRATEGY
from keybench.default import TFIDFRanker
from keybench.default.util import inverse_document_frequencies
from rankers import TextRankRanker
from rankers import ORDERING_CRITERIA
from graph_based_ranking import TextRankStrategy
from graph_based_ranking import SingleRankStrategy
from graph_based_ranking import TopicRankStrategy
from graph_based_ranking import CompleteGraphStrategy
from util import term_scoring
from selectors import UnredundantWholeSelector
from selectors import UnredundantTextRankSelector
from evaluators import StandardPRFMEvaluator

################################################################################
# Run creation functions
################################################################################

RUNS_DIR = "results"

# used for the noun candidate extraction
NOUN_TAGS = ["nn", "nns", "nnp", "nnps", "nc", "npp"]
ADJ_TAGS = ["jj", "adj"]
# used for tokens filtering in ****Rank methods
TEXTRANK_TAGS = ["nn", "nns", "nnp", "nnps", "jj", "nc", "npp", "adj"]

def create_pre_processor(corpus_name,
                         language,
                         file_rep,
                         lazy_processing,
                         debug):
  pre_processor = EnglishPreProcessor(corpus_name,
                                      lazy_processing,
                                      RUNS_DIR,
                                      debug,
                                      "/",
                                      file_rep)
  if language == "french":
    pre_processor = FrenchPreProcessor(corpus_name,
                                       lazy_processing,
                                       RUNS_DIR,
                                       debug,
                                       file_rep)

  return pre_processor

def create_tfidf_run(corpus_name,
                     corpus_directory,
                     reference_file,
                     extension,
                     language,
                     file_rep,
                     lazy_processing=True,
                     debug=True):
  pre_processor = create_pre_processor(corpus_name,
                                       language,
                                       file_rep,
                                       lazy_processing,
                                       debug)
  idfs = inverse_document_frequencies(corpus_directory,
                                      extension,
                                      pre_processor)
  scoring_function = term_scoring.normalized
  stemmer = PorterStemmer()
  if language == "french":
    scoring_function = term_scoring.normalized_right_significance
    stemmer = FrenchStemmer()
  ref_stemmer = stemmer
  if corpus_name == "semeval":
    ref_stemmer = None
  candidate_extractor = LongestNounPhraseExtractor("%s_tfidf"%corpus_name,
                                                   lazy_processing,
                                                   RUNS_DIR,
                                                   debug,
                                                   NOUN_TAGS,
                                                   ADJ_TAGS)
  candidate_clusterer = FakeClusterer("%s_tfidf"%corpus_name,
                                      lazy_processing,
                                      RUNS_DIR,
                                      debug)
  candidate_ranker = TFIDFRanker("%s_tfidf"%corpus_name,
                                 lazy_processing,
                                 RUNS_DIR,
                                 debug,
                                 idfs,
                                 scoring_function)
  candidate_selector = UnredundantWholeSelector("%s_tfidf"%corpus_name,
                                                lazy_processing,
                                                RUNS_DIR,
                                                debug,
                                                stemmer)
  evaluator = StandardPRFMEvaluator("%s_tfidf"%corpus_name,
                                    RUNS_DIR,
                                    True,
                                    reference_file,
                                    pre_processor.encoding(),
                                    ref_stemmer,
                                    stemmer)

  return KeyphraseExtractor(corpus_directory,
                            extension,
                            pre_processor,
                            candidate_extractor,
                            candidate_clusterer,
                            candidate_ranker,
                            candidate_selector,
                            evaluator)

def create_textrank_run(corpus_name,
                        corpus_directory,
                        reference_file,
                        extension,
                        language,
                        file_rep,
                        lazy_processing=True,
                        debug=True):
  pre_processor = create_pre_processor(corpus_name,
                                       language,
                                       file_rep,
                                       lazy_processing,
                                       debug)
  scoring_function = term_scoring.sum
  stemmer = PorterStemmer()
  if language == "french":
    stemmer = FrenchStemmer()
  ref_stemmer = stemmer
  if corpus_name == "semeval":
    ref_stemmer = None
  strategy = TextRankStrategy(2,
                              pre_processor.tag_separator(),
                              TEXTRANK_TAGS)
  candidate_extractor = POSFilteredNGramExtractor("%s_textrank"%corpus_name,
                                                  lazy_processing,
                                                  RUNS_DIR,
                                                  debug,
                                                  4,
                                                  NOUN_TAGS,
                                                  ADJ_TAGS)
  candidate_clusterer = FakeClusterer("%s_textrank"%corpus_name,
                                      lazy_processing,
                                      RUNS_DIR,
                                      debug)
  candidate_ranker = TextRankRanker("%s_textrank"%corpus_name,
                                    lazy_processing,
                                    RUNS_DIR,
                                    debug,
                                    strategy,
                                    scoring_function)
  candidate_selector = UnredundantTextRankSelector("%s_textrank"%corpus_name,
                                                   lazy_processing,
                                                   RUNS_DIR,
                                                   debug,
                                                   10,
                                                   stemmer)
  evaluator = StandardPRFMEvaluator("%s_textrank"%corpus_name,
                                    RUNS_DIR,
                                    True,
                                    reference_file,
                                    pre_processor.encoding(),
                                    ref_stemmer,
                                    stemmer)

  return KeyphraseExtractor(corpus_directory,
                            extension,
                            pre_processor,
                            candidate_extractor,
                            candidate_clusterer,
                            candidate_ranker,
                            candidate_selector,
                            evaluator)

def create_singlerank_run(corpus_name,
                          corpus_directory,
                          reference_file,
                          extension,
                          language,
                          file_rep,
                          lazy_processing=True,
                          debug=True):
  pre_processor = create_pre_processor(corpus_name,
                                       language,
                                       file_rep,
                                       lazy_processing,
                                       debug)
  scoring_function = term_scoring.sum
  stemmer = PorterStemmer()
  if language == "french":
    stemmer = FrenchStemmer()
  ref_stemmer = stemmer
  if corpus_name == "semeval":
    ref_stemmer = None
  strategy = SingleRankStrategy(10,
                                pre_processor.tag_separator(),
                                TEXTRANK_TAGS)
  candidate_extractor = LongestNounPhraseExtractor("%s_singlerank"%corpus_name,
                                                   lazy_processing,
                                                   RUNS_DIR,
                                                   debug,
                                                   NOUN_TAGS,
                                                   ADJ_TAGS)
  candidate_clusterer = FakeClusterer("%s_singlerank"%corpus_name,
                                      lazy_processing,
                                      RUNS_DIR,
                                      debug)
  candidate_ranker = TextRankRanker("%s_singlerank"%corpus_name,
                                    lazy_processing,
                                    RUNS_DIR,
                                    debug,
                                    strategy,
                                    scoring_function)
  candidate_selector = UnredundantWholeSelector("%s_singlerank"%corpus_name,
                                                lazy_processing,
                                                RUNS_DIR,
                                                debug,
                                                stemmer)
  evaluator = StandardPRFMEvaluator("%s_singlerank"%corpus_name,
                                    RUNS_DIR,
                                    True,
                                    reference_file,
                                    pre_processor.encoding(),
                                    ref_stemmer,
                                    stemmer)

  return KeyphraseExtractor(corpus_directory,
                            extension,
                            pre_processor,
                            candidate_extractor,
                            candidate_clusterer,
                            candidate_ranker,
                            candidate_selector,
                            evaluator)

def create_singlerank_phrases_run(corpus_name,
                                  corpus_directory,
                                  reference_file,
                                  extension,
                                  language,
                                  file_rep,
                                  lazy_processing=True,
                                  debug=True):
  pre_processor = create_pre_processor(corpus_name,
                                       language,
                                       file_rep,
                                       lazy_processing,
                                       debug)
  scoring_function = term_scoring.sum
  stemmer = PorterStemmer()
  if language == "french":
    stemmer = FrenchStemmer()
  ref_stemmer = stemmer
  if corpus_name == "semeval":
    ref_stemmer = None
  sub_strategy = SingleRankStrategy(10,
                                    pre_processor.tag_separator(),
                                    TEXTRANK_TAGS)
  strategy = TopicRankStrategy(sub_strategy, stemmer)
  candidate_extractor = LongestNounPhraseExtractor("%s_singlerank_phrases"%corpus_name,
                                                   lazy_processing,
                                                   RUNS_DIR,
                                                   debug,
                                                   NOUN_TAGS,
                                                   ADJ_TAGS)
  candidate_clusterer = FakeClusterer("%s_singlerank_phrases"%corpus_name,
                                      lazy_processing,
                                      RUNS_DIR,
                                      debug)
  candidate_ranker = TextRankRanker("%s_singlerank_phrases"%corpus_name,
                                    lazy_processing,
                                    RUNS_DIR,
                                    debug,
                                    strategy,
                                    scoring_function)
  candidate_selector = UnredundantWholeSelector("%s_singlerank_phrases"%corpus_name,
                                                lazy_processing,
                                                RUNS_DIR,
                                                debug,
                                                stemmer)
  evaluator = StandardPRFMEvaluator("%s_singlerank_phrases"%corpus_name,
                                    RUNS_DIR,
                                    True,
                                    reference_file,
                                    pre_processor.encoding(),
                                    ref_stemmer,
                                    stemmer)

  return KeyphraseExtractor(corpus_directory,
                            extension,
                            pre_processor,
                            candidate_extractor,
                            candidate_clusterer,
                            candidate_ranker,
                            candidate_selector,
                            evaluator)

def create_singlerank_topics_run(corpus_name,
                                 corpus_directory,
                                 reference_file,
                                 extension,
                                 language,
                                 file_rep,
                                 lazy_processing=True,
                                 debug=True):
  pre_processor = create_pre_processor(corpus_name,
                                       language,
                                       file_rep,
                                       lazy_processing,
                                       debug)
  scoring_function = term_scoring.sum
  stemmer = PorterStemmer()
  if language == "french":
    stemmer = FrenchStemmer()
  ref_stemmer = stemmer
  if corpus_name == "semeval":
    ref_stemmer = None
  sub_strategy = SingleRankStrategy(10,
                                    pre_processor.tag_separator(),
                                    TEXTRANK_TAGS)
  strategy = TopicRankStrategy(sub_strategy, stemmer)
  candidate_extractor = LongestNounPhraseExtractor("%s_singlerank_topics"%corpus_name,
                                                   lazy_processing,
                                                   RUNS_DIR,
                                                   debug,
                                                   NOUN_TAGS,
                                                   ADJ_TAGS)
  candidate_clusterer = StemOverlapHierarchicalClusterer("%s_singlerank_topics"%corpus_name,
                                                         lazy_processing,
                                                         RUNS_DIR,
                                                         debug,
                                                         LINKAGE_STRATEGY.AVERAGE,
                                                         0.25,
                                                         stemmer)
  candidate_ranker = TextRankRanker("%s_singlerank_topics"%corpus_name,
                                    lazy_processing,
                                    RUNS_DIR,
                                    debug,
                                    strategy,
                                    scoring_function)
  candidate_selector = UnredundantWholeSelector("%s__singlerank_topics"%corpus_name,
                                                lazy_processing,
                                                RUNS_DIR,
                                                debug,
                                                stemmer)
  evaluator = StandardPRFMEvaluator("%s_singlerank_topics"%corpus_name,
                                    RUNS_DIR,
                                    True,
                                    reference_file,
                                    pre_processor.encoding(),
                                    ref_stemmer,
                                    stemmer)

  return KeyphraseExtractor(corpus_directory,
                            extension,
                            pre_processor,
                            candidate_extractor,
                            candidate_clusterer,
                            candidate_ranker,
                            candidate_selector,
                            evaluator)

def create_singlerank_complete_run(corpus_name,
                                   corpus_directory,
                                   reference_file,
                                   extension,
                                   language,
                                   file_rep,
                                   lazy_processing=True,
                                   debug=True):
  pre_processor = create_pre_processor(corpus_name,
                                       language,
                                       file_rep,
                                       lazy_processing,
                                       debug)
  scoring_function = term_scoring.sum
  stemmer = PorterStemmer()
  if language == "french":
    stemmer = FrenchStemmer()
  ref_stemmer = stemmer
  if corpus_name == "semeval":
    ref_stemmer = None
  strategy = CompleteGraphStrategy(None,
                                   pre_processor.tag_separator(),
                                   TEXTRANK_TAGS)
  candidate_extractor = LongestNounPhraseExtractor("%s_singlerank_complete"%corpus_name,
                                                   lazy_processing,
                                                   RUNS_DIR,
                                                   debug,
                                                   NOUN_TAGS,
                                                   ADJ_TAGS)
  candidate_clusterer = FakeClusterer("%s_singlerank_complete"%corpus_name,
                                      lazy_processing,
                                      RUNS_DIR,
                                      debug)
  candidate_ranker = TextRankRanker("%s_singlerank_complete"%corpus_name,
                                    lazy_processing,
                                    RUNS_DIR,
                                    debug,
                                    strategy,
                                    scoring_function)
  candidate_selector = UnredundantWholeSelector("%s_singlerank_complete"%corpus_name,
                                                lazy_processing,
                                                RUNS_DIR,
                                                debug,
                                                stemmer)
  evaluator = StandardPRFMEvaluator("%s_singlerank_complete"%corpus_name,
                                    RUNS_DIR,
                                    True,
                                    reference_file,
                                    pre_processor.encoding(),
                                    ref_stemmer,
                                    stemmer)

  return KeyphraseExtractor(corpus_directory,
                            extension,
                            pre_processor,
                            candidate_extractor,
                            candidate_clusterer,
                            candidate_ranker,
                            candidate_selector,
                            evaluator)

def create_topicrank_run(corpus_name,
                         corpus_directory,
                         reference_file,
                         extension,
                         language,
                         file_rep,
                         ordering_criteria,
                         lazy_processing=True,
                         debug=True):
  pre_processor = create_pre_processor(corpus_name,
                                       language,
                                       file_rep,
                                       lazy_processing,
                                       debug)
  scoring_function = term_scoring.sum
  stemmer = PorterStemmer()
  if language == "french":
    stemmer = FrenchStemmer()
  ref_stemmer = stemmer
  if corpus_name == "semeval":
    ref_stemmer = None
  sub_strategy = CompleteGraphStrategy(None,
                                       pre_processor.tag_separator(),
                                       TEXTRANK_TAGS)
  strategy = TopicRankStrategy(sub_strategy, stemmer)
  criteria_name = "position"
  if ordering_criteria == ORDERING_CRITERIA.FREQUENCY:
    criteria_name = "frequency"
  else:
    if ordering_criteria == ORDERING_CRITERIA.CENTROID:
      criteria_name = "centroid"
  candidate_extractor = LongestNounPhraseExtractor("%s_topicrank_%s"%(corpus_name, criteria_name),
                                                   lazy_processing,
                                                   RUNS_DIR,
                                                   debug,
                                                   NOUN_TAGS,
                                                   ADJ_TAGS)
  candidate_clusterer = StemOverlapHierarchicalClusterer("%s_topicrank_%s"%(corpus_name, criteria_name),
                                                         lazy_processing,
                                                         RUNS_DIR,
                                                         debug,
                                                         LINKAGE_STRATEGY.AVERAGE,
                                                         0.25,
                                                         stemmer)
  candidate_ranker = TextRankRanker("%s_topicrank_%s"%(corpus_name, criteria_name),
                                    lazy_processing,
                                    RUNS_DIR,
                                    debug,
                                    strategy,
                                    scoring_function,
                                    ordering_criteria)
  candidate_selector = UnredundantWholeSelector("%s_topicrank_%s"%(corpus_name, criteria_name),
                                                lazy_processing,
                                                RUNS_DIR,
                                                debug,
                                                stemmer)
  evaluator = StandardPRFMEvaluator("%s_topicrank_%s"%(corpus_name, criteria_name),
                                    RUNS_DIR,
                                    True,
                                    reference_file,
                                    pre_processor.encoding(),
                                    ref_stemmer,
                                    stemmer)

  return KeyphraseExtractor(corpus_directory,
                            extension,
                            pre_processor,
                            candidate_extractor,
                            candidate_clusterer,
                            candidate_ranker,
                            candidate_selector,
                            evaluator)

################################################################################
# Main
################################################################################

CORPORA_DIR = path.join(path.dirname(sys.argv[0]), "..", "res", "corpora")

def main(argv):
  if len(argv) == 2 or len(argv) == 4:
    runs = [
      # documents directory,
      # documents extension,
      # pre-processor,
      # candidate extractor,
      # candidate clusterer,
      # ranker,
      # selector,
      # evaluator
    ]

    ##### RUNS CREATION ########################################################

    parameters = []

    if len(argv) == 2:
      # TODO create runs
      corpora = []

      if argv[1] == "all":
        corpora.append("inspec")
        corpora.append("semeval")
        corpora.append("wikinews")
        corpora.append("deft")
      else:
        corpora.append(argv[1])

      for corpus in corpora:
        corpus_directory = None
        reference_file = None
        extension = None
        language = None
        file_rep = None

        if corpus == "inspec":
          corpus_directory = path.join(CORPORA_DIR, "inspec", "documents")
          reference_file = path.join(CORPORA_DIR, "inspec", "ref")
          extension = ".abstr"
          language = "english"
          file_rep = InspecFileRep()
        else:
          if corpus == "semeval":
            corpus_directory = path.join(CORPORA_DIR,
                                         "semeval_2010",
                                         "documents")
            reference_file = path.join(CORPORA_DIR,
                                       "semeval_2010",
                                       "ref_modified_stem_combined")
            extension = ".txt"
            language = "english"
            file_rep = SemEvalFileRep()
          else:
            if corpus == "wikinews":
              corpus_directory = path.join(CORPORA_DIR,
                                           "wikinews_2012",
                                           "documents")
              reference_file = path.join(CORPORA_DIR,
                                         "wikinews_2012",
                                         "ref")
              extension = ".html"
              language = "french"
              file_rep = WikiNewsFileRep()
            else:
              if corpus == "deft":
                corpus_directory = path.join(CORPORA_DIR,
                                             "deft_2012",
                                             "test_t2",
                                             "documents")
                reference_file = path.join(CORPORA_DIR,
                                           "deft_2012",
                                           "test_t2",
                                           "ref_test_t2")
                extension = ".xml"
                language = "french"
                file_rep = DEFTFileRep()
              else:
                print "Wrong corpus name..."
                break

        parameters.append((corpus,
                           corpus_directory,
                           reference_file,
                           extension,
                           language,
                           file_rep))
    else:
      parameters.append(("test_%s"%datetime.today().ctime(),
                         argv[1],
                         argv[2],
                         ".txt",
                         argv[3],
                         PlainTextFileRep()))

    for params in parameters:
      corpus, corpus_directory, reference_file, extension, language, file_rep = params

      runs.append(create_tfidf_run(corpus,
                                   corpus_directory,
                                   reference_file,
                                   extension,
                                   language,
                                   file_rep))
      runs.append(create_textrank_run(corpus,
                                      corpus_directory,
                                      reference_file,
                                      extension,
                                      language,
                                      file_rep))
      runs.append(create_singlerank_run(corpus,
                                        corpus_directory,
                                        reference_file,
                                        extension,
                                        language,
                                        file_rep))
      runs.append(create_singlerank_phrases_run(corpus,
                                                corpus_directory,
                                                reference_file,
                                                extension,
                                                language,
                                                file_rep))
      runs.append(create_singlerank_topics_run(corpus,
                                               corpus_directory,
                                               reference_file,
                                               extension,
                                               language,
                                               file_rep))
      runs.append(create_singlerank_complete_run(corpus,
                                                 corpus_directory,
                                                 reference_file,
                                                 extension,
                                                 language,
                                                 file_rep))
      runs.append(create_topicrank_run(corpus,
                                       corpus_directory,
                                       reference_file,
                                       extension,
                                       language,
                                       file_rep,
                                       ORDERING_CRITERIA.POSITION))
      runs.append(create_topicrank_run(corpus,
                                       corpus_directory,
                                       reference_file,
                                       extension,
                                       language,
                                       file_rep,
                                       ORDERING_CRITERIA.FREQUENCY))
      runs.append(create_topicrank_run(corpus,
                                       corpus_directory,
                                       reference_file,
                                       extension,
                                       language,
                                       file_rep,
                                       ORDERING_CRITERIA.CENTROID))

    ##### Runs' execution ######################################################

    print "EXECUTION OF %d RUNS..."%len(runs)
    queue = Queue()
    for run in runs:
      queue.put(run)
      KeyBenchWorker(queue).start()
  else:
    print "Usage:"
    print "  %s default_corpus"%argv[0]
    print "or\n  %s corpus_directory reference_file language"%argv[0]
    print "\n  default_corpus:\n    all, inspec, semeval, wikinews or deft"
    print "  corpus_directory:\n    the path to a directory containing plain text files that must be analysed"
    print "  reference_file:\n    the file containing the corpus reference keyphrases ([line] <filename\tkeyphrase1:keyphrase2;...;keyphraseN>)"
    print "  language:\n    english or french"

################################################################################
if __name__ == "__main__":
  main(sys.argv)
################################################################################

