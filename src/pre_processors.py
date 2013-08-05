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
                                        "english-left3words-distsim.tagger")
ENGLISH_ENCODING = "utf-8"
FRENCH_ENCODING = "utf-8"

################################################################################

class MEltPreProcessor(PreProcessorC):
  """
  Component performing pre-processing of documents using the punkt sentence
  tokenizer and the MElt POS tagger. The file parsing is not implemented.
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               debug,
               encoding):
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
    @param  encoding:       The encoding of the files to pre-process.
    @type   encoding:       C{string}
    @param  tag_separator:  The symbol to use as a separator between a word and
                            its POS tag.
    @type   tag_separator:  C{string}
    """

    super(MEltPreProcessor, self).__init__(name,
                                               is_lazy,
                                               lazy_directory,
                                               debug,
                                               encoding,
                                               "/")

    self.set_sentence_tokenizer = PunktSentenceTokenizer()

  def sentence_tokenizer(self):
    """
    Getter of the tokenizer used for the sentence segmentation.

    @return:  The tokenizer used for the sentence segmentation.
    @rtype:   C{nltk.tokenize.api.TokenizerI}
    """

    return self._sentence_tokenizer

  def set_sentence_tokenizer(self, sentence_tokenizer):
    """
    Setter of the tokenizer used for the sentence segmentation.

    @param  sentence_tokenizer: The new tokenizer used for the sentence
                                segmentation.
    @type   sentence_tokenizer: C{nltk.tokenize.api.TokenizerI}
    """

    self._sentence_tokenizer = sentence_tokenizer

  def sentence_tokenization(self, text):
    """
    Takes a raw text and split it into a list of sentences.

    @param    text: The raw text to pre-processed.
    @type     text: C{string}

    @return:  A list of sentences contained in the text.
    @rtype:   C{list(string)}
    """

    if text != "":
      return self.sentence_tokenizer().tokenize(text)

    return []

  def word_tokenization(self, sentences):
    """
    Takes a list of sentences and applies word tokenize on each.

    @param    sentences: The sentences to tokenize.
    @type     sentences: C{list(string)}

    @return:  A list of sentences which are tokenized.
    @rtype:   C{list(string)}
    """

    # this step is performed in the MElt workflow
    return sentences

  def pos_tagging(self, tokenized_sentences, tag_separator):
    """
    Takes a list of tokenized sentences and applies POS-tagging on each.

    @param    tokenized_sentences: The tokenized sentences to POS-tag.
    @type     tokenized_sentences: C{list(string)}

    @return:  A list of sentences which are POS-tagged.
    @rtype:   C{list(string)}
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

    @param  name:                 The name of the component.
    @type   name:                 C{string}
    @param  is_lazy:              True if the component must load previous data,
                                  False if data must be computed tought they
                                  have already been computed.
    @type   is_lazy:              C{bool}
    @param  lazy_directory:       The directory used to store previously
                                  computed data.
    @type   lazy_directory:       C{string}
    @param  debug:                True if the component is in debug mode, else
                                  False. When the component is in debug mode, it
                                  will output each step of its processing.
    @type   debug:                C{bool}
    @param  encoding:             The encoding of the files to pre-process.
    @type   encoding:             C{string}
    @param  tag_separator:        The symbol to use as a separator between a
                                  word and its POS tag.
    @type   tag_separator:        C{string}
    @param  stanford_jar_path:    The path to the jar of the Java Stanford
                                  Tagger.
    @type   stanford_jar_path:    C{string}
    @param  language_model_path:  The path to the language-specific stafonrd's
                                  model.
    @type   language_model_path:  C{string}
    @param  corpus_file:          The representation of a file (title, abstract,
                                  content).
    @type   corpus_file:          C{CorpusFile}
    """

    super(FrenchPreProcessor, self).__init__(name,
                                             is_lazy,
                                             lazy_directory,
                                             debug,
                                             FRENCH_ENCODING)

    # TODO use a factory instead
    self.set_corpus_file(corpus_file)

  def corpus_file(self):
    """
    Getter of the file representation.

    @return:  The instance representing a file of the analysed corpus.
    @rtype:   C{CorpusFileRep}
    """

    return self._corpus_file

  def set_corpus_file(self, corpus_file):
    """
    Setter of the file representation.

    @param  corpus_file:  The new instance representing a file of the analysed
                          corpus.
    @type   corpus_file:  C{CorpusFileRep}
    """

    self._corpus_file = corpus_file

  def parse_file(self, filepath):
    """
    Extract the title, the abstract and the body contained in a file.

    @param  filepath: The path of the file to analyse.
    @type   filepath: C{string}

    @return:  The title, the abstract and the body of the file's text.
    @rtype:   C{tuple(string, string, string)}
    """

    self.corpus_file().reset(filepath)

    return (self.corpus_file().title(),
            self.corpus_file().abstract(),
            self.corpus_file().content())

