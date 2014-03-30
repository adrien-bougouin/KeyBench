from keybench.main.core import run

class KBBenchmark(object):
  """The executor of a set of runs.

  The executor of a runs specified by names. No instance should be created,
  instead C{KBBenchmark.singleton()} must be called.

  Attributes:
    run_configurations: The run configurations (C{map} of C{string} name keys
      and C{KBComponentFactory} values).
    run_tools: The NLP tools to use in each run (C{map} of C{string} name keys
      and C{KBNLPToolFactory} values).
    run_resources: The NLP resources to use in each run (C{map} of C{string}
      name keys and C{KBNLPToolFactory} values).
  """

  __singleton_instance = None

  @classmethod
  def singleton(cls):
    if cls.__singleton_instance == None:
      cls.__singleton_instance = KBBenchmark()
    return cls.__singleton_instance

  def __init__(self):
    super(KBBenchmark, self).__init__()

    self._run_configurations = {}
    self._run_tools = {}
    self._run_resources = {}

  @property
  def run_configurations(self):
    return self._run_configurations

  @run_configurations.setter
  def run_configurations(self, value):
    self._run_configurations = value

  @property
  def run_tools(self):
    return self._run_tools

  @run_tools.setter
  def run_tools(self, value):
    self._run_tools = value

  @property
  def run_resources(self):
    return self._run_resources

  @run_resources.setter
  def run_resources(self, value):
    self._run_resources = value

  def start(self):
    """Executes every run.

    Executes every run. Runs are executed sequentially.
    """

    for run_name in self._run_configurations:
      run = run.KBRun(run_name)

      run.start()

