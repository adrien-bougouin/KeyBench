#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import codecs
from candidate_extractors import POSSequenceExtractor
from candidate_extractors import FromTerminologyExtractor
from candidate_extractors import NPChunkExtractor
from candidate_extractors import STFilteredNGramExtractor
from candidate_extractors import PatternMatchingExtractor
from candidate_extractors import CLARIT96Extractor
from candidate_extractors import CLARIT96_LEXATOM_TAG
from candidate_extractors import train_clarit
from candidate_clusterers import StemOverlapHierarchicalClusterer
from candidate_clusterers import LINKAGE_STRATEGY
from evaluators import StandardPRFMEvaluator
from keybench import KeyphraseExtractor
from keybench import KeyBenchWorker
from keybench.default import FakeClusterer
from keybench.default.util import document_frequencies
from keybench.default.util import n_to_m_grams
from keybench.default import TFIDFRanker
from multiprocessing import Queue
from pre_processors import FrenchPreProcessor
from pre_processors import EnglishPreProcessor
from rankers import TextRankRanker
from rankers import KEARanker
from rankers import ORDERING_CRITERIA
from rankers import train_kea
from selectors import UnredundantTextRankSelector
from selectors import UnredundantTopKSelector
from selectors import UnredundantWholeSelector
from graph_based_ranking import TextRankStrategy
from graph_based_ranking import SingleRankStrategy
from graph_based_ranking import TopicRankStrategy
from graph_based_ranking import CompleteGraphStrategy
from util import DEFTFileRep
from util import InspecFileRep
from util import PlainTextFileRep
from util import SemEvalFileRep
from util import DUCFileRep
from util import term_scoring
from util import WikiNewsFileRep
from util import bonsai_tokenization
from nltk.stem import PorterStemmer
from nltk.stem.snowball import FrenchStemmer
from nltk.tokenize.treebank import TreebankWordTokenizer
from os import makedirs
from os import path
from os import listdir

################################################################################

RUNS_DIR = "results" # directory used to save informations

##### corpora information ######################################################

CORPORA_DIR = path.join(path.dirname(sys.argv[0]), "..", "res", "corpora")

DEFT_CORPUS_DIR = path.join(CORPORA_DIR, "deft_2012", "test_t2")
DEFT_CORPUS_DOCS = path.join(DEFT_CORPUS_DIR, "documents")
DEFT_CORPUS_REFS = path.join(DEFT_CORPUS_DIR, "ref_test_t2")
DEFT_CORPUS_TERM_SUITE_TERMINOLOGY = path.join(DEFT_CORPUS_DIR, "term_suite_terminology_t2")
DEFT_CORPUS_ACABIT_TERMINOLOGY = path.join(DEFT_CORPUS_DIR, "acabit_terminology_t2")
DEFT_CORPUS_TRAIN_DOCS = path.join(DEFT_CORPUS_DIR, "train")
DEFT_CORPUS_DOCS_EXTENSION = ".xml"

WIKINEWS_CORPUS_DIR = path.join(CORPORA_DIR, "wikinews_2012")
WIKINEWS_CORPUS_DOCS = path.join(WIKINEWS_CORPUS_DIR, "documents")
WIKINEWS_CORPUS_REFS = path.join(WIKINEWS_CORPUS_DIR, "ref")
WIKINEWS_CORPUS_DOCS_EXTENSION = ".html"

SEMEVAL_CORPUS_DIR = path.join(CORPORA_DIR, "semeval_2010")
SEMEVAL_CORPUS_DOCS = path.join(SEMEVAL_CORPUS_DIR, "documents")
SEMEVAL_CORPUS_REFS = path.join(SEMEVAL_CORPUS_DIR,
                                "ref_modified_stem_combined")
SEMEVAL_CORPUS_TERM_SUITE_TERMINOLOGY = path.join(SEMEVAL_CORPUS_DIR, "term_suite_terminology")
SEMEVAL_CORPUS_ACABIT_TERMINOLOGY = path.join(SEMEVAL_CORPUS_DIR, "acabit_terminology")
SEMEVAL_CORPUS_TRAIN_DOCS = path.join(SEMEVAL_CORPUS_DIR, "train")
SEMEVAL_CORPUS_DOCS_EXTENSION = ".txt"

