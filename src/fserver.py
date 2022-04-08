#! /usr/bin/env python3

# framing server program

import socket, sys, re, os, time
sys.path.append("../lib")       # for params
import params
import framer

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "framingserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)
    if os.fork() == 0:      # child becomes server
        print('Connected by', addr)

        '''
        # original
        conn.send(b"hello")
        time.sleep(0.25);       # delay 1/4s
        conn.send(b"world")
        '''

        '''-----BEGIN-----'''
        os.write(1, 'Message to send: '.encode())  # user enters message
        message = os.read(1, 1000)                 # read the message
        framer.send_msg(conn, message)
        '''-----END-----'''

        conn.shutdown(socket.SHUT_WR)
        

        
