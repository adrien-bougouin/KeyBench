#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from corpus_file import CorpusFileRep
from lxml import etree

class DEFTFileRep(CorpusFileRep):
  """
  Representation of a DEFT-2012's XML file.
  """

  def __init__(self):
    """
    Constructor.
    """

    super(DEFTFileRep, self).__init__()

  def parse_file(self, filepath):
    """
    Parses a corpus file and initialize the object.
    
    @param  filepath: The path of the corpus file to parse.
    @type   filepath: C{string}
    """

    xml_file = open(filepath, "r")
    xml = xml_file.read()
    xml_file.close()
    doc = etree.fromstring(xml)

    # parse the abstract
    abstract = ""
    for p in doc.find("article/resume").findall("p"):
      if not p.text == None:
        if abstract != "":
          abstract += " "
        abstract += p.text.strip()
    self.set_abstract(abstract)

    # parse the content
    content = ""
    for p in doc.find("article/corps").findall("p"):
      if not p.text == None:
        if content != "":
          content += " "
        content += p.text.strip()
    self.set_content(content)

