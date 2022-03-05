import pygame

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
			matrizexhortador[i][j]="Exhortador/Exhortador4.wav"
			matriz[i][j]="Exhortador/Exhortador4.wav"
		elif i<32 and j<32:
			matrizexhortador[i][j]="Exhortador/Exhortador3.wav"
			matriz[i][j]="Exhortador/Exhortador3.wav"
		elif i<49 and j<49:
			matrizexhortador[i][j]="Exhortador/Exhortador2.wav"
			matriz[i][j]="Exhortador/Exhortador2.wav"
		elif i<67 and j<67:
			matrizexhortador[i][j]="Exhortador/Exhortador1.wav"
			matriz[i][j]="Exhortador/Exhortador1.wav"
for i in range(len(matrizextricto)):
	for j in range(len(matrizextricto[1])):
		if i<16:
			matrizextricto[i][j]="Extricto/Extricto4.wav"
			matriz[i][j+67]="Extricto/Extricto4.wav"
		elif i<32:
			matrizextricto[i][j]="Extricto/Extricto3.wav"
			matriz[i][j+67]="Extricto/Extricto3.wav"
		elif i<49:
			matrizextricto[i][j]="Extricto/Extricto2.wav"
			matriz[i][j+67]="Extricto/Extricto2.wav"
		elif i<67:
			matrizextricto[i][j]="Extricto/Extricto1.wav"
			matriz[i][j+67]="Extricto/Extricto1.wav"
for i in range(len(matrizorientador)):
	for j in range(len(matrizorientador[1])):
		if j>49 and i<16:
			matrizorientador[i][j]="Orientador/Orientador4.wav"
			matriz[i][j+134]="Orientador/Orientador4.wav"
		elif j>32 and i<32:
			matrizorientador[i][j]="Orientador/Orientador3.wav"
			matriz[i][j+134]="Orientador/Orientador3.wav"
		elif j>16 and i<49:
			matrizorientador[i][j]="Orientador/Orientador2.wav"
			matriz[i][j+134]="Orientador/Orientador2.wav"
		elif j>=0 and i<67:
			matrizorientador[i][j]="Orientador/Orientador1.wav"
			matriz[i][j+134]="Orientador/Orientador1.wav"



for i in range(len(matrizinsatisfecho)):
	for j in range(len(matrizinsatisfecho[1])):
		if j<16:
			matrizinsatisfecho[i][j]="Insatisfecho/Insatisfecho4.wav"
			matriz[i+67][j]="Insatisfecho/Insatisfecho4.wav"
		elif j<32:
			matrizinsatisfecho[i][j]="Insatisfecho/Insatisfecho3.wav"
			matriz[i+67][j]="Insatisfecho/Insatisfecho3.wav"
		elif j<49:
			matrizinsatisfecho[i][j]="Insatisfecho/Insatisfecho2.wav"
			matriz[i+67][j]="Insatisfecho/Insatisfecho2.wav"
		elif j<66:
			matrizinsatisfecho[i][j]="Insatisfecho/Insatisfecho1.wav"
			matriz[i+67][j]="Insatisfecho/Insatisfecho1.wav"
for i in range(len(matrizneutro)):
	for j in range(len(matrizneutro[1])):
		if j<33:
			matrizneutro[i][j]="Neutro/Neutro1.wav"
			matriz[i+67][j+67]="Neutro/Neutro1.wav"
		elif j<67:
			matrizneutro[i][j]="Neutro/Neutro2.wav"
			matriz[i+67][j+67]="Neutro/Neutro2.wav"
for i in range(len(matrizcomplacido)):
	for j in range(len(matrizcomplacido[1])):
		if j<16:
			matrizcomplacido[i][j]="Complacido/Complacido1.wav"
			matriz[i+67][j+134]="Complacido/Complacido1.wav"
		elif j<32:
			matrizcomplacido[i][j]="Complacido/Complacido2.wav"
			matriz[i+67][j+134]="Complacido/Complacido2.wav"
		elif j<49:
			matrizcomplacido[i][j]="Complacido/Complacido3.wav"
			matriz[i+67][j+134]="Complacido/Complacido3.wav"
		elif j<66:
			matrizcomplacido[i][j]="Complacido/Complacido4.wav"
			matriz[i+67][j+134]="Complacido/Complacido4.wav"



for i in range(len(matrizdudoso)):
	for j in range(len(matrizdudoso[1])):
		if j<16 and i>49:
			matrizdudoso[i][j]="Dudoso/Dudoso4.wav"
			matriz[i+134][j]="Dudoso/Dudoso4.wav"
		elif j<32 and i>32:
			matrizdudoso[i][j]="Dudoso/Dudoso3.wav"
			matriz[i+134][j]="Dudoso/Dudoso3.wav"
		elif j<49 and i>16:
			matrizdudoso[i][j]="Dudoso/Dudoso2.wav"
			matriz[i+134][j]="Dudoso/Dudoso2.wav"
		elif j<67 and i>=0:
			matrizdudoso[i][j]="Dudoso/Dudoso1.wav"
			matriz[i+134][j]="Dudoso/Dudoso1.wav"
for i in range(len(matrizinteresado)):
	for j in range(len(matrizinteresado[1])):
		if i<16:
			matrizinteresado[i][j]="Interesado/Interesado1.wav"
			matriz[i+134][j+67]="Interesado/Interesado1.wav"
		elif i<32:
			matrizinteresado[i][j]="Interesado/Interesado2.wav"
			matriz[i+134][j+67]="Interesado/Interesado2.wav"
		elif i<49:
			matrizinteresado[i][j]="Interesado/Interesado3.wav"
			matriz[i+134][j+67]="Interesado/Interesado3.wav"
		elif i<66:
			matrizinteresado[i][j]="Interesado/Interesado4.wav"
			matriz[i+134][j+67]="Interesado/Interesado4.wav"
for i in range(len(matrizalentador)):
	for j in range(len(matrizalentador[1])):
		if j>49 and i>49:
			matrizalentador[i][j]="Alentador/Alentador4.wav"
			matriz[i+134][j+134]="Alentador/Alentador4.wav"
		elif j>32 and i>32:
			matrizalentador[i][j]="Alentador/Alentador3.wav"
			matriz[i+134][j+134]="Alentador/Alentador3.wav"
		elif j>16 and i>16:
			matrizalentador[i][j]="Alentador/Alentador2.wav"
			matriz[i+134][j+134]="Alentador/Alentador2.wav"
		elif j>=0 and i>=0:
			matrizalentador[i][j]="Alentador/Alentador1.wav"
			matriz[i+134][j+134]="Alentador/Alentador1.wav"

pygame.init()
print(matriz[0][100])
pygame.mixer.music.load(matriz[0][100])
pygame.mixer.music.play()
pygame.event.wait()


