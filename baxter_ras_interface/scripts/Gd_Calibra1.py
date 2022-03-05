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
def getKey(item):
    return item[1]
def callback(message):
    global Hmin_verde,Hmax_verde,Vmin_verde,Vmax_verde,Smin_verde,Smax_verde,Hum_verde,Hmin_negro,Hmax_negro,Vmin_negro,Vmax_negro,Smin_negro,Smax_negro,Hum_negro,Hmin_rojo1,Hmax_rojo1,Vmin_rojo1,Vmax_rojo1,Smin_rojo1,Smax_rojo1,Hum_rojo1,Hmin_rojo2,Hmax_rojo2,Vmin_rojo2,Vmax_rojo2,Smin_rojo2,Smax_rojo2,Hum_rojo2
    global act,xmin,xmax,ymin,ymax
    act=cv2.getTrackbarPos('act','enviar')
    bridge = CvBridge()
    frame = bridge.imgmsg_to_cv2(message, "bgr8")
    #frame=cv2.imread('calibrar_guardado.jpg')
    Hmin_verde,Hmax_verde,Vmin_verde,Vmax_verde,Smin_verde,Smax_verde,Hum_verde=asig_Color('verde')
    Hmin_negro,Hmax_negro,Vmin_negro,Vmax_negro,Smin_negro,Smax_negro,Hum_negro=asig_Color('negro')
    Hmin_rojo1,Hmax_rojo1,Vmin_rojo1,Vmax_rojo1,Smin_rojo1,Smax_rojo1,Hum_rojo1=asig_Color('rojo1')
    Hmin_rojo2,Hmax_rojo2,Vmin_rojo2,Vmax_rojo2,Smin_rojo2,Smax_rojo2,Hum_rojo2=asig_Color('rojo2')
    lower_verde,upper_verde=def_color(Hmin_verde,Vmin_verde,Smin_verde,Hmax_verde,Vmax_verde,Smax_verde)
    lower_negro,upper_negro=def_color(Hmin_negro,Vmin_negro,Smin_negro,Hmax_negro,Vmax_negro,Smax_negro)
    lower_rojo1,upper_rojo1=def_color(Hmin_rojo1,Vmin_rojo1,Smin_rojo1,Hmax_rojo1,Vmax_rojo1,Smax_rojo1)
    lower_rojo2,upper_rojo2=def_color(Hmin_rojo2,Vmin_rojo2,Smin_rojo2,Hmax_rojo2,Vmax_rojo2,Smax_rojo2)
    kernel=np.ones((7,7),np.uint8)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask_verde=mask_imagen(hsv,lower_verde,upper_verde)
    mask_negro=mask_imagen(hsv,lower_negro,upper_negro)
    #global arprom_verde,arprom_rojo,arprom_negro
    mask_rojo=mask_imagen_rojo(hsv,lower_rojo1,upper_rojo1,lower_rojo2,upper_rojo2)
    contour_verde,arprom_verde=filtro(mask_verde,kernel,frame)    
    contour_rojo,arprom_rojo=filtro(mask_rojo,kernel,frame)
    #global xmin1,xmax1,ymin1,ymax1,xmin2,xmax2,ymin2,ymax2
    contour_negro,arprom_negro=filtro(mask_negro,kernel,frame)
    #rango_negro=sorted(rango_negro, key=getKey) 
    #n=len(rango_negro)
    #maximo= max(rango_negro, key=getKey)
    #minimo= min(rango_negro, key=getKey)
    #xmin1=1000
    #xmin2=1000
    #xmax1=0
    #xmax2=0
    #for x in range(n):
	#if rango_negro[x][1]>=maximo[1]-7 and rango_negro[x][0]<xmin1:
#		xmin1=rango_negro[x][0]
#		ymax1=rango_negro[x][1]
#		centro1=xmin1,ymax1
 #       if rango_negro[x][1]<=minimo[1]+7 and rango_negro[x][0]<xmin2:
#		ymin1=rango_negro[x][1]
#		centro2=xmin2,ymin1
 #       if rango_negro[x][1]<=minimo[1]+7 and rango_negro[x][0]>xmax1:
#		xmax1=rango_negro[x][0]
#		ymin2=rango_negro[x][1]
#		centro3=xmax1,ymin2	
 #       if rango_negro[x][1]>=maximo[1]-7 and rango_negro[x][0]>xmax2:
#		xmax2=rango_negro[x][0]
#		ymax2=rango_negro[x][1]
#		centro4=xmax2,ymax2
    
 #   cv2.circle(frame, centro1, 5, (0, 255, 255), -1)
  #  cv2.circle(frame, centro2, 5, (0, 255, 255), -1)
   # cv2.circle(frame, centro3, 5, (0, 255, 255), -1)
    #cv2.circle(frame, centro4, 5, (0, 255, 255), -1)	
    cv2.imshow('window',frame)
    cv2.imshow('negro',mask_negro)
    cv2.imshow('rojo',mask_rojo)
    cv2.waitKey(27)
def mask_imagen(hsv,min_value,max_value):
    mask=cv2.inRange(hsv,min_value,max_value)
    return mask
def def_color(Hmin,Vmin,Smin,Hmax,Vmax,Smax):
    lower=np.array([Hmin,Vmin,Smin])
    upper=np.array([Hmax,Vmax,Smax])
    return lower,upper
