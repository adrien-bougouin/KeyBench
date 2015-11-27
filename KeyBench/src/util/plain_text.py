#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
from corpus_file import CorpusFileRep
import nltk

class PlainTextFileRep(CorpusFileRep):
  """
  Representation of a text file.
  """

  def __init__(self):
    """
    Constructor.
    """

    super(PlainTextFileRep, self).__init__()

  def parse_file(self, filepath):
    """
    Parses a corpus file and initialize the object.
    
    @param  filepath: The path of the corpus file to parse.
    @type   filepath: C{string}
    """

    text_file = codecs.open(filepath, "r", "utf-8")
    file_content = text_file.read().split("\n")
    content = ""

    for line in file_content:
      if content != "":
        content += " "
      content += line.strip()
    self.set_content(content)

    text_file.close()

