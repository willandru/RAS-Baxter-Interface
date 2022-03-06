#!/usr/bin/python2

import numpy as np
import math
import sys
import rospy
import cv2
import cv_bridge
import pygame
from sensor_msgs.msg import Image
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from baxter_ras_interface.srv import *
import pygame
import sys
sys.path.append('src/baxter_ras_interface/scripts')
import Matriz_sonidos
x2 = 0
y2 = 0
primera = 0
array = 0

def callback(x,y,z,word):
    print(x,y)
    imagess=emocion(x,y)
    z_1=z
    #rospy.sleep(1)
    nada(imagess,word,z,x,y)
def nada(imagess,word,z,x,y):
	while not rospy.is_shutdown():
	    #print len(imagess)
	    if len(imagess)>0:
    		for path in imagess:
				if z==1:
					FRAMERATE = 30
					pygame.init()
					clock = pygame.time.Clock()
					print("Habla")
					wordPath="src/baxter_ras_interface/share/Sounds/"+word
					print(wordPath)
					pygame.mixer.music.load(wordPath)
					pygame.mixer.music.play()
					while pygame.mixer.music.get_busy():
						send_image(path,2)
						rospy.sleep(0.1)
						send_image(path,3)
						rospy.sleep(0.1)
						send_image(path,2)
						rospy.sleep(0.1)
						send_image(path,1)	
						rospy.sleep(0.1)
						clock.tick(FRAMERATE)
					z=2
				if z==2:
					send_image(path,4)
					rospy.sleep(0.1)
					send_image(path,5)
					rospy.sleep(0.1)
					send_image(path,4)
					rospy.sleep(0.1)
					send_image(path,1)	
					rospy.sleep(0.1)
					z=0
				if z==3:
					send_image(path,2)
					rospy.sleep(0.1)
					send_image(path,3)
					rospy.sleep(0.1)
					send_image(path,2)
					rospy.sleep(0.1)
					send_image(path,1)	
					rospy.sleep(0.1)	   
def send_image(path,folder):
	print(path)
	if (folder ==1):
	    	path = 'src/baxter_ras_interface/share/matriz1/'+path
	if (folder ==2):
	    	path = 'src/baxter_ras_interface/share/images/'+path
	if (folder ==3):
	    	path = 'src/baxter_ras_interface/share/matriz3/'+path
	if (folder ==4):
	    	path = 'src/baxter_ras_interface/share/matriz4/'+path
	if (folder ==5):
	    	path = 'src/baxter_ras_interface/share/matriz5/'+path				
    	img = cv2.imread(path)
    #	newimage = cv2.resize(img,(1024,600))
    	#print newimage
    	msg = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
    	pub = rospy.Publisher('/robot/xdisplay', Image, latch=True, queue_size=0.5)
    	pub.publish(msg)
    	#rospy.sleep(1)
	
def emocion(x,y):
    global x2
    global y2
    global primera
    global array
    if primera == 0:
    	x1 = 0
    	y1 = 0
	primera = 1
    else:
	array=0
	x1 = x2
	y1 = y2
    	x2 = x*20/400
    	y2 = y*20/400

    Espacio_Emociones = np.reshape(np.arange(400),(20,20))
    a=1
    for x in range (0, 20):
	for y in range (0, 20):
	    Espacio_Emociones[x][y] = a
	    a = a+1
    im=["" for x in range(1,401)]
    nombre=".png"

    while (x1 < x2) & (y1 < y2):
	if x1 < x2:
		x1 = x1+1
	if y1 < y2:
		y1 = y1+1
        im[array]=str(Espacio_Emociones[y1,x1])+nombre
        array=array+1

    while (x1 > x2) & (y1 > y2):
	if x1 > x2:
		x1 = x1-1
	if y1 > y2:
		y1 = y1-1
        im[array]=str(Espacio_Emociones[y1,x1])+nombre
        array=array+1

    while (x1 < x2) | (y1 > y2):
	if x1 < x2:
		x1 = x1+1
	if y1 > y2:
		y1 = y1-1
        im[array]=str(Espacio_Emociones[y1,x1])+nombre
        array=array+1

    while (x1 > x2) | (y1 < y2):
	if x1 > x2:
		x1 = x1-1
	if y1 < y2:
		y1 = y1+1
        im[array]=str(Espacio_Emociones[y1,x1])+nombre
        array=array+1

    imagess= ["" for x in range(0,array)]
    for x in range(array):
        imagess[x]=im[x]
    for path in imagess:
        send_image(path,1)
	rospy.sleep(0.1)
    return imagess
