#!/usr/bin/env python
#Reference: the baxter_stocking_stuffer project by students in Northwestern's MSR program - Josh Marino, Sabeen Admani, Andrew Turchina and Chu-Chu Igbokwe
#Service provided - ObjLocation service - contains x,y,z coordinates of object in baxter's stationary body frame, whether it is ok to grasp and if objects were found in the current frame.

import rospy
import numpy as np
import cv2
import cv_bridge
import baxter_interface
import math
import yaml

from std_msgs.msg import String,Float64MultiArray
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge, CvBridgeError
from jp_baxtertry1.srv import *
def yaml_loader(filepath):
	"""Loads a yaml file"""
	with open(filepath, "r") as file_descriptor:
		data =yaml.load(file_descriptor)
	return data

def yaml_dump(filepath, data):
	"""Dumps data to a yaml file"""
	with open(filepath, "w") as file_descriptor:
		yaml.dump(data, file_descriptor)
def main():
    #Initiate left hand camera object detection node
    rospy.init_node('Game_Order')
    filepath = "/home/z420/ros_ws/src/jp_baxtertry1/scripts/test.yaml"
    data = yaml_loader(filepath)
    values = data.values()
    keys= data.keys()
    # cont_color 0=vacio 1=verde 2=rojo
    cont_color = [0,0,0]
    cont_color2 = [0,0,0]
    aux = 0
    posact = [0,0]
    #rospy.sleep(10)
    InfoCoor_service = rospy.ServiceProxy("InfoCoor_service", InfoCoor)
    rospy.wait_for_service('InfoCoor_service')
    response = InfoCoor_service.call(InfoCoorRequest())
    #print response
    camara=      [[0,0,2,0,0,0,1,0,0],
		 [0,0,0,2,0,0,0,0,0],
		 [0,1,0,2,1,0,0,2,0],
		 [0,0,0,0,0,1,0,0,0]]
    camara2=[response.matriz_5,response.matriz_6,response.matriz_7,response.matriz_8]
    n=9
    m=4
    for i in xrange(m):
    	for j in xrange(n):
		camara[i][j]=camara2[i][j]
    print camara
    for i in xrange(m):
    	for j in xrange(n):
        	if data['inicial1'][i][j] == 0:
			cont_color[0] = cont_color[0] + 1
		elif data['inicial1'][i][j] == 1:
			cont_color[1] = cont_color[1] + 1
		elif data['inicial1'][i][j] == 2:
			cont_color[2] = cont_color[2] + 1
		else:
			print("color no valido")

    for i in xrange(m):
    	for j in xrange(n):
        	if camara[i][j] == 0:
			cont_color2[0] = cont_color2[0] + 1
		elif camara[i][j] == 1:
			cont_color2[1] = cont_color2[1] + 1
		elif camara[i][j] == 2:
			cont_color2[2] = cont_color2[2] + 1
		else:
			print("color no valido")
    print cont_color
    print cont_color2
    if cont_color == cont_color2:
	  	for i in xrange(m):
	    		for j in xrange(n):
				print "camara antes de movimiento"
				print camara
				if data['inicial1'][i][j] == camara[i][j]: # este elif se agranda si hay mas colores!!!!
					print "nada"					
					pass
				elif data['inicial1'][i][j] == 0:  #necesito quitar la ficha
					print "quitar"					
					posact[0]=i
					posact[1]=j
					for k in xrange(m):
	    					for l in xrange(n):
							if k <= posact[0] and l <= posact[1]: # no muevo lo que ya esta organizado
								pass
							elif camara[k][l] == 0: # si encuentre un espacio vacio, traigo la otra ficha
								print ("1mover ficha de [i][j] a [k][l]")
								
								aux = camara[i][j]
								camara[i][j]=camara[k][l]
								camara[k][l]=aux
								break
							else:
								pass
						if camara[i][j] == 0:
							break

				elif data['inicial1'][i][j] == 1: #necesito color 1(verde)
					print "traer verde"					
					if camara[i][j] ==0: # y esta vacio (se agrega elif si hay mas colores!!!!!)
						posact[0]=i
						posact[1]=j					
						for k in xrange(m):
		    					for l in xrange(n):
								if k <= posact[0] and l <= posact[1]: # no muevo lo que ya esta organizado
									pass
								elif camara[k][l] == 1: # si encuentre un cubo de color 1(verde), lo llev a donde necesito
									print ("1mover ficha de [k][l] a [i][j]")
									aux = camara[i][j]
									camara[i][j]=camara[k][l]
									camara[k][l]=aux
									break
								else:
									pass
							if camara[i][j] == 1:
								break
					else: # sino esta vacio necesito quitar la ficho y poner la correcta
						posact[0]=i
						posact[1]=j					
						for k in xrange(m):# quito la ficha
		    					for l in xrange(n):
								if k <= posact[0] and l <= posact[1]: # no muevo lo que ya esta organizado
									pass
								elif camara[k][l] == 0: # si encuentre un espacio vacio, traigo la otra ficha
									print ("2mover ficha de [i][j] a [k][l]")
									aux = camara[i][j]
									camara[i][j]=camara[k][l]
									camara[k][l]=aux
									break
								else:
									pass
							#print camara[i][j]
							if camara[i][j] == 0:
								break
						for k in xrange(m):# traigo la correcta
		    					for l in xrange(n):
								if k <= posact[0] and l <= posact[1]: # no muevo lo que ya esta organizado
									pass
								elif camara[k][l] == 1: # si encuentre un cubo de color 1(verde), lo llev a donde necesito
									print ("2mover ficha de [k][l] a [i][j]")
									aux = camara[i][j]
									camara[i][j]=camara[k][l]
									camara[k][l]=aux
									break
								else:
									pass
							if camara[i][j] == 1:
								break
				else: #necesito color 2(roja)  
					print "traer rojo"					
					if camara[i][j] ==0: # y esta vacio (se agrega elif si hay mas colores!!!!!)
						posact[0]=i
						posact[1]=j					
						for k in xrange(m):
		    					for l in xrange(n):
								if k <= posact[0] and l <= posact[1]: # no muevo lo que ya esta organizado
									pass
								elif camara[k][l] == 2: # si encuentre un cubo de color 1(verde), lo llev a donde necesito
									print ("3mover ficha de [k][l] a [i][j]")
									aux = camara[i][j]
									camara[i][j]=camara[k][l]
									camara[k][l]=aux
									break
								else:
									pass
							if camara[i][j] == 2:
								break

					else: # si no esta vacio debo quitar la que esta 
						posact[0]=i
						posact[1]=j					
						for k in xrange(m): # quito la ficha incorrecta
		    					for l in xrange(n):
								if k <= posact[0] and l <= posact[1]: # no muevo lo que ya esta organizado
									pass
								elif camara[k][l] == 2: # si encuentre un espacio vacio, traigo la otra ficha
									print ("3mover ficha de [i][j] a [k][l]")
									aux = camara[i][j]
									camara[i][j]=camara[k][l]
									camara[k][l]=aux
									break
								else:
									pass
						for k in xrange(m): # pongo la ficho correcto 
		    					for l in xrange(n):
								if k <= posact[0] and l <= posact[1]: # no muevo lo que ya esta organizado
									pass
								elif camara[k][l] == 2: # si encuentre un cubo de color 1(verde), lo llev a donde necesito
									print ("4mover ficha de [k][l] a [i][j]")
									aux = camara[i][j]
									camara[i][j]=camara[k][l]
									camara[k][l]=aux
									break
								else:
									pass
				print " final pos"

    if (cont_color[2] < cont_color2[2]) or (cont_color[1] < cont_color2[1]) or (cont_color[2] > cont_color2[2]) or (cont_color[1] > cont_color2[1]):
		if (cont_color[1] < cont_color2[1]):
			print("hay "+str(cont_color2[1]-cont_color[1])+" verdes de mas")
		if (cont_color[2] < cont_color2[2]):
			print("hay "+str(cont_color2[2]-cont_color[2])+" rojos de mas")
		if (cont_color[1] > cont_color2[1]):
			print("hay "+str(cont_color[1]-cont_color2[1])+" verdes de menos")
		if (cont_color[2] > cont_color2[2]):
			print("hay "+str(cont_color[2]-cont_color2[2])+" rojos de menos")
		if (cont_color[1] == cont_color2[1]):
			print("esta la cantidad suficiente de cubos verdes")
		if (cont_color[2] == cont_color2[2]):
			print("esta la cantidad suficiente de cubos rojos")

	
    rospy.spin()
    


if __name__ == '__main__':
     main()
