#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
import random
from datetime import datetime
from os import remove
from os import system

def ngram_model_logprobs(train, phrases, encoding, length=0):
  """
  Trains a language model used to get probabilities of phrases
  (log probabilities).

  @param    train:    The training test used to construct the language model.
  @type     train:    C{list(string)}
  @param    phrases:  The phrases to get the probabilities of.
  @type     phrases:  C{list(string)}
  @param    encoding: The encogind of the strings.
  @type     encoding: C{string}
  @param    length:   The length of the n-grams in the model. If the length is
                      set to 0 (default) the length will be set to the maximum
                      number of words in the phrases.
  @type     length:   C{int}

  @return:  The log probabilities of the candidates).
  @rtype:   C{dict(string, float)}
  """

  ##### preparation for srilm command line tool execution ######################
  date_hash = hash(datetime.today().ctime())
  train_hash = hash(frozenset(train))
  phrases_hash = hash(frozenset(phrases))
  rand = random.randint(0,
                        abs(int(date_hash) - int (train_hash) - int(phrases_hash)))
  train_filename = ".srilm_temp_%s_train_%s_%d"%(date_hash,
                                                 train_hash,
                                                 rand)
  phrases_filename = ".srilm_temp_%s_phrases_%s_%d"%(date_hash,
                                                     phrases_hash,
                                                     rand)
  lm_filename = ".srilm_temp_%s_lm_%d_%s_%s_%d"%(date_hash,
                                                 length,
                                                 train_hash,
                                                 phrases_hash,
                                                 rand)
  stat_filename = ".srilm_temp_%s_stat_%d_%s_%s_%d"%(date_hash,
                                                     length,
                                                     train_hash,
                                                     phrases_hash,
                                                     rand)

  train_file = codecs.open(train_filename, "w", encoding)
  for i, s in enumerate(train):
    if i > 0:
      train_file.write("\n")
    train_file.write(s)
  train_file.close()

  phrases_file = codecs.open(phrases_filename, "w", encoding)
  max_len = 0
  for i, s in enumerate(phrases):
    s_len = len(s.split())
    if s_len > max_len:
      max_len = s_len

    if i > 0:
      phrases_file.write("\n")
    phrases_file.write(s)
  phrases_file.close()

  if length == 0:
    length = max_len

  ##### execution of srilm command line tool ###################################
  system("ngram-count -order %d -text %s -lm %s"%(length,
                                                  train_filename,
                                                  lm_filename))
  system("ngram -lm %s -order %s -ppl %s -debug 1 > %s"%(lm_filename,
                                                         length,
                                                         phrases_filename,
                                                         stat_filename))

  ##### statistics file parsing ################################################
  logprobs = {}
  stat_file = codecs.open(stat_filename, "r", encoding)
  stat_lines = stat_file.read().split("\n")[:-1]
  stat = []

  i = 0
  while i < len(stat_lines) - 3:
    if stat_lines[i] != "":
      stat.append("%s\n%s\n%s"%(stat_lines[i],
                                stat_lines[i + 1],
                                stat_lines[i + 2]))

      i += 3
    else:
      i += 1

  for probs in stat:
    term_stat_probs = probs.split("\n")
    term = term_stat_probs[0]
    logprob = float(term_stat_probs[2].split()[3])

    logprobs[term] = logprob

  stat_file.close()

  ##### removing temp files ####################################################
  remove(train_filename)
  remove(phrases_filename)
  remove(lm_filename)
  remove(stat_filename)

  return logprobs

