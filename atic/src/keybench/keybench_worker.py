#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from multiprocessing import Process

##### Multi-processing #########################################################

def keybench_worker(queue):
  """
  Executes one keyphrase extractor contained in a given queue.

  @param  queue: The queue containing the keyphrase extractor.
  @type   queue: C{multiprocessing.Queue}
  """

  keyphrase_extractor = queue.get()

  keyphrase_extractor.extract_keyphrases()

################################################################################

class KeyBenchWorker(Process):
  """
  Process launching the keyphrase extraction workflow. This class is used to
  allow easy multi-processing. The KeyBenchWorker execute the keyphrase extrator
  that are push into a given queue.
  """

  def __init__(self, queue):
    """
    Constructor.

    @param  queue: The queue containing the keyphrase extractor.
    @type   queue: C{multiprocessing.Queue}
    """

    super(KeyBenchWorker, self).__init__(target=keybench_worker, args=(queue,))

