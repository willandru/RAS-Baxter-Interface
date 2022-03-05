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
def corr(x,y,n,m,frame):
    pixel_x=7
    pixel_x=6*pixel_x
    pixel_y=7
    pixel_y=6*pixel_y
    x_1=x+(pixel_x*n)
    y_1=y+(pixel_y*m)
    center1=x_1,y_1
    print x_1,y_1
    cv2.circle(frame, center1, 5, (0, 0, 255), -1)
def callback(message):
    global matriz,a,hmin,hmax,smin,vmin,smax,vmax
    bridge = CvBridge()
    frame = bridge.imgmsg_to_cv2(message, "bgr8")
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    cv2.imwrite('calibrar_definitivo_guardado.jpg',frame)
    cv2.imshow('frame', frame)    
    cv2.waitKey(3)
def main():
    #Initiate left hand camera object detection node
    rospy.init_node('right_camera_node')
    cv2.namedWindow("frame", 1)
    #cv2.namedWindow("frame1", 1)
    #Subscribe to left hand camera image 
    rospy.Subscriber("/cameras/right_hand_camera/image", Image, callback)
    rospy.spin()

if __name__ == '__main__':
     global matriz,a,hmin,hmax,smin,vmin,smax,vmax,x_1,y_1
     x_1=0
     y_1=0
     a=0
     hmin=1000
     hmax=0
     smin=1000
     vmin=1000
     smax=0
     vmax=0
     matriz=list()
     cv2.namedWindow('bw')
     cv2.createTrackbar('x','bw',0,640,nothing)
     cv2.createTrackbar('y','bw',240,480,nothing)
     main()
