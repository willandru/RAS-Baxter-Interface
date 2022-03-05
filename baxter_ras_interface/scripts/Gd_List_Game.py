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
import sys
sys.path.append('/home/z420/ros_ws/src/jp_baxtertry1/scripts')
import Gd_List_Game1
import Gd_List_Game2
import Gd_List_Game3
def mainmatriz(response):
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
	Order[x+y_2]=response.matriz_8[x]    #0 VERDE,1 ROJO, 2 OBS
    Order[0:n]=Order[0:n]
    Order[n]=0
    return Order

def main():
    #Initiate left hand camera object detection node
    rospy.init_node('matriz_actual_problema')
    InfoCoor_service = rospy.ServiceProxy("InfoCoor_service", InfoCoor)
    juego_dificultad_service = rospy.ServiceProxy("juego_dificultad_service", juego_dificultad)
    beta_juego=0
    aux_help=0
    a=0
    aux2=0
    imp=0
    while not rospy.is_shutdown():
	    rospy.wait_for_service('InfoCoor_service')
	    response = InfoCoor_service.call(InfoCoorRequest())
	    matriz=mainmatriz(response)	
	    rospy.wait_for_service('juego_dificultad_service')
	    responses = juego_dificultad_service.call(juego_dificultadRequest())
	    juego=responses.x
	    dificultad=responses.y
	    if juego==1:
		a=0
		imp=0
		while dificultad==1:
			if a==0:
				beta_juego=0
				aux_help=0
				a=a+1
		        rospy.wait_for_service('InfoCoor_service')
		        response = InfoCoor_service.call(InfoCoorRequest())
		        matriz=mainmatriz(response)
   		        rospy.wait_for_service('juego_dificultad_service')
		        responses = juego_dificultad_service.call(juego_dificultadRequest())
		        juego=responses.x
		        dificultad=responses.y
			close,continuar=Gd_List_Game1.main(dificultad,matriz,beta_juego,aux_help,imp)
			if continuar==2:
				imp=2
			if continuar==1:
				if imp==0:
					imp=1
				if imp==2:
					imp=0
			if continuar==0:
				imp=0
			if close ==1:
				aux_help=1
			if close ==2:
				aux_help=0
			if close ==1:
				aux_help=1
			if close ==2:
				aux_help=0
		a=0
		imp=0
		while dificultad==2:
			if a==0:
				beta_juego=0
				aux_help=0
				a=a+1
		        rospy.wait_for_service('InfoCoor_service')
		        response = InfoCoor_service.call(InfoCoorRequest())
		        matriz=mainmatriz(response)
   		        rospy.wait_for_service('juego_dificultad_service')
		        responses = juego_dificultad_service.call(juego_dificultadRequest())
		        juego=responses.x
		        dificultad=responses.y
			close,continuar=Gd_List_Game1.main(dificultad,matriz,beta_juego,aux_help,imp)
			if continuar==2:
				imp=2
			if continuar==1:
				if imp==0:
					imp=1
				if imp==2:
					imp=0
			if continuar==0:
				imp=0
			if close ==1:
				aux_help=1
			if close ==2:
				aux_help=0
		a=0
		imp=0
		while dificultad==3:
			if a==0:
				beta_juego=0
				aux_help=0
				a=a+1
		        rospy.wait_for_service('InfoCoor_service')
		        response = InfoCoor_service.call(InfoCoorRequest())
		        matriz=mainmatriz(response)
   		        rospy.wait_for_service('juego_dificultad_service')
		        responses = juego_dificultad_service.call(juego_dificultadRequest())
		        juego=responses.x
		        dificultad=responses.y
			close,continuar=Gd_List_Game1.main(dificultad,matriz,beta_juego,aux_help,imp)
			if continuar==2:
				imp=2
			if continuar==1:
				if imp==0:
					imp=1
				if imp==2:
					imp=0
			if continuar==0:
				imp=0
			if close ==1:
				aux_help=1
			if close ==2:
				aux_help=0
	    if juego==2:
		a=0
		aux2=0
		imp=0
		while dificultad==1:
			if a==0:
				beta_juego=0
				aux_help=0
				a=a+1
		        rospy.wait_for_service('InfoCoor_service')
		        response = InfoCoor_service.call(InfoCoorRequest())
		        matriz=mainmatriz(response)
   		        rospy.wait_for_service('juego_dificultad_service')
		        responses = juego_dificultad_service.call(juego_dificultadRequest())
		        juego=responses.x
		        dificultad=responses.y
			close,continuar=Gd_List_Game2.main(dificultad,matriz,beta_juego,aux_help,aux2,imp)
			if continuar==2:
				imp=2
			if continuar==1:
				if imp==0:
					imp=1
				if imp==2:
					imp=0
			if continuar==0:
				imp=0
			if close ==1:
				aux_help=1
			if close ==2:
				aux_help=0
		a=0
		aux2=0
		imp=0
		while dificultad==2:
			if a==0:
				beta_juego=0
				aux_help=0
				a=a+1
		        rospy.wait_for_service('InfoCoor_service')
		        response = InfoCoor_service.call(InfoCoorRequest())
		        matriz=mainmatriz(response)
   		        rospy.wait_for_service('juego_dificultad_service')
		        responses = juego_dificultad_service.call(juego_dificultadRequest())
		        juego=responses.x
		        dificultad=responses.y
			close,continuar=Gd_List_Game2.main(dificultad,matriz,beta_juego,aux_help,aux2,imp)
			if continuar==2:
				imp=2
			if continuar==1:
				if imp==0:
					imp=1
				if imp==2:
					imp=0
			if continuar==0:
				imp=0
			if close ==1:
				aux_help=1
			if close ==2:
				aux_help=0
		a=0
		aux2=0
		imp=0
		while dificultad==3:
			if a==0:
				beta_juego=0
				aux_help=0
				a=a+1
		        rospy.wait_for_service('InfoCoor_service')
		        response = InfoCoor_service.call(InfoCoorRequest())
		        matriz=mainmatriz(response)
   		        rospy.wait_for_service('juego_dificultad_service')
		        responses = juego_dificultad_service.call(juego_dificultadRequest())
		        juego=responses.x
		        dificultad=responses.y
			close,continuar=Gd_List_Game2.main(dificultad,matriz,beta_juego,aux_help,aux2,imp)
			if continuar==2:
				imp=2
			if continuar==1:
				if imp==0:
					imp=1
				if imp==2:
					imp=0
			if continuar==0:
				imp=0
			if close ==1:
				aux_help=1
			if close ==2:
				aux_help=0
		a=0
		aux2=0
		imp=0
		while dificultad==4:
			if a==0:
				beta_juego=0
				aux_help=0
				a=a+1
		        rospy.wait_for_service('InfoCoor_service')
		        response = InfoCoor_service.call(InfoCoorRequest())
		        matriz=mainmatriz(response)
   		        rospy.wait_for_service('juego_dificultad_service')
		        responses = juego_dificultad_service.call(juego_dificultadRequest())
		        juego=responses.x
		        dificultad=responses.y
			close,continuar=Gd_List_Game2.main(dificultad,matriz,beta_juego,aux_help,aux2,imp)
			if continuar==2:
				imp=2
			if continuar==1:
				if imp==0:
					imp=1
				if imp==2:
					imp=0
			if continuar==0:
				imp=0
			if close ==1:
				aux_help=1
			if close ==2:
				aux_help=0
	    if juego==3:
		a=0
		imp=0
		while dificultad==1:
			if a==0:
				beta_juego=0
				aux_help=0
				a=a+1
		        rospy.wait_for_service('InfoCoor_service')
		        response = InfoCoor_service.call(InfoCoorRequest())
		        matriz=mainmatriz(response)
   		        rospy.wait_for_service('juego_dificultad_service')
		        responses = juego_dificultad_service.call(juego_dificultadRequest())
		        juego=responses.x
		        dificultad=responses.y
			close,continuar=Gd_List_Game3.main(dificultad,matriz,beta_juego,aux_help,imp)
			if continuar==2:
				imp=2
			if continuar==1:
				if imp==0:
					imp=1
				if imp==2:
					imp=0
			if continuar==0:
				imp=0
			if close ==1:
				aux_help=1
			if close ==2:
				aux_help=0
		a=0
		imp=0
		while dificultad==2:
			if a==0:
				beta_juego=0
				aux_help=0
				a=a+1
		        rospy.wait_for_service('InfoCoor_service')
		        response = InfoCoor_service.call(InfoCoorRequest())
		        matriz=mainmatriz(response)
   		        rospy.wait_for_service('juego_dificultad_service')
		        responses = juego_dificultad_service.call(juego_dificultadRequest())
		        juego=responses.x
		        dificultad=responses.y
			close,continuar=Gd_List_Game3.main(dificultad,matriz,beta_juego,aux_help,imp)
			if continuar==2:
				imp=2
			if continuar==1:
				if imp==0:
					imp=1
				if imp==2:
					imp=0
			if continuar==0:
				imp=0
			if close ==1:
				aux_help=1
			if close ==2:
				aux_help=0
		a=0
if __name__ == '__main__':
     main()
