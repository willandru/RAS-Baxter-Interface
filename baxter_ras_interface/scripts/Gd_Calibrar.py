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
def nothing(x):
    pass
def verde():
    Hmin=cv2.getTrackbarPos('Hmin','verde')
    Hmax=cv2.getTrackbarPos('Hmax','verde')
    Vmin=cv2.getTrackbarPos('Vmin','verde')
    Vmax=cv2.getTrackbarPos('Vmax','verde')
    Smin=cv2.getTrackbarPos('Smin','verde')
    Smax=cv2.getTrackbarPos('Smax','verde')
    Hum=cv2.getTrackbarPos('Hum','verde')	 
    return Hmin,Hmax,Vmin,Vmax,Smin,Smax,Hum
def azul():
    Hmin=cv2.getTrackbarPos('Hmin','azul')
    Hmax=cv2.getTrackbarPos('Hmax','azul')
    Vmin=cv2.getTrackbarPos('Vmin','azul')
    Vmax=cv2.getTrackbarPos('Vmax','azul')
    Smin=cv2.getTrackbarPos('Smin','azul')
    Smax=cv2.getTrackbarPos('Smax','azul')
    Hum=cv2.getTrackbarPos('Hum','azul')
    return Hmin,Hmax,Vmin,Vmax,Smin,Smax,Hum
def rojo():
    Hmin1=cv2.getTrackbarPos('Hmin1','rojo')
    Hmax1=cv2.getTrackbarPos('Hmax1','rojo')
    Vmin1=cv2.getTrackbarPos('Vmin1','rojo')
    Vmax1=cv2.getTrackbarPos('Vmax1','rojo')
    Smin1=cv2.getTrackbarPos('Smin1','rojo')
    Smax1=cv2.getTrackbarPos('Smax1','rojo')
    Hmin2=cv2.getTrackbarPos('Hmin2','rojo')
    Hmax2=cv2.getTrackbarPos('Hmax2','rojo')
    Vmin2=cv2.getTrackbarPos('Vmin2','rojo')
    Vmax2=cv2.getTrackbarPos('Vmax2','rojo')
    Smin2=cv2.getTrackbarPos('Smin2','rojo')
    Smax2=cv2.getTrackbarPos('Smax2','rojo')
    Hum=cv2.getTrackbarPos('Hum','rojo')
    return Hmin1,Hmax1,Vmin1,Vmax1,Smin1,Smax1,Hmin2,Hmax2,Vmin2,Vmax2,Smin2,Smax2,Hum
def mask_imagen(hsv,min_value,max_value):
    mask=cv2.inRange(hsv,min_value,max_value)
    return mask
def mask_imagen_rojo(hsv,min_value1,max_value1,min_value2,max_value2):
    mask1=cv2.inRange(hsv,min_value1,max_value1)
    mask2=cv2.inRange(hsv,min_value2,max_value2)
    mask=cv2.add(mask1,mask2)
    return mask
def filtro(mask,kernel,frame):
    #blur=cv2.GaussianBlur(mask,(3,3),0)
    #_,th3=cv2.threshold(blur,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #mask=th3
    ret,mask = cv2.threshold(mask,157,255,0)
    mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
    contours=cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(contours)>0:
	n_1=len(contours)
	for x_1 in range(n_1):
		c=contours[x_1]
		area=cv2.contourArea(c)
		M=cv2.moments(c)
		y=int(M["m01"] / M["m00"])
		x=int(M["m10"] / M["m00"])	
		if area>250  and y<420: 
			accuracy=0.06*cv2.arcLength(c,True)
			approx=cv2.approxPolyDP(c,accuracy,True)
			cv2.drawContours(frame,[approx],0,(0,255,0),2)
                        w,h=frame.shape[:2]
                        center=x,y
			print area
		        cv2.circle(frame, center, 5, (0, 0, 255), -1)
        #c1=max(contours, key=cv2.contourArea)
        #M=cv2.moments(c1)
        #if M['m00']>400:
            #for c in contours:
		#area=cv2.contourArea(c)
                #n=cv2.moments(c)
		#print area
                #if area>250: 
                    #accuracy=0.06*cv2.arcLength(c,True)
                    #approx=cv2.approxPolyDP(c,accuracy,True)
                    #cv2.drawContours(frame,[approx],0,(0,255,0),2) 
    return mask,contours
