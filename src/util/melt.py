#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
import random
import sys
from datetime import datetime
from os import path
from os import remove
from os import system

def melt(sentences, encoding):
  """
  Performs word tokenization and POS tagging on a list of sentences.

  @param    sentence: The list of the sentences to process.
  @type     sentence: C{list of string}
  @param    encoding: The encoding of the sentences.
  @type     encoding: C{string}

  @return:  A list of word tokenized and POS tagged sentences.
  @rtype:   C{list of string}
  """

  date_hash = hash(datetime.today().ctime())
  sentences_hash = hash(frozenset(sentences))
  rand = random.randint(0, abs(int(date_hash) - int(sentences_hash)) + 10)
  input_filename = ".melt_temp_input_%s_%s_%d"%(date_hash, sentences_hash, rand)
  output_filename = ".melt_temp_output_%s_%s_%d"%(date_hash,
                                                  sentences_hash,
                                                  rand)

  input_file = codecs.open(input_filename, "w", encoding)

  for i, s in enumerate(sentences):
    if i != 0:
      input_file.write("\n")
    input_file.write(s)
  input_file.close()

  system("MElt -T < %s > %s"%(input_filename, output_filename))

  output_file = codecs.open(output_filename, "r", encoding)
  output = output_file.read()

  output_file.close()

  remove(input_filename)
  remove(output_filename)

  return output.split("\n")
