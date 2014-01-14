#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
from corpus_file import CorpusFileRep
import nltk

class InspecFileRep(CorpusFileRep):
  """
  Representation of a Inspec's file.
  """

  def __init__(self):
    """
    Constructor.
    """

    super(InspecFileRep, self).__init__()

  def parse_file(self, filepath):
    """
    Parses a corpus file and initialize the object.
    
    @param  filepath: The path of the corpus file to parse.
    @type   filepath: C{string}
    """

    abstr_file = codecs.open(filepath, "r", "utf-8")
    file_content = abstr_file.read().split("\n")
    title = ""
    abstract = ""

    parse_title = True
    for i, line in enumerate(file_content):
      if line != "":
        if parse_title and i != 0 and line[0] != "\t":
          parse_title = False

        if parse_title:
          if title != "":
            title += " "
          title += line.strip()
        else:
          if abstract != "":
            abstract += " "
          abstract += line.strip()
    if title[-1] != ".":
      title += "."
    if abstract[-1] != ".":
      abstract += "."

    self.set_title(title)
    self.set_abstract(abstract)

    abstr_file.close()

