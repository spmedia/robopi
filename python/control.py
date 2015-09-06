#!/usr/bin/env python

# Based on work by iRobot Corporation
###########################################################################
# Copyright (c) 2015 iRobot Corporation
# http://www.irobot.com/
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#   Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
#   Neither the name of iRobot Corporation nor the names
#   of its contributors may be used to endorse or promote products
#   derived from this software without specific prior written
#   permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###########################################################################
# Based on work at <http://blog.scphillips.com/posts/2012/12/a-simple-python-webserver/>

import socket
import re

import struct
import sys, glob
import serial

connection = None

class TetheredDriveApp():
    callbackKeyUp = False
    callbackKeyDown = False
    callbackKeyLeft = False
    callbackKeyRight = False
    callbackKeyLastDriveCommand = ''

    def __init__(self):
      host = ''
      port = 61338
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.bind((host, port))
      sock.listen(1)

      self.onConnect()

      while True:
          csock, caddr = sock.accept()
          req = csock.recv(1024)
          match = re.match('GET /api\?action=(\d|[A-Z]+)\sHTTP/1', req)
          motionChange = False
          if match:
              action = match.group(1)

              # KeyPress
              if action == 'PP':
                self.sendCommandASCII('128')
              elif action == 'PS':
                  self.sendCommandASCII('131')
              elif action == 'PF':
                  self.sendCommandASCII('132')
              elif action == 'PC':
                  self.sendCommandASCII('135')
              elif action == 'PD':
                  self.sendCommandASCII('143')
              elif action == 'PSPACE':
                  self.sendCommandASCII('140 3 1 64 16 141 3')
              elif action == 'PR':
                  self.sendCommandASCII('7')
              elif action == 'PUP':
                  self.callbackKeyUp = True
                  motionChange = True
              elif action == 'PDOWN':
                  self.callbackKeyDown = True
                  motionChange = True
              elif action == 'PLEFT':
                  self.callbackKeyLeft = True
                  motionChange = True
              elif action == 'PRIGHT':
                  self.callbackKeyRight = True
                  motionChange = True

              # KeyRelease
              elif action == 'RUP':
                  self.callbackKeyUp = False
                  motionChange = True
              elif action == 'RDOWN':
                  self.callbackKeyDown = False
                  motionChange = True
              elif action == 'RLEFT':
                  self.callbackKeyLeft = False
                  motionChange = True
              elif action == 'RRIGHT':
                  self.callbackKeyRight = False
                  motionChange = True

              if motionChange == True:
                velocity = 0
                if self.callbackKeyUp == True:
                    velocity += 200
                if self.callbackKeyDown == True:
                    velocity -= 200
                rotation = 0
                if self.callbackKeyLeft == True:
                    rotation += 300
                if self.callbackKeyRight == True:
                    rotation -= 300
                vr = velocity + (rotation/2)
                vl = velocity - (rotation/2)
                cmd = struct.pack(">Bhh", 145, vr, vl)
                if cmd != self.callbackKeyLastDriveCommand:
                    self.sendCommandRaw(cmd)
                    self.callbackKeyLastDriveCommand = cmd

                csock.sendall("""HTTP/1.0 200 OK
Content-Type: text/html

1
""")
          else:
              csock.sendall("""HTTP/1.0 200 OK
Content-Type: text/html

0
""")
          csock.close()

    # sendCommandASCII takes a string of whitespace-separated, ASCII-encoded base 10 values to send
    def sendCommandASCII(self, command):
        cmd = ""
        for v in command.split():
            cmd += chr(int(v))

        self.sendCommandRaw(cmd)

    # sendCommandRaw takes a string interpreted as a byte array
    def sendCommandRaw(self, command):
        global connection

        try:
            connection.write(command)
        except serial.SerialException:
            connection = None

    # getDecodedBytes returns a n-byte value decoded using a format string.
    # Whether it blocks is based on how the connection was set up.
    def getDecodedBytes(self, n, fmt):
        global connection

        try:
            return struct.unpack(fmt, connection.read(n))[0]
        except serial.SerialException:
            connection = None
            return None
        except struct.error:
            return None

    # get8Unsigned returns an 8-bit unsigned value.
    def get8Unsigned(self):
        return getDecodedBytes(1, "B")

    # get8Signed returns an 8-bit signed value.
    def get8Signed(self):
        return getDecodedBytes(1, "b")

    # get16Unsigned returns a 16-bit unsigned value.
    def get16Unsigned(self):
        return getDecodedBytes(2, ">H")

    # get16Signed returns a 16-bit signed value.
    def get16Signed(self):
        return getDecodedBytes(2, ">h")

    def onConnect(self):
        global connection

        port = '/dev/ttyUSB0'
        connection = serial.Serial(port, baudrate=115200, timeout=1)

if __name__ == "__main__":
    app = TetheredDriveApp()
    app.mainloop()
