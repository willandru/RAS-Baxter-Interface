#!/usr/bin/env python
import rospy
import yaml
from std_msgs.msg import String,Int32MultiArray
from geometry_msgs.msg import Twist
from jp_baxtertry1.srv import *
import sys
sys.path.append('/home/z420/ros_ws/src/jp_baxtertry1/scripts')
import Baxtermovimiento2
def callback(data):
    global pub,pub2
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data)
    x_1=int(data.linear.x)
    y_1=int(data.linear.y)
    x_2=int(data.angular.x)
    y_2=int(data.angular.y)
    velocidad=data.linear.z
    Baxtermovimiento2.initialpose(velocidad)
    puntoa=(x_1,y_1)
    puntob=(x_2,y_2)
    camara= [[0,0,0,0,0,0,0,0,0],
	     [0,0,0,0,1,0,0,0,0],
	     [0,0,0,0,0,0,0,0,0],
	     [0,0,2,2,0,1,0,0,1],]
    InfoCoor_service = rospy.ServiceProxy("InfoCoor_service", InfoCoor)
    rospy.wait_for_service('InfoCoor_service')
    response = InfoCoor_service.call(InfoCoorRequest())
    camara2=[response.matriz_5,response.matriz_6,response.matriz_7,response.matriz_8]
    n = 9 # Numero de filas
    m = 4 # Numero de columnas
    for i in xrange(m):
    	for j in xrange(n):
	    camara[i][j]=camara2[i][j]
    Baxtermovimiento2.moverbaxter(puntoa,puntob,velocidad,camara)
    Baxtermovimiento2.finalpose(velocidad)
    terminar='Acabe'
    vector3=Twist()
    vector3.linear.z=2
    rospy.loginfo(terminar)
    pub.publish(terminar)    
def main():
    global pub,pub2
    rospy.init_node('baxter_pick_and_place')
    pub = rospy.Publisher('Termine_baxter_posicion', String, queue_size=10)
    rospy.Subscriber("/baxter_posicion", Twist, callback)
    rospy.spin()
if __name__ == '__main__':	
    main()
