#!/usr/bin/python2
import rospy
import numpy as np
import cv2
import cv_bridge
import baxter_interface


from std_msgs.msg import String, Int32
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge, CvBridgeError


def callback(message):
	pub = rospy.Publisher('/robot/xdisplay', Image, latch=True, queue_size=0.7)
    	pub.publish(message)
def main():
	rospy.init_node('camera_node')
	rospy.Subscriber("/cameras/head_camera/image",Image,callback)
	rospy.spin()

if __name__ == '__main__':
	main()
