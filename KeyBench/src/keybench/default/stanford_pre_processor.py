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
               debug,
               encoding,
               tag_separator,
               stanford_jar_path,
               language_model_path):
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
    """

    super(StanfordPreProcessor, self).__init__(name,
                                               is_lazy,
                                               lazy_directory,
                                               debug,
                                               encoding,
                                               tag_separator)

    self.set_sentence_tokenizer(PunktSentenceTokenizer())
    self.set_pos_tagger(POSTagger(language_model_path,
                                  stanford_jar_path,
                                  encoding))

  def sentence_tokenizer(self):
    """
    Getter of the sentence tokenizer.

    @return:  The sentence tokenizer.
    @rtype:   C{nltk.tokenize.punkt.PunktSentenceTokenizer}
    """

    return self._sentence_tokenizer

  def set_sentence_tokenizer(self, sentence_tokenizer):
    """
    Setter of the sentence tokenizer.

    @param  sentence_tokenizer: The new sentence tokenizer.
    @type   sentence_tokenizer: C{nltk.tokenize.api.TokenizerI}
    """

    self._sentence_tokenizer = sentence_tokenizer

  def pos_tagger(self):
    """
    Getter of the POS tagger.

    @return:  The POS tagger.
    @rtype:   C{nltk.tag.api.TaggerI}
    """

    return self._pos_tagger

  def set_pos_tagger(self, pos_tagger):
    """
    Setter of the POS tagger.

    @param  pos_tagger: The new POS tagger.
    @type   pos_tagger:  C{nltk.tag.api.TaggerI}
    """

    self._pos_tagger = pos_tagger

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

  def pos_tagging(self, tokenized_sentences, tag_separator):
    """
    Takes a list of tokenized sentences and applies POS-tagging on each.

    @param    tokenized_sentences: The tokenized sentences to POS-tag.
    @type     tokenized_sentences: C{list(string)}

    @return:  A list of sentences which are POS-tagged.
    @rtype:   C{list(string)}
    """

    pos_tagged_sentences = []

    for tokenized_sentence in tokenized_sentences:
      tagged_tokens = self.pos_tagger().tag([tokenized_sentence])
      pos_tagged_sentence = ""

      for token, tag in tagged_tokens:
        if string.punctuation.count(token) > 0:
          tag = "PUNCT"

        if pos_tagged_sentence != "":
          pos_tagged_sentence += " "
        pos_tagged_sentence += token + self.tag_separator() + tag

      pos_tagged_sentences.append(pos_tagged_sentence)

    return pos_tagged_sentences

