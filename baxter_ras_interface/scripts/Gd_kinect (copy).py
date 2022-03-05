#!/usr/bin/env python
#Reference: the baxter_stocking_stuffer project by students in Northwestern's MSR program - Josh Marino, Sabeen Admani, Andrew Turchina and Chu-Chu Igbokwe
#Service provided - ObjLocation service - contains x,y,z coordinates of object in baxter's stationary body frame, whether it is ok to grasp and if objects were found in the current frame.

import rospy
import numpy as np
import cv 
import cv_bridge
import baxter_interface
import math
import sys
import glob
from std_msgs.msg import String, Int  
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge, CvBridgeError
from jp_baxtertry .srv import * #nombre del catkin(carpeta)
from matplotlib import pyplot as plt
def filtro(mask,frame,kernel):
    #thresh=mask
    mask=cv .morphologyEx(mask,cv .MORPH_OPEN,kernel)
    mask=cv .morphologyEx(mask,cv .MORPH_CLOSE,kernel)
    #mask=cv .morphologyEx(mask,cv .MORPH_OPEN,kernel)
    mask=cv .erode(mask,kernel,iterations= )
    mask=cv .dilate(mask,kernel,iterations= )
    blur=cv .GaussianBlur(mask,( , ), )
    _,th =cv .threshold(blur, ,   ,cv .THRESH_BINARY + cv .THRESH_OTSU)
    #ret,th  = cv .threshold(mask,   ,   , )
    mask=th 
    contours=cv .findContours(mask,cv .RETR_EXTERNAL, cv .CHAIN_APPROX_SIMPLE)[- ]
    if len(contours)> :
	n_ =len(contours)
        rango=list(range( ,n_ + ))
	cont= 
	xmin=    
	ymin=    
	xmax= 
	ymax= 
	beta= 
	ar= 
	for x_  in range(n_ ):
		c=contours[x_ ]
		area=cv .contourArea(c)
		M=cv .moments(c)
		
		y=int(M["m  "] / M["m  "])
		x=int(M["m  "] / M["m  "])	
		if area>   :
			ar=ar+area 
			beta=beta+ 
	#arprom=ar/beta
	for x_  in range(n_ ):
		c=contours[x_ ]
		area=cv .contourArea(c)
		M=cv .moments(c)
		
		y=int(M["m  "] / M["m  "])
		x=int(M["m  "] / M["m  "])	
		if area>=   : 
                        w,h=frame.shape[: ]
                        center=x,y
			rango[cont]=center
			cont=cont+ 
		        cv .circle(frame, center,  , ( ,  ,    ), - )
    mask = cv .merge((mask,mask,mask))
    res = cv .bitwise_and(frame,mask)
    return res,contours
def imagenes(hsv,hsvt,frame):
    kernel=np.ones(( , ),np.uint )
    roihist = cv .calcHist([hsv],[ ,  ], None, [   ,    ], [ ,    ,  ,    ] )
    cv .normalize(roihist,roihist, ,   ,cv .NORM_MINMAX)
    dst = cv .calcBackProject([hsvt],[ , ],roihist,[ ,   , ,   ], )
    disc = cv .getStructuringElement(cv .MORPH_ELLIPSE,( , ))
    cv .filter D(dst,- ,disc,dst)
    # threshold and binary AND
    ret,thresh = cv .threshold(dst,  ,   , )
    return thresh
def recorrerimagen(nombre,cantidad,frame,hsvt):
    carpeta='/home/z   /ros_ws/'+nombre+'/'+nombre
    for x in range( ,cantidad):
	num=str(x)
	imagenleida=carpeta+num+'.jpg'
	img=cv .imread(imagenleida)
	hsv=cv .cvtColor(img,cv .COLOR_BGR HSV)
	res_sub=imagenes(hsv,hsvt,frame)
        if x== :
		rest=res_sub
        if x> :
		rest=cv .add(rest,res_sub)
    return rest	
def callback (message):
    bridge = CvBridge()
    frame = bridge.imgmsg_to_cv (message, "bgr ")
    hsv=cv .cvtColor(frame,cv .COLOR_BGR HSV)
    w,h=frame.shape[: ]
    center=(h/ ),(w/ )
    cv .circle(frame, center,  , ( ,  ,    ), - )
    print hsv[h/ ],[w/ ]
    # show the images
    cv .imshow("frame",frame)

    cv .waitKey( )
def callback(message):
    x_red1,y_red1=centro(150,60,frame)
    x_blue1,y_blue1=centro(192,60,frame)
    x_obs1,y_obs1=centro(230,76,frame)
    x_obs2,y_obs2=centro(269,76,frame)
    x_orange1,y_orange1=centro(305,58,frame)
    x_obs3,y_obs3=centro(342,73,frame)
    x_obs4,y_obs4=centro(378,73,frame)
    x_obs5,y_obs5=centro(415,73,frame)
    x_green1,y_green1=centro(456,54,frame)
    x_orange2,y_orange2=centro(145,105,frame)
    x_obs6,y_obs6=centro(192,118,frame)
    x_red2,y_red2=centro(227,108,frame)
    x_obs7,y_obs7=centro(267,117,frame)
    x_green2,y_green2=centro(304,103,frame)
    x_obs8,y_obs8=centro(343,115,frame)
    x_blue2,y_blue2=centro(384,99,frame)
    x_obs9,y_obs9=centro(421,113,frame)
    x_obs10,y_obs10=centro(458,113,frame)
    x_obs11,y_obs11=centro(147,165,frame)
    x_orange3,y_orange3=centro(182,151,frame)
    x_obs12,y_obs12=centro(226,163,frame)
    x_green3,y_green3=centro(266,150,frame)
    x_red3,y_red3=centro(307,148,frame)
    x_obs13,y_obs13=centro(347,159,frame)
    x_obs14,y_obs14=centro(385,159,frame)
    x_blue3,y_blue3=centro(431,145,frame)
    x_obs15,y_obs15=centro(464,156,frame)
    x_obs16,y_obs16=centro(143,213,frame)
    x_green4,y_green4=centro(178,202,frame)
    x_blue4,y_blue4=centro(222,203,frame)
    x_obs17,y_obs17=centro(267,210,frame)
    x_obs18,y_obs18=centro(308,210,frame)
    x_orange4,y_orange4=centro(350,196,frame)
    x_obs19,y_obs19=centro(391,207,frame)
    x_obs20,y_obs20=centro(431,207,frame)
    x_red4,y_red4=centro(479,195,frame)

    print len(contour_rojo)
    #cv .imshow('frame', frame)
    #cv .waitKey( )
def main():
    #Initiate left hand camera object detection node
    rospy.init_node('right_camera_node')
    cv .namedWindow("frame",  )
    #cv .namedWindow("verde",  )
    #cv .namedWindow("rojo",  )
    #cv .namedWindow(" ",  )
    #$v .namedWindow("palo",  )
    #Subscribe to left hand camera image 
    rospy.Subscriber("/camera/rgb/image_color", Image, callback )
    rospy.spin()

if __name__ == '__main__':
     main()
