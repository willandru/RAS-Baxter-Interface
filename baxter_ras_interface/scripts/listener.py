#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

def callback(data):
    global z_1,data_1
    data_1=data
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.linear.z)
    z=data.linear.z
    z_1=z
    nada()
def callback2(data):
	rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.linear.z)
def nada():
	global z_1,data_1
	while not rospy.is_shutdown():	
		if z_1==0:
			break
		print z_1,data_1.linear.z
		rospy.Subscriber('chatter1', Twist, callback2)
		rospy.sleep(5)
		
def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener123')
    rospy.Subscriber('chatter1', Twist, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    global a
    a=0
    listener()
