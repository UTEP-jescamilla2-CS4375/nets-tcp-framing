#! /usr/bin/env python3

# framing server program

import socket, sys, re, os, time
sys.path.append("../lib")       # for params
import _thread as thread
import params
import framer

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "framingserver"
#paramMap = params.parseParams(switchesVarDefaults)

listenPort = 50001 #paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

'''
if paramMap['usage']:
    params.usage()
'''

if '-?' in sys.argv:
    os.write(1, './fserver.py -f <filename>\n'.encode())

if '-f' in sys.argv:
    file_name = sys.argv[sys.argv.index('-f') + 1]
else:
    file_name = ''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

thread_lock = thread.allocate_lock()

while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)
    print('Connected by', addr)
    os.write(1, f'Sending file: {file_name} \n'.encode())
    thread.start_new_thread(framer.send_file, (conn, file_name, thread_lock))


    '''
    if os.fork() == 0:      # child becomes server
        print('Connected by', addr)
        os.write(1, 'Message to send: '.encode())  # user enters message
        message = os.read(1, 1000)                 # read the message
        framer.send_msg(conn, message)
    '''

conn.shutdown(socket.SHUT_WR)
        

        