DUC_CORPUS_DIR = path.join(CORPORA_DIR, "duc_2001")
DUC_CORPUS_DOCS = path.join(DUC_CORPUS_DIR, "documents")
DUC_CORPUS_REFS = path.join(DUC_CORPUS_DIR, "ref")
DUC_CORPUS_TERM_SUITE_TERMINOLOGY = path.join(DUC_CORPUS_DIR, "term_suite_terminology")
DUC_CORPUS_ACABIT_TERMINOLOGY = path.join(DUC_CORPUS_DIR, "acabit_terminology")
DUC_CORPUS_TRAIN_DOCS = path.join(DUC_CORPUS_DIR, "train")
DUC_CORPUS_DOCS_EXTENSION = ".xml"

INSPEC_CORPUS_DIR = path.join(CORPORA_DIR, "inspec")
INSPEC_CORPUS_DOCS = path.join(INSPEC_CORPUS_DIR, "documents")
INSPEC_CORPUS_REFS = path.join(INSPEC_CORPUS_DIR, "ref")
INSPEC_CORPUS_TRAIN_DOCS = path.join(INSPEC_CORPUS_DIR, "train")
INSPEC_CORPUS_DOCS_EXTENSION = ".abstr"

FRENCH_LA = "fr"
FRENCH_STOP_WORDS_FILEPATH = path.join(CORPORA_DIR, "french_unine_stop_words")
ENGLISH_LA = "en"
ENGLISH_STOP_WORDS_FILEPATH = path.join(CORPORA_DIR, "english_unine_stop_words")

##### execution configurations #################################################

LAZY_PRE_PROCESSING = True
LAZY_CANDIDATE_EXTRACTION = True
LAZY_CANDIDATE_CLUSTERING = True
LAZY_RANKING = False
LAZY_SELECTION = False

##### runs possibilities #######################################################

# corpora names
DEFT_CO = "deft"
WIKINEWS_CO = "wikinews"
SEMEVAL_CO = "semeval"
DUC_CO = "duc"
INSPEC_CO = "inspec"

# method names
TFIDF_ME = "tfidf"
TEXTRANK_ME = "textrank"
SINGLERANK_ME = "singlerank"
COMPLETERANK_ME = "completerank"
TOPICRANK_S_ME = "topicrank_s"
TOPICRANK_ME = "topicrank"
KEA_ME = "kea"

# candidate names
ST_FILTERED_NGRAM_CA = "st_filtered_ngram"
NP_CHUNK_CA = "np_chunk"
LONGEST_NOUN_PHRASE_CA = "longest_noun_phrase"
BEST_PATTERN_CA = "best_pattern"
CLARIT96_CA = "clarit96"
TERM_SUITE_TERMINOLOGY_CA = "term_suite"
ACABIT_TERMINOLOGY_CA = "acabit"

# clustering names
NO_CLUSTER_CC = "no_cluster"
HIERARCHICAL_CLUSTER_CC = "hierarchical"

# scoring names
SUM_SC = "sum"
WEIGHT_SC = "weight"

# selection names
WHOLE_SE = "whole"
TOP_K_SE = "top_k"
TEXTRANK_SE = "textrank"

##### runs #####################################################################

CORPORA_RU = [DUC_CO, SEMEVAL_CO, DEFT_CO]
METHODS_RU = [TFIDF_ME]
NUMBERS_RU = [10]
LENGTHS_RU = [0]
CANDIDATES_RU = [ACABIT_TERMINOLOGY_CA]
CLUSTERING_RU = [NO_CLUSTER_CC]
SCORINGS_RU = [WEIGHT_SC]
SELECTIONS_RU = [WHOLE_SE]