global Hmin_green,Hmax_green,Vmin_green,Vmax_green,Smin_green,Smax_green,Hum_green,Hmin_blue,Hmax_blue,Vmin_blue,Vmax_blue,Smin_blue,Smax_blue,Hum_blue,Hmin_red1,Hmax_red1,Vmin_red1,Vmax_red1,Smin_red1,Smax_red1,Hmin_red2,Hmax_red2,Vmin_red2,Vmax_red2,Smin_red2,Smax_red2,Hum_red 
def callback(message):
    global Hmin_green,Hmax_green,Vmin_green,Vmax_green,Smin_green,Smax_green,Hum_green,Hmin_blue,Hmax_blue,Vmin_blue,Vmax_blue,Smin_blue,Smax_blue,Hum_blue,Hmin_red1,Hmax_red1,Vmin_red1,Vmax_red1,Smin_red1,Smax_red1,Hmin_red2,Hmax_red2,Vmin_red2,Vmax_red2,Smin_red2,Smax_red2,Hum_red 
    bridge = CvBridge()
    frame = bridge.imgmsg_to_cv2(message, "bgr8")
    cv_image=frame
    Hmin_red1,Hmax_red1,Vmin_red1,Vmax_red1,Smin_red1,Smax_red1,Hmin_red2,Hmax_red2,Vmin_red2,Vmax_red2,Smin_red2,Smax_red2,Hum_red=rojo()
    Hmin_blue,Hmax_blue,Vmin_blue,Vmax_blue,Smin_blue,Smax_blue,Hum_blue=azul()
    Hmin_green,Hmax_green,Vmin_green,Vmax_green,Smin_green,Smax_green,Hum_green=verde()
    lower_red1=np.array([Hmin_red1,Vmin_red1,Smin_red1])
    upper_red1=np.array([Hmax_red1,Vmax_red1,Smax_red1 ])
    lower_red2=np.array([Hmin_red2,Vmin_red2,Smin_red2])
    upper_red2=np.array([Hmax_red2,Vmax_red2,Smax_red2 ])
    lower_blue=np.array([Hmin_blue,Vmin_blue,Smin_blue])
    upper_blue=np.array([Hmax_blue,Vmax_blue,Smax_blue ])
    lower_green=np.array([Hmin_green,Vmin_green,Smin_green])
    upper_green=np.array([Hmax_green,Vmax_green,Smax_green ])
    Height,Width,depth=frame.shape
    kernel=np.ones((7,7),np.uint8)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask_red=mask_imagen_rojo(hsv,lower_red1,upper_red1,lower_red2,upper_red2)
    mask_blue=mask_imagen(hsv,lower_blue,upper_blue)
    mask_green=mask_imagen(hsv,lower_green,upper_green)
    mask_red,contour_red=filtro(mask_red,kernel,frame)
    mask_blue,contour_blue=filtro(mask_blue,kernel,frame)
    mask_green,contour_green=filtro(mask_green,kernel,frame)
    cv2.imshow('mask_rojo', mask_red)
    cv2.imshow('mask_azul', mask_blue)
    cv2.imshow('mask_verde', mask_green)
    cv2.imshow('window',cv_image)
    cv2.waitKey(27)
