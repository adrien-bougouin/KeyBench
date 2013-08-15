TopicRank: Graph-Based Topic Ranking fo Keyphrase Extraction [1]
===========================================================================

This is the work presented in the 6th International Joint
Conference on Natural Language Processing (IJCNLP).

Purpose
-------

The provided source code and command line tool aim to ease the reproduction and
usage of TopicRank and a few implemented baselines. Four keyphrase extraction
datasets (from various sources:
https://github.com/snkim/AutomaticKeyphraseExtraction;
https://github.com/adrien-bougouin/WikinewsKeyphraseCorpus) are also included
and used for evaluation purpose.

The command line tool <code>ijcnlp\_2013.py</code> allows to either execute the
experiments given in [1].

Usage
-----

### requirements

The project is developed in Python (2.6.6 or later) and makes use of third party
tools:
- NLTK \[2\] (python Natural Language Tool Kit)
- Stanford POS tagger \[3\] (java software -- included)
- Bonsai word tokenizer (perl command line tool used by the Bonsai PCFG-LA
  parser -- included)
- MElt POS tagger \[4\] (python french POS tagger -- not included)

### TopicRank evaluation settings

One can choose to execute TopicRank for either inspec, semeval, wikinews, deft
or all of these datasets:

    python ijcnlp_2013.py all|inspec|semeval|wikinews|deft

### Processing new evaluation datasets

One can shoose to execute TopicRank for a new (english or french) dataset:

    python ijcnlp_2013.py <corpus_directory> <reference_file> <language>

- <code>corpus\_directory</code> must contain the plain text ".txt" files
  composing the dataset
- <code>reference\_file</code> must contain the reference keyphrases per each
  document of the dataset:

        file1.txt + tabulation + semi-column separated keyphrases
        file2.txt + tabulation + semi-column separated keyphrases
        ...
        filen.txt + tabulation + semi-column separated keyphrases
    
- <code>language</code> must be set to either <code>english</code> or
  <code>french</code>

### Output

<code>ijcnlp\_2013.py</code> create a directory named <code>results</code>
containing one directory per processing step:
- <code>pre\_processings</code>: contains the pre-processed documents of each
  analysed dataset
- <code>candidates</code>: contains the candidates extracted from the documents
  of each analysed dataset
- <code>clusters</code>: contains the clustered candidates of the documents of
  each dataset
- <code>rankings</code>: contains the ranked candidates of the documents of each
  dataset
- <code>selections</code>: contains the candidates selected as keyphrases for
  each document of each dataset
- <code>evaluations</code>: contains the results of the evaluation for each
  methods and each dataset

These directories contain serialized files (<code>pickle</code>) used for lazy
loading, as well as a readable version of them in a <code>string</code>
directory.

References
----------

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

