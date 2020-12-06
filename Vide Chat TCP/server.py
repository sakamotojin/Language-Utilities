import socket
import cv2
import numpy

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

TCP_IP = 'localhost'
TCP_PORT = 5999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(True)
conn, addr = s.accept()
while True:
	
	
	
	length = recvall(conn,16)
	stringData = recvall(conn, int(length))
	#print(stringData)
	data = numpy.fromstring(stringData, dtype='uint8')
	decimg=cv2.imdecode(data,1)
	#cv2.imwrite('e.jpg', decimg)

	#decimg  = cv2.resize(decimg,(480,640),3) 
	#f=cv2.imread('e.jpg',1)
	cv2.imshow("S",decimg)
	cv2.waitKey(0)
s.close()
cv2.waitKey(0)
cv2.destroyAllWindows() 
