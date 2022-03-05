#!/usr/bin/env python
import rospy
import numpy as np
import cv2  # OpenCV module

from sensor_msgs.msg import Image, CameraInfo
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point, Pose, Twist, Vector3, Quaternion
from std_msgs.msg import ColorRGBA

from cv_bridge import CvBridge, CvBridgeError
import message_filters
import math
from jp_baxtertry1.srv import *
def nothing(x):
    pass
def Callback(rgb_data, depth_data):
    global act,xc,yc,response,xc1,xc2,xc3,xc4,yc1,yc2,yc3,yc4
    cv_bridge = CvBridge()
    cv_image = cv_bridge.imgmsg_to_cv2(rgb_data, "bgr8")
    cv_depthimage = cv_bridge.imgmsg_to_cv2(depth_data, "32FC1")
    cv_depthimage2 = np.array(cv_depthimage, dtype=np.float32)
    tamx1=len(response.matriz_1x)
    tamx2=len(response.matriz_2x)
    tamx3=len(response.matriz_3x)
    tamx4=len(response.matriz_4x)
    tamy1=len(response.matriz_1y)
    tamy2=len(response.matriz_2y)
    tamy3=len(response.matriz_3y)
    tamy4=len(response.matriz_4y)
    zc1=list(range(0,tamx1+1))
    zc2=list(range(0,tamx2+1))
    zc3=list(range(0,tamx3+1))
    zc4=list(range(0,tamx4+1))
    xc_1=list(range(0,tamx1+1))
    xc_2=list(range(0,tamx2+1))
    xc_3=list(range(0,tamx3+1))
    xc_4=list(range(0,tamx4+1))
    yc_1=list(range(0,tamx1+1))
    yc_2=list(range(0,tamx2+1))
    yc_3=list(range(0,tamx3+1))
    yc_4=list(range(0,tamx4+1))
    msg = rospy.wait_for_message('/camera/rgb/camera_info', CameraInfo, timeout=None)
    fx = msg.P[0]
    fy = msg.P[5]
    cx = msg.P[2]
    cy = msg.P[6]
    for x in range(tamx1):
	zc1[x]=(cv_depthimage2[int(response.matriz_1y[x])][int(response.matriz_1x[x])])
    	xn = (response.matriz_1x[x] - cx) / fx
    	yn = (response.matriz_1y[x] - cy) / fy
    	xc_1[x] = -1*((xn * zc1[x])/1000)
    	yc_1[x] = abs((yn * zc1[x])/1000)
    for x in range(tamx2):
	zc2[x]=(cv_depthimage2[int(response.matriz_2y[x])][int(response.matriz_2x[x])])
    	xn = (response.matriz_2x[x] - cx) / fx
    	yn = (response.matriz_2y[x] - cy) / fy
    	xc_2[x] = -1*((xn * zc2[x])/1000)
    	yc_2[x] = abs((yn * zc2[x])/1000)
    for x in range(tamx3):
	zc3[x]=(cv_depthimage2[int(response.matriz_3y[x])][int(response.matriz_3x[x])])
    	xn = (response.matriz_3x[x] - cx) / fx
    	yn = (response.matriz_3y[x] - cy) / fy
    	xc_3[x] = -1*((xn * zc3[x])/1000)
    	yc_3[x] = abs((yn * zc3[x])/1000)
    for x in range(tamx1):
	zc4[x]=(cv_depthimage2[int(response.matriz_4y[x])][int(response.matriz_4x[x])])
    	xn = (response.matriz_4x[x] - cx) / fx
    	yn = (response.matriz_4y[x] - cy) / fy
    	xc_4[x] = -1*((xn * zc4[x])/1000)
    	yc_4[x] = abs((yn * zc4[x])/1000)
    xc1=xc_1[0:tamx1]
    xc2=xc_2[0:tamx2]
    xc3=xc_3[0:tamx3]
    xc4=xc_4[0:tamx4]
    yc1=yc_1[0:tamx1]
    yc2=yc_2[0:tamx2]
    yc3=yc_3[0:tamx3]
    yc4=yc_4[0:tamx4]
    #print yc1,yc2,yc3,yc4
    #zc = (cv_depthimage2[int(y)][int(x)])
    center=320,240
    #w=320
    #h=240
    #miniD=-10
    #scaleF=0.0021
    #x1=((x-w)*(zc+miniD)*(scaleF))/1000
    #y1=((y-h)*(zc+miniD)*(scaleF))/1000
    cv2.circle(cv_image, center, 5, (0, 0, 255), -1)
    cv2.imshow('frame', cv_image)
    #print xc1
    cv2.waitKey(3)
def get_obj_calibrate(request):
    global xc1,xc2,xc3,xc4,yc1,yc2,yc3,yc4
    rospy.sleep(0.5)
    return CoordinatesResponse(xc1,xc2,xc3,xc4,yc1,yc2,yc3,yc4)
def main():
    global response
    rospy.init_node('calcular_posicion_cubo_kinect')
    #rospy.sleep(10)
    InfoCoor_service = rospy.ServiceProxy("InfoCoor_service", InfoCoor)
    rospy.wait_for_service('InfoCoor_service')
    response = InfoCoor_service.call(InfoCoorRequest())
    image_sub=message_filters.Subscriber("/camera/rgb/image_color", Image)
    depth_sub = message_filters.Subscriber("/camera/depth/image_raw", Image)
    ts = message_filters.ApproximateTimeSynchronizer([image_sub, depth_sub], 10, 0.5)
    ts.registerCallback(Callback)
    Coordinates_srv = rospy.Service("Coordinates_service", Coordinates, get_obj_calibrate)
    rospy.spin()

if __name__ == '__main__':
     main()
