#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
import string
from corpus_file import CorpusFileRep
import re

class SemEvalFileRep(CorpusFileRep):
  """
  Representation of a SemEval-2010's HTML file.
  """

  def __init__(self):
    """
    Constructor.
    """

    super(SemEvalFileRep, self).__init__()

  def parse_file(self, filepath):
    """
    Parses a corpus file and initialize the object.
    
    @param  filepath: The path of the corpus file to parse.
    @type   filepath: C{string}
    """

    text_file = codecs.open(filepath, "r", "utf-8")
    article = text_file.read()
    abstract_to_end = re.split(r"(?im)^abstract$", article, 1)[1]
    sections = re.split(r"(?m)^\d+\.(\d\.?)+ [A-Z].*", abstract_to_end)

    abstract = ""
    for l in sections[0].strip().split("\n"):
      if abstract != "":
        abstract += " "
      abstract += l
    self.set_abstract(abstract)
    content = ""
    for section in sections[1:-1]: # Do not take references
      sec = self.clean_section(section.split("\n"))

      if content != "" and sec !="":
        content += " "
      content += sec
    self.set_content(content)

    text_file.close()

  def clean_section(self, section):
    """
    """

    punct = [".", "!", "?"]
    in_env = False
    cleaned_section = ""

    for line in section:
      line = line.strip()
      nb_symbols = 0
      nb_numbers = 0
      nb_small_words = 0

      for character in line:
        if string.digits.count(character) > 0:
          nb_numbers += 1
        else:
          try:
            character.decode("utf-8")
          except:
            nb_symbols += 1
      for word in line.split():
        if len(word) <= 2:
          nb_small_words += 1

      if (nb_symbols < 4 and nb_numbers < 20 and nb_small_words < 4) \
         or punct.count(line[-1]) > 0:
        for ref, noise in re.findall(r"( ?\[\d+(, \d+)*\])", line):
          line = line.replace(ref, "")

        if len(line) >= 1:
          if line.find("Figure") == 0 \
             or line.find("Table") == 0\
             or line.find("Definition") == 0\
             or line.find("Claim") == 0\
             or line.find("Proof") == 0\
             or line.find("Corollary") == 0\
             or line.find("Lemma") == 0\
             or line.find("Theorem") == 0:
            in_env = True

          if (len(line) >= 40 or punct.count(line[-1]) > 0) \
             and len(line) <= 80 \
             and not in_env:
            if cleaned_section != "":
              cleaned_section += " "
            cleaned_section += line

          if in_env and punct.count(line[-1]) > 0:
            in_env = False

    return cleaned_section

