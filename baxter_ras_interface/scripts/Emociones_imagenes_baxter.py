#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import yaml
from jp_baxtertry1.srv import *
import sys
sys.path.append('/home/z420/ros_ws/src/jp_baxtertry1/scripts')
import jp_baxter_emotions_speak
import analog_io_rampup

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.linear.x)
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.linear.y)
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.linear.z)
    jp_baxter_emotions_speak.callback(data.linear.x,data.linear.y,data.linear.z)
def main():
    global pub,pub2
    rospy.init_node('Emociones_imagenes_baxter')
    rospy.Subscriber('/emociones_baxter', Twist, callback)
    rospy.spin()
if __name__ == '__main__':	
    main()
