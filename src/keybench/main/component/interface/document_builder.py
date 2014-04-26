# -*- encoding: utf-8 -*-

import codecs
import exceptions

from keybench.main import core
from keybench.main import model
from keybench.main.component import component

class KBDocumentBuilderI(component.KBComponent):
  """The abstract component responsible of the creation of a document
  representation.

  The component that creates a C{KBDocument} from a file. In most cases,
  subclasses must not override C{buidDocument()}, but only
  C{documentParsing()}.
  """

  def buildDocument(self,
                    filepath,
                    corpus_name,
                    name,
                    language,
                    encoding):
    """Builds a document from a file.

    Args:
      filepath: The C{string} path of the file from which the document must be
        built.
      corpus_name: The C{string} of the corpus to which the document belongs.
      name: The C{string} name of the document.
      language: The C{string} language of the document (see
        C{keybench.main.language.KBLanguage.ENGLISH}).
      encoding: The C{string} encoding of the file from which the document must
        be built.

    Returns:
      The C{KBDocument} representation.
    """

    # first initialization so the cache functions can be used
    document = model.KBDocument(corpus_name,
                                filepath,
                                name,
                                language,
                                encoding,
                                "", "", "",
                                [], [], [],
                                [], [], [],
                                [], [], [])

    ## complete the document ###################################################

    # - can the component do lazy loading?
    # - does the document elready xist?
    if self.isLazy() \
       and self.exists(document):
      # complete the document from cache
      document = self.load(document)
    # parse and preprocess the document
    else:
      ## parsing ###############################################################
      self.logDebug("Parsing of %s..."%(name))
      document_file = codecs.open(filepath, "r", encoding)
      title, abstract, content = self._documentParsing(document_file)

      document_file.close()

      if title != "" or abstract != "" or content != "":
        ## NLP tools ###########################################################
        tool_factory = core.KBBenchmark.singleton().run_tools[self._run_name]
        tokenizer = tool_factory.tokenizer(language)
        pos_tagger = tool_factory.pos_tagger(language)
        ########################################################################

        ## tokenization ########################################################
        self.logDebug("Sentence tokenization of %s..."%(name))
        title_sentences = tokenizer.tokenizeSentences(title)
        abstract_sentences = tokenizer.tokenizeSentences(abstract)
        content_sentences = tokenizer.tokenizeSentences(content)
        self.logDebug("Word tokenization of %s..."%(name))
        title_sentence_tokens = tokenizer.tokenizeWords(title_sentences)
        abstract_sentence_tokens = tokenizer.tokenizeWords(abstract_sentences)
        content_sentence_tokens = tokenizer.tokenizeWords(content_sentences)
        ## part-of-speech tagging ##############################################
        self.logDebug("Part-of-Speech tagging of %s..."%(name))
        title_token_pos_tags = pos_tagger.tag(title_sentence_tokens)
        abstract_token_pos_tags = pos_tagger.tag(abstract_sentence_tokens)
        content_token_pos_tags = pos_tagger.tag(content_sentence_tokens)
        ## fill every attributes of the document ###############################
        document = model.KBDocument(corpus_name,
                                    filepath,
                                    name,
                                    language,
                                    encoding,
                                    title,
                                    abstract,
                                    content,
                                    title_sentences,
                                    abstract_sentences,
                                    content_sentences,
                                    title_sentence_tokens,
                                    abstract_sentence_tokens,
                                    content_sentence_tokens,
                                    title_token_pos_tags,
                                    abstract_token_pos_tags,
                                    content_token_pos_tags)
      ## serialization #########################################################
      self.logDebug("Saving the document representation of %s..."%(name))
      self.store(document, document)

    return document

  def _documentParsing(self, document_file):
    """Extracts the title, the abstract and the content of a document.

    Args:
      document_file: The C{file} to parse.

    Returns:
      The C{string} title, C{string} abstract and C{string} content of the
      document (C{tuple}).
    """

    raise exceptions.NotImplementedError()

