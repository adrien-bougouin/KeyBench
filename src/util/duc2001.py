#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
from corpus_file import CorpusFileRep

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
    content = ""

    xml_file.close()

    for line in xml.replace("&amp;", "&").split("\n"):
      if content != "":
        content += " "
      content += line.strip()
    self.set_content(re.sub("(.*<LP>)|(<\\/LP>.*<TEXT>)|(<\\/LP>.*)|(.*<TEXT>)|(<\\/TEXT>.*)", "", content))
