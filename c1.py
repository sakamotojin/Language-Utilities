#!/usr/bin/python
import socket
import cv2
import numpy

TCP_IP = '192.168.43.201'
TCP_PORT = 7890

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

capture = cv2.VideoCapture(0)
while True:
	ret, frame = capture.read()

	encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
	result, imgencode = cv2.imencode('.jpg', frame, encode_param)
	data = numpy.array(imgencode)
	stringData = data.tostring()

	sock.send( str(len(stringData)).ljust(16));
	sock.send( stringData );
	#decimg=cv2.imdecode(data,1)

	#decimg  = cv2.resize(decimg,(480,640),3)

	#decimg =data.reshape((480,640,3)) 
	#cv2.imshow('CLIENT',decimg)
sock.close()
cv2.waitKey(0)
cv2.destroyAllWindows() 
