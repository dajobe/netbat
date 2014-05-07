#!/usr/bin/env python
""" Receive data """

import argparse
import socket
import hashlib

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

    args = parser.parse_args()

    debug = args.debug
    host = args.host
    port = args.port

    # Main code
    BUFFER_SIZE = 1024

    mm = MessageMaker()

    s = None
    conn = None
    count = 0
    try:
      print 'Listening on {host}:{port}'.format(host=host, port=port)
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.bind((host, port))
      s.listen(1)

      conn, addr = s.accept()
      print 'Accepted connection on address: {addr}'.format(addr=str(addr))
      while True:
          data = None
          try:
              data = conn.recv(BUFFER_SIZE)
          except Exception, e:
              data = None
              print "recv() failed with exception {exc}".format(str(e))
              raise e
          if data is None or len(data) == 0:
              break

          (edata, edigest) = mm.message()
          m = hashlib.md5()
          m.update(data)
          digest = m.hexdigest()
          if len(data) != len(edata):
              print "{count}: FAIL size mismatch - got {size} bytes expected {esize} bytes".format(count=count, size=len(data), esize=len(edata))
          elif digest != edigest:
              print "{count}: FAIL digest mismatch - got {digest} expected {edigest} (size {size})".format(count=count, size=len(data), digest=digest, edigest=edigest)
          else:
              print "{count}: OK".format(count=count)
          count += 1
    except Exception, e:
        raise e
    finally:
        if conn is not None:
            conn.close()
        if s is not None:
            s.close()

if __name__ == '__main__':
    main()
