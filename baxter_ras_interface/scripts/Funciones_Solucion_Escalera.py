#!/usr/bin/env python
import rospy
import yaml
from std_msgs.msg import String,Int32MultiArray
from geometry_msgs.msg import Twist
from jp_baxtertry1.srv import *
import sys
sys.path.append('/home/z420/ros_ws/src/jp_baxtertry1/scripts')
import Solucion_Escalera
def callback(data):
    global pub,pub2
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    n=len(data.data)
    print 'hola'
    matriz=list(range(n-2))
    matriz=data.data[0:n-2]
    dificultad=data.data[n-2]
    avanzar=data.data[n-1]
    print matriz,dificultad,avanzar
    Solucion_Escalera.main(matriz,dificultad,avanzar)
    terminar='Acabe'
    rospy.loginfo(terminar)
    pub.publish(terminar)   
def main():
    global pub
    rospy.init_node('solucion_facil')
    pub = rospy.Publisher('Terminamos', String, queue_size=10)
    rospy.Subscriber("/solucion_escalera", Int32MultiArray, callback)
    rospy.spin()
if __name__ == '__main__':	
    main()
