#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class PreProcessedFile(object):
  """
  Represents a file containing a title, an abstract and a body. Those three
  attributes are pre-processed (sentences are tokenized into words which are POS
  tagged).
  """

  def __init__(self,
               encoding="",
               tag_separator="",
               title=[],
               abstract=[],
               body=[]):
    """
    Constructor.

    @param  encoding:       The encoding of the file.
    type    encoding:       C{string}
    @param  tag_separator:  The separator used between a word and its POS tag.
    type    tag_separator:  C{string}
    @param  title:          The POS tagged title of the file's document.
    type    title:          C{list(string)}
    @param  abstract:       The POS tagged abstract of the file's document.
    type    abstract:       C{list(string)}
    @param  body:           The POS tagged body of the file's document.
    type    body:           C{list(string)}
    """

    super(PreProcessedFile, self).__init__()

    self.set_encoding(encoding)
    self.set_tag_separator(tag_separator)
    self.set_title(title)
    self.set_abstract(abstract)
    self.set_body(body)
    # to fill using lazy loading
    self._full_text = []
    self._title_words = []
    self._abstract_words = []
    self._body_words = []
    self._full_text_words = []

  def encoding(self):
    """
    Getter of the encoding of the pre-processed file.

    @return:  The encoding of the pre-processed file.
    @rtype:   C{string}
    """

    return self._encoding

  def set_encoding(self, encoding):
    """
    Setter of the encoding of the pre-processed file.

    @param  encoding: The new encoding of the pre-processed file.
    @type   encoding: C{string}
    """

    self._encoding = encoding

  def tag_separator(self):
    """
    Getter of the tag separator used in the pre-processed file.

    @return:  The tag separator used in the pre-processed file.
    @rtype:   C{string}
    """

    return self._tag_separator

  def set_tag_separator(self, tag_separator):
    """
    Setter the tag_separator used in the pre-processed file.

    @param  tag_separator: The new tag separator used in the pre-processed file.
    @type   tag_separator: C{string}
    """

    self._tag_separator = tag_separator

  def title(self):
    """
    Getter of the POS tagged title of the pre-processed file.

    @return:  The POS tagged title of the pre-processed file (as a list of POS
              tagged sentences).
    @rtype:   C{list(string)}
    """

    return self._title

  def set_title(self, title):
    """
    Setter of the POS tagged title the pre-processed file.

    @param  title: The new POS tagged title of the pre-processed file (as a list
                   of POS tagged sentences).
    @type   title: C{list(string)}
    """

    self._title = title
    # reset lazy loading
    self._title_words = []
    self._full_text = []
    self._full_text_words = []

  def abstract(self):
    """
    Getter of the POS tagged abstract of the pre-processed file.

    @return:  The POS tagged abstract of the pre-processed file (as a list of
              POS tagged sentences).
    @rtype:   C{list(string)}
    """

    return self._abstract

  def set_abstract(self, abstract):
    """
    Setter of the POS tagged abstract the pre-processed file.

    @param  abstract: The new POS tagged abstract of the pre-processed file (as
                      a list of POS tagged sentences).
    @type   abstract: C{list(string)}
    """

    self._abstract = abstract
    # reset lazy loading
    self._abstract_words = []
    self._full_text = []
    self._full_text_words = []

  def body(self):
    """
    Gitter of the POS tagged body of the pre-processed file.

    @return:  The POS tagged body of the pre-processed file (as a list of POS
              tagged sentences).
    @rtype:   C{list(string)}
    """

    return self._body

  def set_body(self, body):
    """
    Setter of the POS tagged body the pre-processed file.

    @param  body: The new POS tagged body of the pre-processed file (as a list
                  of POS tagged sentences).
    @type   body: C{list of string}
    """

    self._body = body
    # reset lazy loading
    self._body_words = []
    self._full_text = []
    self._full_text_words = []

  def title_words(self):
    """
    Gives all the POS tagged words of the title.

    @return:  The POS tagged title's words (as a list of POS tagged words).
    @rtype:   C{list of string}
    """

    if self._title_words == []:
      for s in self.title():
        for w in s.split():
          self._title_words.append(w)

    return self._title_words

  def abstract_words(self):
    """
    Gives all the POS tagged words of the abstract.

    @return:  The POS tagged abstract's words (as a list of POS tagged words).
    @rtype:   C{list of string}
    """

    if self._abstract_words == []:
      for s in self.abstract():
        for w in s.split():
          self._abstract_words.append(w)

    return self._abstract_words

  def body_words(self):
    """
    Gives all the POS tagged words of the body.

    @return:  The POS tagged body's words (as a list of POS tagged words).
    @rtype:   C{list of string}
    """

    if self._body_words == []:
      for s in self.body():
        for w in s.split():
          self._body_words.append(w)

    return self._body_words

  def full_text(self):
    """
    Gives all the POS tagged attributes (title, abstract and body).

    @return:  The POS tagged title, abstract and body of the pre-processed file
              (as a list of POS tagged sentences).
    @rtype:   C{list of string}
    """

    if self._full_text == []:
      for sentence in self.title():
        self._full_text.append(sentence)
      for sentence in self.abstract():
        self._full_text.append(sentence)
      for sentence in self.body():
        self._full_text.append(sentence)

    return self._full_text

  def full_text_words(self):
    """
    Gives all the POS tagged words of all the text's attributes (title, abstract
    and body).

    @return:  The POS tagged text's words (as a list of POS tagged words).
    @rtype:   C{list of string}
    """

    if self._full_text_words == []:
      for s in self.full_text():
        for w in s.split():
          self._full_text_words.append(w)

    return self._full_text_words