def mask_imagen_rojo(hsv,min_value1,max_value1,min_value2,max_value2):
    mask1=cv2.inRange(hsv,min_value1,max_value1)
    mask2=cv2.inRange(hsv,min_value2,max_value2)
    mask=cv2.add(mask1,mask2)
    return mask
def asig_Color(color):
    Hmin=cv2.getTrackbarPos('Hmin',color)
    Hmax=cv2.getTrackbarPos('Hmax',color)
    Vmin=cv2.getTrackbarPos('Vmin',color)
    Vmax=cv2.getTrackbarPos('Vmax',color)
    Smin=cv2.getTrackbarPos('Smin',color)
    Smax=cv2.getTrackbarPos('Smax',color)
    Hum=cv2.getTrackbarPos('Hum',color)	 
    return Hmin,Hmax,Vmin,Vmax,Smin,Smax,Hum
def filtro(mask,kernel,frame):
    ret,mask = cv2.threshold(mask,157,255,0)
    mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
    contours=cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    arprom=0
    if len(contours)>0:
	n_1=len(contours)
	cont=0
	xmin=1000
	ymin=1000
	xmax=0
	ymax=0
	beta=0
	ar=0
	#for x_1 in range(n_1):
	#	c=contours[x_1]
	#	area=cv2.contourArea(c)
	#	M=cv2.moments(c)
		
	#	y=int(M["m01"] / M["m00"])
	#	x=int(M["m10"] / M["m00"])	
	#	if area>250  and y<420 and y>30:
	#		ar=ar+area 
	#		beta=beta+1
	#arprom=ar/beta
	for x_1 in range(n_1):
		c=contours[x_1]
		area=cv2.contourArea(c)
		M=cv2.moments(c)
		
		y=int(M["m01"] / M["m00"])
		x=int(M["m10"] / M["m00"])	
		if area>250  and y<420 and y>30: 
			accuracy=0.06*cv2.arcLength(c,True)
			approx=cv2.approxPolyDP(c,accuracy,True)
			cv2.drawContours(frame,[approx],0,(0,255,0),2)
                        w,h=frame.shape[:2]
                        center=x,y
			#rango[cont]=center
			cont=cont+1
		        cv2.circle(frame, center, 5, (0, 0, 255), -1)
	#rango=rango[0:cont]
    return contours,arprom
def nothing(x):
    pass
def crearslider(color,Hmin,Hmax,Smin,Smax,Vmin,Vmax):
    cv2.namedWindow(color)
    cv2.createTrackbar('Hmin',color,Hmin,255,nothing)
    cv2.createTrackbar('Hmax',color,Hmax,255,nothing)
    cv2.createTrackbar('Vmin',color,Vmin,255,nothing)
    cv2.createTrackbar('Vmax',color,Vmax,255,nothing)
    cv2.createTrackbar('Smin',color,Smin,255,nothing)
    cv2.createTrackbar('Smax',color,Smax,255,nothing)
    cv2.createTrackbar('Hum',color,0,100,nothing)  
def get_obj_calibrate(request):
    global Hmin_verde,Hmax_verde,Vmin_verde,Vmax_verde,Smin_verde,Smax_verde,Hum_verde,Hmin_negro,Hmax_negro,Vmin_negro,Vmax_negro,Smin_negro,Smax_negro,Hum_negro,Hmin_rojo1,Hmax_rojo1,Vmin_rojo1,Vmax_rojo1,Smin_rojo1,Smax_rojo1,Hum_rojo1,Hmin_rojo2,Hmax_rojo2,Vmin_rojo2,Vmax_rojo2,Smin_rojo2,Smax_rojo2,Hum_rojo2,act,xmin1,xmax1,ymin1,ymax1,xmin2,xmax2,ymin2,ymax2,arprom_verde,arprom_rojo,arprom_negro
    rospy.sleep(0.5)
    return CalibradoResponse(Hmin_verde,Hmax_verde,Vmin_verde,Vmax_verde,Smin_verde,Smax_verde,Hum_verde,Hmin_negro,Hmax_negro,Vmin_negro,Vmax_negro,Smin_negro,Smax_negro,Hum_negro,Hmin_rojo1,Hmax_rojo1,Vmin_rojo1,Vmax_rojo1,Smin_rojo1,Smax_rojo1,Hum_rojo1,Hmin_rojo2,Hmax_rojo2,Vmin_rojo2,Vmax_rojo2,Smin_rojo2,Smax_rojo2,Hum_rojo2,act,xmin1,xmax1,ymin1,ymax1,xmin2,xmax2,ymin2,ymax2,arprom_verde,arprom_rojo,arprom_negro)
def user():
	    cv2.namedWindow("window", 1)
	    #Subscribe to left hand camera image 
	    rospy.Subscriber("/camera/rgb/image_color", Image, callback)
            #Calibrado_srv = rospy.Service("Calibrado_service", Calibrado, get_obj_calibrate)
            rospy.spin()
def main():
    #Initiate left hand camera object detection node
    rospy.init_node('calibrate')
    crearslider('verde',30,59,97,255,109,255)
    crearslider('rojo1',0,12,115,255,104,255)
    crearslider('rojo2',148,255,92,255,138,255)
    crearslider('negro',0,255,0,82,0,83)
    cv2.namedWindow('enviar')
    cv2.createTrackbar('act','enviar',0,1,nothing)
    user()

if __name__ == '__main__':
     main()
