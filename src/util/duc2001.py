#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from corpus_file import CorpusFileRep
from lxml import etree

class DUCFileRep(CorpusFileRep):
  """
  """

  def __init__(self):
    """
    Constructor.
    """

    super(DUCFileRep, self).__init__()

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

    # parse the content
    content = ""
    for p in doc.find("TEXT").findall("P"):
      if content != "":
        content += " "
      content += p.text.strip()
    if content == "":
      for line in doc.find("TEXT").text.split("\n"):
        if content != "":
          content += " "
        content += line.strip()
    self.set_content(content)
