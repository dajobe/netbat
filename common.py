""" common code for natbatpy """

import hashlib
import random
import string


class MessageMaker(object):
  """ Create a sequence of messages from random data """

  # Default seed if none given
  SEED = 1331

  def __init__(self, seed = None):
    """ Construct object with optional random int seed """
    if seed is None:
      seed = self.SEED
    self.seed = seed
    self.counter = 0
    self.r = random.Random()

    self.r.seed(seed)

  def message(self):
    """Generate a (message, hash) tuple"""

    rsize = self.r.randint(1, 1024)
    rdata = ''.join(self.r.choice(string.letters + string.digits) for x in range(rsize))

    data = "Hello, World {c} {d}".format(c=self.counter, d=rdata)

    m = hashlib.md5()
    m.update(data)
    digest = m.hexdigest()

    self.counter += 1

    return (data, digest)
