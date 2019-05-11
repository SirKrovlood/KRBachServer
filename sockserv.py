#!/usr/bin/python
# source: http://www.binarytides.com/python-socket-programming-tutorial/
#
# partial socket server example in python
# file: nutilahendused-2018-prax-sockets-code-sample-07.py

import socket 
import sys
from _thread import *

HOST='' # symbolic name meaning all available interfaces
PORT= int(input('port to listen: ')) # arbitrary non-privileged port
numconn=10 # number of simultaneous connections
sisendandmetepikkus=1024

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('...socket created...')
#s.bind((HOST,PORT))
#s.bind(("172.17.64.155",PORT))



try:
	s.bind((HOST,PORT))
	print('...werkin...')
except:

	print('...bind failed...')
	sys.exit()

print('...socket bind complete...')

# make socket to listen incomming connections

s.listen(numconn)
print('...socket now listening...')

file = open('test.png', 'wb')


# function for handling connections...this will be used to create threads
def clientthread(conn):
    
    conn.send(('...welcome to the server...type something and hit enter \n').encode()) # send only takes strings
    while True:
        # receiving from client
        data=conn.recv(sisendandmetepikkus)
        print(data)
        #reply='...OK...'+data.decode()
        try:
            if data.decode() == "sha budet":
                break
        except:
            l = 0
        file.write(data)
        #conn.sendall(reply.encode())
    file.close()
    print('we done here')
    conn.close()
		
# now keep talking with the client
try:
    while 1:
            # wait to accept a connection - blocking call
            conn, addr = s.accept()

            # display client information
            print('...connected with '+addr[0] + ':'+str(addr[1]))

            # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function
            start_new_thread(clientthread,(conn,))

except KeyboardInterrupt:
    file.close()
    s.close()
    sys.exit()
