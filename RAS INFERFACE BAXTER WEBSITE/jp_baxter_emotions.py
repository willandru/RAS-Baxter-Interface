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

x2 = 0
y2 = 0
primera = 0
array = 0

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.linear.x)
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.linear.y)
    emocion(data.linear.x,data.linear.y)

def listener():

    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('chatter', Twist, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

def send_image(path):
    path = '/home/z420/ros_ws/src/baxter_examples/share/images/'+path
    img = cv2.imread(path)
    newimage = cv2.resize(img,(1024,600))
    #print newimage
    msg = cv_bridge.CvBridge().cv2_to_imgmsg(newimage, encoding="bgr8")
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
    #rospy.init_node('rsdk_xdisplay_image', anonymous=True)
    for path in imagess:
        send_image(path)
	rospy.sleep(0.1)

if __name__ == '__main__':
#    sys.exit(main())
    listener()

