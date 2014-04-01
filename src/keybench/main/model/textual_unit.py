from keybench.main import exception

class KBTextualUnit(object):
  """A representation of a textual unit.

  A representation of a normalized textual unit along with its seen forms,
  occurrence information and linguistic information (tokens, lemmas, stems and
  POS tags). Seen forms and occurrence information are store per document in
  which the textual unit appears.

  Attributes:
    corpus_name: The C{string} name of the corpus from which the textual unit is
      extracted.
    language: The C{string} name of the textual unit's language (see
      C{keybench.main.language_support.KBLanguage}).
    normalized_form: The most generic C{string} form of the textual unit.
    tokens: The C{list} of the textual unit's tokens.
    lemmas: The C{list} of the textual unit's lemmas.
    stems: The C{list} of the textual unit's  stems.
    pos_tags: The C{list} of the textual unit's POS tags.
  """

  def __init__(self,
               corpus_name,
               language,
               normalized_form,
               tokens,
               lemmas,
               stems,
               pos_tags):
    super(KBTextualUnit, self).__init__()

    self._corpus_name = corpus_name
    self._language = language
    self._normalized_form = normalized_form
    self._tokens = tokens
    self._lemmas = lemmas
    self._stems = stems
    self._pos_tags = pos_tags
    self._seen_forms = {}
    self._offsets = {}

  def __eq__(self, other):
    return self._corpus_name == other.corpus_name \
           and self._language == other._language \
           and self._normalized_form == other._normalized_form \
           and self._tokens == other._tokens \
           and self._lemmas == other._lemmas \
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
  def tokens(self):
    return self._tokens

  @property
  def lemmas(self):
    return self._lemmas

  @property
  def stems(self):
    return self._stems

  @property
  def pos_tags(self):
    return self._pos_tags

  def seen_forms(self, document):
    """Access the seen forms of the textual unit in a given document.
    
    Args:
      document: The C{string} identifier of the document from which to access
        the textual unit's seen forms.

    Returns:
      A C{map} of C{list} of all offsets of the textual unit's seen form
      associated to the index of a sentence, within the given C{document}.
    """

    return self._seen_forms[document].items()

  def offsets(self, document):
    """Access the offsets of the textual unit in a given document.
    
    Args:
      document: The C{string} identifier of the document from which to access
        the textual unit's offsets.

    Returns:
      A C{map} of C{list} of all offsets of the textual unit associated to the
      index of a sentence, within the given C{document}.
    """

    return self._offsets[document]

  def addOccurrence(self,
                    seen_form,
                    document,
                    sentence_offset,
                    inner_sentence_offset):
    """Records another occurrence of the textual unit.

    Adds another occurrencei, within a C{document} of the textual unit
    identified by its C{normalized_form}.

    Args:
      seen_form: The C{string} representing the textual unit. It may differs
        from the C{normalized_form} (case, spelling, abbreviation, etc.).
      document: The C{string} identifier of the document it appears in.
      sentence_offset: The C{int} sentence position of the C{seen_form} within
        the C{document}.
      inner_sentence_offset: The C{int} position of the C{seen_form} within the
        C{document}'s sentence.

    Raises:
      KBOffsetException: An exception occurred when the offset is already
        recorded for the given document.
    """

    if document not in self._offsets:
      self._seen_forms[document] = {}
      self._offsets[document] = {}

    if sentence_offset not in self._offsets[document] \
       or inner_sentence_offset not in self._offsets[document][sentence_offset]:
      if sentence_offset not in self._offsets[document]:
        self._offsets[document][sentence_offset] = []
      self._offsets[document][sentence_offset].append(inner_sentence_offset)

      if seen_form not in self._seen_forms[document]:
        self._seen_forms[document][seen_form] = {}
      if sentence_offset not in self._seen_forms[document][seen_form]:
        self._seen_forms[document][seen_form][sentence_offset] = []
      self._seen_forms[document][seen_form][sentence_offset].append(inner_sentence_offset)
    else:
      raise exception.KBOffsetException(sentence_offset,
                                        inner_sentence_offset,
                                        self._normalized_form,
                                        document,
                                        "Already exists!")

  def numberOfOccurrences(self, document):
    """Gives the number of time the textual unit appears within a given
    document.

    Args:
      document: The C{string} identifier of the document from which to get the
        number of occurrences.

    Returns:
      The number of occurrences of the textual unit within the C{document}.
    """

    number_of_occurrences = 0

    for sentence in self._offsets[document]:
      number_of_occurrences += len(self._offsets[document][sentence])

    return number_of_occurrences

  def numberOfDocuments(self):
    """Gives the number of documents where the textual unit appears.

    Returns:
      The number of documents where the textual unit appears.
    """

    return len(self._offsets)

