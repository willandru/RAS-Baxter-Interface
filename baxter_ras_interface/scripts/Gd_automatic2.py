#!/usr/bin/env python
#Reference: the baxter_stocking_stuffer project by students in Northwestern's MSR program - Josh Marino, Sabeen Admani, Andrew Turchina and Chu-Chu Igbokwe
#Service provided - ObjLocation service - contains x,y,z coordinates of object in baxter's stationary body frame, whether it is ok to grasp and if objects were found in the current frame.

import rospy
import numpy as np
import cv2
import cv_bridge
import baxter_interface
import math
import sys
import glob
import yaml
from std_msgs.msg import String, Int32,UInt8MultiArray
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge, CvBridgeError
from jp_baxtertry1.srv import * #nombre del catkin(carpeta)
from matplotlib import pyplot as plt
# mouse callback function
def getKey(item):
    return item[1]
def centro(x,y,frame):
    center=x,y
    cv2.circle(frame, center, 5, (0, 0, 255), -1)
    return x,y
def matrizdef(hsv,x,y,matriz):
	matriz.append(hsv[y][x])
def coor(center_green,center_red,center_obs,center_orange,center_blue,frame):
	n1=len(center_green)
	n2=len(center_red)
	n3=len(center_obs)
	n4=len(center_orange)
	n5=len(center_blue)
	n=n1+n2+n3+n4+n5
        morder=list(range(0,n1+n2+n3+n4+n5+1))
	for x in range(n1):
		morder[x]=center_green[x]
	y=x+1
	for x in range(n2):
		morder[x+y]=center_red[x]

	y=y+x+1
	for x in range(n3):
		morder[x+y]=center_obs[x]
	y=y+x+1
	for x in range(n4):
		morder[x+y]=center_orange[x]
	y=y+x+1
	for x in range(n5):
		morder[x+y]=center_blue[x]
	morder=morder[0:n]
        morder=sorted(morder, key=getKey)
        n=len(morder)
        maximo= max(morder, key=getKey)
        minimo= min(morder, key=getKey)
        xmin1=10000
        xmin2=10000
        xmax1=0
        xmax2=0
        for x in range(n):
	    if morder[x][1]>=maximo[1]-30 and morder[x][0]<xmin1:
     		    xmin1=morder[x][0]
 		    ymax1=morder[x][1]
		    centro1=xmin1,ymax1
            if morder[x][1]<=minimo[1]+30 and morder[x][0]<xmin2:
		    ymin1=morder[x][1]
		    xmin2=morder[x][0]
		    centro2=xmin2,ymin1
            if morder[x][1]<=minimo[1]+30 and morder[x][0]>xmax1:
		    xmax1=morder[x][0]
		    ymin2=morder[x][1]
		    centro3=xmax1,ymin2
            if morder[x][1]>=maximo[1]-30 and morder[x][0]>xmax2:
		    xmax2=morder[x][0]
		    ymax2=morder[x][1]
		    centro4=xmax2,ymax2
        cv2.circle(frame, centro1, 5, (0, 0, 0), -1)
        cv2.circle(frame, centro2, 5, (0, 0, 0), -1)
        cv2.circle(frame, centro3, 5, (0, 0, 0), -1)
        cv2.circle(frame, centro4, 5, (0, 0, 0), -1)
	return xmin1,xmin2,ymin1,ymin2,xmax1,xmax2,ymax1,ymax2


def cal1(matriz,hsv,kernel):
        global hmin_red1,hmax_red1,smin_red1,vmin_red1,smax_red1,vmax_red1,hmin_red2,hmax_red2,smin_red2,smax_red2,vmin_red2,vmax_red2,hmax_obs
	for x in range(len(matriz[:])):
		if matriz[x][0]<13:
			if hmin_red1>matriz[x][0]:
				hmin_red1=matriz[x][0]
			if hmax_red1<matriz[x][0]:
				hmax_red1=matriz[x][0]
			if smin_red1>matriz[x][1]:
				smin_red1=matriz[x][1]
			if vmin_red1>matriz[x][2]:
				vmin_red1=matriz[x][2]
			if smax_red1<matriz[x][1]:
				smax_red1=matriz[x][1]
			if vmax_red1<matriz[x][2]:
				vmax_red1=matriz[x][2]
	#print 'rojo'
	#print hmin_red1,hmax_red1,smin_red1,smax_red1,vmin_red1,vmax_red1
	hmax_red2=hmax_obs+5
	hmin_red2=150
	smin_red2=smin_red1
	smax_red2=smax_red1
	vmin_red2=vmin_red1
	vmax_red2=vmax_red1
        lower1=np.array([hmin_red1,smin_red1-5,vmin_red1-5])
        upper1=np.array([hmax_red1,smax_red1+5,vmax_red1+5])
        mask1=cv2.inRange(hsv,lower1,upper1)
        lower=np.array([hmin_red2,smin_red2,vmin_red2])
        upper=np.array([hmax_red2,smax_red2,vmax_red2])
        mask2=cv2.inRange(hsv,lower,upper)
        mask=cv2.add(mask1,mask2)
    	#ret,mask = cv2.threshold(mask,157,255,0)
   	#mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    	#mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
        #cv2.imshow('mask',mask)
	return mask
