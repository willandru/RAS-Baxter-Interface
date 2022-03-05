#!/usr/bin/env python
#Reference: the baxter_stocking_stuffer project by students in Northwestern's MSR program - Josh Marino, Sabeen Admani, Andrew Turchina and Chu-Chu Igbokwe
#Service provided - ObjLocation service - contains x,y,z coordinates of object in baxter's stationary body frame, whether it is ok to grasp and if objects were found in the current frame.

import rospy
import numpy as np
import cv2
import cv_bridge
import baxter_interface
import math

from std_msgs.msg import String, Int32
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge, CvBridgeError
from jp_baxtertry1.srv import *

def main():
    #Initiate left hand camera object detection node
    rospy.init_node('recibirejemplo1')
    Calibrado_service = rospy.ServiceProxy("Calibrado_service", Calibrado)
    #rospy.sleep(1)
    while not rospy.is_shutdown():
	    rospy.wait_for_service('Calibrado_service')
	    response = Calibrado_service.call(CalibradoRequest())
	    print response.mask_verde
	    #rospy.Subscriber("/camera/rgb/image_color", Image, callback)
	    

if __name__ == '__main__':

     main()
