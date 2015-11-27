#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
import string
from corpus_file import CorpusFileRep
import re

semeval_categories = {
  "-820517091818547490": "C",
  "4008630294400927761": "C",
  "4665767659033776276": "C",
  "-8352201225032013890": "C",
  "-8378270571655521356": "C",
  "-9101034949785841765": "C",
  "-8795033500898553264": "C",
  "-3138902056894228350": "C",
  "3731653623435463983": "C",
  "1220133094820556823": "C",
  "7056752825410589273": "C",
  "2671762581939142668": "C",
  "5217914650821050735": "C",
  "-2089794446488676765": "C",
  "-1506471556904334165": "C",
  "8018981295373612867": "C",
  "6037262018240962782": "C",
  "-6413527700397510078": "C",
  "-5938267804198885474": "C",
  "5725048849646521121": "C",
  "3169468100588231313": "C",
  "-322447897144477455": "C",
  "-7562673281901547125": "C",
  "2214456798597966935": "C",
  "-5772622167996368500": "C",
  "-7036780561555562600": "H",
  "-8403139690061277408": "H",
  "1024366063613640978": "H",
  "-485586961204480304": "H",
  "1727311689792203778": "H",
  "-6467609248736134009": "H",
  "3753780565176843118": "H",
  "-1376047745402207090": "H",
  "568934874379542351": "H",
  "1216768983322546531": "H",
  "4381276615240165786": "H",
  "1712760368287488341": "H",
  "-7559919955583189571": "H",
  "8167569298035565821": "H",
  "6122605439384155818": "H",
  "-8418794661266725926": "H",
  "5170451956776206580": "H",
  "8218856655571363658": "H",
  "-2113515853831038798": "H",
  "-6415814930405996583": "H",
  "-4468660559220123073": "H",
  "2029689477993051151": "H",
  "4935870046778374124": "H",
  "3767812085982023258": "H",
  "7693403320714672312": "H",
  "1299513048976276897": "I",
  "-8295202912489528671": "I",
  "6516094536678669435": "I",
  "118693626860032893": "I",
  "-8871206841302371206": "I",
  "-2829019003510940590": "I",
  "531765611953509161": "I",
  "-4852055268315530876": "I",
  "1372546942408805255": "I",
  "5425100196354885044": "I",
  "5892235039052225349": "I",
  "1667777023529388775": "I",
  "-955281883289917728": "I",
  "3773441147309856694": "I",
  "4234982997930133705": "I",
  "-3354815853736353262": "I",
  "8453641569000405965": "I",
  "628523409468714879": "I",
  "7780388455821854395": "I",
  "8803478310652534477": "I",
  "5979092766683666820": "I",
  "-3289620238533078944": "I",
  "-1125629715094395544": "I",
  "-7633870643853449582": "I",
  "6465098070272727505": "I",
  "1439817923763284366": "J",
  "5969630033942657659": "J",
  "-481729801376545451": "J",
  "-5306861531608808050": "J",
  "-2947421839016777554": "J",
  "-4833750732787261924": "J",
  "3945549972672193060": "J",
  "-7168851163575415043": "J",
  "-7978610347540638557": "J",
  "7111221309350301369": "J",
  "5403388229944444424": "J",
  "2999756644955133119": "J",
  "234754689154245781": "J",
  "-3228057846552098825": "J",
  "5892343915559524889": "J",
  "-9181257696325033190": "J",
  "-6653451101922556022": "J",
  "-1470832683216162856": "J",
  "-524306885526205713": "J",
  "5273152015718264855": "J",
  "-3426891720868292141": "J",
  "6601374297536948039": "J",
  "-6275857869948065678": "J",
  "7430891151535731244": "J",
  "-309645004362245352": "J"
}

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

