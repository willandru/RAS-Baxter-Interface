#!/usr/bin/env python

import sys
import yaml
import operator
import rospy
sys.path.append('/home/z420/ros_ws/src/jp_baxtertry1/scripts')
import tablero
import Baxtermovimiento
from jp_baxtertry1.srv import *

def main(dificultad,tipojuego):
	Baxtermovimiento.initialpose()
	filepath = "/home/z420/ros_ws/src/jp_baxtertry1/scripts/Escalera.yaml"
	#dificultad=5 #3 y 4 dos cubos 5 y 6 tres cubos 7 y 8 cuatro cubos
	#data es un diccionario
	data = tablero.yaml_loader(filepath)
	data_list = sorted(data.items(), key=operator.itemgetter(0))
	data_list2 = sorted(data[data_list[dificultad][0]].items(), key=operator.itemgetter(0))
	# cont_color 0=vacio 1=verde 2=rojo
	cont_color = [0,0,0,0,0]
	cont_color2 = [0,0,0,0,0]
	print "pos_inicial"	
	print data[data_list[dificultad][0]][data_list2[0][0]]
	camara= [[0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,1,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0],
		 [0,0,2,2,0,1,0,0,1],]
        InfoCoor_service = rospy.ServiceProxy("InfoCoor_service", InfoCoor)
        rospy.wait_for_service('InfoCoor_service')
        response = InfoCoor_service.call(InfoCoorRequest())
        camara2=[response.matriz_5,response.matriz_6,response.matriz_7,response.matriz_8]
	n = 9 # Numero de filas
	m = 4 # Numero de columnas
        for i in xrange(m):
    	    for j in xrange(n):
		    camara[i][j]=camara2[i][j]
	print "camara"
	print camara
	cont=tablero.tablero(m,n,data,data_list,data_list2,cont_color,cont_color2,dificultad,camara)
	cont_color=cont[0]
	cont_color2=cont[1]
	while cont_color != cont_color2:
		cont_color = [0,0,0,0,0]
		cont_color2 = [0,0,0,0,0]
		InfoCoor_service = rospy.ServiceProxy("InfoCoor_service", InfoCoor)
		rospy.wait_for_service('InfoCoor_service')
		response = InfoCoor_service.call(InfoCoorRequest())
		camara2=[response.matriz_5,response.matriz_6,response.matriz_7,response.matriz_8]
		n = 9 # Numero de filas
		m = 4 # Numero de columnas
		for i in xrange(m):
	    	    for j in xrange(n):
			    camara[i][j]=camara2[i][j]
		print "camara"
		print camara
		cont=tablero.tablero(m,n,data,data_list,data_list2,cont_color,cont_color2,dificultad,camara)		
    	if cont_color == cont_color2:
		for i in xrange(m):
	    		for j in xrange(n):
				#print "camara antes de movimiento"
				#print camara
				if data[data_list[dificultad][0]][data_list2[0][0]][i][j] == camara[i][j]: # este elif se agranda si hay mas colores!!!!
					#print "nada"					
					pass
				elif data[data_list[dificultad][0]][data_list2[0][0]][i][j] == 0:  #necesito quitar la ficha
					#print "quitar"					
					tablero.quitar_ficha(0,i,j,m,n,camara,data,data_list,data_list2,camara[i][j],dificultad)

				elif data[data_list[dificultad][0]][data_list2[0][0]][i][j] == 1: #necesito color 1(verde)
					#print "traer verde"
					bandera_mov=0					
					if camara[i][j] ==0: # y esta vacio (se agrega elif si hay mas colores!!!!!)
						tablero.traer_ficha(0,i,j,m,n,camara,data,data_list,data_list2,data[data_list[dificultad][0]][data_list2[0][0]][i][j],dificultad)
					else: # sino esta vacio necesito quitar la ficho y poner la correcta
						tablero.quitar_ficha(0,i,j,m,n,camara,data,data_list,data_list2,camara[i][j],dificultad)				
						tablero.traer_ficha(0,i,j,m,n,camara,data,data_list,data_list2,data[data_list[dificultad][0]][data_list2[0][0]][i][j],dificultad)
				elif data[data_list[dificultad][0]][data_list2[0][0]][i][j] == 2: #necesito color 2(roja)  
					#print "traer rojo"
					bandera_mov=0					
					if camara[i][j] ==0: # y esta vacio (se agrega elif si hay mas colores!!!!!)
						tablero.traer_ficha(0,i,j,m,n,camara,data,data_list,data_list2,data[data_list[dificultad][0]][data_list2[0][0]][i][j],dificultad)
					else: # si no esta vacio debo quitar la que esta 
						tablero.quitar_ficha(0,i,j,m,n,camara,data,data_list,data_list2,camara[i][j],dificultad)				
						tablero.traer_ficha(0,i,j,m,n,camara,data,data_list,data_list2,data[data_list[dificultad][0]][data_list2[0][0]][i][j],dificultad)
				elif data[data_list[dificultad][0]][data_list2[0][0]][i][j] == 3: #necesito color 3(amarillo)  
					#print "traer amarillo"
					bandera_mov=0					
					if camara[i][j] ==0: # y esta vacio (se agrega elif si hay mas colores!!!!!)
						tablero.traer_ficha(0,i,j,m,n,camara,data,data_list,data_list2,data[data_list[dificultad][0]][data_list2[0][0]][i][j],dificultad)
					else: # si no esta vacio debo quitar la que esta 
						tablero.quitar_ficha(0,i,j,m,n,camara,data,data_list,data_list2,camara[i][j],dificultad)				
						tablero.traer_ficha(0,i,j,m,n,camara,data,data_list,data_list2,data[data_list[dificultad][0]][data_list2[0][0]][i][j],dificultad)
				elif data[data_list[dificultad][0]][data_list2[0][0]][i][j] == 4: #necesito color 4(azul)  
					#print "traer azul"
					bandera_mov=0					
					if camara[i][j] ==0: # y esta vacio (se agrega elif si hay mas colores!!!!!)
						tablero.traer_ficha(0,i,j,m,n,camara,data,data_list,data_list2,data[data_list[dificultad][0]][data_list2[0][0]][i][j],dificultad)
					else: # si no esta vacio debo quitar la que esta 
						tablero.quitar_ficha(0,i,j,m,n,camara,data,data_list,data_list2,camara[i][j],dificultad)				
						tablero.traer_ficha(0,i,j,m,n,camara,data,data_list,data_list2,data[data_list[dificultad][0]][data_list2[0][0]][i][j],dificultad)
				
	
	print camara
	Baxtermovimiento.initialpose()

