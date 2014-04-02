from keybench.main.component import interface

class PlainTextDocumentBuilder(interface.KBDocumentBuilderI):
  """The component responsible of the creation of a document representation.

  The component that creates a C{KBDocument} from a file. In this case file are
  considered unstructured (plain text) and everything is part of the document's
  contain.
  """

  def _documentParsing(self, document_file):
    """Extracts the title, the abstract and the content of a document.

    Args:
      document_file: The C{file} to parse.

    Returns:
      The C{string} title, C{string} abstract and C{string} content of the
      document (C{tuple}).
    """

    return ("", "", " ".join(document_file.read().splitlines()))