def cal(matriz,hsv,kernel,n):
	global hmin_green,hmax_green,smin_green,vmin_green,smax_green,vmax_green,hmin_obs,hmax_obs,smin_obs,vmin_obs,smax_obs,vmax_obs,hmin_blue,hmax_blue,smin_blue,vmin_blue,smax_blue,vmax_blue,hmin_orange,hmax_orange,smin_orange,vmin_orange,smax_orange,vmax_orange,hmin_trash,hmax_trash,smin_trash,smax_trash,vmin_trash,vmax_trash
	if n==0:
		for x in range(len(matriz[:])):
			if hmin_green>matriz[x][0]:
				hmin_green=matriz[x][0]
			if hmax_green<matriz[x][0]:
				hmax_green=matriz[x][0]
			if smin_green>matriz[x][1]:
				smin_green=matriz[x][1]
			if vmin_green>matriz[x][2]:
				vmin_green=matriz[x][2]
			if smax_green<matriz[x][1]:
				smax_green=matriz[x][1]
			if vmax_green<matriz[x][2]:
				vmax_green=matriz[x][2]
		#print hmin,hmax,smin,smax,vmin,vmax
		lower=np.array([hmin_green,smin_green-5,vmin_green-5])
		upper=np.array([hmax_green,smax_green+5,vmax_green+5])
		mask=cv2.inRange(hsv,lower,upper)
	    	ret,mask = cv2.threshold(mask,157,255,0)
	   	#mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
	    	#mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
		#cv2.imshow('mask',mask)
		return mask
	if n==1:
		for x in range(len(matriz[:])):
			if hmin_obs>matriz[x][0]:
				hmin_obs=matriz[x][0]
			if hmax_obs<matriz[x][0]:
				hmax_obs=matriz[x][0]
			if smin_obs>matriz[x][1]:
				smin_obs=matriz[x][1]
			if vmin_obs>matriz[x][2]:
				vmin_obs=matriz[x][2]
			if smax_obs<matriz[x][1]:
				smax_obs=matriz[x][1]
			if vmax_obs<matriz[x][2]:
				vmax_obs=matriz[x][2]
		lower=np.array([hmin_obs,smin_obs-5,vmin_obs-5])
		upper=np.array([hmax_obs,smax_obs+5,vmax_obs+5])
		mask=cv2.inRange(hsv,lower,upper)
	    	ret,mask = cv2.threshold(mask,157,255,0)
	   	#mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
	    	#mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
		#cv2.imshow('mask',mask)
		return mask
	if n==2:
		for x in range(len(matriz[:])):
			if hmin_blue>matriz[x][0]:
				hmin_blue=matriz[x][0]
			if hmax_blue<matriz[x][0]:
				hmax_blue=matriz[x][0]
			if smin_blue>matriz[x][1]:
				smin_blue=matriz[x][1]
			if vmin_blue>matriz[x][2]:
				vmin_blue=matriz[x][2]
			if smax_blue<matriz[x][1]:
				smax_blue=matriz[x][1]
			if vmax_blue<matriz[x][2]:
				vmax_blue=matriz[x][2]
		#print hmin,hmax,smin,smax,vmin,vmax
		lower=np.array([hmin_blue,smin_blue-5,vmin_blue-5])
		upper=np.array([hmax_blue,smax_blue+5,vmax_blue+5])
		mask=cv2.inRange(hsv,lower,upper)
	    	ret,mask = cv2.threshold(mask,157,255,0)
	   	#mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
	    	#mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
		#cv2.imshow('mask',mask)
		return mask

	if n==3:
		for x in range(len(matriz[:])):
			if hmin_orange>matriz[x][0]:
				hmin_orange=matriz[x][0]
			if hmax_orange<matriz[x][0]:
				hmax_orange=matriz[x][0]
			if smin_orange>matriz[x][1]:
				smin_orange=matriz[x][1]
			if vmin_orange>matriz[x][2]:
				vmin_orange=matriz[x][2]
			if smax_orange<matriz[x][1]:
				smax_orange=matriz[x][1]
			if vmax_orange<matriz[x][2]:
				vmax_orange=matriz[x][2]
		#print 'naranja'
		#print hmin_orange,hmax_orange,smin_orange,smax_orange,vmin_orange,vmax_orange
		lower=np.array([hmin_orange,smin_orange-5,vmin_orange-5])
		upper=np.array([hmax_orange,smax_orange+5,vmax_orange+5])
		mask=cv2.inRange(hsv,lower,upper)
	    	ret,mask = cv2.threshold(mask,157,255,0)
	   	#mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
	    	#mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
		#cv2.imshow('mask',mask)
		return mask

	if n==4:
		for x in range(len(matriz[:])):
			if hmin_trash>matriz[x][0]:
				hmin_trash=matriz[x][0]
			if hmax_trash<matriz[x][0]:
				hmax_trash=matriz[x][0]
			if smin_trash>matriz[x][1]:
				smin_trash=matriz[x][1]
			if vmin_trash>matriz[x][2]:
				vmin_trash=matriz[x][2]
			if smax_trash<matriz[x][1]:
				smax_trash=matriz[x][1]
			if vmax_trash<matriz[x][2]:
				vmax_trash=matriz[x][2]
		#print 'trash'
		#print hmin_trash,hmax_trash,smin_trash,smax_trash,vmin_trash,vmax_trash
		lower=np.array([3,smin_trash-1,vmin_trash-1])
		upper=np.array([hmax_trash,smax_trash+1,vmax_trash+1])
		mask=cv2.inRange(hsv,lower,upper)
	    	ret,mask = cv2.threshold(mask,157,255,0)
	        #mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
        	#mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
	   	#mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
	    	#mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
		#cv2.imshow('mask',mask)
		return mask
