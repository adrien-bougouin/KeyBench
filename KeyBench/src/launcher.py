#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import argparse
import sys
import codecs
from os import path
from keybench import KeyBenchWorker
from keybench import KeyphraseExtractor
from keybench import set_nb_documents_per_run
from multiprocessing import Queue
from pre_processors import EnglishPreProcessor
from pre_processors import FrenchPreProcessor
from nltk.stem import PorterStemmer
from nltk.stem.snowball import FrenchStemmer
from util import PlainTextFileRep
from candidate_extractors import PatternMatchingExtractor
from candidate_clusterers import StemOverlapHierarchicalClusterer
from candidate_clusterers import LINKAGE_STRATEGY
from rankers import TextRankRanker
from rankers import ORDERING_CRITERIA
from graph_based_ranking import TopicRankStrategy
from graph_based_ranking import CompleteGraphStrategy
from selectors import UnredundantWholeSelector
from evaluators import StandardPRFMEvaluator
from topicrank_pp import TopicRankPPRanker
from topicrank_pp import create_domain_graph
from topicrank_pp import add_topicrankpp_graph

################################################################################
# Run creation functions
################################################################################

# used for the noun candidate extraction
NOUN_TAGS = ["nn", "nns", "nnp", "nnps", "nc", "npp"]
ADJ_TAGS = ["jj", "adj"]
TAGGED_WORD_PATTERN = "([^ ]+\\/%s( |$))"
LNP_TAGS = "(jj|nnps|nnp|nns|nn|adj|npp|nc)"
LNP_PATTERNS = ["%s+"%(TAGGED_WORD_PATTERN%LNP_TAGS)]

def create_pre_processor(corpus_name,
                         runs_dir,
                         language,
                         file_rep,
                         lazy_processing,
                         debug):
  pre_processor = EnglishPreProcessor(corpus_name,
                                      lazy_processing,
                                      runs_dir,
                                      debug,
                                      "/",
                                      file_rep)
  if language == "french":
    pre_processor = FrenchPreProcessor(corpus_name,
                                       lazy_processing,
                                       runs_dir,
                                       debug,
                                       file_rep)

  return pre_processor

