#!/usr/bin/env python
#Reference: the baxter_stocking_stuffer project by students in Northwestern's MSR program - Josh Marino, Sabeen Admani, Andrew Turchina and Chu-Chu Igbokwe
#Service provided - ObjLocation service - contains x,y,z coordinates of object in baxter's stationary body frame, whether it is ok to grasp and if objects were found in the current frame.

import rospy
import numpy as np
import cv2
import cv_bridge
import baxter_interface
import math
import datetime
from std_msgs.msg import String,Int32MultiArray
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge, CvBridgeError
from jp_baxtertry1.srv import *
import time

def matriz1(response,Orderold):
    global time1,n
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
    Order[0:n]=Order[0:n]
    Order[n]=time1
    change=0
    for x in range(n):
	if Order[x]!=Orderold[x]:
		print(Order[x])
		change=1

    if change==0:
        Order[0:n]=Orderold[0:n]
    if change==1:
	Orderold[0:n]=Order[0:n]
	Orderold[n]=Order[n]-Orderold[n]
    return change
def matriz2(response,Orderold):
    global time1,n
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
    Order[0:n]=Order[0:n]
    Order[n]=time1
    Orderold[0:n]=Order[0:n]
    Orderold[n]=Order[n]-Orderold[n]
    return Orderold
def cantidad_colores(color,Orderold):
    n_1=len(Orderold)
    azul_aux=0
    verde_aux=0
    rojo_aux=0
    amarillo_aux=0
    for x in range(n_1-1):
	if Orderold[x]==1:
		verde_aux=verde_aux+1
	if Orderold[x]==2:
		rojo_aux=rojo_aux+1
	if Orderold[x]==4:
		azul_aux=azul_aux+1
	if Orderold[x]==3:
		amarillo_aux=amarillo_aux+1
    obstaculos=36-color
    obstaculos_aux=36-azul_aux-verde_aux-rojo_aux-amarillo_aux
    continuar=0 
    if color==1:
	    if ((azul_aux==2 and verde_aux==0 and rojo_aux==0 and amarillo_aux==0) or (azul_aux==0 and verde_aux==2 and rojo_aux==0 and amarillo_aux==0)or (azul_aux==0 and verde_aux==0 and rojo_aux==2 and amarillo_aux==0) or (azul_aux==0 and verde_aux==0 and rojo_aux==0 and amarillo_aux==2)):
		continuar=1
    if color==2:
	    if ((azul_aux==2 and verde_aux==2 and rojo_aux==0 and amarillo_aux==0) or (azul_aux==2 and verde_aux==0 and rojo_aux==2 and amarillo_aux==0) or (azul_aux==2 and verde_aux==0 and rojo_aux==0 and amarillo_aux==2) or (azul_aux==0 and verde_aux==2 and rojo_aux==2 and amarillo_aux==0) or (azul_aux==0 and verde_aux==2 and rojo_aux==0 and amarillo_aux==2) or (azul_aux==0 and verde_aux==0 and rojo_aux==2 and amarillo_aux==2)):
		continuar=1
    if color==3:
	    if ((azul_aux==2 and verde_aux==2 and rojo_aux==2 and amarillo_aux==0) or (azul_aux==2 and verde_aux==2 and rojo_aux==0 and amarillo_aux==2) or (azul_aux==2 and verde_aux==0 and rojo_aux==2 and amarillo_aux==2) or (azul_aux==0 and verde_aux==2 and rojo_aux==2 and amarillo_aux==2)):
		continuar=1
    if color==4:
	    if ((azul_aux==2 and verde_aux==2 and rojo_aux==2 and amarillo_aux==2)):
		continuar=1
    if obstaculos_aux==36:
	continuar=2
    return continuar  
def main(dificultad,matriz,beta_juego,aux_help,aux2,imp):
    global Orderold
    if aux_help ==0:
	    Orderold=matriz
    global time1
    close=0
    time1 = datetime.datetime.now()
    time1=time.mktime(time1.timetuple())
    time2=time1
    pub = rospy.Publisher('matriz', Int32MultiArray, queue_size=36)
    rate = rospy.Rate(10) # 10hz
    Orderes=Int32MultiArray()
    #print Orderold
    time1 = datetime.datetime.now()
    time1=time.mktime(time1.timetuple())
    global n
    continuar=0
    if dificultad==1:
	color=1
        continuar=cantidad_colores(color,Orderold)
	aux2=1
    elif dificultad==2:
	color=2
        continuar=cantidad_colores(color,Orderold)
	aux2=1
    elif dificultad==3:
	color=3
        continuar=cantidad_colores(color,Orderold)
	aux2=1
    elif dificultad==4:
	color=4
        continuar=cantidad_colores(color,Orderold)
	aux2=1
    else:
	aux2=0
    if continuar==1:
        close=1
        print 'bien'
        InfoCoor_service = rospy.ServiceProxy("InfoCoor_service", InfoCoor)
        rospy.wait_for_service('InfoCoor_service')
        response = InfoCoor_service.call(InfoCoorRequest())
        change=matriz1(response,Orderold)
        if (change==1 and aux2==1) or imp==0:
	    	 if dificultad==1:
			color=1
			continuar=cantidad_colores(color,Orderold)
	    	 elif dificultad==2:
			color=2
			continuar=cantidad_colores(color,Orderold)
	    	 elif dificultad==3:
			color=3
			continuar=cantidad_colores(color,Orderold)
	    	 elif dificultad==4:
			color=4
			continuar=cantidad_colores(color,Orderold)
		 if continuar==1:	
			 Orderes.data=Orderold
			 rospy.loginfo(Orderes)
			 pub.publish(Orderes)
			 Orderold[n]=time1
		         close=2
			 aux2=0
    if continuar==2 and imp==0:
	    InfoCoor_service = rospy.ServiceProxy("InfoCoor_service", InfoCoor)
    	    rospy.wait_for_service('InfoCoor_service')
    	    response = InfoCoor_service.call(InfoCoorRequest())
	    mat=matriz2(response,Orderold)
	    Orderes.data=mat
	    rospy.loginfo(Orderes)
	    pub.publish(Orderes)
	    Orderold[n]=time1
	    close=2	
    return close,continuar
