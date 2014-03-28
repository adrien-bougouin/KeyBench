import codecs
import exceptions

from keybench.main import core
from keybench.main import model
from keybench.main.component import component # avoid recursive import

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
      language: The C{string} language of the document.
      encoding: The C{string} encoding of the file from which the document must
        be built.

    Returns:
      The C{KBDocument} representation.
    """

    document = model.KBDocument()

    ## fill the document 'meta-data' ###########################################
    document.corpus_name = corpus_name
    document.name = name
    document.language = language
    document.encoding = encoding

    ## complete the document ###################################################

    # - can the component do lazy loading?
    # - does the document elready xist?
    if self.isLazy() \
       and self.exists(document):
      # complete the document from cache
      document = self.load(document)
    # parse and preprocess the document
    else:
      document_file = codecs.open(filepath, "r", encoding)
      title, abstract, content = self._documentParsing(document_file)

      document_file.close()

      ## NLP tools #############################################################
      tool_factory = core.KBBenchmark.singleton().run_tools[self.run_name]
      tokenizer = tool_factory.tokenizer(language)
      pos_tagger = tool_factory.pos_tagger(language)
      ##########################################################################

      ## parsing ###############################################################
      self.logDebug("Parsing of %s..."%(name))
      document.title = title
      document.abstract = abstract
      document.content = content
      ## tokenization ##########################################################
      self.logDebug("Sentence tokenization of %s..."%(name))
      document.title_sentences = tokenizer.tokenizeSentences(document.title)
      document.abstract_sentences = tokenizer.tokenizeSentences(document.abstract)
      document.content_sentences = tokenizer.tokenizeSentences(document.content)
      self.logDebug("Word tokenization of %s..."%(name))
      document.title_sentence_tokens = tokenizer.tokenizeWords(document.title_sentences)
      document.abstract_sentence_tokens = tokenizer.tokenizeWords(document.abstract_sentences)
      document.content_sentence_tokens = tokenizer.tokenizeWords(document.content_sentences)
      ## part-of-speech tagging ################################################
      self.logDebug("Part-of-Speech tagging of %s..."%(name))
      document.title_token_pos_tags = pos_tagger.tag(document.title_sentence_tokens)
      document.abstract_token_pos_tags = pos_tagger.tag(document.abstract_sentence_tokens)
      document.content_token_pos_tags = pos_tagger.tag(document.content_sentence_tokens)
      ## serialization #########################################################
      self.logDebug("Saving the document representation of %s..."%(name))
      self.store(document, document)

    return document

  def _documentParsing(document_file):
    """Extracts the title, the abstract and the content of a document.

    Args:
      document_file: The C{file} to parse.

    Returns:
      The C{string} title, C{string} abstract and C{string} content of the
      document (C{tuple}).
    """

    raise exceptions.NotImplementedError()

