# -*- encoding: utf-8 -*-

from keybench.main import exception

class KBTextualUnit(object):
  """A representation of a textual unit.

  A representation of a normalized textual unit along with its seen forms,
  occurrence information and linguistic information (tokens, lemmas, stems and
  POS tags).

  Attributes:
    corpus_name: The C{string} name of the corpus from which the textual unit is
      extracted.
    language: The C{string} name of the textual unit's language (see
      C{keybench.main.language_support.KBLanguage}).
    normalized_form: The most generic C{string} form of the textual unit.
    normalized_tokens: The C{list} of the textual unit's normalized tokens.
    normalized_lemmas: The C{list} of the textual unit's normalized lemmas.
    normalized_stems: The C{list} of the textual unit's  normalized stems.
    pos_tags: The C{list} of the textual unit's POS tags.
    seen_forms: The C{string} seen forms associated to their offset positions
      (C{map} of C{map} of C{list} of C{int}, where the second map as the
      sentence offsets as keys and the inner sentence offsets as values).
    offsets: The offsets of the textual unit (C{map} of C{map} of C{list} of
      C{int}, where the second map as the sentence offsets as keys and the inner
      sentence offsets as values).
  """

  def __init__(self,
               corpus_name,
               language,
               normalized_form,
               normalized_tokens,
               normalized_lemmas,
               normalized_stems,
               pos_tags):
    super(KBTextualUnit, self).__init__()

    self._corpus_name = corpus_name
    self._language = language
    self._normalized_form = normalized_form
    self._normalized_tokens = normalized_tokens
    self._normalized_lemmas = normalized_lemmas
    self._normalized_stems = normalized_stems
    self._pos_tags = pos_tags
    self._seen_forms = {}
    self._offsets = {}

  def __eq__(self, other):
    return self._corpus_name == other.corpus_name \
           and self._language == other._language \
           and self._normalized_form == other._normalized_form \
           and self._normalized_tokens == other._normalized_tokens \
           and self._normalized_lemmas == other._normalized_lemmas \
           and self._normalized_stems == other._normalized_stems \
           and self._pos_tags == other._pos_tags \
           and self._seen_forms == other._seen_forms \
           and self._offsets == other._offsets

  def __ne__(self, other):
    return not self.__eq__(other)

  @property
  def corpus_name(self):
    return self._corpus_name

  @property
  def language(self):
    return self._language

  @property
  def normalized_form(self):
    return self._normalized_form

  @property
  def normalized_tokens(self):
    return self._normalized_tokens

  @property
  def normalized_lemmas(self):
    return self._normalized_lemmas

  @property
  def normalized_stems(self):
    return self._normalized_stems

  @property
  def pos_tags(self):
    return self._pos_tags

  @property
  def seen_forms(self):
    return self._seen_forms

  @property
  def offsets(self):
    return self._offsets

  def addOccurrence(self,
                    seen_form,
                    sentence_offset,
                    inner_sentence_offset):
    """Records another occurrence of the textual unit.

    Adds another occurrence of the textual unit.

    Args:
      seen_form: The C{string} representing the textual unit. It may differs
        from the C{normalized_form} (case, spelling, abbreviation, etc.).
      sentence_offset: The C{int} sentence position of the C{seen_form}.
      inner_sentence_offset: The C{int} position of the C{seen_form} within the
        sentence.

    Raises:
      KBOffsetException: An exception occurred when the offset is already.
    """

    if sentence_offset not in self._offsets \
       or inner_sentence_offset not in self._offsets[sentence_offset]:
      if sentence_offset not in self._offsets:
        self._offsets[sentence_offset] = []
      self._offsets[sentence_offset].append(inner_sentence_offset)

      if seen_form not in self._seen_forms:
        self._seen_forms[seen_form] = {}
      if sentence_offset not in self._seen_forms[seen_form]:
        self._seen_forms[seen_form][sentence_offset] = []
      self._seen_forms[seen_form][sentence_offset].append(inner_sentence_offset)
    else:
      raise exception.KBOffsetException(sentence_offset,
                                        inner_sentence_offset,
                                        self._normalized_form,
                                        "Already exists!")

  def numberOfOccurrences(self):
    """Gives the number of time the textual unit appears.

    Returns:
      The number of occurrences of the textual unit.
    """

    number_of_occurrences = 0

    for sentence in self._offsets:
      number_of_occurrences += len(self._offsets[sentence])

    return number_of_occurrences

