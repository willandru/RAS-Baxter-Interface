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

def callback(message):
    global response
    bridge = CvBridge()
    frame = bridge.imgmsg_to_cv2(message, "bgr8")
    lower_verde,upper_verde=def_color(response.Hmin_verde,response.Vmin_verde,response.Smin_verde,response.Hmax_verde,response.Vmax_verde,response.Smax_verde)
    lower_negro,upper_negro=def_color(response.Hmin_negro,response.Vmin_negro,response.Smin_negro,response.Hmax_negro,response.Vmax_negro,response.Smax_negro)
    lower_rojo1,upper_rojo1=def_color(response.Hmin_rojo1,response.Vmin_rojo1,response.Smin_rojo1,response.Hmax_rojo1,response.Vmax_rojo1,response.Smax_rojo1)
    lower_rojo2,upper_rojo2=def_color(response.Hmin_rojo2,response.Vmin_rojo2,response.Smin_rojo2,response.Hmax_rojo2,response.Vmax_rojo2,response.Smax_rojo2)
    kernel=np.ones((7,7),np.uint8)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask_verde=mask_imagen(hsv,lower_verde,upper_verde)
    contour_verde,Centro_verde=filtro(mask_verde,kernel,frame,response.arprom_verde,response.Hum_verde)
    mask_negro=mask_imagen(hsv,lower_negro,upper_negro)
    contour_negro,Centro_negro=filtro(mask_negro,kernel,frame,response.arprom_negro,response.Hum_negro)
    mask_rojo=mask_imagen_rojo(hsv,lower_rojo1,upper_rojo1,lower_rojo2,upper_rojo2)
    contour_rojo,Centro_rojo=filtro(mask_rojo,kernel,frame,response.arprom_rojo,response.Hum_rojo1)  
    organizar(Centro_verde,Centro_negro,Centro_rojo)	
    cv2.imshow('frame', frame)
    cv2.waitKey(3)   
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
def filtro(mask,kernel,frame,arprom,Hum):
    global response
    ret,mask = cv2.threshold(mask,157,255,0)
    mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
    contours=cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    n=len(contours)
    a=0
    Centro=list(range(0,n+1))
    ar=(arprom*Hum)/100
    if len(contours)>0:
	n_1=len(contours)
	for x_1 in range(n_1):
		c=contours[x_1]
		area=cv2.contourArea(c)
		M=cv2.moments(c)
		y=int(M["m01"] / M["m00"])
		x=int(M["m10"] / M["m00"])
	        
		if area>=ar and (((x>response.xmin1-5 or x>response.xmin2-5) and (x<response.xmax1+5 or x<response.xmax2+5)) and ((y<response.ymax1+5 or y<response.ymax2+5) and (y>response.ymin1-20 or y>response.ymin2-20))):
			 
                        center=x,y
                        Centro[a]=x,y
                        a=a+1
		        cv2.circle(frame, center, 5, (0, 0, 255), -1)
    Centro=Centro[0:a]
    return contours,Centro
def getKey(item):
    return item[0][1]
def getKey1(item):
    return item[0][0]
def organizar(Centro_verde,Centro_negro,Centro_rojo):
	global matriz1,matriz2,matriz3,matriz4,now,alpha
	longitud=len(Centro_verde)+len(Centro_negro)+len(Centro_rojo)
        Order=list(range(0,longitud+1))
        if longitud==36:
		for x in range(len(Centro_verde)):
			Centro_verde[x]=Centro_verde[x],0
		for x in range(len(Centro_rojo)):
			Centro_rojo[x]=Centro_rojo[x],1
		for x in range(len(Centro_negro)):
			Centro_negro[x]=Centro_negro[x],2 

		for x in range(len(Centro_verde)):
			Order[x]=Centro_verde[x]
		y=x+1
		for x in range(len(Centro_rojo)):
			Order[x+y]=Centro_rojo[x]
		m=y+x+1
		for x in range(len(Centro_negro)):
			Order[x+m]=Centro_negro[x] 
		Order=Order[0:longitud]
		Order=sorted(Order,key=getKey)
	
		matriz = [range(9) for i in range(4)]
		aux=0
		for x in range(4):
			for y in range(9):
				matriz[x][y]=Order[aux]
				aux=aux+1
		for x in range(4):
		    matriz[x]=sorted(matriz[x],key=getKey1)
		
		for x in range(4):
			for y in range(9):
				matriz[x][y]=matriz[x][y][1]
			
		matriz1=matriz[0]
		matriz2=matriz[1]
		matriz3=matriz[2]
		matriz4=matriz[3]
		now =rospy.get_time()
		alpha=1
	else:
                alpha=0


	
       
def get_obj_calibrate(request):
        global matriz1,matriz2,matriz3,matriz4,now
	rospy.sleep(0.5)
	return InfoResponse(matriz1,matriz2,matriz3,matriz4,now) 
def look(request):
        global alpha
	rospy.sleep(0.5)
	return CorResponse(alpha)        
def user():
    global response
    Calibrado_service = rospy.ServiceProxy("Calibrado_service", Calibrado)
    rospy.wait_for_service('Calibrado_service')
    response = Calibrado_service.call(CalibradoRequest())
    cv2.namedWindow("frame",1)
    rospy.Subscriber("/camera/rgb/image_color", Image, callback)
    Info_srv = rospy.Service("Info_service", Info, get_obj_calibrate)
    Cor_srv = rospy.Service("Cor_service", Cor, look)
    rospy.spin()
def main():
    rospy.init_node('colornode')
    Calibrado_service = rospy.ServiceProxy("Calibrado_service", Calibrado)
    rospy.wait_for_service('Calibrado_service')
    while not rospy.is_shutdown():
	    response = Calibrado_service.call(CalibradoRequest())
            print response.act 
	    if response.act==1:
               user()

	    

if __name__ == '__main__':
     main()
