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
import Ordenar_Fichas_Estado_Final_Problema
def callback(data):
    global pub,pub2
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data)
    x=int(data.linear.x)
    y=int(data.linear.y)

    Ordenar_Fichas_Estado_Final_Problema.main(x,y)
    terminar='Acabe'
    vector3=Twist()
    vector3.linear.z=2
    rospy.loginfo(terminar)
    pub.publish(terminar) 
    #rospy.loginfo(vector3)
    #pub2.publish(vector3)   
def main():
    global pub
    rospy.init_node('Ordenar_Fichas_Estado_Final_Problema')
    pub = rospy.Publisher('Termine_ordenar_fichas_estado_final_problema', String, queue_size=10)
    rospy.Subscriber("/ordenar_fichas_estado_final_problema", Twist, callback)
    rospy.spin()
if __name__ == '__main__':	
    main()
