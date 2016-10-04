TopicRank \[1\] - TopicCoRank \[6\]
===========================================================================

This is the work presented in the 26th International Conference on Computational Linguistics (COLING 2016).
This work was supported by the French National Research Agency (TermITH project -- ANR-12-CORD-0029).

# Purpose

The provided source code and command line tool aim to ease the reproduction and usage of TopicCoRank.
You will also find the subset listing to reconstruct our dataset from recently published DEFT-2016 dataset \[5\].

# Requirements

The project is developed in Python (2.6.6 or later) and makes use of third party
tools:
- NLTK-2.0.4 \[2\] ([python Natural Language Tool Kit](https://pypi.python.org/pypi/nltk/2.0.4)): `sudo pip install http://pypi.python.org/packages/source/n/nltk/nltk-2.0.4.tar.gz`
- LXML: `sudo pip install lxml`
- NetworkX: `sudo pip install networkx`
- MElt POS tagger \[4\] (python french POS tagger --
  [to install](http://ressources.labex-efl.org/melt))
- Stanford POS tagger \[3\] (java software -- included)
- Bonsai word tokenizer (perl command line tool used by the Bonsai PCFG-LA
  parser -- included)

# Usage

## TopicCoRank

To process a corpus of plain text (.txt) files with TopicCoRank, one can use:
```
  usage: sh topiccorank.sh [options] corpus training_references language

  positional arguments:
    corpus                path to the .txt files to process
    training_references   pathto the file containing training references
    language              language of the corpus files (french or english)

  optional arguments:
    -h, --help            show this help message and exit
    -n RUN_NAME, --run-name RUN_NAME
                          name of the run (for identification within the output
                          directory)
    -r REFERENCE_FILEPATH, --reference REFERENCE_FILEPATH
                          path to the file containing the references (for
                          evaluation only)
    -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                          path to the directory where processings must be stored
                          (default=results)
    -p PROCESSUS_NUMBER, --processus-number PROCESSUS_NUMBER
                          number of documents to process simultaneously
  
```

## TopicRank

To process a corpus of plain text (.txt) files with TopicRank \[1\], one can
use:
```
  usage: sh topicrank.sh [options] corpus language

  positional arguments:
    corpus                path to the .txt files to process
    language              language of the corpus files (french or english)

  optional arguments:
    -h, --help            show this help message and exit
    -n RUN_NAME, --run-name RUN_NAME
                          name of the run (for identification within the output
                          directory)
    -r REFERENCE_FILEPATH, --reference REFERENCE_FILEPATH
                          path to the file containing the references (for
                          evaluation only)
    -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                          path to the directory where processings must be stored
                          (default=results)
    -p PROCESSUS_NUMBER, --processus-number PROCESSUS_NUMBER
                          number of documents to process simultaneously
```

# Format

## Corpus documents

The documents of the corpus must be in plain text. The document files must have
the ".txt" extension.

## Reference and training reference files

A reference file is a list of documents associated with keyphrases:
```
  document_name1.txt<TAB>semi-column separated keyphrases
  document_name2.txt<TAB>semi-column separated keyphrases
  ...
  document_name3.txt<TAB>semi-column separated keyphrases
```

## Outputs

The results of every processing steps are serialized in an output directory.
Their is one directory for each processing step: `pre_processings/<run_or_corpus_name>`
(POS tagging), `candidates/<run_or_corpus_name><method_name>` (candidate selection),
`clusters/<run_or_corpus_name><method_name>` (candidate clustering),
`rankings/<run_or_corpus_name><method_name>` (candidate ranking),
`selections/<run_or_corpus_name><method_name>` (keyphrase identification) and
`evaluation/<run_or_corpus_name><method_name>` (evaluation). They are used for lazy
processing of already done steps (e.g. POS tagging), but a readable version
can be found in a sub-directory name `string`.

# References

[1] Adrien Bougouin, Florian Boudin and Béatrice Daille. 2013. Topicrank:
Graph-Based Topic Ranking for keyphrase Extraction. In Proceedings of the
6th International Joint Conference on Natural Language Processing (IJCNLP),
Nagoya, Japan, October.

[2] Stephen Bird, Ewan Klein and Edward Loper. 2009. Natural Language
Processing with Python. O'Reilly Media.

[3] Kristina Toutanova, Dan Klein, Christopher D. Manning and Yoram Singer.
2003. Feature-Rich Part-of-Speech Tagging with a Cyclic Dependency Network.
In Proceedings of the 2003 Conference of the North American Chapter of the
Association for Computational Linguistics on Human Language
Technology - Volume 1, pages 173-180, Stroudsburg, PA, USA. Association for
Computational Linguistics.

[4] Pascal Denis and Benoît Sagot. 2009. Coupling an Annotated Corpus and a
Morphosyntactic Lexicon for State-of-the-Art POS tagging with Less Human
Effort. In Proceedings of the 23rd Pacific Asia Conference on Language,
Information and Computation (PACLIC), pages 110-119, Hong Kong, December.
City University of Hong Kong.

[5] Béatrice Daille, Sabine Barreaux, Florian Boudin, Adrien Bougouin, Damien Cram, et Amir Hazem. 2016.
Indexation d'articles scientifiques : Présentation et résultats du défi fouille de textes DEFT 2016.
In Défi fouille de textes (DEFT), Paris, France.

[1] Adrien Bougouin, Florian Boudin and Béatrice Daille. 2016.
Keyphrase Annotation with Graph Co-Ranking. In Proceedings of the
26th International Conference on Computational Linguistics (COLING),
Osaka, Japan, December.