# used for the noun phrases extraction
NOUN_TAGS = ["nn", "nns", "nnp", "nnps", "nc", "npp"]
ADJ_TAGS = ["jj", "adj"]
# used for tokens filtering in ****Rank methods
TEXTRANK_TAGS = ["nn", "nns", "nnp", "nnps", "jj", "nc", "npp", "adj"]
# rules for NP chunking
english_np_chunk_rules = "{(<nnps|nnp>+)|(<jj>+<nns|nn>)|(<nns|nn>+)}"
french_np_chunk_rules = "{(<npp>+)|(<adj>?<nc><adj>+)|(<adj><nc>)|(<nc>+)}"
# rules for pattern matching
tagged_word_pattern = "([^ ]+\\/%s( |$))" # WARNING space or end line delimiter is in the pattern
english_lnp_tags = "(jj|nnps|nnp|nns|nn)"
french_lnp_tags = "(adj|npp|nc)"
english_lnp_patterns = ["%s+"%(tagged_word_pattern%english_lnp_tags)]
french_lnp_patterns = ["%s+"%(tagged_word_pattern%french_lnp_tags)]
# rules for CLARIT'96 subcompounding
english_clarit_np_patterns = english_lnp_patterns
french_clarit_np_patterns = french_lnp_patterns
english_clarit_lexatom_patterns = [
  "%s%s"%(tagged_word_pattern%("(nnps|nnp|nns|nn|%s)"%CLARIT96_LEXATOM_TAG),
          tagged_word_pattern%("(nnps|nnp|nns|nn|%s)"%CLARIT96_LEXATOM_TAG)),
  "%s%s"%(tagged_word_pattern%"(jjr|jjs|jj)",
          tagged_word_pattern%("(nnps|nnp|nns|nn|%s)"%CLARIT96_LEXATOM_TAG))
]
french_clarit_lexatom_patterns = [
  "%s%s"%(tagged_word_pattern%("(nc|npp|%s)"%CLARIT96_LEXATOM_TAG),
          tagged_word_pattern%"(adj)")
]
english_clarit_special_patterns = [
  "%s%s"%(tagged_word_pattern%"(rbr|rbs|rb)",
          tagged_word_pattern%"(rbr|rbs|rb|jjr|jjs|jj|vbg|vbn)")
]
french_clarit_special_patterns = [
  "%s%s"%(tagged_word_pattern%"(advwh|adv|adjwh|adj|vpp|vpr)",
          tagged_word_pattern%"(advwh|adv|adjwh|adj|vpp|vpr)")
]
english_clarit_impossible_patterns = [
  "%s%s"%(tagged_word_pattern%"(nnps|nnp|nns|nn|vpp|vpr)",
          tagged_word_pattern%"(rbr|rbs|rb|jjr|jjs|jj)"),
  "%s%s"%(tagged_word_pattern%"(jjr|jjs|jj)",
          tagged_word_pattern%"(jjr|jjs|jj)")
]
french_clarit_impossible_patterns = [
  "%s%s"%(tagged_word_pattern%"(advwh|adv)",
          tagged_word_pattern%"(npp|nc)"),
  "%s%s"%(tagged_word_pattern%"(adjwh|adj)",
          tagged_word_pattern%"(advwh|adv|adjwh|adj)")]

################################################################################

def extract_stop_words(stop_words_filepath):
  st_file = codecs.open(stop_words_filepath, "r", "utf-8")
  stop_words = st_file.read().split("\n")

  st_file.close()

  for i, st in enumerate(stop_words):
    stop_words[i] = st.replace("\r", "")

  stop_words.append(",")
  stop_words.append(".")
  stop_words.append("!")
  stop_words.append("?")

  return stop_words

def english_tokenization(term):
  word_tokenizer = TreebankWordTokenizer()
  tokenized_term = ""

  for word in word_tokenizer.tokenize(term):
    if tokenized_term != "":
      tokenized_term += " "
    tokenized_term += word

  return tokenized_term

def learn_tag_sequences(train_docs,
                        ext,
                        pre_processor,
                        tokenize):
  tag_sequences = {}

