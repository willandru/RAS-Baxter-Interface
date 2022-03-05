#!/usr/bin/env python
import rospy
import yaml
from std_msgs.msg import String,Int32MultiArray
from geometry_msgs.msg import Twist
from jp_baxtertry1.srv import *
def callback(data):
     global acabe,fin
     print "Acabe"	
     acabe=acabe+1
     fin=2
def get_obj_calibrate(request):
        global acabe,fin
	rospy.sleep(0.2)
	return auxiliarResponse(acabe,fin)		  
def main():
    global pub,pub2,acabe,fin
    rospy.init_node('Aux')
    auxiliar_srv = rospy.Service("auxiliar_service", auxiliar, get_obj_calibrate)
    rospy.Subscriber("/Terminamos", String, callback)
    rospy.spin()
if __name__ == '__main__':
    global acabe,fin
    acabe=0
    fin=0		
    main()
