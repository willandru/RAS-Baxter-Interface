#!/usr/bin/env python
import rospy
import yaml
from std_msgs.msg import String,Int32MultiArray
from geometry_msgs.msg import Twist
from jp_baxtertry1.srv import *
import sys
sys.path.append('/home/z420/ros_ws/src/jp_baxtertry1/scripts')
import Ordenar_Estado_inicial
import Ordenar_fichas_para_demostracion
import Ubicar_bloques_estado_actual_problema
import Avanzar_n_Estados_Correctos
import Devolver_n_Estados_Correctos
def callback(data):
    global pub,pub2
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data)
    n=len(data.data)
    matriz=list(range(n-2))
    matriz=data.data[0:n-2]
    dificultad=data.data[n-2]
    avanzar=data.data[n-1]
    Devolver_n_Estados_Correctos.main(matriz,dificultad,avanzar)
    terminar='Acabe'
    vector3=Twist()
    vector3.linear.z=2
    rospy.loginfo(terminar)
    pub.publish(terminar) 
    #rospy.loginfo(vector3)
    #pub2.publish(vector3)   
def main():
    global pub
    rospy.init_node('Devolver_n_Estados_Correctos')
    pub = rospy.Publisher('Termine_devolver_n_estados_correctos', String, queue_size=10)
    rospy.Subscriber("/devolver_n_estados_correctos", Int32MultiArray, callback)
    rospy.spin()
if __name__ == '__main__':	
    main()
