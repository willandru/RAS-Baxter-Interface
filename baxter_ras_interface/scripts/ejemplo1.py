#!/usr/bin/env python
#Reference: the baxter_stocking_stuffer project by students in Northwestern's MSR program - Josh Marino, Sabeen Admani, Andrew Turchina and Chu-Chu Igbokwe
#Service provided - ObjLocation service - contains x,y,z coordinates of object in baxter's stationary body frame, whether it is ok to grasp and if objects were found in the current frame.

import rospy
import numpy as np

from jp_baxtertry1.srv import *
def get_obj_calibrate(request):
    global mask_verde,mask_rojo,mask_negro
    rospy.sleep(0.5)
    return CalibradoResponse(mask_verde,mask_rojo,mask_negro)
global mask_verde,mask_rojo,mask_negro
def main():
    #Initiate left hand camera object detection node
    rospy.init_node('ejemplo')
    global mask_verde,mask_rojo,mask_negro    
    mask_verde=np.zeros(5)
    mask_rojo=np.zeros(5)
    mask_negro=np.zeros(5)
    #Subscribe to left hand camera image 
    Calibrado_srv = rospy.Service("Calibrado_service", Calibrado, get_obj_calibrate)
    rospy.spin()

if __name__ == '__main__':
     main()
