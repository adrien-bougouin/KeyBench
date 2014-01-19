import unittest

from keybench.test import model

def runTests():
  testLoader = unittest.TestLoader()
  testSuite = unittest.TestSuite()

  # adds tests from the keybench test modules
  testSuite.addTests(testLoader.loadTestsFromModule(model))

  # executes all the tests
  unittest.TextTestRunner(verbosity=2).run(testSuite)

