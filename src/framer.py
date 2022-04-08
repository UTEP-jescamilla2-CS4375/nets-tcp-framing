import socket

'''
parameters: socket, string
'''
def send_msg(sock, message):
    data = bytearray()
    data += bytearray(len(message).to_bytes(8, 'big'))
    data += bytearray(message)
    
    sock.sendall(data)

'''
parameters: socket
return: data as byte array
'''
def recv_msg(sock):

    # get the length of the message
    len_prefix = bytearray()
    remaining = 8
    while remaining > 0:
        packet = sock.recv(remaining)
        len_prefix.extend(packet)
        remaining -= len(packet)

    # get the actual message        
    data = bytearray()
    remaining = int.from_bytes(len_prefix, 'big')
    while remaining > 0:
        packet = sock.recv(remaining)
        data.extend(packet)
        remaining -= len(packet)
    
    return data
