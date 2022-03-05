#!/usr/bin/env python
#Reference: the baxter_stocking_stuffer project by students in Northwestern's MSR program - Josh Marino, Sabeen Admani, Andrew Turchina and Chu-Chu Igbokwe
#Service provided - ObjLocation service - contains x,y,z coordinates of object in baxter's stationary body frame, whether it is ok to grasp and if objects were found in the current frame.

import rospy
import numpy as np
import cv2
import cv_bridge
import baxter_interface
import math
import sys
import glob
from std_msgs.msg import String, Int32
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge, CvBridgeError
from jp_baxtertry1.srv import * #nombre del catkin(carpeta)
from matplotlib import pyplot as plt
# mouse callback function
def nothing(x):
    pass
def callback(message):
    global matriz,a,hmin,hmax,smin,vmin,smax,vmax
    bridge = CvBridge()
    frame = bridge.imgmsg_to_cv2(message, "bgr8")
    x=cv2.getTrackbarPos('x','bw')
    y=cv2.getTrackbarPos('y','bw')
    center=x,y
    cv2.circle(frame, center, 5, (0, 0, 255), -1)
    #cv2.imwrite('calibrar_definitivo_guardado.jpg',frame)
    cv2.imshow('frame', frame)    
    cv2.waitKey(3)
def main():
    #Initiate left hand camera object detection node
    rospy.init_node('right_camera_node')
    cv2.namedWindow("frame", 1)
    #cv2.namedWindow("frame1", 1)
    #Subscribe to left hand camera image 
    rospy.Subscriber("/kinect2/qhd/image_color_rect", Image, callback)
    rospy.spin()

if __name__ == '__main__':
     cv2.namedWindow('bw')
     cv2.createTrackbar('x','bw',0,640,nothing)
     cv2.createTrackbar('y','bw',240,480,nothing)
     main()