def colors():
    cv2.createTrackbar('Hmin','verde',30,255,nothing)
    cv2.createTrackbar('Hmax','verde',59,255,nothing)
    cv2.createTrackbar('Vmin','verde',109,255,nothing)
    cv2.createTrackbar('Vmax','verde',254,255,nothing)
    cv2.createTrackbar('Smin','verde',97,255,nothing)
    cv2.createTrackbar('Smax','verde',254,255,nothing)
    cv2.createTrackbar('Hum','verde',0,10,nothing)
    cv2.createTrackbar('Hmin','azul',0,255,nothing)
    cv2.createTrackbar('Hmax','azul',255,255,nothing)
    cv2.createTrackbar('Vmin','azul',0,255,nothing)
    cv2.createTrackbar('Vmax','azul',83,255,nothing)
    cv2.createTrackbar('Smin','azul',0,255,nothing)
    cv2.createTrackbar('Smax','azul',82,255,nothing)
    cv2.createTrackbar('Hum','azul',0,100,nothing)
    cv2.createTrackbar('Hmin1','rojo',0,255,nothing)
    cv2.createTrackbar('Hmax1','rojo',12,255,nothing)
    cv2.createTrackbar('Vmin1','rojo',104,255,nothing)
    cv2.createTrackbar('Vmax1','rojo',255,255,nothing)
    cv2.createTrackbar('Smin1','rojo',115,255,nothing)
    cv2.createTrackbar('Smax1','rojo',255,255,nothing)
    cv2.createTrackbar('Hmin2','rojo',148,255,nothing)
    cv2.createTrackbar('Hmax2','rojo',255,255,nothing)
    cv2.createTrackbar('Vmin2','rojo',138,255,nothing)
    cv2.createTrackbar('Vmax2','rojo',255,255,nothing)
    cv2.createTrackbar('Smin2','rojo',92,255,nothing)
    cv2.createTrackbar('Smax2','rojo',255,255,nothing)
    cv2.createTrackbar('Hum','rojo',0,100,nothing)
def enviar():
    cv2.createTrackbar('Calibra','enviar',0,1,nothing)
    enviar=cv2.getTrackbarPos('Calibra','enviar')	
def get_obj_calibrate(request):
    global Hmin_green,Hmax_green,Vmin_green,Vmax_green,Smin_green,Smax_green,Hum_green,Hmin_blue,Hmax_blue,Vmin_blue,Vmax_blue,Smin_blue,Smax_blue,Hum_blue,Hmin_red1,Hmax_red1,Vmin_red1,Vmax_red1,Smin_red1,Smax_red1,Hmin_red2,Hmax_red2,Vmin_red2,Vmax_red2,Smin_red2,Smax_red2,Hum_red,act 
    rospy.sleep(0.5)
    return CalibrarResponse(Hmin_green,Hmax_green,Vmin_green,Vmax_green,Smin_green,Smax_green,Hum_green,Hmin_blue,Hmax_blue,Vmin_blue,Vmax_blue,Smin_blue,Smax_blue,Hum_blue,Hmin_red1,Hmax_red1,Vmin_red1,Vmax_red1,Smin_red1,Smax_red1,Hmin_red2,Hmax_red2,Vmin_red2,Vmax_red2,Smin_red2,Smax_red2,Hum_red,act)
global act
def main():
    #Initiate left hand camera object detection node
    global act
    act=enviar()
    colors()
    rospy.init_node('calibrate')
    cv2.namedWindow("mask_rojo", 4)
    cv2.namedWindow("mask_azul", 5)
    cv2.namedWindow("mask_verde", 6)
    cv2.namedWindow("azul", 1)
    cv2.namedWindow("verde", 2)
    cv2.namedWindow("rojo", 3)
    cv2.namedWindow("window", 7)
    cv2.namedWindow("enviar",8)
    #Subscribe to left hand camera image 
    rospy.Subscriber("/cameras/left_hand_camera/image", Image, callback)
    Calibrar_srv = rospy.Service("Calibrar_service",Calibrar, get_obj_calibrate)
    rospy.spin()
	    

if __name__ == '__main__':

     img = np.zeros((50,320,3), np.uint8)
     cv2.namedWindow('verde')
     img1 = np.zeros((50,320,3), np.uint8)
     cv2.namedWindow('azul')
     img2 = np.zeros((50,320,3), np.uint8)
     cv2.namedWindow('rojo')
     img3 = np.zeros((50,320,3), np.uint8)
     cv2.namedWindow('enviar')
     main()
