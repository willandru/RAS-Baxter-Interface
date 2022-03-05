#!/usr/bin/env python
#Reference: the baxter_stocking_stuffer project by students in Northwestern's MSR program - Josh Marino, Sabeen Admani, Andrew Turchina and Chu-Chu Igbokwe
#Service provided - ObjLocation service - contains x,y,z coordinates of object in baxter's stationary body frame, whether it is ok to grasp and if objects were found in the current frame.

import rospy
import numpy as np
import cv2
import cv_bridge
import baxter_interface
import math

from std_msgs.msg import String, Int32
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge, CvBridgeError
from jp_baxtertry1.srv import *

def matriz(response,Orderold):
    global total,orderone
    n=len(response.matriz1)+len(response.matriz2)+len(response.matriz3)+len(response.matriz4)
    Order=list(range(0,n+1))
    for x in range(len(response.matriz1)):
	Order[x]=response.matriz1[x]
    y=x+1
    for x in range(len(response.matriz2)):
	Order[x+y]=response.matriz2[x]
    y_1=x+y+1
    for x in range(len(response.matriz3)):
	Order[x+y_1]=response.matriz3[x]
    y_2=x+y_1+1
    for x in range(len(response.matriz4)):
	Order[x+y_2]=response.matriz4[x]    
    Order[n]=response.timer
    change=0
    for x in range(n-1):
	if Order[x]!=orderone[x]:
		change=1

    if change==0:
	orderone[n]=Order[n]
        Orderold[0:n]=orderone[0:n]
    if change==1:
	orderone[n]=Order[n]-orderone[n]
	orderone[0:n-1]=Order[0:n-1]
	total.append(orderone[0:n+1])        
	print total
	change=0
    #return change,Orderold		
def mainmatriz(response):
    n=len(response.matriz1)+len(response.matriz2)+len(response.matriz3)+len(response.matriz4)
    Order=list(range(0,n+1))
    for x in range(len(response.matriz1)):
	Order[x]=response.matriz1[x]
    y=x+1
    for x in range(len(response.matriz2)):
	Order[x+y]=response.matriz2[x]
    y_1=x+y+1
    for x in range(len(response.matriz3)):
	Order[x+y_1]=response.matriz3[x]
    y_2=x+y_1+1
    for x in range(len(response.matriz4)):
	Order[x+y_2]=response.matriz4[x]    
    Order[n]=0
    ac=response.timer
    return Order,ac		
def main():
    #Initiate left hand camera object detection node
    rospy.init_node('Game_start')
    a=0
    Ord=list(range(0,2))
    Info_service = rospy.ServiceProxy("Info_service", Info)
    rospy.wait_for_service('Info_service')
    response_1 = Info_service.call(InfoRequest())
    global total,orderone
    orderone,ac=mainmatriz(response_1)
    total=list()
    total.append(orderone[0:37])
    Orderold=list(range(0,36+1))
    
    while not rospy.is_shutdown():
            Cor_service = rospy.ServiceProxy("Cor_service", Cor)
            rospy.wait_for_service('Cor_service')
            aceptar = Cor_service.call(CorRequest())
	    if aceptar.alpha==1:	
		    Info_service = rospy.ServiceProxy("Info_service", Info)
		    rospy.wait_for_service('Info_service')
		    response = Info_service.call(InfoRequest())
		    matriz(response,Orderold)
		    a=a+1
#    rospy.spin()

if __name__ == '__main__':

     main()
