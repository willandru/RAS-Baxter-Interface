#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String,Int32MultiArray,MultiArrayLayout,MultiArrayDimension,Float32MultiArray
import numpy as np


def talker():
    pub = rospy.Publisher('chatter', Int32MultiArray, queue_size=32)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        a = Int32MultiArray(data=[1,2,3])
        #a = Int32MultiArray(layout=["a","b","c"],data=[1.3,2.3,3.3])

        pub.publish(a)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
