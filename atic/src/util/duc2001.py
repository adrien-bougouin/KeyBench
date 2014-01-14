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
      content += re.sub("(<(P|F).*?>)|(<\\/P>)", "", line).strip()
    # XML cleanning

    start_offset = "<START_OFFSET_DUCFileRep>"
    content = start_offset + content
    content = content.replace("</LP>", "</LP>%s"%start_offset)
    content = content.replace("</TEXT>", "</TEXT>%s"%start_offset)
    content = re.sub("%s.*?<LP>(.*?)<\\/LP>"%start_offset, "\\1", content)
    content = re.sub("%s.*?<TEXT>(.*?)<\\/TEXT>"%start_offset, "\\1", content)
    content = re.sub("%s.*"%start_offset, "", content)

    self.set_content(content)

