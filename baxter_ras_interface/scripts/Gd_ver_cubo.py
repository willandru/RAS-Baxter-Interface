#!/usr/bin/env python
#Reference: the baxter_stocking_stuffer project by students in Northwestern's MSR program - Josh Marino, Sabeen Admani, Andrew Turchina and Chu-Chu Igbokwe
#Service provided - ObjLocation service - contains x,y,z coordinates of object in baxter's stationary body frame, whether it is ok to grasp and if objects were found in the current frame.

import rospy
import numpy as np
import cv2
import cv_bridge
import baxter_interface
import math

from std_msgs.msg import String,Int32MultiArray
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge, CvBridgeError
from jp_baxtertry1.srv import *


def matriz(response,Orderold):
    n=len(response.matriz_5)+len(response.matriz_6)+len(response.matriz_7)+len(response.matriz_8)
    Order=list(range(0,n+1))
    for x in range(len(response.matriz_5)):
	Order[x]=response.matriz_5[x]
    y=x+1
    for x in range(len(response.matriz_6)):
	Order[x+y]=response.matriz_6[x]
    y_1=x+y+1
    for x in range(len(response.matriz_7)):
	Order[x+y_1]=response.matriz_7[x]
    y_2=x+y_1+1
    for x in range(len(response.matriz_8)):
	Order[x+y_2]=response.matriz_8[x]
    Order=Order[0:n]
    change=0
    for x in range(n):
	if Order[x]!=Orderold[x]:
		change=1

    if change==0:
        Order[0:n]=Orderold[0:n]
    if change==1:
	#print Orderold
	Orderold[0:n]=Order[0:n]
	#print Order
    return change
def mainmatriz(response):
    n=len(response.matriz_5)+len(response.matriz_6)+len(response.matriz_7)+len(response.matriz_8)
    Order=list(range(0,n+1))
    for x in range(len(response.matriz_5)):
	Order[x]=response.matriz_5[x]
    y=x+1
    for x in range(len(response.matriz_6)):
	Order[x+y]=response.matriz_6[x]
    y_1=x+y+1
    for x in range(len(response.matriz_7)):
	Order[x+y_1]=response.matriz_7[x]
    y_2=x+y_1+1
    for x in range(len(response.matriz_8)):
	Order[x+y_2]=response.matriz_8[x]    #0 VERDE,1 ROJO, 2 OBS
    Order=Order[0:n]
    return Order

def main():
    #Initiate left hand camera object detection node
    rospy.init_node('matriz_del_problema')
    rospy.sleep(10)
    global response
    InfoCoor_service = rospy.ServiceProxy("InfoCoor_service", InfoCoor)
    rospy.wait_for_service('InfoCoor_service')
    response = InfoCoor_service.call(InfoCoorRequest())
    Orderold=mainmatriz(response)
    pub = rospy.Publisher('matriz', Int32MultiArray, queue_size=36)
    rate = rospy.Rate(10) # 10hz
    Orderes=Int32MultiArray()
    a=0
    #print Orderold
    while not rospy.is_shutdown():
	  rospy.wait_for_service('InfoCoor_service')
    	  response = InfoCoor_service.call(InfoCoorRequest())
          change=matriz(response,Orderold)
          if a==0:
		  Orderes.data=Orderold
		  rospy.loginfo(Orderes)
		  pub.publish(Orderes)
		  rate.sleep()
		  a=a+1
	  if change==1:
		  Orderes.data=Orderold
		  rospy.loginfo(Orderes)
		  pub.publish(Orderes)
		  rate.sleep()
		  change=0
if __name__ == '__main__':
     main()
