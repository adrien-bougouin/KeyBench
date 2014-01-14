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

    self.set_title("")
    self.set_abstract("")
    self.set_content("")

  def title(self):
    """
    Getter of the title of the text.

    @return:  The title of the file.
    @rtype:   C{string}
    """

    return self._title

  def set_title(self, title):
    """
    Setter of the title of the text.

    @param  title: The new title of the file.
    @type   title: C{string}
    """

    self._title = title

  def abstract(self):
    """
    Getter of the abstract of the text.

    @return:  The abstract of the file.
    @rtype:   C{string}
    """

    return self._abstract

  def set_abstract(self, abstract):
    """
    Setter of the abstract of the text.

    @param  abstract: The new abstract of the file.
    @type   abstract: C{string}
    """

    self._abstract = abstract

  def content(self):
    """
    Getter of the content of the text.

    @return:  The content of the file.
    @rtype:   C{string}
    """

    return self._content

  def set_content(self, content):
    """
    Setter of the content of the text.

    @param  content: The new content of the file.
    @type   content: C{string}
    """

    self._content = content

  def reset(self, filepath):
    """
    Parses a corpus file and initialize the object.
    
    @param  filepath: The path of the corpus file to parse.
    @type   filepath: C{string}
    """

    self.set_title("")
    self.set_abstract("")
    self.set_content("")

    self.parse_file(filepath)

  def parse_file(self, filepath):
    """
    Parses a corpus file and initialize the object.
    
    @param  filepath: The path of the corpus file to parse.
    @type   filepath: C{string}
    """

    raise NotImplementedError()

