import unittest

from keybench.main import core

class KBBenchmarkTests(unittest.TestCase):
  def testInitialization(self):
    self.failUnless(core.KBBenchmark.singleton().run_configurations == {})
    self.failUnless(core.KBBenchmark.singleton().run_tools == {})
    self.failUnless(core.KBBenchmark.singleton().run_resources == {})
    self.failUnless(core.KBBenchmark.singleton().run_threads == {})

  def testModification(self):
    core.KBBenchmark.singleton().run_configurations["run"] = "Dummy configuration"
    core.KBBenchmark.singleton().run_tools["run"] = "Dummy tool"
    core.KBBenchmark.singleton().run_resources["run"] = "Dummy resource"
    core.KBBenchmark.singleton().run_threads["run"] = 1

    self.failUnless(core.KBBenchmark.singleton().run_configurations == {"run": "Dummy configuration"})
    self.failUnless(core.KBBenchmark.singleton().run_tools == {"run": "Dummy tool"})
    self.failUnless(core.KBBenchmark.singleton().run_resources == {"run": "Dummy resource"})
    self.failUnless(core.KBBenchmark.singleton().run_threads == {"run": 1})

    core.KBBenchmark.singleton().run_configurations = {"run": "Dummy configuration2"}
    core.KBBenchmark.singleton().run_tools = {"run": "Dummy tool2"}
    core.KBBenchmark.singleton().run_resources = {"run": "Dummy resource2"}
    core.KBBenchmark.singleton().run_threads = {"run": 2}

    self.failUnless(core.KBBenchmark.singleton().run_configurations == {"run": "Dummy configuration2"})
    self.failUnless(core.KBBenchmark.singleton().run_tools == {"run": "Dummy tool2"})
    self.failUnless(core.KBBenchmark.singleton().run_resources == {"run": "Dummy resource2"})
    self.failUnless(core.KBBenchmark.singleton().run_threads == {"run": 2})