################################################################################

class EnglishPreProcessor(StanfordPreProcessor):
  """
  Pre-processor for english documents. Words are tokenized with NLTK's
  C{TreeBankWordTokenizer}.
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               tag_separator,
               corpus_file):
    """
    Constructor of the component.

    @param  name:                 The name of the component.
    @type   name:                 C{string}
    @param  is_lazy:              True if the component must load previous data,
                                  False if data must be computed tought they
                                  have already been computed.
    @type   is_lazy:              C{bool}
    @param  lazy_directory:       The directory used to store previously
                                  computed data.
    @type   lazy_directory:       C{string}
    @param  debug:                True if the component is in debug mode, else
                                  False. When the component is in debug mode, it
                                  will output each step of its processing.
    @type   debug:                C{bool}
    @param  encoding:             The encoding of the files to pre-process.
    @type   encoding:             C{string}
    @param  tag_separator:        The symbol to use as a separator between a
                                  word and its POS tag.
    @type   tag_separator:        C{string}
    @param  stanford_jar_path:    The path to the jar of the Java Stanford
                                  Tagger.
    @type   stanford_jar_path:    C{string}
    @param  language_model_path:  The path to the language-specific stafonrd's
                                  model.
    @type   language_model_path:  C{string}
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

    self.set_word_tokenizer(TreebankWordTokenizer())
    # TODO use a factory instead
    self.set_corpus_file(corpus_file)

  def word_tokenizer(self):
    """
    Getter of the tokenizer used for the word tokenization.

    @return:  The tokenizer used for the word tokenization.
    @rtype:   C{nltk.tokenize.api.TokenizerI}
    """

    return self._word_tokenizer

  def set_word_tokenizer(self, word_tokenizer):
    """
    Setter of the tokenizer used for the word tokenization.

    @param  word_tokenizer: The new tokenizer used for the word
                                tokenization.
    @type   word_tokenizer: C{nltk.tokenize.api.TokenizerI}
    """

    self._word_tokenizer = word_tokenizer

  def corpus_file(self):
    """
    Getter of the file representation.

    @return:  The instance representing a file of the analysed corpus.
    @rtype:   C{CorpusFileRep}
    """

    return self._corpus_file

  def set_corpus_file(self, corpus_file):
    """
    Setter of the file representation.

    @param  corpus_file:  The new instance representing a file of the analysed
                          corpus.
    @type   corpus_file:  C{CorpusFileRep}
    """

    self._corpus_file = corpus_file

  def parse_file(self, filepath):
    """
    Extract the title, the abstract and the body contained in a file.

    @param  filepath: The path of the file to analyse.
    @type   filepath: C{string}

    @return:  The title, the abstract and the body of the file's text.
    @rtype:   C{tuple(string, string, string)}
    """

    self.corpus_file().reset(filepath)

    return (self.corpus_file().title(),
            self.corpus_file().abstract(),
            self.corpus_file().content())

  def word_tokenization(self, sentences):
    """
    Takes a list of sentences and applies word tokenize on each.

    @param    sentences: The sentences to tokenize.
    @type     sentences: C{list(string)}

    @return:  A list of sentences which are tokenized.
    @rtype:   C{list(string)}
    """

    tokenized_sentences = []

    for s in sentences:
      tokenized_sentence = ""

      for w in self.word_tokenizer().tokenize(s):
        if tokenized_sentence != "":
          tokenized_sentence += " "
        tokenized_sentence += w

      tokenized_sentences.append(tokenized_sentence)

    return tokenized_sentences

