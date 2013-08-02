#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
import sys
from keybench import PreProcessorC
from keybench.default import StanfordPreProcessor
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tokenize.treebank import TreebankWordTokenizer
from os import path
from util import bonsai_tokenization
from util import melt

################################################################################
# MEltPreProcessor
# FrenchPreProcessor
# EnglishPreProcessor

TOOLS_PATH = path.join(path.dirname(sys.argv[0]), "..", "res", "tools")
STANFORD_JAR_PATH = path.join(TOOLS_PATH,
                              "stanford-postagger-full-2012-11-11",
                              "stanford-postagger-3.1.4.jar")
ENGLISH_LANGUAGE_MODEL_PATH = path.join(TOOLS_PATH,
                                        "stanford-postagger-full-2012-11-11",
                                        "models",
                                        #"english-bidirectional-distsim.tagger")
                                        "english-left3words-distsim.tagger")
                                        #"english-caseless-left3words-distsim.tagger")
                                        #"wsj-0-18-left3words-distsim.tagger")
                                        #"wsj-0-18-left3words.tagger")
ENGLISH_ENCODING = "utf-8"
FRENCH_ENCODING = "utf-8"

################################################################################

class MEltPreProcessor(PreProcessorC):
  """
  Component performing pre-processing of documents using the punkt sentence
  tokenizer and the MElt pos tagger. The file parsing is not implemented.
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               debug,
               encoding):
    """
    Constructor of the component.

    @param  name:           The name of the pre-processor.
    @type   name:           C{string}
    @param  is_lazy:        True if the component can load previous datas, false
                            if everything must be computed tought it has already
                            been computed.
    @type   is_lazy:        C{boolean}
    @param  lazy_directory: The directory used for caching.
    @type   lazy_directory: C{string}
    @param  debug:          True if the component is in debug mode, else False.
                            When the component is in debug mode, it will output
                            each step of its processing.
    @type   debug:          C{bool}
    @param  encoding:       The encoding of the files to pre-process.
    @type   encoding:       C{string}
    """

    super(MEltPreProcessor, self).__init__(name,
                                               is_lazy,
                                               lazy_directory,
                                               debug,
                                               encoding,
                                               "/")

    self._sentence_tokenizer = PunktSentenceTokenizer()

  def sentence_tokenization(self, text):
    """
    Takes a raw text and split it into a list of sentences.

    @param    text: The raw text to pre-processed.
    @type     text: C{string}

    @return:  A list of sentences contained in the text.
    @rtype:   C{list of string}
    """

    if text != "":
      return self._sentence_tokenizer.tokenize(text)

    return []

  def word_tokenization(self, sentences):
    """
    Takes a list of sentences and applies word tokenize on each.

    @param    sentences: The sentences to tokenize.
    @type     sentences: C{list of string}

    @return:  A list of sentences which are tokenized.
    @rtype:   C{list of string}
    """

    # this step is performed in the MElt workflow
    return sentences

  def pos_tagging(self, tokenized_sentences, tag_separator):
    """
    Takes a list of tokenized sentences and applies POS-tagging on each.

    @param    tokenized_sentences: The tokenized sentences to POS-tag.
    @type     tokenized_sentences: C{list of string}

    @return:  A list of sentences which are POS-tagged.
    @rtype:   C{list of string}
    """

    return melt(tokenized_sentences, self.encoding())

################################################################################

class FrenchPreProcessor(MEltPreProcessor):
  """
  Pre-processor for french documents.
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               debug,
               corpus_file):
    """
    Constructor of the component.

    @param  name:           The name of the pre-processor.
    @type   name:           C{string}
    @param  is_lazy:        True if the component can load previous datas,
                            false if everything must be computed tought it
                            has already been computed.
    @type   is_lazy:        C{boolean}
    @param  lazy_directory: The directory used for caching.
    @type   lazy_directory: C{string}
    @param  debug:          True if the component is in debug mode, else False.
                            When the component is in debug mode, it will output
                            each step of its processing.
    @type   debug:          C{bool}
    @param  corpus_file:    The representation of a file (title, abstract,
                            content).
    @type   corpus_file:    C{CorpusFile}
    """

    super(FrenchPreProcessor, self).__init__(name,
                                             is_lazy,
                                             lazy_directory,
                                             debug,
                                             FRENCH_ENCODING)
    self._corpus_file = corpus_file

  def parse_file(self, filepath):
    """
    Extract the title, the abstract and the body contained in a french document.

    @param  filepath: The path of the file to analyse.
    @type   filepath: C{string}

    @return:  The title, the abstract and the body of the file's text.
    @rtype:   C{(string, string, string)}
    """

    self._corpus_file.reset(filepath)

    return (self._corpus_file.title(),
            self._corpus_file.abstract(),
            self._corpus_file.content())

################################################################################

class EnglishPreProcessor(StanfordPreProcessor):
  """
  Pre-processor for english documents.
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               tag_separator,
               corpus_file):
    """
    Constructor of the component.

    @param  name:           The name of the pre-processor.
    @type   name:           C{string}
    @param  is_lazy:        True if the component can load previous datas,
                            false if everything must be computed tought it
                            has already been computed.
    @type   is_lazy:        C{boolean}
    @param  lazy_directory: The directory used for caching.
    @type   lazy_directory: C{string}
    @param  tag_separator:  The symbol to use as a separator between a
                            word and its POS tag.
    @type   tag_separator:  C{string}
    @param  corpus_file:    The representation of a file (title, abstract,
                            content).
    @type   corpus_file:    C{CorpusFile}
    """

    super(EnglishPreProcessor, self).__init__(name,
                                              is_lazy,
                                              lazy_directory,
                                              ENGLISH_ENCODING,
                                              tag_separator,
                                              STANFORD_JAR_PATH,
                                              ENGLISH_LANGUAGE_MODEL_PATH)
    self._word_tokenizer = TreebankWordTokenizer()
    self._corpus_file = corpus_file

  def parse_file(self, filepath):
    """
    Extract the title, the abstract and the body contained in a english
    document.

    @param  filepath: The path of the file to analyse.
    @type   filepath: C{string}

    @return:  The title, the abstract and the body of the file's text.
    @rtype:   C{(string, string, string)}
    """

    self._corpus_file.reset(filepath)

    return (self._corpus_file.title(),
            self._corpus_file.abstract(),
            self._corpus_file.content())

  def word_tokenization(self, sentences):
    """
    Takes a list of sentences and applies word tokenize on each.

    @param    sentences: The sentences to tokenize.
    @type     sentences: C{list of string}

    @return:  A list of sentences which are tokenized.
    @rtype:   C{list of string}
    """

    tokenized_sentences = []

    for s in sentences:
      tokenized_sentence = ""

      for w in self._word_tokenizer.tokenize(s):
        if tokenized_sentence != "":
          tokenized_sentence += " "
        tokenized_sentence += w

      tokenized_sentences.append(tokenized_sentence)

    return tokenized_sentences

