#!/usr/bin/env python

import sys
import yaml
import operator
import rospy
sys.path.append('/home/z420/ros_ws/src/jp_baxtertry1/scripts')
import Baxtermovimiento2
def yaml_loader(filepath):
	"""Loads a yaml file"""
	with open(filepath, "r") as stream:
		data =yaml.load(stream)
	return data

def traer_ficha(t,i,j,m,n,camara,data,data_list,data_list2,color,dificultad):
	aux = 0
	bandera_mov=0	
	for k in xrange(m):
		for l in xrange(n):
			if camara[k][l] == data[data_list[dificultad][0]][data_list2[t][0]][k][l]:
				pass
			elif camara[k][l] == color: # si encuentre un cubo del color que se quiere, lo lleva donde necesito
				print ("traer ficha de [k][l] a [i][j]")
				aux = camara[i][j]
				puntoa=(k,l)
				puntob=(i,j)
				Baxtermovimiento2.moverbaxter(puntoa,puntob,1,camara)
				Baxtermovimiento2.finalpose(1)
				camara[i][j]=camara[k][l]
				camara[k][l]=aux
				break
			else:
				pass
		if camara[i][j] == color:
			break

def quitar_ficha(t,i,j,m,n,camara,data,data_list,data_list2,color,dificultad):
	aux = 0
	bandera_mov=0
	for k in xrange(m): # busco si esta ficha se necesita en algun otro lado
		for l in xrange(n):
			if k <= i and l <= j: # no muevo lo que ya esta organizado
				pass
			elif camara[k][l] == 0 and data[data_list[dificultad][0]][data_list2[t][0]][k][l]==color: # si encuentre un espacio vacio y que la necesite,traigo la otra ficha
				print ("quitar ficha de [i][j] a [k][l]")
				aux = camara[i][j]
				puntoa=(i,j)
				puntob=(k,l)
				Baxtermovimiento2.moverbaxter(puntoa,puntob,1,camara)
				Baxtermovimiento2.finalpose(1)
				camara[i][j]=camara[k][l]
				camara[k][l]=aux
				bandera_mov=1;
				break
			else:
				pass
		if camara[i][j] == 0:
			break
	if bandera_mov==0:
		for k in xrange(m): # si no se necesita en otro lado la pongo en un sitio vacio
			for l in xrange(n):
				if k <= i and l <= j: # no muevo lo que ya esta organizado
					pass
				elif camara[k][l] == 0: # si encuentre un espacio vacio, traigo la otra ficha
					print ("5mover ficha de [i][j] a [k][l]")
					print i,j,k,l
					aux = camara[i][j]
					puntoa=(i,j)
					puntob=(k,l)
					Baxtermovimiento2.moverbaxter(puntoa,puntob,1,camara)
					Baxtermovimiento2.finalpose(1)
					camara[i][j]=camara[k][l]
					camara[k][l]=aux
					break
				else:
					pass
			if camara[i][j] == 0:
				break


def traer_ficha2(i,j,m,n,camara,data,color,dificultad):
	aux = 0
	bandera_mov=0	
	for k in xrange(m):
		for l in xrange(n):
			if camara[k][l] == data[k][l]:
				pass
			elif camara[k][l] == color: # si encuentre un cubo del color que se quiere, lo lleva donde necesito
				print ("traer ficha de [k][l] a [i][j]")
				aux = camara[i][j]
				puntoa=(k,l)
				puntob=(i,j)
				Baxtermovimiento2.moverbaxter(puntoa,puntob,1,camara)
				Baxtermovimiento2.finalpose(1)
				camara[i][j]=camara[k][l]
				camara[k][l]=aux
				break
			else:
				pass
		if camara[i][j] == color:
			break

def quitar_ficha2(i,j,m,n,camara,data,color,dificultad):
	aux = 0
	bandera_mov=0
	for k in xrange(m): # busco si esta ficha se necesita en algun otro lado
		for l in xrange(n):
			if k <= i and l <= j: # no muevo lo que ya esta organizado
				pass
			elif camara[k][l] == 0 and data[k][l]==color: # si encuentre un espacio vacio y que la necesite,traigo la otra ficha
				print ("quitar ficha de [i][j] a [k][l]")
				aux = camara[i][j]
				puntoa=(i,j)
				puntob=(k,l)
				Baxtermovimiento2.moverbaxter(puntoa,puntob,1,camara)
				Baxtermovimiento2.finalpose(1)
				camara[i][j]=camara[k][l]
				camara[k][l]=aux
				bandera_mov=1;
				break
			else:
				pass
		if camara[i][j] == 0:
			break
	if bandera_mov==0:
		for k in xrange(m): # si no se necesita en otro lado la pongo en un sitio vacio
			for l in xrange(n):
				if k <= i and l <= j: # no muevo lo que ya esta organizado
					pass
				elif camara[k][l] == 0: # si encuentre un espacio vacio, traigo la otra ficha
					print ("mover ficha de [i][j] a [k][l]")
					aux = camara[i][j]
					puntoa=(i,j)
					puntob=(k,l)
					Baxtermovimiento2.moverbaxter(puntoa,puntob,1,camara)
					Baxtermovimiento2.finalpose(1)
					camara[i][j]=camara[k][l]
					camara[k][l]=aux
					break
				else:
					pass
			if camara[i][j] == 0:
				break



def tablero2(m,n,data,cont_color,cont_color2,dificultad,camara):
	for i in xrange(m):
    		for j in xrange(n):
        		if data[i][j] == 0:
				cont_color[0] = cont_color[0] + 1
			elif data[i][j] == 1:
				cont_color[1] = cont_color[1] + 1
			elif data[i][j] == 2:
				cont_color[2] = cont_color[2] + 1
			elif data[i][j] == 3:
				cont_color[3] = cont_color[3] + 1
			elif data[i][j] == 4:
				cont_color[4] = cont_color[4] + 1
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
			elif camara[i][j] == 3:
				cont_color2[3] = cont_color2[3] + 1
			elif camara[i][j] == 4:
				cont_color2[4] = cont_color2[4] + 1
			else:
				print("color no valido")
	cont=[cont_color,cont_color2]
	return cont 
def tablero(m,n,data,data_list,data_list2,cont_color,cont_color2,dificultad,camara):
	for i in xrange(m):
    		for j in xrange(n):
        		if data[data_list[dificultad][0]][data_list2[0][0]][i][j] == 0:
				cont_color[0] = cont_color[0] + 1
			elif data[data_list[dificultad][0]][data_list2[0][0]][i][j] == 1:
				cont_color[1] = cont_color[1] + 1
			elif data[data_list[dificultad][0]][data_list2[0][0]][i][j] == 2:
				cont_color[2] = cont_color[2] + 1
			elif data[data_list[dificultad][0]][data_list2[0][0]][i][j] == 3:
				cont_color[3] = cont_color[3] + 1
			elif data[data_list[dificultad][0]][data_list2[0][0]][i][j] == 4:
				cont_color[4] = cont_color[4] + 1
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
			elif camara[i][j] == 3:
				cont_color2[3] = cont_color2[3] + 1
			elif camara[i][j] == 4:
				cont_color2[4] = cont_color2[4] + 1
			else:
				print("color no valido")
	cont=[cont_color,cont_color2]
	return cont 
