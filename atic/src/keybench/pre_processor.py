#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from benchmark_component import BenchmarkComponent
from exceptions import NotImplementedError
from os import path
from pre_processed_file import PreProcessedFile

class PreProcessorC(BenchmarkComponent):
  """
  Component responsible of the document pre-processing. It pre-processed files
  in three steps:
    1. Sentence segmentation
    2. Word tokenization
    3. Part-of-Speech tagging (POS tagging)
  """

  def __init__(self,
               name,
               is_lazy,
               lazy_directory,
               debug,
               encoding,
               tag_separator):
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

    super(PreProcessorC, self).__init__(name,
                                        is_lazy,
                                        path.join(lazy_directory,
                                                  "pre_processings"),
                                        debug)

    self.set_encoding(encoding)
    self.set_tag_separator(tag_separator)

  def encoding(self):
    """
    Getter of the encoding used by the pre-processor.

    @return:  The encoding of the files to pre-process.
    @rtype:   C{string}
    """

    return self._encoding

  def set_encoding(self, encoding):
    """
    Setter of the encoding used by the pre-processor.

    @param  encoding: The new encoding of the files to pre-process.
    @type   encoding: C{string}
    """

    self._encoding = encoding

  def tag_separator(self):
    """
    Gitter of the tag separator used for the POS tagging.

    @return:  The symbol to use as a separator between a word and its tag.
    @rtype:   tag_separator:  C{string}
    """

    return self._tag_separator

  def set_tag_separator(self, tag_separator):
    """
    Setter of the tag separator used for the POS tagging.

    @param  tag_separator:  The symbol to use as a separator between a word and
                            its tag.
    @type   tag_separator:  C{string}
    """

    self._tag_separator = tag_separator

  def pre_process_file(self, filepath):
    """
    Applies the three pre-processing steps.

    @param    filepath: The path of the file to pre-process.
    @type     filepath: C{string}

    @return:  The pre-processed file in which everything is lowercase.
    @rtype:   C{PreProcessedFile}
    """

    lazy_filename = path.split(filepath)[1] + ".pre"
    pre_processed_file = PreProcessedFile()

    if super(PreProcessorC, self).is_lazy() \
       and super(PreProcessorC, self).is_cached(lazy_filename):
      # lazy loading
      pre_processed_file = super(PreProcessorC, self).load(lazy_filename)
    else:
      # open the file
      title, abstract, body = self.parse_file(filepath)

      # sentence tokenization
      super(PreProcessorC, self).log("Tokenizing %s into sentences..."%filepath)
      title_sentences = self.sentence_tokenization(title)
      abstract_sentences = self.sentence_tokenization(abstract)
      body_sentences = self.sentence_tokenization(body)
      # word tokenization
      super(PreProcessorC,
            self).log("Tokenizing %s's sentences into words..."%filepath)
      if len(title_sentences) > 0:
        tokenized_title_sentences = self.word_tokenization(title_sentences)
      else:
        tokenized_title_sentences = []
      if len(abstract_sentences) > 0:
        tokenized_abstract_sentences = self.word_tokenization(abstract_sentences)
      else:
        tokenized_abstract_sentences = []
      if len(body_sentences) > 0:
        tokenized_body_sentences = self.word_tokenization(body_sentences)
      else:
        tokenized_body_sentences = []
      # pos tagging
      super(PreProcessorC, self).log("POS tagging of %s..."%filepath)
      if len(tokenized_title_sentences) > 0:
        pos_tagged_title_sentences = self.pos_tagging(tokenized_title_sentences,
                                                      self.tag_separator())
      else:
        pos_tagged_title_sentences = []
      if len(tokenized_abstract_sentences) > 0:
        pos_tagged_abstract_sentences = self.pos_tagging(tokenized_abstract_sentences,
                                                         self.tag_separator())
      else:
        pos_tagged_abstract_sentences = []
      if len(tokenized_body_sentences) > 0:
        pos_tagged_body_sentences = self.pos_tagging(tokenized_body_sentences,
                                                    self.tag_separator())
      else:
        pos_tagged_body_sentences = []

      # remove possible blank sentences and lowercase the others
      index = 0
      while index < len(pos_tagged_title_sentences):
        if pos_tagged_title_sentences[index] == "":
          pos_tagged_title_sentences.pop(index)
        else:
          pos_tagged_title_sentences[index] = pos_tagged_title_sentences[index].lower()
          index += 1
      index = 0
      while index < len(pos_tagged_abstract_sentences):
        if pos_tagged_abstract_sentences[index] == "":
          pos_tagged_abstract_sentences.pop(index)
        else:
          pos_tagged_abstract_sentences[index] = pos_tagged_abstract_sentences[index].lower()
          index += 1
      index = 0
      while index < len(pos_tagged_body_sentences):
        if pos_tagged_body_sentences[index] == "":
          pos_tagged_body_sentences.pop(index)
        else:
          pos_tagged_body_sentences[index] = pos_tagged_body_sentences[index].lower()
          index += 1

      # pre_processed_file creation
      pre_processed_file.set_encoding(self.encoding())
      pre_processed_file.set_tag_separator(self.tag_separator())
      pre_processed_file.set_title(pos_tagged_title_sentences)
      pre_processed_file.set_abstract(pos_tagged_abstract_sentences)
      pre_processed_file.set_body(pos_tagged_body_sentences)

      # serialization
      super(PreProcessorC,
            self).log("Puting the pre-processed version of %s into cache..."%filepath)
      super(PreProcessorC,
            self).store(lazy_filename, pre_processed_file)

      # store string representation
      super(PreProcessorC,
            self).log("Saving the readable pre-processing of %s..."%filepath)
      string_rep = ""
      for c in pos_tagged_title_sentences:
        if string_rep != "":
          string_rep += "\n"
        string_rep += c
      for c in pos_tagged_abstract_sentences:
        if string_rep != "":
          string_rep += "\n"
        string_rep += c
      for c in pos_tagged_body_sentences:
        if string_rep != "":
          string_rep += "\n"
        string_rep += c
      super(PreProcessorC, self).store_string(lazy_filename, string_rep)


    return pre_processed_file

  def parse_file(self, filepath):
    """
    Extract the title, the abstract and the body contained in a file.

    @param  filepath: The path of the file to analyse.
    @type   filepath: C{string}

    @return:  The title, the abstract and the body of the file's text.
    @rtype:   C{tuple(string, string, string)}
    """

    raise NotImplementedError()

  def sentence_tokenization(self, text):
    """
    Takes a raw text and split it into a list of sentences.

    @param    text: The raw text to pre-processed.
    @type     text: C{string}

    @return:  A list of sentences contained in the text.
    @rtype:   C{list(string)}
    """

    raise NotImplementedError()

  def word_tokenization(self, sentences):
    """
    Takes a list of sentences and applies word tokenize on each.

    @param    sentences: The sentences to tokenize.
    @type     sentences: C{list(string)}

    @return:  A list of sentences which are tokenized.
    @rtype:   C{list(string)}
    """

    raise NotImplementedError()

  def pos_tagging(self, tokenized_sentences, tag_separator):
    """
    Takes a list of tokenized sentences and applies POS-tagging on each.

    @param    tokenized_sentences: The tokenized sentences to POS-tag.
    @type     tokenized_sentences: C{list(string)}

    @return:  A list of sentences which are POS-tagged.
    @rtype:   C{list(string)}
    """

    raise NotImplementedError()

