#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from exceptions import NotImplementedError

class CorpusFileRep(object):
  """
  Representation of a file of a corpus. It has a title, an abstract and a
  content.
  """

  def __init__(self):
    """
    Constructor.
    """

    super(CorpusFileRep, self).__init__()

    self._title = ""
    self._abstract = ""
    self._content = ""

  def set_file(self, filepath):
    """
    Parses a corpus file and initialize the object.
    
    @param  filepath: The path of the corpus file to parse.
    @type   filepath: C{string}
    """

    super(CorpusFileRep, self).__init__()

    self._title = ""
    self._abstract = ""
    self._content = ""

    self.parse_file(filepath)

  def parse_file(self, filepath):
    """
    Parses a corpus file and initialize the object.
    
    @param  filepath: The path of the corpus file to parse.
    @type   filepath: C{string}
    """

    raise NotImplementedError()

  def title(self):
    """
    Gives the title of the text.

    @return:  The title of the file.
    @rtype:   C{string}
    """

    return self._title

  def set_title(self, title):
    """
    Changes the title of the text.

    @param  title: The title of the file.
    @type   title: C{string}
    """

    self._title = title

  def abstract(self):
    """
    Gives the abstract of the text.

    @return:  The abstract of the file.
    @rtype:   C{string}
    """

    return self._abstract

  def set_abstract(self, abstract):
    """
    Changes the abstract of the text.

    @param  abstract: The abstract of the file.
    @type   abstract: C{string}
    """

    self._abstract = abstract

  def content(self):
    """
    Gives the content of the text.

    @return:  The content of the file.
    @rtype:   C{string}
    """

    return self._content

  def set_content(self, content):
    """
    Changes the content of the text.

    @param  content: The content of the file.
    @type   content: C{string}
    """

    self._content = content

