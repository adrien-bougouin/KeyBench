#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
import string

from corpus_file import CorpusFileRep
from lxml import etree
from nltk.util import clean_html

class INISTFileRep(CorpusFileRep):
  """
  """

  def __init__(self):
    """
    Constructor.
    """

    super(INISTFileRep, self).__init__()

  def parse_file(self, filepath):
    """
    Parses a corpus file and initialize the object.
    
    @param  filepath: The path of the corpus file to parse.
    @type   filepath: C{string}
    """

    xml_file = open(filepath, "r")
    xml = re.sub(" (corresp|xml:id)=\"[^>]*\">", ">", xml_file.read())
    xml = re.sub("</?sup>", "", xml)
    xml = re.sub("</?sub>", "", xml)
    xml = re.sub("<note[^>]*>", "__NOTE_START__", xml)
    xml = re.sub("</note>", "__NOTE_END__", xml)
    xml_file.close()
    doc = etree.fromstring(xml)

    # parse title
    title = doc.xpath("//tei:sourceDesc/tei:biblStruct/tei:analytic/tei:title[@type=\"main\"][@xml:lang=\"fr\"]",
                       namespaces={"tei": "http://www.tei-c.org/ns/1.0"})[0].text + "."
    self.set_title(title)

    # parse the abstract
    abstract = ""
    for p in doc.xpath("//tei:profileDesc/tei:abstract[@xml:lang=\"fr\"]/tei:p",
                       namespaces={"tei": "http://www.tei-c.org/ns/1.0"}):
      if not p.xpath("string()") == None:
        if abstract != "":
          abstract += " "
        abstract += p.xpath("string()").strip()
    self.set_abstract(abstract)

    # parse the abstract
    content = ""
    for p in doc.xpath("//tei:body//*[self::tei:head or self::tei:p or self::tei:q][not(@rend=\"figure-title\" or @rend=\"footnote\")]",
                       namespaces={"tei": "http://www.tei-c.org/ns/1.0"}):
      if not p.xpath("string()") == None:
        text = " ".join(l.strip() for l in p.xpath("string()").strip().splitlines())

        if text != "":
          text = re.sub(" ?__NOTE_START__.*?__NOTE_END__", "", text)

          if text != "":
            if text[-1] not in string.punctuation and p.tag == "{http://www.tei-c.org/ns/1.0}head":
              text += "."

            if content != "":
              content += " "
            content += text
    self.set_content(" ".join(l for l in content.splitlines()))

