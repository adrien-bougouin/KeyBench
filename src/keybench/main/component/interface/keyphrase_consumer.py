import exceptions

from keybench.main.component import component # avoid recursive import

class KBKeyphraseConsumerI(component.KBComponent):
  """The abstract component that make usage of extracted keyphrases.

  The component that uses extracted keyphrases (keyphrase evaluation, keyphrase
  indexing, word cloud creation, etc.). In most cases, subclasses must not
  override C{consumeKeyphrases()}, but only C{keyphraseConsumption()}.
  """

  def consumeKeyphrases(self, corpus, keyphrases):
    """Consumes the keyphrases associcated to the documents of a given corpus.

    Args:
      corpus: The C{KBCorpus} for which the keyphrases have been extracted.
      keyphrases: The extracted keyphrases (C{map} of C{list} of
        C{KBTextualUnit}s associated to a document's name).
    """

    self.logDebug("Consuming keyphrases of %s..."%(document.name))
    self._keyphraseConsumption(document)

  def _keyphraseConsumption(self, document):
    """Consumes the keyphrases associcated to the documents of a given corpus.

    Args:
      corpus: The C{KBCorpus} for which the keyphrases have been extracted.
      keyphrases: The extracted keyphrases (C{map} of C{list} of
        C{KBTextualUnit}s associated to a document's name).
    """

    raise exceptions.NotImplementedError()

