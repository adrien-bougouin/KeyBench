# -*- encoding: utf-8 -*-

from keybench.main.component import component

class StemFilter(component.KBKeyphraseExtractorI.RedundancyFilter):
  """A filter that considers redundant two keyphrases having the same stems.
  """

  def areRedundant(self, textual_unit1, textual_unit2):
    """Checks if two textual units are redundant.

    Args:
      textual_unit1: The first C{KBTextualUnit} to check.
      textual_unit2: The second C{KBTextualUnit} to check.

    Returns:
      True if the C{textual_unit}s are redundant. False, otherwise.
    """

    return textual_unit1.normalized_stems == textual_unit2.normalized_stems

