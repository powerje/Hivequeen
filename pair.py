#!/usr/bin/env python
#
# Copyright 2012 Steven Le (stevenle08@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Pairs a certfiicate with a Google TV server."""

__author__ = 'stevenle08@gmail.com (Steven Le)'

import optparse
import os
import shlex
import subprocess
import time
import googletv


def get_parser():
  """Creates an optparse.OptionParser object used by this script."""
  usage = 'Usage: %prog [--host=] [--port=9552] [--cert=cert.pem]'
  parser = optparse.OptionParser(usage=usage)

  parser.add_option(
      '--cert',
      default='cert.pem',
      help='Path to cert file.')

  parser.add_option(
      '--host',
      default='NSZGT1-6131194.local',
      help='Host of the Google TV server.')

  parser.add_option(
      '--port',
      default=9552,
      type='int',
      help='Port number.')

  return parser


def generate_cert(filename, country='US', state='CA', city='Mountain View',
                  cn='anymote\/python\/googletv'):
  """Generates a self-signed certificate."""
  kwargs = {
      'city': city,
      'cn': cn,
      'country': country,
      'filename': filename,
      'state': state,
  }
  command = [
      'openssl req -x509 -nodes -days 365',
      '-subj \'/C=%(country)s/ST=%(state)s/L=%(city)s/CN=%(cn)s\'',
      '-newkey rsa:1024 -keyout %(filename)s -out %(filename)s',
  ]
  command = ' '.join(command) % kwargs
  args = shlex.split(command)
  subprocess.call(args)

class Pair():

    def __init__(self):
        self.pairing_code = None

    def connect(self, host, cert, port=9552):
      global pairing_code
      if not os.path.isfile(cert):
        generate_cert(cert)

      print 'Initiating pairing...'
      with googletv.PairingProtocol(host, cert, port=port) as gtv:
        client_name = host
        gtv.send_pairing_request(client_name)
        gtv.recv_pairing_request_ack()
        gtv.send_options()
        gtv.recv_options()
        gtv.send_configuration()
        gtv.recv_configuration_ack()

        # Block until pairing_code is set
        while self.pairing_code is None:
            time.sleep(1)

        gtv.send_secret(self.pairing_code)

        to_hex = lambda byte_str: ''.join(['%02X' % ord(x) for x in byte_str])
        try:
          secret = to_hex(gtv.recv_secret_ack().secret)
          print 'Success! Received secret (hash) from Google TV: %s' % secret
        except:
          print 'Pairing failed'

def main():
  parser = get_parser()
  options = parser.parse_args()[0]
  host = options.host
  port = options.port
  cert = options.cert
  if not os.path.isfile(cert):
    generate_cert(cert)

  print 'Initiating pairing...'
  with googletv.PairingProtocol(host, cert, port=port) as gtv:
    client_name = raw_input('Client name: ')
    gtv.send_pairing_request(client_name)
    gtv.recv_pairing_request_ack()
    gtv.send_options()
    gtv.recv_options()
    gtv.send_configuration()
    gtv.recv_configuration_ack()
    code = raw_input('Code from Google TV: ')
    gtv.send_secret(code)

    to_hex = lambda byte_str: ''.join(['%02X' % ord(x) for x in byte_str])
    try:
      secret = to_hex(gtv.recv_secret_ack().secret)
      print 'Success! Received secret (hash) from Google TV: %s' % secret
    except:
      print 'Pairing failed'


if __name__ == '__main__':
  main()
