import requests
import cv2

# A Simple HTTP Server Hosted ON NodeMCU 
# The Python Code Sends A POST Request to the server to change the appropriate state
# Some Image Processing Can Be Done On The PC And Then Appropriate Decissions can be taken
# Eg.. Detecting a face and opening the door


def led_on():
    requests.post('http://192.168.43.28:80/led',data={"state" : "On"})

def led_off():
    requests.post('http://192.168.43.28:80/led',data={"state" : "Off"})


def init():
    #face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    #smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
    print('here')

init()