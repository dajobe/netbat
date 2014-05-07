#!/usr/bin/env python
""" Send data 

License: see UNLICENSE

"""

import argparse
import socket
import hashlib
import time
import random
import string
import errno

from common import MessageMaker

def main():
    """Main method"""

    parser = argparse.ArgumentParser(description='Receive data.')
    parser.add_argument('-d', '--debug',
                        action = 'store_true',
                        default = False,
                        help = 'debug messages (default: False)')
    parser.add_argument('-H', '--host',
                        default = '127.0.0.1',
                        help = 'hostname (default 127.0.0.1)')
    parser.add_argument('-p', '--port',
                        type = int,
                        default = 5005,
                        help = 'port (default 5005')
    parser.add_argument('-c', '--corrupt',
                        action = 'store_true',
                        default = False,
                        help = 'corrupt data? (default false')

    args = parser.parse_args()

    debug = args.debug
    host = args.host
    port = args.port
    corrupt = args.corrupt

    if corrupt:
        print '*** Will corrupt data ***'

    # Main code
    mm = MessageMaker()

    s = None
    try:
      print 'Connecting to {host}:{port}'.format(host=host, port=port)
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((host, port))
      count = 0
      while True:
          (data, digest) = mm.message()

          print "{count}: Sending {size} bytes data digest {digest}".format(count=count, size=len(data), digest=digest)

          if corrupt:
              if random.random() > 0.7:
                  offset = random.randint(0, len(data)-1)
                  print "  Corrupting message"
                  ndata = list(data)
                  what = random.randint(1, 3)
                  if what == 1:
                      ndata[offset] = '!'
                  elif what == 2:
                      del ndata[offset]
                  else:
                      ndata.append(random.choice(string.letters + string.digits))
                  data = ''.join(ndata)

          s.send(data)
          count += 1

          time.sleep(1)

    except socket.error, e:
        if e.errno == errno.ECONNREFUSED:
            print "ERROR: Connection refused - is the receiver running on {host}:{port} ? ".format(host=host, port=port)
        else:
            raise e

    except KeyboardInterrupt:
        # ^C - exit silently
        pass

    except Exception, e:
        raise e

    finally:
        if s is not None:
            s.close()

if __name__ == '__main__':
    main()
