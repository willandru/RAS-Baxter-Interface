#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String,Int32MultiArray,MultiArrayLayout,MultiArrayDimension,Float32MultiArray
import numpy as np

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("chatter7", Int32MultiArray, callback)
#    rospy.Subscriber("chatter2", Int32MultiArray, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()
