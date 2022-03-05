#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from baxter_ras_interface.srv import *

def callback(data):
    global x,y,z
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.linear.z)
    x=data.linear.x
    y=data.linear.y
    z=data.linear.z
def get_obj_calibrate(request):
        global z 
	rospy.sleep(0.1)
	return infozResponse(z)
def get_obj_calibrate2(request):
        global x,y
	rospy.sleep(0.1)
	return infoxyzResponse(x,y)
		
def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('Escuchar_HRS')
    rospy.Subscriber('/emociones_baxter', Twist, callback)
    infoz_srv = rospy.Service("infoz_service", infoz, get_obj_calibrate)
    infoxyz_srv = rospy.Service("infoxyz_service", infoxyz, get_obj_calibrate2)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
