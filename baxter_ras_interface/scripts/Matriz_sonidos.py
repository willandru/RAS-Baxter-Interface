#!/usr/bin/env python
import pygame
import rospy
def sonido(x,y):
	matriz = [range(200) for i in range(200)]
	matrizexhortador = [range(67) for i in range(67)]
	matrizextricto = [range(67) for i in range(67)]
	matrizorientador = [range(66) for i in range(67)]
	matrizinsatisfecho = [range(67) for i in range(67)]
	matrizneutro = [range(67) for i in range(67)]
	matrizcomplacido = [range(66) for i in range(67)]
	matrizdudoso = [range(67) for i in range(66)]
	matrizinteresado = [range(67) for i in range(66)]
	matrizalentador = [range(66) for i in range(66)]
	for i in range(len(matrizexhortador)):
		for j in range(len(matrizexhortador[1])):
			if i<16 and j<16:
				matrizexhortador[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Exhortador/Exhortador4.wav"
				matriz[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Exhortador/Exhortador4.wav"
			elif i<32 and j<32:
				matrizexhortador[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Exhortador/Exhortador3.wav"
				matriz[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Exhortador/Exhortador3.wav"
			elif i<49 and j<49:
				matrizexhortador[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Exhortador/Exhortador2.wav"
				matriz[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Exhortador/Exhortador2.wav"
			elif i<67 and j<67:
				matrizexhortador[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Exhortador/Exhortador1.wav"
				matriz[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Exhortador/Exhortador1.wav"
	for i in range(len(matrizextricto)):
		for j in range(len(matrizextricto[1])):
			if i<16:
				matrizextricto[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Extricto/Extricto4.wav"
				matriz[i][j+67]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Extricto/Extricto4.wav"
			elif i<32:
				matrizextricto[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Extricto/Extricto3.wav"
				matriz[i][j+67]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Extricto/Extricto3.wav"
			elif i<49:
				matrizextricto[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Extricto/Extricto2.wav"
				matriz[i][j+67]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Extricto/Extricto2.wav"
			elif i<67:
				matrizextricto[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Extricto/Extricto1.wav"
				matriz[i][j+67]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Extricto/Extricto1.wav"
	for i in range(len(matrizorientador)):
		for j in range(len(matrizorientador[1])):
			if j>49 and i<16:
				matrizorientador[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Orientador/Orientador4.wav"
				matriz[i][j+134]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Orientador/Orientador4.wav"
			elif j>32 and i<32:
				matrizorientador[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Orientador/Orientador3.wav"
				matriz[i][j+134]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Orientador/Orientador3.wav"
			elif j>16 and i<49:
				matrizorientador[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Orientador/Orientador2.wav"
				matriz[i][j+134]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Orientador/Orientador2.wav"
			elif j>=0 and i<67:
				matrizorientador[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Orientador/Orientador1.wav"
				matriz[i][j+134]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Orientador/Orientador1.wav"



	for i in range(len(matrizinsatisfecho)):
		for j in range(len(matrizinsatisfecho[1])):
			if j<16:
				matrizinsatisfecho[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Insatisfecho/Insatisfecho4.wav"
				matriz[i+67][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Insatisfecho/Insatisfecho4.wav"
			elif j<32:
				matrizinsatisfecho[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Insatisfecho/Insatisfecho3.wav"
				matriz[i+67][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Insatisfecho/Insatisfecho3.wav"
			elif j<49:
				matrizinsatisfecho[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Insatisfecho/Insatisfecho2.wav"
				matriz[i+67][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Insatisfecho/Insatisfecho2.wav"
			elif j<66:
				matrizinsatisfecho[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Insatisfecho/Insatisfecho1.wav"
				matriz[i+67][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Insatisfecho/Insatisfecho1.wav"
	for i in range(len(matrizneutro)):
		for j in range(len(matrizneutro[1])):
			if j<33:
				matrizneutro[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Neutro/Neutro1.wav"
				matriz[i+67][j+67]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Neutro/Neutro1.wav"
			elif j<67:
				matrizneutro[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Neutro/Neutro2.wav"
				matriz[i+67][j+67]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Neutro/Neutro2.wav"
	for i in range(len(matrizcomplacido)):
		for j in range(len(matrizcomplacido[1])):
			if j<16:
				matrizcomplacido[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Complacido/Complacido1.wav"
				matriz[i+67][j+134]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Complacido/Complacido1.wav"
			elif j<32:
				matrizcomplacido[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Complacido/Complacido2.wav"
				matriz[i+67][j+134]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Complacido/Complacido2.wav"
			elif j<49:
				matrizcomplacido[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Complacido/Complacido3.wav"
				matriz[i+67][j+134]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Complacido/Complacido3.wav"
			elif j<66:
				matrizcomplacido[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Complacido/Complacido4.wav"
				matriz[i+67][j+134]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Complacido/Complacido4.wav"



	for i in range(len(matrizdudoso)):
		for j in range(len(matrizdudoso[1])):
			if j<16 and i>49:
				matrizdudoso[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Dudoso/Dudoso4.wav"
				matriz[i+134][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Dudoso/Dudoso4.wav"
			elif j<32 and i>32:
				matrizdudoso[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Dudoso/Dudoso3.wav"
				matriz[i+134][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Dudoso/Dudoso3.wav"
			elif j<49 and i>16:
				matrizdudoso[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Dudoso/Dudoso2.wav"
				matriz[i+134][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Dudoso/Dudoso2.wav"
			elif j<67 and i>=0:
				matrizdudoso[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Dudoso/Dudoso1.wav"
				matriz[i+134][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Dudoso/Dudoso1.wav"
	for i in range(len(matrizinteresado)):
		for j in range(len(matrizinteresado[1])):
			if i<16:
				matrizinteresado[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Interesado/Interesado1.wav"
				matriz[i+134][j+67]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Interesado/Interesado1.wav"
			elif i<32:
				matrizinteresado[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Interesado/Interesado2.wav"
				matriz[i+134][j+67]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Interesado/Interesado2.wav"
			elif i<49:
				matrizinteresado[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Interesado/Interesado3.wav"
				matriz[i+134][j+67]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Interesado/Interesado3.wav"
			elif i<66:
				matrizinteresado[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Interesado/Interesado4.wav"
				matriz[i+134][j+67]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Interesado/Interesado4.wav"
	for i in range(len(matrizalentador)):
		for j in range(len(matrizalentador[1])):
			if j>49 and i>49:
				matrizalentador[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Alentador/Alentador4.wav"
				matriz[i+134][j+134]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Alentador/Alentador4.wav"
			elif j>32 and i>32:
				matrizalentador[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Alentador/Alentador3.wav"
				matriz[i+134][j+134]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Alentador/Alentador3.wav"
			elif j>16 and i>16:
				matrizalentador[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Alentador/Alentador2.wav"
				matriz[i+134][j+134]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Alentador/Alentador2.wav"
			elif j>=0 and i>=0:
				matrizalentador[i][j]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Alentador/Alentador1.wav"
				matriz[i+134][j+134]="/home/z420/ros_ws/src/jp_baxtertry1/share/Sounds/Alentador/Alentador1.wav"
	x=int(x/2)
	y=int(y/2)
	print(matriz[y][x])	
	return matriz,y,x