def filtro(mask,frame,n):
    global arprom_green,arprom_red,arprom_obs,arprom_blue,arprom_orange,center_green,center_red,center_obs,center_blue,center_orange
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
	minarea=1000
	if n==0:
		for x_1 in range(n_1):
			c=contours[x_1]
			area=cv2.contourArea(c)
			M=cv2.moments(c)
			if M["m00"]>0:
				y=int(M["m01"] / M["m00"])
				x=int(M["m10"] / M["m00"])

				if area>100 and y<387:
					center=x,y
					if area<minarea and y<387:
						ar=area
					beta=beta+1
				        center_green.append(center)
					cv2.circle(frame, center, 5, (0, 255, 0), -1)
		arprom_green=ar
	if n==1:
		for x_1 in range(n_1):
			c=contours[x_1]
			area=cv2.contourArea(c)
			M=cv2.moments(c)
			
		        if M["m00"]>0:
				y=int(M["m01"] / M["m00"])
				x=int(M["m10"] / M["m00"])

				if area>120 and y<387:
					n_1=len(center_orange)
					chase=0
 					center=x,y
					if area<minarea and y<387:
						ar=area
					beta=beta+1
					center_red.append(center)
					cv2.circle(frame, center, 5, (0, 0, 255), -1)
		arprom_red=ar
	if n==2:
		for x_1 in range(n_1):
			c=contours[x_1]
			area=cv2.contourArea(c)
			M=cv2.moments(c)
			if M["m00"]>0:
				y=int(M["m01"] / M["m00"])
				x=int(M["m10"] / M["m00"])
				if area>100 and y<387 :
					center=x,y
					if area<minarea and y<387:
						ar=area
					beta=beta+1
				        center_obs.append(center)
					cv2.circle(frame, center, 5, (255, 0, 255), -1)
		arprom_obs=ar

	if n==3:
		for x_1 in range(n_1):
			c=contours[x_1]
			area=cv2.contourArea(c)
			M=cv2.moments(c)
			if M["m00"]>0:
				y=int(M["m01"] / M["m00"])
				x=int(M["m10"] / M["m00"])
				if area>100 and y<387 :
					center=x,y
					if area<minarea and y<387:
						ar=area
					beta=beta+1
				        center_blue.append(center)
					cv2.circle(frame, center, 5, (255, 0, 0), -1)
		arprom_blue=ar

	if n==4:
		for x_1 in range(n_1):
			c=contours[x_1]
			area=cv2.contourArea(c)
			M=cv2.moments(c)
			if M["m00"]>0:
				y=int(M["m01"] / M["m00"])
				x=int(M["m10"] / M["m00"])
				if area>100 and y<387 :
					center=x,y
					if area<minarea and y<387:
						ar=area
					beta=beta+1
				        center_orange.append(center)
					cv2.circle(frame, center, 5, (0, 165, 255), -1)
		arprom_orange=ar
