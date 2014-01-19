from keybench.main import exception

class KBTextualUnit(object):
  """A representation of a textual unit.

  A representation of a normalized textual unit along with its seen forms,
  occurrence information and linguistic information (tokens, lemmas, stems and
  POS tags). Seen forms and occurrence information are store per document in
  which the textual unit appears.

  Attributes:
    language: The C{string} name of the textual unit's language.
    normalized_form: The most generic C{string} form of the textual unit.
    tokens: The C{list} of the textual unit's tokens.
    lemmas: The C{list} of the textual unit's lemmas.
    stems: The C{list} of the textual unit's  stems.
    pos_tags: The C{list} of the textual unit's POS tags.
  """

  def __init__(self,
               language,
               normalized_form,
               tokens,
               lemmas,
               stems,
               pos_tags,):
    self._language = language
    self._normalized_form = normalized_form
    self._tokens = tokens
    self._lemmas = lemmas
    self._stems = stems
    self._pos_tags = pos_tags
    self._seen_forms = {}
    self._offsets = {}

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
      A C{list} of all the textual unit's seen forms paired with a list of their
      offsets, within the given C{document}.
    """

    return self._seen_forms[document].items()

  def offsets(self, document):
    """Access the offsets of the textual unit in a given document.
    
    Args:
      document: The C{string} identifier of the document from which to access
        the textual unit's offsets.

    Returns:
      A C{list} of all offsets of the textual unit, within the given
      C{document}.
    """

    return self._offsets[document]

  def addOccurrence(self, seen_form, document, offset):
    """Records another occurrence of the textual unit.

    Adds another occurrencei, within a C{document} of the textual unit
    identified by its C{normalized_form}.

    Args:
      seen_form: The C{string} representing the textual unit. It may differs
        from the C{normalized_form} (case, spelling, abbreviation, etc.).
      document: The C{string} identifier of the document it appears in.
      offset: The C{int} position of the C{seen_form} within the C{document}.
    """

    if document not in self._offsets:
      self._seen_forms[document] = {}
      self._offsets[document] = []

    if offset not in self._offsets[document]:
      self._offsets[document].append(offset)

      if seen_form not in self._seen_forms[document]:
        self._seen_forms[document][seen_form] = []
      self._seen_forms[document][seen_form].append(offset)
    else:
      raise exception.KBOffsetException("Already exists!",
                                        document,
                                        self._normalized_form,
                                        offset)

  def numberOfOccurrences(self, document):
    """Gives the number of time the textual unit appears within a given
    document.

    Args:
      document: The C{string} identifier of the document from which to get the
        number of occurrences.

    Returns:
      The number of occurrences of the textual unit within the C{document}.
    """

    return len(self._offsets[document])

  def numberOfDocuments(self):
    """Gives the number of documents where the textual unit appears.

    Returns:
      The number of documents where the textual unit appears.
    """

    return len(self._offsets)

