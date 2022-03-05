#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String,Int32MultiArray
from geometry_msgs.msg import Twist
from jp_baxtertry1.srv import *
global fin
fin=0
def talker():
    while not rospy.is_shutdown():
	    global Acabe,fin
	    cara = rospy.Publisher('/emociones_baxter', Twist, queue_size=40)
	    mover = rospy.Publisher('/solucion_escalera', Int32MultiArray, queue_size=40)
	    rospy.init_node('Obra', anonymous=True)
	    auxiliar_service = rospy.ServiceProxy("auxiliar_service", auxiliar)	
	    rospy.wait_for_service('auxiliar_service')
	    response = auxiliar_service.call(auxiliarRequest())
	    rate = rospy.Rate(0.2) # 10hz
	    Emocion=Twist()
	    #Neutro1
	    Emocion.linear.x=185	
	    Emocion.linear.y=252	
	    Emocion.linear.z=0
	    cara.publish(Emocion)
	    rate.sleep()
	    #Neutro1
	    Emocion.linear.x=200	
	    Emocion.linear.y=180	
	    Emocion.linear.z=1
	    cara.publish(Emocion)
	    rate.sleep()	
	    datos=Int32MultiArray()
	    print "ACABE",response.acabe
	    if response.fin==2:
	    		fin=0
	    while response.acabe==0: 
			rospy.wait_for_service('auxiliar_service')
	    		response = auxiliar_service.call(auxiliarRequest())
			if fin==0:
				datos.data=[0,0,1,1,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
				rospy.loginfo(datos)
				mover.publish(datos)
				fin=1	
			if response.acabe!= 0:
				break
			#Interesado4
			Emocion.linear.x=398	
			Emocion.linear.y=200	
			Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()	
			#Interesado3
			Emocion.linear.x=360	
			Emocion.linear.y=200	
			Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()	
			#Interesado2
			Emocion.linear.x=320	
			Emocion.linear.y=200	
			Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()	
			#Interesado1
			Emocion.linear.x=280	
			Emocion.linear.y=200	
			Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()
	    if response.fin==2:
	    		fin=0	
	    antman=input("pendejos")	
	    while response.acabe==1:
			rospy.wait_for_service('auxiliar_service')
	    		response = auxiliar_service.call(auxiliarRequest())
			if fin==0:
			    	datos.data=[0,0,1,1,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]
			    	rospy.loginfo(datos)
			    	mover.publish(datos)
			    	fin=1
			if response.acabe!= 1:
				break	
			#Estricto4
		    	Emocion.linear.x=0	
		    	Emocion.linear.y=200	
		    	Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()	
		    	#Estricto3
		    	Emocion.linear.x=40	
		    	Emocion.linear.y=200	
		    	Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()	
		    	#Estricto2
		    	Emocion.linear.x=80	
		    	Emocion.linear.y=200	
		    	Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()	
		    	#Estricto1
		    	Emocion.linear.x=120	
		    	Emocion.linear.y=200	
		    	Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()
	    if response.fin==2:
	    		fin=0
	    antman=input("pendejos")
	    while response.acabe==2: 
			rospy.wait_for_service('auxiliar_service')
	    		response = auxiliar_service.call(auxiliarRequest())
			if fin==0:
				datos.data=[0,0,1,1,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
				rospy.loginfo(datos)
				mover.publish(datos)
				fin=1
			if response.acabe!= 2:
				break
		    	#Orientador4
		    	Emocion.linear.x=0	
		    	Emocion.linear.y=398	
		    	Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()	
		    	#Orientador3
		    	Emocion.linear.x=40	
		    	Emocion.linear.y=360	
		    	Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()	
		    	#Orientador2
		    	Emocion.linear.x=80	
		    	Emocion.linear.y=320	
		    	Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()	
		    	#Orientador1
		    	Emocion.linear.x=120	
		    	Emocion.linear.y=280	
		    	Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()	
	    if response.fin==2:
	    		fin=0	
	    antman=input("pendejos")	
	    while response.acabe==3:
			rospy.wait_for_service('auxiliar_service')
	    		response = auxiliar_service.call(auxiliarRequest())
			if fin==0:
			    	datos.data=[0,0,1,1,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]
			    	rospy.loginfo(datos)
			    	mover.publish(datos)
			    	fin=1	
			if response.acabe!= 3:
				break
		    	#Insatisfecho4
		    	Emocion.linear.x=200	
		    	Emocion.linear.y=0	
		    	Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()	
		    	#Insatisfecho3
		    	Emocion.linear.x=200	
		    	Emocion.linear.y=40	
		    	Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()	
		    	#Insatisfecho2
		    	Emocion.linear.x=200	
		    	Emocion.linear.y=80	
		    	Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()
		    	#Insatisfecho1
		    	Emocion.linear.x=200	
		    	Emocion.linear.y=120	
		   	Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()
	    if response.fin==2:
	    		fin=0
	    antman=input("pendejos")
	    while response.acabe==4: 
			rospy.wait_for_service('auxiliar_service')
	    		response = auxiliar_service.call(auxiliarRequest())
			if fin==0:
				datos.data=[0,0,1,1,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
				rospy.loginfo(datos)
				mover.publish(datos)
				fin=1
			if response.acabe!= 4:
				break		
		    	#Dudoso4
		    	Emocion.linear.x=398	
		    	Emocion.linear.y=0	
		    	Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()	
		    	#Dudoso3
		    	Emocion.linear.x=360	
		    	Emocion.linear.y=40	
		    	Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()
		    	#Dudoso2
		    	Emocion.linear.x=320	
		    	Emocion.linear.y=80	
		    	Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()
		    	#Dudoso1
		    	Emocion.linear.x=280	
		    	Emocion.linear.y=120	
		    	Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()
	    if response.fin==2:
	    		fin=0	
	    antman=input("pendejos")	
	    while response.acabe==5:
			rospy.wait_for_service('auxiliar_service')
	    		response = auxiliar_service.call(auxiliarRequest())
			if fin==0:
			    	datos.data=[0,0,1,1,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]
			    	rospy.loginfo(datos)
			    	mover.publish(datos)
			    	fin=1	
			if response.acabe!= 5:
				break
		    	#Complaciante4
		    	Emocion.linear.x=200	
		    	Emocion.linear.y=398	
		    	Emocion.linear.z=1	
			cara.publish(Emocion)
			rate.sleep()
		    	#Complaciante3
		    	Emocion.linear.x=200	
		    	Emocion.linear.y=360	
		    	Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()
		    	#Complaciante2
		    	Emocion.linear.x=200	
		    	Emocion.linear.y=320	
		    	Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()	
		    	#Complaciante1
		    	Emocion.linear.x=200	
		    	Emocion.linear.y=280	
		    	Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()
	    if response.fin==2:
	    		fin=0
	    antman=input("pendejos")
	    while response.acabe==6: 
			rospy.wait_for_service('auxiliar_service')
	    		response = auxiliar_service.call(auxiliarRequest())
			if fin==0:
				datos.data=[0,0,1,1,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
				rospy.loginfo(datos)
				mover.publish(datos)
				fin=1
			if response.acabe!= 6:
				break			
			#Interesado4
			Emocion.linear.x=398	
			Emocion.linear.y=200	
			Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()	
			#Interesado3
			Emocion.linear.x=360	
			Emocion.linear.y=200	
			Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()	
			#Interesado2
			Emocion.linear.x=320	
			Emocion.linear.y=200	
			Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()	
			#Interesado1
			Emocion.linear.x=280	
			Emocion.linear.y=200	
			Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()	
	    if response.fin==2:
	    		fin=0	
	    antman=input("pendejos")	
	    while response.acabe==7:
			rospy.wait_for_service('auxiliar_service')
	    		response = auxiliar_service.call(auxiliarRequest())
			if fin==0:
			    	datos.data=[0,0,0,1,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]
			    	rospy.loginfo(datos)
			    	mover.publish(datos)
			    	fin=1
			if response.acabe!= 7:
				break	
			#Alentador4
			Emocion.linear.x=398	
			Emocion.linear.y=398	
			Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()	
			#Alentador3
			Emocion.linear.x=360	
			Emocion.linear.y=360	
			Emocion.linear.z=1	
			cara.publish(Emocion)
			rate.sleep()
			#Alentador2
			Emocion.linear.x=320	
			Emocion.linear.y=320	
			Emocion.linear.z=1	
			cara.publish(Emocion)
			rate.sleep()
			#Alentador1
			Emocion.linear.x=280	
			Emocion.linear.y=280	
			Emocion.linear.z=1
			cara.publish(Emocion)
			rate.sleep()
	    #Neutro2
	    Emocion.linear.x=200	
	    Emocion.linear.y=220	
	    Emocion.linear.z=1	
	    cara.publish(Emocion)
	    rate.sleep()	
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
