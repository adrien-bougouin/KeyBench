TopicRank \[1\] - TopicCoRank
===========================================================================

This work was supported by the French National Research Agency (TermITH project
-- ANR-12-CORD-0029).

# Requirements

The project is developed in Python (2.6.6 or later) and makes use of third party
tools:
- NLTK \[2\] (python Natural Language Tool Kit --
  [to install](https://pypi.python.org/pypi/nltk/2.0.4))
- Stanford POS tagger \[3\] (java software -- included)
- Bonsai word tokenizer (perl command line tool used by the Bonsai PCFG-LA
  parser -- included)
- MElt POS tagger \[4\] (python french POS tagger --
  [to install](http://ressources.labex-efl.org/melt))

# Usage

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
Their is one directory for each processing step: `pre_processings/CORPUS_NAME`
(POS tagging), `candidates/CORPUS_NAME` (candidate selection),
`clusters/CORPUS_NAME` (candidate clustering), `rankings/CORPUS_NAME` (candidate
ranking), `selections/CORPUS_NAME` (keyphrase identification) and
`evaluation/CORPUS_NAME` (evaluation). They are used for lazy processing of
already done steps (e.g. POS tagging), but a readable version can be found in a
sub-directory name `string`.

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