def callback(message):
    global act,a,matriz,matriz1,matriz2,matriz4,matriz5,matriz6,matriz7,matriz8,matriz9,matriz10,matriz11,matriz12,matriz13,matriz14,matriz15,matriz16,matriz17,matriz18,matriz19,matriz20,matriz21,matriz22,matriz23,matriz24,matriz25,matriz26,matriz27,matriz28,matriz29,matriz30,matriz31,matriz32,matriz33,matriz34,matriz35,matriz36,matriz37,matriz38,matriz39,matriz36,matriz37,matriz38,matriz39
    bridge = CvBridge()
    frame = bridge.imgmsg_to_cv2(message, "bgr8")
    #frame=cv2.imread('calibrar_guardado.jpg')
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    kernel=np.ones((7,7),np.uint8)
    x_red1,y_red1=centro(145,60,frame)
    x_blue1,y_blue1=centro(185,60,frame)
    x_obs1,y_obs1=centro(230,70,frame)
    x_obs2,y_obs2=centro(269,70,frame)
    x_orange1,y_orange1=centro(305,55,frame)
    x_obs3,y_obs3=centro(342,68,frame)
    x_obs4,y_obs4=centro(384,68,frame)
    x_obs5,y_obs5=centro(419,65,frame)
    x_green1,y_green1=centro(463,50,frame)
    x_orange2,y_orange2=centro(140,106,frame)
    x_obs6,y_obs6=centro(182,115,frame)
    x_red2,y_red2=centro(220,105,frame)
    x_obs7,y_obs7=centro(267,117,frame)
    x_green2,y_green2=centro(304,100,frame)
    x_obs8,y_obs8=centro(343,115,frame)
    x_blue2,y_blue2=centro(385,99,frame)
    x_obs9,y_obs9=centro(428,113,frame)
    x_obs10,y_obs10=centro(464,113,frame)
    x_obs11,y_obs11=centro(139,165,frame)
    x_orange3,y_orange3=centro(174,153,frame)
    x_obs12,y_obs12=centro(220,163,frame)
    x_green3,y_green3=centro(260,150,frame)
    x_red3,y_red3=centro(302,150,frame)
    x_obs13,y_obs13=centro(347,159,frame)
    x_obs14,y_obs14=centro(390,161,frame)
    x_blue3,y_blue3=centro(435,150,frame)
    x_obs15,y_obs15=centro(470,160,frame)
    x_obs16,y_obs16=centro(133,213,frame)
    x_green4,y_green4=centro(168,208,frame)
    x_blue4,y_blue4=centro(212,208,frame)
    x_obs17,y_obs17=centro(260,215,frame)
    x_obs18,y_obs18=centro(308,215,frame)
    x_orange4,y_orange4=centro(345,206,frame)
    x_obs19,y_obs19=centro(391,217,frame)
    x_obs20,y_obs20=centro(435,217,frame)
    x_red4,y_red4=centro(485,205,frame)
    if a<200:
	    matrizdef(hsv,x_green1,y_green1,matriz)
	    matrizdef(hsv,x_green2,y_green2,matriz1)
	    matrizdef(hsv,x_green3,y_green3,matriz2)
	    matrizdef(hsv,x_green4,y_green4,matriz3)
	    matrizdef(hsv,x_blue1,y_blue1,matriz4)
	    matrizdef(hsv,x_blue2,y_blue2,matriz5)
	    matrizdef(hsv,x_blue3,y_blue3,matriz6)
	    matrizdef(hsv,x_blue4,y_blue4,matriz7)
	    matrizdef(hsv,x_obs1,y_obs1,matriz8)
	    matrizdef(hsv,x_obs2,y_obs2,matriz9)
	    matrizdef(hsv,x_obs3,y_obs3,matriz10)
	    matrizdef(hsv,x_obs4,y_obs4,matriz11)
	    matrizdef(hsv,x_obs5,y_obs5,matriz12)
	    matrizdef(hsv,x_obs6,y_obs6,matriz13)
	    matrizdef(hsv,x_obs7,y_obs7,matriz14)
	    matrizdef(hsv,x_obs8,y_obs8,matriz15)
	    matrizdef(hsv,x_obs9,y_obs9,matriz16)
	    matrizdef(hsv,x_obs10,y_obs10,matriz17)
	    matrizdef(hsv,x_obs11,y_obs11,matriz18)
	    matrizdef(hsv,x_obs12,y_obs12,matriz19)
	    matrizdef(hsv,x_obs13,y_obs13,matriz20)
	    matrizdef(hsv,x_obs14,y_obs14,matriz21)
	    matrizdef(hsv,x_obs15,y_obs15,matriz22)
	    matrizdef(hsv,x_obs16,y_obs16,matriz23)
	    matrizdef(hsv,x_obs17,y_obs17,matriz24)
	    matrizdef(hsv,x_obs18,y_obs18,matriz25)
	    matrizdef(hsv,x_obs19,y_obs19,matriz26)
	    matrizdef(hsv,x_obs20,y_obs20,matriz27)
	    matrizdef(hsv,x_red1,y_red1,matriz28)
	    matrizdef(hsv,x_red2,y_red2,matriz29)
	    matrizdef(hsv,x_red3,y_red3,matriz30)
	    matrizdef(hsv,x_red4,y_red4,matriz31)
	    matrizdef(hsv,x_orange1,y_orange1,matriz32)
	    matrizdef(hsv,x_orange2,y_orange2,matriz33)
	    matrizdef(hsv,x_orange3,y_orange3,matriz34)
	    matrizdef(hsv,x_orange4,y_orange4,matriz35)
	    a=a+1
	    cv2.imshow('frame', frame)
    if a>200:
	    act=1
	    global mask_green,mask_red,mask_obs
	    mask_green1=cal(matriz,hsv,kernel,0)
	    mask_green2=cal(matriz1,hsv,kernel,0)
	    mask_green3=cal(matriz2,hsv,kernel,0)
	    mask_green4=cal(matriz3,hsv,kernel,0)
	    mask_green=cv2.add(mask_green1,mask_green2,mask_green3,mask_green4)
	    mask_blue1=cal(matriz4,hsv,kernel,2)
	    mask_blue2=cal(matriz5,hsv,kernel,2)
	    mask_blue3=cal(matriz6,hsv,kernel,2)
	    mask_blue4=cal(matriz7,hsv,kernel,2)
	    mask_blue=cv2.add(mask_blue1,mask_blue2,mask_blue3,mask_blue4)
	    #mask_green_2=cv2.add(mask_green5,mask_green6,mask_green7,mask_green8)
	    #mask_green=cv2.add(mask_green_1,mask_green_2)
	    mask_obs1=cal(matriz8,hsv,kernel,1)
	    mask_obs2=cal(matriz9,hsv,kernel,1)
	    mask_obs3=cal(matriz10,hsv,kernel,1)
	    mask_obs4=cal(matriz11,hsv,kernel,1)
	    mask_obs5=cal(matriz12,hsv,kernel,1)
	    mask_obs6=cal(matriz13,hsv,kernel,1)
	    mask_obs7=cal(matriz14,hsv,kernel,1)
	    mask_obs8=cal(matriz15,hsv,kernel,1)
	    mask_obs9=cal(matriz16,hsv,kernel,1)
	    mask_obs10=cal(matriz17,hsv,kernel,1)
	    mask_obs11=cal(matriz18,hsv,kernel,1)
	    mask_obs12=cal(matriz19,hsv,kernel,1)
	    mask_obs13=cal(matriz20,hsv,kernel,1)
	    mask_obs14=cal(matriz21,hsv,kernel,1)
	    mask_obs15=cal(matriz22,hsv,kernel,1)
	    mask_obs16=cal(matriz23,hsv,kernel,1)
	    mask_obs17=cal(matriz24,hsv,kernel,1)
	    mask_obs18=cal(matriz25,hsv,kernel,1)
	    mask_obs19=cal(matriz26,hsv,kernel,1)
	    mask_obs20=cal(matriz27,hsv,kernel,1)
	    mask_obs_1=cv2.add(mask_obs1,mask_obs2,mask_obs3,mask_obs4)
	    mask_obs_2=cv2.add(mask_obs5,mask_obs6,mask_obs7,mask_obs8)
	    mask_obs_3=cv2.add(mask_obs9,mask_obs10,mask_obs11,mask_obs12)
	    mask_obs_4=cv2.add(mask_obs13,mask_obs14,mask_obs15,mask_obs16)
	    mask_obs_5=cv2.add(mask_obs17,mask_obs18,mask_obs19,mask_obs20)
	    mask_obs_6=cv2.add(mask_obs_1,mask_obs_2,mask_obs_3)
	    mask_obs_7=cv2.add(mask_obs_4,mask_obs_5)
	    mask_obs=cv2.add(mask_obs_6,mask_obs_7)
	    mask_orange1=cal(matriz32,hsv,kernel,3)
	    mask_orange2=cal(matriz33,hsv,kernel,3)
	    mask_orange3=cal(matriz34,hsv,kernel,3)
	    mask_orange4=cal(matriz35,hsv,kernel,3)
	    mask_orange=cv2.add(mask_orange1,mask_orange2,mask_orange3,mask_orange4)
	    mask_red1=cal1(matriz28,hsv,kernel)
	    mask_red2=cal1(matriz29,hsv,kernel)
	    mask_red3=cal1(matriz30,hsv,kernel)
	    mask_red4=cal1(matriz31,hsv,kernel)
	    mask_red=cv2.add(mask_red1,mask_red2,mask_red3,mask_red4)
	    mask_red=cv2.subtract(mask_red,mask_obs)
	    #mask_red=cv2.subtract(mask_red,mask_orange)
	    #mask_red=cv2.subtract(mask_red,mask_trash)
	    #mask_red_2=cv2.add(mask_red5,mask_red6,mask_red7,mask_red8)
	    #mask_red=cv2.add(mask_red_1,mask_red_2)
	    filtro(mask_green,frame,0)
	    filtro(mask_obs,frame,2)
	    filtro(mask_blue,frame,3)
	    filtro(mask_orange,frame,4)
	    filtro(mask_red,frame,1)
	    cv2.imshow('mask_rojo', mask_red)
	    cv2.imshow('mask_blue',mask_blue)
	    cv2.imshow('mask_orange',mask_orange)
	    cv2.imshow('mask_obs',mask_obs)
	    global center_green,center_red,center_obs,center_blue,center_orange
	    global xmin1,xmin2,ymin1,ymin2,xmax1,xmax2,ymax1,ymax2
	    #frame2= bridge.imgmsg_to_cv2(message, "bgr8")
	    if a==200:
	    	xmin1,xmin2,ymin1,ymin2,xmax1,xmax2,ymax1,ymax2=coor(center_green,center_red,center_obs,center_orange,center_blue,frame)
	    #center1=xmin1,ymax1
	    #center2=xmin2,ymin1
	    #center3=xmax1,ymin2
	    #center4=xmax2,ymax2
            #cv2.circle(frame2, center1, 5, (0, 0, 0), -1)
            #cv2.circle(frame2, center2, 5, (0, 0, 0), -1)
            #cv2.circle(frame2, center3, 5, (0, 0, 0), -1)
            #cv2.circle(frame2, center4, 5, (0, 0, 0), -1)
	    #cv2.imshow('frame2',frame2)
    	    #global arprom_green,arprom_red,arprom_obs,mask_green,mask_red,mask_obs,xmin1,xmin2,ymin1,ymin2,xmax1,xmax2,ymax1,ymax2
            frame1= bridge.imgmsg_to_cv2(message, "bgr8")
	    Centro_green=filtro2(mask_green,kernel,frame1,0)
	    Centro_red=filtro2(mask_red,kernel,frame1,1)
	    Centro_obs=filtro2(mask_obs,kernel,frame1,2)
	    Centro_orange=filtro2(mask_orange,kernel,frame1,3)
	    Centro_blue=filtro2(mask_blue,kernel,frame1,4)
	    organizar(Centro_green,Centro_obs,Centro_red,Centro_orange,Centro_blue)
            organizar2(Centro_green,Centro_obs,Centro_red,Centro_orange,Centro_blue)
	    #cv2.destroyAllWindows()
	    cv2.imshow('frame1', frame1)
	     
	    a=a+1

    cv2.imshow('frame', frame)
    cv2.waitKey(3)
