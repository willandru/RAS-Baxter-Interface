#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import yaml
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
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.linear.x) # dificultad
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.linear.y) # juego
    #3 y 4 dos cubos 5 y 6 tres cubos 7 y 8 cuatro cubos
    x=int(data.linear.x)
    y=int(data.linear.y)
    Ordenar_Estado_inicial.main(x,y)
    terminar='Acabe'
    vector3=Twist()
    vector3.linear.z=2
    rospy.loginfo(terminar)
    pub.publish(terminar) 
    #rospy.loginfo(vector3)
    #pub2.publish(vector3)   
def main():
    global pub
    rospy.init_node('Ordenar_Estado_inicial')
    pub = rospy.Publisher('Termine_ordenar_estado_inicial', String , queue_size=10)
    rospy.Subscriber("/ordenar_estado_inicial", Twist, callback)
    rospy.spin()
if __name__ == '__main__':	
    main()
