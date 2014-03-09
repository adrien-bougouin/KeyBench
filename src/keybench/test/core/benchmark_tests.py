import unittest

from keybench.main import core

class KBBenchmarkTests(unittest.TestCase):
  def testInitialization(self):
    self.failUnless(core.KBBenchmark.singleton().run_configurations == {})

  def testModification(self):
    core.KBBenchmark.singleton().run_configurations["run"] = "Dummy configuration"

    self.failUnless(core.KBBenchmark.singleton().run_configurations == {"run": "Dummy configuration"})

    core.KBBenchmark.singleton().run_configurations = {"run": "Dummy configuration2"}

    self.failUnless(core.KBBenchmark.singleton().run_configurations == {"run": "Dummy configuration2"})