def filtro2(mask,kernel,frame,colortip):
    global arprom_green,arprom_red,arprom_obs,arprom_blue,arprom_orange,xmin1,xmin2,ymin1,ymin2,xmax1,xmax2,ymax1,ymax2
    contours=cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    n=len(contours)
    a=0
    Centro=list(range(0,n+1))
    if len(contours)>0:
	n_1=len(contours)
	for x_1 in range(n_1):
		c=contours[x_1]
		area=cv2.contourArea(c)
		M=cv2.moments(c)
		if M["m00"]>0:
			y=int(M["m01"] / M["m00"])
			x=int(M["m10"] / M["m00"])
			if colortip==0:
				if area>=100 and (((x>xmin1-20 or x>xmin2-20) and (x<xmax1+20 or x<xmax2+20)) and ((y<ymax1+20 or y<ymax2+20) and (y>ymin1-20 or y>ymin2-20))):

				        center=x,y
				        Centro[a]=x,y
				        a=a+1
					cv2.circle(frame, center, 5, (0, 255, 0), -1)
			if colortip==1:
				if area>=100 and (((x>xmin1-20 or x>xmin2-20) and (x<xmax1+20 or x<xmax2+20)) and ((y<ymax1+20 or y<ymax2+20) and (y>ymin1-20 or y>ymin2-20))):

				        center=x,y
				        Centro[a]=x,y
				        a=a+1
					cv2.circle(frame, center, 5, (0, 0, 255), -1)
			if colortip==2:
				if area>=100 and (((x>xmin1-20 or x>xmin2-20) and (x<xmax1+20 or x<xmax2+20)) and ((y<ymax1+20 or y<ymax2+20) and (y>ymin1-20 or y>ymin2-20))):
				        center=x,y
				        Centro[a]=x,y
				        a=a+1
					cv2.circle(frame, center, 5, (255, 0, 255), -1)
			if colortip==3:
				if area>=100 and (((x>xmin1-20 or x>xmin2-20) and (x<xmax1+20 or x<xmax2+20)) and ((y<ymax1+20 or y<ymax2+20) and (y>ymin1-20 or y>ymin2-20))):

				        center=x,y
				        Centro[a]=x,y
				        a=a+1
					cv2.circle(frame, center, 5, (0, 165, 255), -1)
			if colortip==4:
				if area>=100 and (((x>xmin1-20 or x>xmin2-20) and (x<xmax1+20 or x<xmax2+20)) and ((y<ymax1+20 or y<ymax2+20) and (y>ymin1-20 or y>ymin2-20))):

				        center=x,y
				        Centro[a]=x,y
				        a=a+1
					cv2.circle(frame, center, 5, (255, 0, 0), -1)
    Centro=Centro[0:a]
    return Centro
