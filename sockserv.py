#!/usr/bin/python
# source: http://www.binarytides.com/python-socket-programming-tutorial/
#
# partial socket server example in python
# file: nutilahendused-2018-prax-sockets-code-sample-07.py

import socket 
import sys
from _thread import *

HOST='localhost' # symbolic name meaning all available interfaces
PORT= int(input('port to listen: ')) # arbitrary non-privileged port
numconn=10 # number of simultaneous connections
sisendandmetepikkus=1024
global LedSeis
LedSeis = False

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('...socket created...')

try:
	s.bind((HOST,PORT))
except socket.error():
	print(('...bind failed...error code: ' + str(msg[0]) + ', error message: ' + msg[1]))
	sys.exit()

print('...socket bind complete...')

# make socket to listen incomming connections

s.listen(numconn)
print('...socket now listening...')



# function for handling connections...this will be used to create threads
def clientthread(conn):
	# sending message to connected client
	conn.send(('...welcome to the server...type something and hit enter \n').encode()) # send only takes strings
	# infinite loop so that function do not terminate and thread do not end
	while True:
		# receiving from client
                data=conn.recv(sisendandmetepikkus)
                print(data)
                reply='...OK...'+data.decode()
                        
                if not data:
                    break
                        
                conn.sendall(reply.encode())
	# came out of loop
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
    s.close()
    sys.exit()
