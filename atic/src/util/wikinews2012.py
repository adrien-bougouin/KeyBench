#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
from corpus_file import CorpusFileRep
import nltk

class WikiNewsFileRep(CorpusFileRep):
  """
  Representation of a WikiNews-2012's HTML file.
  """

  def __init__(self):
    """
    Constructor.
    """

    super(WikiNewsFileRep, self).__init__()

  def parse_file(self, filepath):
    """
    Parses a corpus file and initialize the object.
    
    @param  filepath: The path of the corpus file to parse.
    @type   filepath: C{string}
    """

    html_file = codecs.open(filepath, "r", "utf-8")
    raw_html = html_file.read()
    body = raw_html.split("<body>",1)[1]
    raw_content = nltk.clean_html(body.split("</h1>", 1)[1])

    self.set_title(nltk.clean_html(body.split("</h1>", 1)[0]).strip() + ".")
    
    content = ""
    for p in raw_content.split("\n"):
      p = p.strip()

      if p != "":
        if content != "":
          content += " "
        content += p
    content = content.split("-", 1)[1].replace(u"\u202F", " ").strip()

    self.set_content(content)

    html_file.close()