# FIXME not needed when candidates are extracted
#  for filename in listdir(train_docs):
#    if filename.rfind(ext) >= 0 \
#       and len(filename) - filename.rfind(ext) == len(ext):
#      filepath = path.join(train_docs, filename)
#      keyphrase_path = path.join(train_docs, filename.replace(ext, ".key"))
#      pre_processed_file = pre_processor.pre_process_file(filepath)
#      sentences = pre_processed_file.full_text()
#      keyphrase_file = codecs.open(keyphrase_path,
#                                   "r",
#                                   pre_processed_file.encoding())
#      keyphrases = keyphrase_file.read().split(";")
#      tokenized_keyphrases = {}
#
#      # tokenize keyphrases
#      for keyphrase in keyphrases:
#        tokenized_keyphrases[tokenize(keyphrase.lower().strip())] = True
#
#      # parse n-grams
#      for sentence in sentences:
#        sentence = sentence.strip()
#
#        for tagged_candidate in n_to_m_grams(sentence.split(), 1, len(sentence.split())):
#          untagged_candidate = ""
#          tag_sequence = ""
#
#          for wt in tagged_candidate.split():
#            if untagged_candidate != "":
#              untagged_candidate += " "
#            untagged_candidate += wt.rsplit(pre_processed_file.tag_separator(),
#                                            1)[0]
#
#            if tag_sequence != "":
#              tag_sequence += " "
#            tag_sequence += wt.rsplit(pre_processed_file.tag_separator(), 1)[1]
#
#          # add tag sequence if it is a keyphrase
#          if untagged_candidate in tokenized_keyphrases:
#            tag_sequences[tag_sequence] = True
#
#      keyphrase_file.close()

  return tag_sequences

################################################################################
# Main
################################################################################

