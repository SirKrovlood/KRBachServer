import socket 
import sys
import cv2
import numpy as np
from _thread import *
from copy import deepcopy


global prevIm, capIm, outIm, camera

def listner(conn):
    while True:      
        reply=s.recv(4096)
        if reply.decode() == '':
            break
        print(reply)
    sys.exit()


def imgShow():
    global prevIm, capIm, outIm, camera
    while True:
        cv2.waitKey(20)
        ret, prevIm = camera.read()
        cv2.imshow('preview', prevIm)
        
        if not capIm is None:
            cv2.imshow('captured', capIm)

        if not outIm is None:
            cv2.imshow('output', outIm)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                 break
    cv2.destroyAllWindows()
    camera.release()
    sys.exit()

camera = cv2.VideoCapture(0)
remote_ip="172.17.64.155"
port=8888

try:
	# create an AF_INET, STREAM socket (TCP)
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error (msg):
	print('...failed to create socket...error code: ' + str(msg[0]) + ', error message: ' + msg[1])
	sys.exit()

print('...socket created...')
s.connect((remote_ip,port))

print('...socket connected to '+remote_ip+' on IP ')


outIm = np.zeros((480, 640))
    
#start_new_thread(listner,(s,))
start_new_thread(imgShow,())
'''
with open("egga.png", "rb") as image:
  f = image.read()
  b = bytearray(f)
  size = str(len(b))
  size = ' '*(10-len(size)) + size
'''


emotions_list = ('anger', 'fear', 'calm', 'sadness',
                 'happiness', 'surprise', 'disgust')
while True:
    try:
            cv2.waitKey(20)
            ret, capIm = camera.read()
            height, width, channels = capIm.shape
            
            
            ret, b = cv2.imencode('.png', capIm)
            size = str(len(b))
            size = ' '*(10-len(size)) + size
            
            s.sendall(size.encode());
            # send string
            s.sendall(b)
            # now receive data
            if cv2.waitKey(1) & 0xFF == ord('q'):
                 break
            
            reply=s.recv(8).decode()
            if reply == '':
                break
            outIm = deepcopy(capIm)
            cv2.putText(outIm, emotions_list[int(reply)], (width-240,height-20), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0), thickness=3)
            cv2.putText(outIm, emotions_list[int(reply)], (width-240,height-20), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), thickness=1)
                      
            print(reply+ '\n')
    except socket.error:
            # send failed
            print('...send failed...')
            sys.exit()
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        camera.release()
        s.close()
        sys.exit()
cv2.destroyAllWindows()
camera.release()
s.close()
sys.exit()