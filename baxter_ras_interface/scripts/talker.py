#!/usr/bin/env python
import rospy
import yaml
from std_msgs.msg import String,Int32MultiArray
from geometry_msgs.msg import Twist
from jp_baxtertry1.srv import *
def callback(data):
    global pub,pub2
    n=len(data.data)
    print n
    matriz=list(range(n-3))
    matriz=data.data[0:n-3]
    dificultad=data.data[n-2]
    avanzar=data.data[n-1]
    print matriz,dificultad,avanzar
    #rospy.loginfo(vector3)
    #pub2.publish(vector3)    
def main():
    global pub,pub2
    rospy.init_node('Avanzar_n_Estados_Correctos')
    rospy.Subscriber("/avanzar", Int32MultiArray, callback)
    rospy.spin()
if __name__ == '__main__':	
    main()
