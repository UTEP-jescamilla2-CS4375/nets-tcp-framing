#! /usr/bin/env python3

# server program

import socket, sys, re
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "server"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

'''
if '-?' in sys.argv:
    os.write(1, './fserver.py -f <filename>\n'.encode())

if '-f' in sys.argv:
    file_name = sys.argv[sys.argv.index('-f') + 1]
else:
    file_name = ''
'''



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

conn, addr = s.accept() # wait until incoming connection request (and accept it)
print('Connected by', addr)

while 1:
    
    data = conn.recv(1024).decode()
    if len(data) == 0:
        print("Zero length read, nothing to send, terminating")
        break
    sendMsg = ("Echoing %s" % data).encode()
    print("Received '%s', sending '%s'" % (data, sendMsg.decode()))
    while len(sendMsg):
        bytesSent = conn.send(sendMsg)
        sendMsg = sendMsg[bytesSent:0]

    '''
    os.write(1, f'Sending file: {file_name} \n'.encode())
    thread.start_new_thread(framer.send_file, (conn, file_name, thread_lock))
    '''

    '''
    if os.fork() == 0:      # child becomes server
        print('Connected by', addr)
        os.write(1, 'Message to send: '.encode())  # user enters message
        message = os.read(1, 1000)                 # read the message
        framer.send_msg(conn, message)
    '''

conn.shutdown(socket.SHUT_WR)
conn.close()
        

        
