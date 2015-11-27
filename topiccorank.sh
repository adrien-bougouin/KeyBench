#!/usr/bin/env sh
# -*- encoding: utf-8 -*-

ROOT_DIR=$(dirname $0)

options=""
corpus=""
language=""

if [ $# -gt 2 ]
then
  while [ $# -gt 3 ]
  do
    key="$1"

    case $key in
      -n|--run-name)
        options="${options} -n $2 "
        shift
        shift
      ;;
      -r|--reference)
        options="${options} -r $2 "
        shift
        shift
      ;;
      -o|--output-dir)
        options="${options} -o $2 "
        shift
        shift
      ;;
      -p|--processus-number)
        options="${options} -p $2 "
        shift
        shift
      ;;
      *)
        shift
      ;;
    esac
  done

  if [ $# -eq 3 ]
  then
    corpus="$1"
    options="${options} -t $2"
    language="$3"

    python ${ROOT_DIR}/KeyBench/src/launcher.py ${options} TopicCoRank ${corpus} ${language}
  else
    echo "missing positional argument..."
    echo ""
    echo "usage: sh $0 [options] corpus training_references language"
    echo ""
    echo "positional arguments:"
    echo "    corpus                path to the .txt files to process"
    echo "    training_references   pathto the file containing training references"
    echo "    language              language of the corpus files (french or english)"
    echo ""
    echo "optional arguments:"
    echo "    -h, --help            show this help message and exit"
    echo "    -n RUN_NAME, --run-name RUN_NAME"
    echo "                          name of the run (for identification within the output"
    echo "                          directory)"
    echo "    -r REFERENCE_FILEPATH, --reference REFERENCE_FILEPATH"
    echo "                          path to the file containing the references (for"
    echo "                          evaluation only)"
    echo "    -o OUTPUT_DIR, --output-dir OUTPUT_DIR"
    echo "                          path to the directory where processings must be stored"
    echo "                          (default=results)"
    echo "    -p PROCESSUS_NUMBER, --processus-number PROCESSUS_NUMBER"
    echo "                          number of documents to process simultaneously"
  fi
else
  echo "usage: sh $0 [options] corpus training_references language"
  echo ""
  echo "positional arguments:"
  echo "    corpus                path to the .txt files to process"
  echo "    training_references   pathto the file containing training references"
  echo "    language              language of the corpus files (french or english)"
  echo ""
  echo "optional arguments:"
  echo "    -h, --help            show this help message and exit"
  echo "    -n RUN_NAME, --run-name RUN_NAME"
  echo "                          name of the run (for identification within the output"
  echo "                          directory)"
  echo "    -r REFERENCE_FILEPATH, --reference REFERENCE_FILEPATH"
  echo "                          path to the file containing the references (for"
  echo "                          evaluation only)"
  echo "    -o OUTPUT_DIR, --output-dir OUTPUT_DIR"
  echo "                          path to the directory where processings must be stored"
  echo "                          (default=results)"
  echo "    -p PROCESSUS_NUMBER, --processus-number PROCESSUS_NUMBER"
  echo "                          number of documents to process simultaneously"
fi

