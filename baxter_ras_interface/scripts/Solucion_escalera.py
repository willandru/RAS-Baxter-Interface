import yaml
import operator

def yaml_loader(filepath):
	"""Loads a yaml file"""
	with open(filepath, "r") as stream:
		data =yaml.load(stream)
	return data

def yaml_dump(filepath, data):
	"""Dumps data to a yaml file"""
	with open(filepath, "w") as file_descriptor:
		yaml.dump(data, file_descriptor)

def traer_ficha(t,i,j,m,n,camara,data,color):
	aux = 0
	bandera_mov=0	
	for k in xrange(m):
		for l in xrange(n):
			if camara[k][l] == data[data_list[t][0]][k][l]:
				pass
			elif camara[k][l] == color: # si encuentre un cubo del color que se quiere, lo lleva donde necesito
				print ("traer ficha de [k][l] a [i][j]")
				aux = camara[i][j]
				camara[i][j]=camara[k][l]
				camara[k][l]=aux
				break
			else:
				pass
		if camara[i][j] == color:
			break

def quitar_ficha(t,i,j,m,n,camara,data,color):
	aux = 0
	bandera_mov=0
	for k in xrange(m): # busco si esta ficha se necesita en algun otro lado
		for l in xrange(n):
			if k <= i and l <= j: # no muevo lo que ya esta organizado
				pass
			elif camara[k][l] == 0 and data[data_list[t][0]][k][l]==color: # si encuentre un espacio vacio y que la necesite,traigo la otra ficha
				print ("quitar ficha de [i][j] a [k][l]")
				aux = camara[i][j]
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
					camara[i][j]=camara[k][l]
					camara[k][l]=aux
					break
				else:
					pass
			if camara[i][j] == 0:
				break

if __name__ == "__main__":
	filepath = "solucion_escalera.yaml"
	#data es un diccionario
	data = yaml_loader(filepath)
	data_list = sorted(data.items(), key=operator.itemgetter(0))
	# cont_color 0=vacio 1=verde 2=rojo
	cont_color = [0,0,0,0,0]
	cont_color2 = [0,0,0,0,0]
	print "inicial1"	
	print data[data_list[0][0]]
	camara= [[0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0],
		 [2,2,2,2,0,1,1,1,1],]
	print "camara"
	print camara
	
	n = 9 # Numero de filas
	m = 4 # Numero de columnas
	for i in xrange(m):
    		for j in xrange(n):
        		if data[data_list[0][0]][i][j] == 0:
				cont_color[0] = cont_color[0] + 1
			elif data[data_list[0][0]][i][j] == 1:
				cont_color[1] = cont_color[1] + 1
			elif data[data_list[0][0]][i][j] == 2:
				cont_color[2] = cont_color[2] + 1
			elif data[data_list[0][0]][i][j] == 3:
				cont_color[3] = cont_color[3] + 1
			elif data[data_list[0][0]][i][j] == 4:
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
    	if cont_color == cont_color2:
		for t in xrange(len(data_list)):
			for i in xrange(m):
		    		for j in xrange(n):
					#print "camara antes de movimiento"
					#print camara
					if data[data_list[t][0]][i][j] == camara[i][j]: # este elif se agranda si hay mas colores!!!!
						#print "nada"					
						pass
					elif data[data_list[t][0]][i][j] == 0:  #necesito quitar la ficha
						#print "quitar"					
						quitar_ficha(t,i,j,m,n,camara,data,camara[i][j])

					elif data[data_list[t][0]][i][j] == 1: #necesito color 1(verde)
						#print "traer verde"
						bandera_mov=0					
						if camara[i][j] ==0: # y esta vacio (se agrega elif si hay mas colores!!!!!)
							traer_ficha(t,i,j,m,n,camara,data,data[data_list[t][0]][i][j])
						else: # sino esta vacio necesito quitar la ficho y poner la correcta
							quitar_ficha(t,i,j,m,n,camara,data,camara[i][j])				
							traer_ficha(t,i,j,m,n,camara,data,data[data_list[t][0]][i][j])
					elif data[data_list[t][0]][i][j] == 2: #necesito color 2(roja)  
						#print "traer rojo"
						bandera_mov=0					
						if camara[i][j] ==0: # y esta vacio (se agrega elif si hay mas colores!!!!!)
							traer_ficha(t,i,j,m,n,camara,data,data[data_list[t][0]][i][j])
						else: # si no esta vacio debo quitar la que esta 
							quitar_ficha(t,i,j,m,n,camara,data,camara[i][j])				
							traer_ficha(t,i,j,m,n,camara,data,data[data_list[t][0]][i][j])
					elif data[data_list[t][0]][i][j] == 3: #necesito color 3(amarillo)  
						#print "traer amarillo"
						bandera_mov=0					
						if camara[i][j] ==0: # y esta vacio (se agrega elif si hay mas colores!!!!!)
							traer_ficha(t,i,j,m,n,camara,data,data[data_list[t][0]][i][j])
						else: # si no esta vacio debo quitar la que esta 
							quitar_ficha(t,i,j,m,n,camara,data,camara[i][j])				
							traer_ficha(t,i,j,m,n,camara,data,data[data_list[t][0]][i][j])
					elif data[data_list[t][0]][i][j] == 4: #necesito color 4(azul)  
						#print "traer azul"
						bandera_mov=0					
						if camara[i][j] ==0: # y esta vacio (se agrega elif si hay mas colores!!!!!)
							traer_ficha(t,i,j,m,n,camara,data,data[data_list[t][0]][i][j])
						else: # si no esta vacio debo quitar la que esta 
							quitar_ficha(t,i,j,m,n,camara,data,camara[i][j])				
							traer_ficha(t,i,j,m,n,camara,data,data[data_list[t][0]][i][j])
					#print camara
					#print " final pos"
			print camara
			print data_list[t][0]
			
	if cont_color[0] < cont_color2[0]:
		print("hay menos cubos en el trablero")		
		if cont_color[1] < cont_color2[1]:
			print("hay mas cubos verdes")				
		if cont_color[2] < cont_color2[2]:
			print("hay mas cubos rojos")
		if cont_color[1] > cont_color2[1]:
			print("hay menos cubos verdes")				
		if cont_color[2] > cont_color2[2]:
			print("hay menos cubos rojos")
		

	print camara

