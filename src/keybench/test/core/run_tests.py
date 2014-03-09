import unittest

from keybench.main import core

class KBRunTests(unittest.TestCase):

  def setUp(self):
    self._run = core.KBRun("test_run")

  def tearDown(self):
    self._run = None

  def testInitialization(self):
    self.failUnless(self._run.name == "test_run")

  def testEqual(self):
    run1 = core.KBRun("test_run")
    run2 = core.KBRun("another_test_run")

    self.failUnless(self._run == run1)
    self.failIf(self._run == run2)

  def testNotEqual(self):
    run1 = core.KBRun("test_run")
    run2 = core.KBRun("another_test_run")

    self.failIf(self._run != run1)
    self.failUnless(self._run != run2)