def getKey2(item):
    return item[1]
def getKey3(item):
    return item[0]
def organizar(Centro_verde,Centro_negro,Centro_rojo,Centro_naranja,Centro_azul):
	global matriz_1x,matriz_2x,matriz_3x,matriz_4x,matriz_1y,matriz_2y,matriz_3y,matriz_4y
	longitud=len(Centro_verde)+len(Centro_negro)+len(Centro_rojo)+len(Centro_naranja)+len(Centro_azul)
        Order=list(range(0,longitud+10))
	print len(Centro_verde),len(Centro_negro),len(Centro_rojo),len(Centro_naranja),len(Centro_azul)
	y=0
        if longitud==36:
		if len(Centro_verde)>0:
			for x in range(len(Centro_verde)):
				Order[x]=Centro_verde[x]
			y=x+1
		if len(Centro_rojo)>0:
			for x in range(len(Centro_rojo)):
				Order[x+y]=Centro_rojo[x]
			y=y+x+1
		if len(Centro_negro)>0:
			for x in range(len(Centro_negro)):
				Order[x+y]=Centro_negro[x]
			y=y+x+1
		if len(Centro_naranja)>0:
			for x in range(len(Centro_naranja)):
				Order[x+y]=Centro_naranja[x]
			y=y+x+1
		if len(Centro_azul)>0:
			for x in range(len(Centro_azul)):
				Order[x+y]=Centro_azul[x]
		Order=Order[0:longitud]
		Order=sorted(Order,key=getKey2)

		matriz = [range(9) for i in range(4)]
		aux=0
		for x in range(4):
			for y in range(9):
				matriz[x][y]=Order[aux]
				aux=aux+1
		for x in range(4):
		    matriz[x]=sorted(matriz[x],key=getKey3)
		matriz_1x=list(range(0,9))
		matriz_1y=list(range(0,9))
		matriz_2x=list(range(0,9))
		matriz_2y=list(range(0,9))
		matriz_3x=list(range(0,9))
		matriz_3y=list(range(0,9))
		matriz_4x=list(range(0,9))
		matriz_4y=list(range(0,9))
		for x in range(9):
			matriz_1x[x]=matriz[0][x][0]
			matriz_1y[x]=matriz[0][x][1]
			matriz_2x[x]=matriz[1][x][0]
			matriz_2y[x]=matriz[1][x][1]
			matriz_3x[x]=matriz[2][x][0]
			matriz_3y[x]=matriz[2][x][1]
			matriz_4x[x]=matriz[3][x][0]
			matriz_4y[x]=matriz[3][x][1]