def main(argv):
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

  ##### runs' creation #########################################################

  # lazy loading of idfs
  for corpus in CORPORA_RU:
    for method in METHODS_RU:
      for number in NUMBERS_RU:
        for length in LENGTHS_RU:
          docs = None
          ext = None
          term_suite_terms = None
          acabit_terms = None
          train_docs = None
          refs = None
          stop_words = None
          stemmer = None
          ref_stemmer = None
          tokenize = None
          pre_processor = None
          language = None
          dfs = None
          nb_documents = None
          np_chunk_rules = None
          lnp_patterns = None
          clarit_np_patterns = None
          clarit_lexatom_patterns = None
          clarit_special_patterns = None
          clarit_impossible_patterns = None

          if corpus == DEFT_CO:
            docs = DEFT_CORPUS_DOCS
            ext = DEFT_CORPUS_DOCS_EXTENSION
            term_suite_terms = DEFT_CORPUS_TERM_SUITE_TERMINOLOGY
            acabit_terms = DEFT_CORPUS_ACABIT_TERMINOLOGY
            train_docs = DEFT_CORPUS_TRAIN_DOCS
            refs = DEFT_CORPUS_REFS
            stop_words = extract_stop_words(FRENCH_STOP_WORDS_FILEPATH)
            stemmer = FrenchStemmer()
            ref_stemmer = stemmer
            tokenize = bonsai_tokenization
            pre_processor = FrenchPreProcessor("%s_pre_processor"%corpus,
                                               LAZY_PRE_PROCESSING,
                                               RUNS_DIR,
                                               True,
                                               DEFTFileRep())
            language = FRENCH_LA
            np_chunk_rules = french_np_chunk_rules
            lnp_patterns = french_lnp_patterns
            clarit_np_patterns = french_clarit_np_patterns
            clarit_lexatom_patterns = french_clarit_lexatom_patterns
            clarit_special_patterns = french_clarit_special_patterns
            clarit_impossible_patterns = french_clarit_impossible_patterns
          else:
            if corpus == WIKINEWS_CO:
              docs = WIKINEWS_CORPUS_DOCS
              train_docs = docs # FIXME
              ext = WIKINEWS_CORPUS_DOCS_EXTENSION
              refs = WIKINEWS_CORPUS_REFS
              stop_words = extract_stop_words(FRENCH_STOP_WORDS_FILEPATH)
              stemmer = FrenchStemmer()
              ref_stemmer = stemmer
              tokenize = bonsai_tokenization
              pre_processor = FrenchPreProcessor("%s_pre_processor"%corpus,
                                                 LAZY_PRE_PROCESSING,
                                                 RUNS_DIR,
                                                 True,
                                                 WikiNewsFileRep())
              language = FRENCH_LA
              np_chunk_rules = french_np_chunk_rules
              lnp_patterns = french_lnp_patterns
              clarit_np_patterns = french_clarit_np_patterns
              clarit_lexatom_patterns = french_clarit_lexatom_patterns
              clarit_special_patterns = french_clarit_special_patterns
              clarit_impossible_patterns = french_clarit_impossible_patterns
            else:
              if corpus == SEMEVAL_CO:
                docs = SEMEVAL_CORPUS_DOCS
                ext = SEMEVAL_CORPUS_DOCS_EXTENSION
                term_suite_terms = SEMEVAL_CORPUS_TERM_SUITE_TERMINOLOGY
                acabit_terms = SEMEVAL_CORPUS_ACABIT_TERMINOLOGY
                train_docs = SEMEVAL_CORPUS_TRAIN_DOCS
                refs = SEMEVAL_CORPUS_REFS
                stop_words = extract_stop_words(ENGLISH_STOP_WORDS_FILEPATH)
                stemmer = PorterStemmer()
                ref_stemmer = None
                tokenize = english_tokenization
                pre_processor = EnglishPreProcessor("%s_pre_processor"%corpus,
                                                    LAZY_PRE_PROCESSING,
                                                    RUNS_DIR,
                                                    True,
                                                    "/",
                                                    SemEvalFileRep())
                language = ENGLISH_LA
                np_chunk_rules = english_np_chunk_rules
                lnp_patterns = english_lnp_patterns
                clarit_np_patterns = english_clarit_np_patterns
                clarit_lexatom_patterns = english_clarit_lexatom_patterns
                clarit_special_patterns = english_clarit_special_patterns
                clarit_impossible_patterns = english_clarit_impossible_patterns
              else:
                if corpus == DUC_CO:
                  docs = DUC_CORPUS_DOCS
                  ext = DUC_CORPUS_DOCS_EXTENSION
                  term_suite_terms = DUC_CORPUS_TERM_SUITE_TERMINOLOGY
                  acabit_terms = DUC_CORPUS_ACABIT_TERMINOLOGY
                  train_docs = DUC_CORPUS_TRAIN_DOCS
                  refs = DUC_CORPUS_REFS
                  stop_words = extract_stop_words(ENGLISH_STOP_WORDS_FILEPATH)
                  stemmer = PorterStemmer()
                  ref_stemmer = PorterStemmer()
                  tokenize = english_tokenization
                  pre_processor = EnglishPreProcessor("%s_pre_processor"%corpus,
                                                      LAZY_PRE_PROCESSING,
                                                      RUNS_DIR,
                                                      True,
                                                      "/",
                                                      DUCFileRep())
                  language = ENGLISH_LA
                  np_chunk_rules = english_np_chunk_rules
                  lnp_patterns = english_lnp_patterns
                  clarit_np_patterns = english_clarit_np_patterns
                  clarit_lexatom_patterns = english_clarit_lexatom_patterns
                  clarit_special_patterns = english_clarit_special_patterns
                  clarit_impossible_patterns = english_clarit_impossible_patterns
                else:
                  if corpus == INSPEC_CO:
                    docs = INSPEC_CORPUS_DOCS
                    ext = INSPEC_CORPUS_DOCS_EXTENSION
                    train_docs = INSPEC_CORPUS_TRAIN_DOCS
                    refs = INSPEC_CORPUS_REFS
                    stop_words = extract_stop_words(ENGLISH_STOP_WORDS_FILEPATH)
                    stemmer = PorterStemmer()
                    ref_stemmer = stemmer
                    tokenize = english_tokenization
                    pre_processor = EnglishPreProcessor("%s_pre_processor"%corpus,
                                                        LAZY_PRE_PROCESSING,
                                                        RUNS_DIR,
                                                        True,
                                                        "/",
                                                        InspecFileRep())
                    language = ENGLISH_LA
                    np_chunk_rules = english_np_chunk_rules
                    lnp_patterns = english_lnp_patterns
                    clarit_np_patterns = english_clarit_np_patterns
                    clarit_lexatom_patterns = english_clarit_lexatom_patterns
                    clarit_special_patterns = english_clarit_special_patterns
                    clarit_impossible_patterns = english_clarit_impossible_patterns

          for candidate in CANDIDATES_RU:
            for cluster in CLUSTERING_RU:
              for scoring in SCORINGS_RU:
                for selection in SELECTIONS_RU:
                  run_name = "%s_%s_%d_%d_%s_%s_%s_%s"%(corpus,
                                                        method,
                                                        number,
                                                        length,
                                                        candidate,
                                                        cluster,
                                                        scoring,
                                                        selection)
                  c = None # candidate_extractor
                  cc = None # candidate_clusterer
                  r = None # ranker
                  s = None # selector
                  e = None # evaluator

                  ##### candidate extractor ####################################
                  if candidate == ST_FILTERED_NGRAM_CA:
                      c = STFilteredNGramExtractor(run_name,
                                                   LAZY_CANDIDATE_EXTRACTION,
                                                   RUNS_DIR,
                                                   True,
                                                   length,
                                                   stop_words)
                  else:
                    if candidate == LONGEST_NOUN_PHRASE_CA:
                      c = PatternMatchingExtractor(run_name,
                                                   LAZY_CANDIDATE_EXTRACTION,
                                                   RUNS_DIR,
                                                   True,
                                                   lnp_patterns)
                    else:
                      if candidate == BEST_PATTERN_CA:
                        c = POSSequenceExtractor(run_name,
                                                 LAZY_CANDIDATE_EXTRACTION,
                                                 RUNS_DIR,
                                                 True,
                                                 learn_tag_sequences(train_docs,
                                                                     ext,
                                                                     pre_processor,
                                                                     tokenize))
                      else:
                        if candidate == NP_CHUNK_CA:
                          c = NPChunkExtractor(run_name,
                                               LAZY_CANDIDATE_EXTRACTION,
                                               RUNS_DIR,
                                               True,
                                               np_chunk_rules)
                        else:
                          if candidate == CLARIT96_CA:
                            c = CLARIT96Extractor(run_name,
                                                  LAZY_CANDIDATE_EXTRACTION,
                                                  RUNS_DIR,
                                                  True,
                                                  clarit_np_patterns,
                                                  clarit_lexatom_patterns,
                                                  clarit_special_patterns,
                                                  clarit_impossible_patterns,
                                                  train_clarit(train_docs,
                                                               ext,
                                                               pre_processor,
                                                               PatternMatchingExtractor(run_name + "_pre",
                                                                                        LAZY_CANDIDATE_EXTRACTION,
                                                                                        RUNS_DIR,
                                                                                        True,
                                                                                        clarit_np_patterns)))
                          else:
                            if candidate == TERM_SUITE_TERMINOLOGY_CA:
                              c = FromTerminologyExtractor(run_name,
                                                           LAZY_CANDIDATE_EXTRACTION,
                                                           RUNS_DIR,
                                                           True,
                                                           term_suite_terms,
                                                           "utf-8", # FIXME
                                                           tokenize)
                            else:
                              if candidate == ACABIT_TERMINOLOGY_CA:
                                c = FromTerminologyExtractor(run_name,
                                                             LAZY_CANDIDATE_EXTRACTION,
                                                             RUNS_DIR,
                                                             True,
                                                             acabit_terms,
                                                             "utf-8", # FIXME
                                                             tokenize)
                  ##### candidate clusterer ####################################
                  if cluster == NO_CLUSTER_CC:
                    cc = FakeClusterer(run_name,
                                       LAZY_CANDIDATE_CLUSTERING,
                                       RUNS_DIR,
                                       True)
                  else:
                    if cluster == HIERARCHICAL_CLUSTER_CC:
                      cc = StemOverlapHierarchicalClusterer(run_name,
                                                            LAZY_CANDIDATE_CLUSTERING,
                                                            RUNS_DIR,
                                                            True,
                                                            LINKAGE_STRATEGY.AVERAGE,
                                                            0.25,
                                                            stemmer)
                  ##### scoring ################################################
                  scoring_function = None
                  if scoring == SUM_SC:
                    scoring_function = term_scoring.sum
                  else:
                    if scoring == WEIGHT_SC:
                      if language == FRENCH_LA:
                        scoring_function = term_scoring.normalized_right_significance
                      else:
                        if language == ENGLISH_LA:
                            scoring_function = term_scoring.normalized
                  ##### ranker #################################################
                  if method == TFIDF_ME:
                    ##### DF computation ###################################
                    nb_documents, dfs = document_frequencies(train_docs,
                                                             ext,
                                                             # no candidate
                                                             # means word
                                                             # TF-IDF
                                                             pre_processor,
                                                             c)
                    ############################################################
                    r = TFIDFRanker(run_name,
                                    LAZY_RANKING,
                                    RUNS_DIR,
                                    True,
                                    # no scoring function means n-gram TF-IDF
                                    dfs,
                                    nb_documents)#,
                                    #scoring_function)
                  else:
                    if method == TEXTRANK_ME \
                       or method == SINGLERANK_ME \
                       or method == COMPLETERANK_ME \
                       or method == TOPICRANK_S_ME \
                       or method == TOPICRANK_ME:
                      strategy = None

                      if method == TEXTRANK_ME:
                        strategy = TextRankStrategy(2,
                                                    pre_processor.tag_separator(),
                                                    TEXTRANK_TAGS)
                      else:
                        if method == SINGLERANK_ME:
                          strategy = SingleRankStrategy(10,
                                                        pre_processor.tag_separator(),
                                                        TEXTRANK_TAGS)
                        else:
                          if method == COMPLETERANK_ME:
                            strategy = CompleteGraphStrategy(None,
                                                             pre_processor.tag_separator(),
                                                             TEXTRANK_TAGS)
                          else:
                            if method == TOPICRANK_S_ME \
                               or method == TOPICRANK_ME:
                              if method == TOPICRANK_S_ME:
                                sub_strategy = SingleRankStrategy(10,
                                                                  pre_processor.tag_separator(),
                                                                  TEXTRANK_TAGS)
                              if method == TOPICRANK_ME:
                                sub_strategy = CompleteGraphStrategy(None,
                                                                     pre_processor.tag_separator(),
                                                                     TEXTRANK_TAGS)
                              strategy = TopicRankStrategy(sub_strategy,
                                                           stemmer)
                      r =  TextRankRanker(run_name,
                                          LAZY_RANKING,
                                          RUNS_DIR,
                                          True,
                                          strategy,
                                          scoring_function)
                    else:
                      if method == KEA_ME:
                        kea_train_dir = path.join(RUNS_DIR, "kea_models")
                        if not path.exists(kea_train_dir):
                          makedirs(kea_train_dir)
                        # TF-IDFs are computed based on n-gram counts
                        train_nb_documents, train_dfs = document_frequencies(train_docs,
                                                                             ext,
                                                                             pre_processor,
                                                                             c)
                        train_tfidf_ranker = TFIDFRanker(run_name,
                                                         LAZY_RANKING,
                                                         RUNS_DIR,
                                                         True,
                                                         train_dfs,
                                                         train_nb_documents)
                        classifier = train_kea(path.join(kea_train_dir, "kea_model_%s"%run_name),
                                               train_docs,
                                               ext,
                                               ".key",
                                               tokenize,
                                               stemmer,
                                               pre_processor,
                                               c,
                                               cc,
                                               train_tfidf_ranker)
                        r = KEARanker(run_name,
                                      LAZY_RANKING,
                                      RUNS_DIR,
                                      True,
                                      classifier,
                                      train_tfidf_ranker)
                  ##### selector ###############################################
                  if selection == WHOLE_SE:
                    s = UnredundantWholeSelector(run_name,
                                                 LAZY_SELECTION,
                                                 RUNS_DIR,
                                                 True,
                                                 stemmer)
                  else:
                    if selection == TOP_K_SE:
                      s = UnredundantTopKSelector(run_name,
                                                  LAZY_SELECTION,
                                                  RUNS_DIR,
                                                  True,
                                                  number,
                                                  stemmer)
                    else:
                      if selection == TEXTRANK_SE:
                        s = UnredundantTextRankSelector(run_name,
                                                        LAZY_SELECTION,
                                                        RUNS_DIR,
                                                        True,
                                                        number,
                                                        stemmer)
                  ##### evaluator ##############################################
                  e = StandardPRFMEvaluator(run_name,
                                            RUNS_DIR,
                                            True,
                                            refs,
                                            pre_processor.encoding(),
                                            ref_stemmer,
                                            stemmer,
                                            tokenize)

                  runs.append(KeyphraseExtractor(docs,
                                                 ext,
                                                 pre_processor,
                                                 c,
                                                 cc,
                                                 r,
                                                 s,
                                                 e))

  ##### Runs' execution ########################################################

  print "EXECUTION OF %d RUNS..."%len(runs)
  queue = Queue()
  for run in runs:
    queue.put(run)
    KeyBenchWorker(queue).start()

################################################################################
if __name__ == "__main__":
  main(sys.argv)
################################################################################

