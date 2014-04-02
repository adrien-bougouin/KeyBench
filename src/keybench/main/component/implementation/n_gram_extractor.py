from keybench.main import core
from keybench.main import model
from keybench.main.component import interface

class NGramExtractor(interface.KBCandidateExtractorI):
  """N-gram candidate extractor.

  Attributes:
    n: The maximum word size of a candidate.
  """

  def __init__(self,
               name,
               run_name,
               shared,
               lazy_mode,
               debug_mode,
               root_cache,
               n):
    """Constructor.

    Args:
      name: The C{string} name of the component.
      run_name: The C{string} name of the run for which the component is
        affected to.
      shared: True if the component shares informations with equivalent
        components (same name).
      lazy_mode: True if the component load precomputed data. False, otherwise.
      debug_mode: True if the component can log debug messages. False,
        otherwise.
      root_cache: The root of the cache directory where the cached objects must
        be stored.
      n: The maximum word size of a candidate.
    """

    super(NGramExtractor, self).__init__()

    self._n = n

  @property
  def n(self):
    return self._n

  def _candidateExtraction(self, document):
    """Extracts the candidates of a given document.

    Args:
      document: The C{KBDocument} from which the candidates must be extracted.

    Returns:
      The C{list} of extracted, and filtered, candidates (C{KBTextualUnit}s).
    """

    tokenized_sentences = document.full_text_sentence_tokens()
    pos_tagged_sentences = document.full_text_token_pos_tags()
    candidates = {}

    ## NLP tools ###############################################################
    tool_factory = core.KBBenchmark.singleton().run_tools[self._run_name]
    normalizer = tool_factory.normalizer(document.language)
    lemmatizer = tool_factory.lemmatizer(document.language)
    stemmer = tool_factory.stemmer(document.language)
    ############################################################################

    # extract sentences' n-grams
    for sentence_offset, tokenized_sentence in enumerate(tokenized_sentences):
      pos_tagged_sentence = pos_tagged_sentences[sentence_offset]

      # extract word lists of size up to n
      for n in range(1, self._n + 1):
        for i in range(n, len(tokenized_sentence) + 1):
          inner_sentence_offset = i - n
          n_gram = " ".join(tokenized_sentence[inner_sentence_offset:i])
          n_gram_seen_form = n_gram # FIXME tokenized form, not seen form :{
          n_gram_normalized_form = normalizer.normalize(n_gram)
          n_gram_normalized_tokens = n_gram_normalized_form.split(" ")
          n_gram_pos_tags = pos_tagged_sentence[inner_sentence_offset:i]

          # identify the candidates using the POS tags, so same normalized forms
          # with different POS tags are considered as different candidates
          n_gram_id = "%s%s"%(n_gram_normalized_form, str(n_gram_pos_tags))
          # create the textual unit if no existing candidate matches it
          if n_gram_id not in candidates:
            # compute the n-gram's lemmas and stems
            n_gram_normalized_lemmas = []
            n_gram_normalized_stems = []
            for word in n_gram_normalized_tokens:
              n_gram_normalized_lemmas.append(lemmatizer.lemmatize(word))
              n_gram_normalized_stems.append(stemmer.stem(word))

            candidates[n_gram_id] = model.KBTextualUnit(document.corpus_name,
                                                        document.language,
                                                        n_gram_normalized_form,
                                                        n_gram_normalized_tokens,
                                                        n_gram_normalized_lemmas,
                                                        n_gram_normalized_stems,
                                                        n_gram_pos_tags)
          candidates[n_gram_id].addOccurrence(n_gram_seen_form,
                                              document.name,
                                              sentence_offset,
                                              inner_sentence_offset)

    return candidates.values()

