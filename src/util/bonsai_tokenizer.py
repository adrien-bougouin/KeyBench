#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
import random
import sys
from datetime import datetime
from os import path
from os import remove
from os import system

BONSAI_TOKENIZER_PATH = path.join(path.dirname(sys.argv[0]),
                                  "..",
                                  "res",
                                  "tools",
                                  "bonsai_tokenizer.pl")

def bonsai_tokenization(sentence, encoding="utf-8"):
  """
  Performs word tokenization on a sentence.

  @param    sentence: A sentence to word tokenized.
  @type     sentence: C{string}
  @param    encoding: The encoding of the sentence.
  @type     encoding: C{string}

  @return:  The list of the sentence's words.
  @rtype:   C{list of string}
  """

  date_hash = hash(datetime.today().ctime())
  sentence_hash = hash(frozenset(sentence))
  rand = random.randint(0, abs(int(date_hash) - int(sentence_hash)))
  input_filename = ".bonsai_temp_input_%s_%s_%d"%(date_hash,
                                                  sentence_hash,
                                                  rand)
  output_filename = ".bonsai_temp_output_%s_%s_%d"%(date_hash,
                                                    sentence_hash,
                                                    rand)

  input_file = codecs.open(input_filename, "w", encoding)

  input_file.write(sentence)
  input_file.close()

  system("%s %s > %s"%(BONSAI_TOKENIZER_PATH, input_filename, output_filename))

  output_file = codecs.open(output_filename, "r", encoding)
  output = output_file.read()

  output_file.close()

  remove(input_filename)
  remove(output_filename)

  return output.split()

