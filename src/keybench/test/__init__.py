import unittest

from keybench.test import component
from keybench.test import core
from keybench.test import model
from keybench.test import nlp_tool

def runTests():
  testLoader = unittest.TestLoader()
  testSuite = unittest.TestSuite()

  # adds tests from the keybench test modules
  testSuite.addTests(testLoader.loadTestsFromModule(component))
  testSuite.addTests(testLoader.loadTestsFromModule(core))
  testSuite.addTests(testLoader.loadTestsFromModule(model))
  testSuite.addTests(testLoader.loadTestsFromModule(nlp_tool))

  # executes all the tests
  unittest.TextTestRunner(verbosity=2).run(testSuite)

