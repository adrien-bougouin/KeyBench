from keybench.main import component
from keybench.main import core
from keybench.main import model
from keybench.main import exception

def launch(run_configurations):
  benchmark = core.KBBenchmark.singleton()
  benchmark.run_configurations = run_configurations

  benchmark.start()

