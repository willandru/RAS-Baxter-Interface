#!/usr/bin/env python
import rospy
import yaml
from std_msgs.msg import String,Int32MultiArray
from geometry_msgs.msg import Twist
from jp_baxtertry1.srv import *
def callback(data):
    global matriz
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    matriz.append(data.data[0:36])
    print matriz
def callback2(data):
	global matriz
	if data.linear.x==0:
		with open('datos_validacion_cubo_1.yml', 'w') as outfile:
    			yaml.dump(matriz, outfile, default_flow_style=False)
		del matriz[:]
		matriz=list()
	if data.linear.x==1:
		with open('datos_validacion_cubo_2.yml', 'w') as outfile:
    			yaml.dump(matriz, outfile, default_flow_style=False)
		del matriz[:]
		matriz=list()
	if data.linear.x==2:
		with open('datos_validacion_cubo_3.yml', 'w') as outfile:
    			yaml.dump(matriz, outfile, default_flow_style=False)
		del matriz[:]
		matriz=list()
	if data.linear.x==3:
		with open('datos_validacion_cubo_4.yml', 'w') as outfile:
    			yaml.dump(matriz, outfile, default_flow_style=False)
		del matriz[:]
		matriz=list()
def main():
    global pub
    rospy.init_node('solucion_validacion_1')
    pub = rospy.Publisher('Terminamos', String, queue_size=10)
    rospy.Subscriber("/matriz2", Int32MultiArray, callback)
    rospy.Subscriber("/guardardatos", Twist, callback2)
    rospy.spin()
if __name__ == '__main__':	
    global matriz
    matriz=list()
    main()