def getKey4(item):
    return item[0][1]
def getKey5(item):
    return item[0][0]
def organizar2(Centro_verde,Centro_negro,Centro_rojo,Centro_naranja,Centro_azul):
	global matriz_5,matriz_6,matriz_7,matriz_8,now,alpha
	longitud=len(Centro_verde)+len(Centro_negro)+len(Centro_rojo)+len(Centro_naranja)+len(Centro_azul)
        Order=list(range(0,longitud+10))
	y=0
        if longitud==36:
		for x in range(len(Centro_verde)):
			Centro_verde[x]=Centro_verde[x],1
		for x in range(len(Centro_rojo)):
			Centro_rojo[x]=Centro_rojo[x],2
		for x in range(len(Centro_naranja)):
			Centro_naranja[x]=Centro_naranja[x],3
		for x in range(len(Centro_azul)):
			Centro_azul[x]=Centro_azul[x],4
		for x in range(len(Centro_negro)):
			Centro_negro[x]=Centro_negro[x],0

		if len(Centro_verde)>0:
			for x in range(len(Centro_verde)):
				Order[x]=Centro_verde[x]
			y=x+1
		if len(Centro_rojo)>0:
			for x in range(len(Centro_rojo)):
				Order[x+y]=Centro_rojo[x]
			y=y+x+1
		if len(Centro_negro)>0:
			for x in range(len(Centro_negro)):
				Order[x+y]=Centro_negro[x]
			y=y+x+1
		if len(Centro_naranja)>0:
			for x in range(len(Centro_naranja)):
				Order[x+y]=Centro_naranja[x]
			y=y+x+1
		if len(Centro_azul)>0:
			for x in range(len(Centro_azul)):
				Order[x+y]=Centro_azul[x]

		Order=Order[0:longitud]
		Order=sorted(Order,key=getKey4)

		matriz = [range(9) for i in range(4)]
		aux=0
		for x in range(4):
			for y in range(9):
				matriz[x][y]=Order[aux]
				aux=aux+1
		for x in range(4):
		    matriz[x]=sorted(matriz[x],key=getKey5)
		for x in range(4):
			for y in range(9):
				matriz[x][y]=matriz[x][y][1]

		matriz_5=matriz[0]
		matriz_6=matriz[1]
		matriz_7=matriz[2]
		matriz_8=matriz[3]
		now =rospy.get_time()
		alpha=1
	else:
                alpha=0
