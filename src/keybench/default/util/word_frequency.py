#/usr/bin/env python
# -*- encoding: utf-8 -*-

from multiprocessing import Pool
from os import listdir
from os import path

def word_bag_extraction_pool_worker(arguments):
  """
  """

  pre_processor, filepath = arguments
  pre_processed_file = pre_processor.pre_process_file(filepath)
  words = pre_processed_file.full_text_words()
  bag = []

  for i, w in enumerate(words):
    bag.append(w.lower().rsplit(pre_processed_file.tag_separator(), 1)[0])

  return set(bag)

def document_frequencies(corpus_directory, extension, pre_processor):
  """
  Gives the document frequency of all the words appearing in the corpus.

  @param    corpus_directory: The path of the directory containing the corpus'
                              files.
  @type     corpus_directory: C{string}
  @param    extension:        The extension of the corpus files (to avoid other
                              files).
  @type     extension:        C{string}
  @param    pre_processor:    A pre-processor to get the files' full tex.
  @type     pre_processor:    C{keybench.PreProcessorC}

  @return:  All the lowercased (not POS tagged) words in the corpus associated
            with their DF.
  @rtype:   C{dict: string -> float}
  """


  working_pool = Pool()
  pool_args = []
  document_words = []
  dfs = {}

  for filename in listdir(corpus_directory):
    if filename.rfind(extension) >= 0 \
       and len(filename) - filename.rfind(extension) == len(extension):
      filepath = path.join(corpus_directory, filename)

      pool_args.append((pre_processor, filepath))
  document_words = working_pool.map(word_bag_extraction_pool_worker, pool_args)
  #for args in pool_args:
  #  document_words.append(word_bag_extraction_pool_worker(args))

  for words in document_words:
    for w in words:
      if not dfs.has_key(w):
        dfs[w] = 0.0
      dfs[w] += 1.0

  return dfs

def inverse_document_frequencies(corpus_directory,
                                 extension,
                                 pre_processor):
  """
  Gives the inverse document frequency of all the words appearing in the corpus.

  @param    corpus_directory: The path of the directory containing the corpus'
                              files.
  @type     corpus_directory: C{string}
  @param    extension:        The extension of the corpus files (to avoid other
                              files).
  @type     extension:        C{string}
  @param    pre_processor:    A pre-processor to get the files' full tex.
  @type     pre_processor:    C{keybench.PreProcessorC}

  @return:  All the lowercased (not POS tagged) words in the corpus associated
            with their IDFs.
  @rtype:   C{dict: string -> float}
  """

  dfs = document_frequencies(corpus_directory, extension, pre_processor)
  idfs = {}

  nb_documents = 0.0
  for filename in listdir(corpus_directory):
    if filename.rfind(extension) >= 0 \
       and len(filename) - filename.rfind(extension) == len(extension):
      nb_documents += 1.0

  for w in dfs:
    idfs[w] = nb_documents / dfs[w]

  return idfs

