#!/usr/bin/env python
# -*- encoding: utf-8

import sys

import keybench
import run_factories

from keybench.main.factory.nlp_tool import french_nlp_tool_factory

################################################################################
# Main
################################################################################

def main(argv):
  keybench.launch(
    {"test_run": run_factories.TestRunFactory()},
    {"test_run": french_nlp_tool_factory.FrenchNLPToolFactory()},
    {"test_run": None}
  )

################################################################################
if __name__ == "__main__":
  main(sys.argv)