def get_obj_calibrate(request):
        global matriz_1x,matriz_2x,matriz_3x,matriz_4x,matriz_1y,matriz_2y,matriz_3y,matriz_4y,matriz_5,matriz_6,matriz_7,matriz_8
	rospy.sleep(0.5)
	return InfoCoorResponse(matriz_1x,matriz_2x,matriz_3x,matriz_4x,matriz_1y,matriz_2y,matriz_3y,matriz_4y,matriz_5,matriz_6,matriz_7,matriz_8)
def main():
    #Initiate left hand camera object detection node
    rospy.init_node('calibrador_color_camara')
    cv2.namedWindow("frame", 1)
    #cv2.namedWindow("frame1", 1)
    #Subscribe to left hand camera image
    rospy.Subscriber("/camera/rgb/image_color", Image, callback)
    InfoCoor_srv = rospy.Service("InfoCoor_service", InfoCoor, get_obj_calibrate)
    rospy.spin()

if __name__ == '__main__':
     global act,matriz,matriz1,matriz2,matriz4,matriz5,matriz6,matriz7,matriz8,matriz9,matriz10,matriz11,matriz12,matriz13,matriz14,matriz15,matriz16,matriz17,matriz18,matriz19,matriz20,matriz21,matriz22,matriz23,matriz24,matriz25,matriz26,matriz27,matriz28,matriz29,matriz30,matriz31,matriz32,matriz33,matriz34,matriz35,a,hmin_green,hmax_green,smin_green,vmin_green,smax_green,vmax_green,hmin_obs,hmax_obs,smin_obs,vmin_obs,smax_obs,vmax_obs,hmin_red1,hmax_red1,smin_red1,vmin_red1,smax_red1,vmax_red1,hmin_red2,hmax_red2,smin_red2,smax_red2,vmin_red2,vmax_red2,x_1,y_1,arprom_green,arprom_red,arprom_obs,arprom_blue,arprom_orange,center_green,center_red,center_obs,center_blue,center_orange,hmin_blue,hmax_blue,smin_blue,vmin_blue,smax_blue,vmax_blue,hmin_orange,hmax_orange,smin_orange,vmin_orange,smax_orange,vmax_orange
     x_1=0
     y_1=0
     a=0
     act=0
     center_green=list()
     center_red=list()
     center_obs=list()
     center_blue=list()
     center_orange=list()
     arprom_green=0
     arprom_red=0
     arprom_obs=0
     arprom_blue=0
     arprom_orange=0
     hmin_green=1000
     hmax_green=0
     smin_green=1000
     vmin_green=1000
     smax_green=0
     vmax_green=0
     hmin_obs=1000
     hmax_obs=0
     smin_obs=1000
     vmin_obs=1000
     smax_obs=0
     vmax_obs=0
     hmin_red1=1000
     hmax_red1=0
     smin_red1=1000
     vmin_red1=1000
     smax_red1=0
     vmax_red1=0
     hmin_blue=1000
     hmax_blue=0
     smin_blue=1000
     vmin_blue=1000
     smax_blue=0
     vmax_blue=0
     hmin_orange=1000
     hmax_orange=0
     smin_orange=1000
     vmin_orange=1000
     smax_orange=0
     vmax_orange=0
     matriz=list()
     matriz1=list()
     matriz2=list()
     matriz3=list()
     matriz4=list()
     matriz5=list()
     matriz6=list()
     matriz7=list()
     matriz8=list()
     matriz9=list()
     matriz10=list()
     matriz11=list()
     matriz12=list()
     matriz13=list()
     matriz14=list()
     matriz15=list()
     matriz16=list()
     matriz17=list()
     matriz18=list()
     matriz19=list()
     matriz20=list()
     matriz21=list()
     matriz22=list()
     matriz23=list()
     matriz24=list()
     matriz25=list()
     matriz26=list()
     matriz27=list()
     matriz28=list()
     matriz29=list()
     matriz30=list()
     matriz31=list()
     matriz32=list()
     matriz33=list()
     matriz34=list()
     matriz35=list()
     global matriz36,matriz37,matriz38,matriz39,hmin_trash,hmax_trash,smin_trash,smax_trash,vmin_trash,vmax_trash
     hmin_trash=1000
     hmax_trash=0
     smin_trash=1000
     vmin_trash=1000
     smax_trash=0
     vmax_trash=0
     matriz36=list()
     matriz37=list()
     matriz38=list()
     matriz39=list()
     main()

