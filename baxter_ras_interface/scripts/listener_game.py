#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from jp_baxtertry1.srv import *

def callback(data):
    global x,y
    x=data.linear.x
    y=data.linear.y
def get_obj_calibrate(request):
        global x,y 
	rospy.sleep(0.2)
	return juego_dificultadResponse(x,y)
def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('escuchar_juego_dificultad')
    rospy.Subscriber('/recibir_juego_dificultad', Twist, callback)
    juego_dificultad_srv = rospy.Service("juego_dificultad_service", juego_dificultad, get_obj_calibrate)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
if __name__ == '__main__':
    global x,y 
    x=0
    y=0
    listener()
