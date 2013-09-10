#/usr/bin/env python
# -*- encoding: utf-8 -*-

from keybench.default.util import n_to_m_grams
from multiprocessing import Pool
from os import listdir
from os import path

##### Multi-processing #########################################################

def term_bag_extraction_pool_worker(arguments):
  """
  TODO
  """

  pre_processor, candidate_extractor, filepath = arguments

  if candidate_extractor != None:
    pre_processed_file = pre_processor.pre_process_file(filepath)
    candidates = candidate_extractor.extract_candidates(filepath, pre_processed_file)
    sentences = pre_processed_file.full_text()
    normalized_candidates = {}
    max_len = 0
    bag = []

    for candidate in candidates:
      max_len = max(max_len, len(candidate.split()))
      normalized_candidate = ""

      for word in candidate.split():
        if normalized_candidate != "":
          normalized_candidate += " "
        normalized_candidate += word.rsplit(pre_processed_file.tag_separator(), 1)[0]

      normalized_candidates[normalized_candidate] = True

    for sentence in sentences:
      for term in n_to_m_grams(sentence.split(), 1, max_len):
        normalized_term = ""

        for word in term.split():
          if normalized_term != "":
            normalized_term += " "
          normalized_term += word.lower().rsplit(pre_processed_file.tag_separator(), 1)[0]

        if normalized_candidates.has_key(normalized_term):
          bag.append(normalized_term)
  else:
    pre_processed_file = pre_processor.pre_process_file(filepath)
    words = pre_processed_file.full_text_words()
    bag = []

    for word in words:
      bag.append(word.lower().rsplit(pre_processed_file.tag_separator(), 1)[0])

  return set(bag)

################################################################################

def document_frequencies(corpus_directory,
                         extension,
                         pre_processor,
                         candidate_extractor=None):
  """
  Gives the document frequency of all the terms (n-grams) appearing in a given
  corpus.

  @param    corpus_directory: The path of the directory containing the corpus'
                              files.
  @type     corpus_directory: C{string}
  @param    extension:        The extension of the corpus files (to avoid other
                              files).
  @type     extension:        C{string}
  @param    pre_processor:    A pre-processor to get the files' full tex.
  @type     pre_processor:    C{keybench.PreProcessorC}
  TODO candidate_extractor
  TODO candidate_extractor

  @return:  The number of documents plus all the lowercased (not POS tagged)
            n-grams in the corpus associated with their document frequency.
  @rtype:   C{(float, dict(string, float))}
  """


  working_pool = Pool()
  pool_args = []
  document_terms = []
  nb_documents = 0.0
  dfs = {}

  for filename in listdir(corpus_directory):
    if filename.rfind(extension) >= 0 \
       and len(filename) - filename.rfind(extension) == len(extension):
      filepath = path.join(corpus_directory, filename)
      nb_documents += 1.0

      pool_args.append((pre_processor, candidate_extractor, filepath))
  #document_terms = working_pool.map(term_bag_extraction_pool_worker, pool_args)
  for args in pool_args:
    document_terms.append(term_bag_extraction_pool_worker(args))

  for terms in document_terms:
    for term in terms:
      if not dfs.has_key(term):
        dfs[term] = 0.0
      dfs[term] += 1.0

  return nb_documents, dfs

