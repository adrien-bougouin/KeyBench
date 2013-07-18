#!/usr/bin/env python
# -*- encoding utf-8 -*-

import string
from exceptions import NotImplementedError
from nltk.tag.stanford import POSTagger
from nltk.tokenize.punkt import PunktSentenceTokenizer
from keybench.pre_processor import PreProcessorC

class StanfordPreProcessor(PreProcessorC):
  """
  Component performing pre-processing of documents using the punkt sentence
  tokenizer and the stanford's pos tagger. The file parsing and the word
  tokenization are not implemented.
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               encoding,
               tag_separator,
               stanford_jar_path,
               language_model_path):
    """
    Constructor of the component.

    @param  name:                 The name of the pre-processor.
    @type   name:                 C{string}
    @param  is_lazy:              True if the component can load previous datas,
                                  false if everything must be computed tought it
                                  has already been computed.
    @type   is_lazy:              C{boolean}
    @param  lazy_directory:       The directory used for caching.
    @type   lazy_directory:       C{string}
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
    """

    super(StanfordPreProcessor, self).__init__(name,
                                               is_lazy,
                                               lazy_directory,
                                               encoding,
                                               tag_separator)

    self._sentence_tokenizer = PunktSentenceTokenizer()
    self._pos_tagger = POSTagger(language_model_path,
                                 stanford_jar_path,
                                 encoding)

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

  def pos_tagging(self, tokenized_sentences, tag_separator):
    """
    Takes a list of tokenized sentences and applies POS-tagging on each.

    @param    tokenized_sentences: The tokenized sentences to POS-tag.
    @type     tokenized_sentences: C{list of string}

    @return:  A list of sentences which are POS-tagged.
    @rtype:   C{list of string}
    """

    pos_tagged_sentences = []

    for tokenized_sentence in tokenized_sentences:
      tagged_tokens = self._pos_tagger.tag([tokenized_sentence])
      pos_tagged_sentence = ""

      for token, tag in tagged_tokens:
        if string.punctuation.count(token) > 0:
          tag = "PUNCT"

        if pos_tagged_sentence != "":
          pos_tagged_sentence += " "
        pos_tagged_sentence += token + self.tag_separator() + tag

      pos_tagged_sentences.append(pos_tagged_sentence)

    return pos_tagged_sentences

