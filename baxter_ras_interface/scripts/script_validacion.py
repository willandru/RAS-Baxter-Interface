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
	    mover = rospy.Publisher('/Validacion_script', Int32MultiArray, queue_size=40)
            Guardar_Archivo = rospy.Publisher('guardardatos', Twist, queue_size=36)
	    datosaguardar=Twist()
	    rospy.init_node('Obra', anonymous=True)
	    auxiliar_service = rospy.ServiceProxy("auxiliar_service", auxiliar)	
	    rospy.wait_for_service('auxiliar_service')
	    response = auxiliar_service.call(auxiliarRequest())
	    rate = rospy.Rate(0.2) # 10hz
	    datos=Int32MultiArray()
	    print "ACABE",response.acabe
	    if response.fin==2:
	    		fin=0
	    while response.acabe==0:
			rospy.wait_for_service('auxiliar_service')
	    		response = auxiliar_service.call(auxiliarRequest())
			if fin==0:
			    	datos.data=[0,0,1,1,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,1]
			    	rospy.loginfo(datos)
			    	mover.publish(datos)
			    	fin=1
	    datosaguardar.linear.x=2
	    Guardar_Archivo.publish(datosaguardar)
	    break	    
	
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