def create_topicrank_run(corpus_name,
                         runs_dir,
                         corpus_directory,
                         reference_filepath,
                         extension,
                         language,
                         file_rep,
                         ordering_criteria,
                         evaluation=True,
                         lazy_processing=True,
                         debug=True):
  pre_processor = create_pre_processor(corpus_name,
                                       runs_dir,
                                       language,
                                       file_rep,
                                       lazy_processing,
                                       debug)
  stemmer = PorterStemmer()
  if language == "french":
    stemmer = FrenchStemmer()
  ref_stemmer = stemmer
  sub_strategy = CompleteGraphStrategy(None,
                                       pre_processor.tag_separator(),
                                       list(set(NOUN_TAGS) | set(ADJ_TAGS)))
  strategy = TopicRankStrategy(sub_strategy, stemmer)
  candidate_extractor = PatternMatchingExtractor("%s_topicrank"%(corpus_name),
                                                 lazy_processing,
                                                 runs_dir,
                                                 debug,
                                                 LNP_PATTERNS)
  candidate_clusterer = StemOverlapHierarchicalClusterer("%s_topicrank"%(corpus_name),
                                                         lazy_processing,
                                                         runs_dir,
                                                         debug,
                                                         LINKAGE_STRATEGY.AVERAGE,
                                                         0.25,
                                                         stemmer)
  candidate_ranker = TextRankRanker("%s_topicrank"%(corpus_name),
                                    lazy_processing,
                                    runs_dir,
                                    debug,
                                    strategy,
                                    None,
                                    ordering_criteria)
  candidate_selector = UnredundantWholeSelector("%s_topicrank"%(corpus_name),
                                                lazy_processing,
                                                runs_dir,
                                                debug,
                                                stemmer)
  evaluator = None
  if evaluation == True:
    evaluator = StandardPRFMEvaluator("%s_topicrank"%(corpus_name),
                                      runs_dir,
                                      True,
                                      reference_filepath,
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

def create_topiccorank_run(corpus_name,
                           runs_dir,
                           corpus_directory,
                           training_reference_filepath,
                           reference_filepath,
                           extension,
                           language,
                           file_rep,
                           evaluation=True,
                           lazy_processing=True,
                           debug=True):
  pre_processor = create_pre_processor(corpus_name,
                                       runs_dir,
                                       language,
                                       file_rep,
                                       lazy_processing,
                                       debug)
  stemmer = PorterStemmer()
  if language == "french":
    stemmer = FrenchStemmer()
  ref_stemmer = stemmer
  candidate_extractor = PatternMatchingExtractor("%s_topiccorank"%(corpus_name),
                                                 lazy_processing,
                                                 runs_dir,
                                                 debug,
                                                 LNP_PATTERNS)
  candidate_clusterer = StemOverlapHierarchicalClusterer("%s_topiccorank"%(corpus_name),
                                                         lazy_processing,
                                                         runs_dir,
                                                         debug,
                                                         LINKAGE_STRATEGY.AVERAGE,
                                                         0.25,
                                                         stemmer)
  #-----------------------------------------------------------------------------
  add_topicrankpp_graph(corpus_name,
                        create_domain_graph(training_reference_filepath, pre_processor.encoding()),
                        stemmer)
  #-----------------------------------------------------------------------------
  candidate_ranker = TopicRankPPRanker("%s_topiccorank"%(corpus_name),
                                       lazy_processing,
                                       runs_dir,
                                       debug,
                                       corpus_name,
                                       stemmer,
                                       lambda_k=0.5,
                                       lambda_t=0.1)
  candidate_selector = UnredundantWholeSelector("%s_topiccorank"%(corpus_name),
                                                lazy_processing,
                                                runs_dir,
                                                debug,
                                                stemmer)
  evaluator = None
  if evaluation == True:
    evaluator = StandardPRFMEvaluator("%s_topiccorank"%(corpus_name),
                                      runs_dir,
                                      True,
                                      reference_filepath,
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

def main(argv):
  # retrieve arguments
  arg_parser = argparse.ArgumentParser(
    usage="%s [options] method corpus language"%(sys.argv[0])
  )

  arg_parser.add_argument("-n",
                          "--run-name",
                          dest="run_name",
                          default=None,
                          help="name of the run (for identification within the output directory)")
  arg_parser.add_argument("-r",
                          "--reference",
                          default="",
                          dest="reference_filepath",
                          help="path to the file containing the references (for evaluation only)")
  arg_parser.add_argument("-t",
                          "--training-reference",
                          default=None,
                          dest="training_reference_filepath",
                          help="path to the file containing the training references (for TopicCoRank only)")
  arg_parser.add_argument("-o",
                          "--output-dir",
                          default="results",
                          dest="output_dir",
                          help="path to the directory where processings must be stored (default=results)")
  arg_parser.add_argument("-p",
                          "--processus-number",
                          default=8,
                          dest="processus_number",
                          help="number of documents to process simultaneously")
  arg_parser.set_defaults(must_strip=False)
  arg_parser.add_argument("method",
                          help="method to use for keyphrase identification (TopicRank or TopicCoRank)")
  arg_parser.add_argument("corpus",
                          help="path to the .txt files to process")
  arg_parser.add_argument("language",
                          help="language of the corpus files (french or english)")

  if len(argv) < 4:
    arg_parser.print_help()
  else:
    # accept positional arguments starting with '-'
    arguments = arg_parser.parse_args(args=sys.argv[1:-3] + ["--"] + sys.argv[-3:])
    #---------------------------------------------------------------------------
    corpus_name = arguments.run_name
    ref_filepath = arguments.reference_filepath
    training_ref_filepath = arguments.training_reference_filepath
    runs_dir = arguments.output_dir
    set_nb_documents_per_run(int(arguments.processus_number))
    method = arguments.method.lower()
    corpus_dir = arguments.corpus
    language = arguments.language.lower()
    evaluation = (ref_filepath != "")

    if corpus_name == None:
      tail, head = path.split(corpus_dir)
      while head == "":
        tail, head = path.split(tail)
      corpus_name = head.replace(" ", "_").lower()

    ##### RUN CREATION #########################################################
    run = None
    if(method == "topicrank"):
      run = create_topicrank_run(
        corpus_name,
        runs_dir,
        corpus_dir,
        ref_filepath,
        ".txt",
        language,
        PlainTextFileRep(),
        ORDERING_CRITERIA.POSITION,
        evaluation
      )
    elif method == "topiccorank":
      if training_ref_filepath != None:
        run = create_topiccorank_run(
          corpus_name,
          runs_dir,
          corpus_dir,
          training_ref_filepath,
          ref_filepath,
          ".txt",
          language,
          PlainTextFileRep(),
          evaluation
        )
      else:
        print "Missing training reference keyphrases for TopicCoRank training..."
    else:
      print "Unknown method: %s..."%(method)

    ##### Runs' execution ######################################################
    if run != None:
      queue = Queue()
      queue.put(run)
      KeyBenchWorker(queue).start()

################################################################################
if __name__ == "__main__":
  main(sys.argv)
################################################################################

