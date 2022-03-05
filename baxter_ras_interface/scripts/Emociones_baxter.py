#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import yaml
from baxter_ras_interface.srv import *
import sys
sys.path.append('src/baxter_ras_interface/scripts')
import baxter_ras_interface_speak
import analog_io_rampup
x=0
y=0
z=0
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.linear.x)
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.linear.y)
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.linear.z)
    global x,y,z
    x=data.linear.x
    y=data.linear.y
    z=data.linear.z
def listenVoice(data):
    global x,y,z
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data)
    baxter_ras_interface_speak.callback(x,y,z,data)
def main():
    global pub,pub2
    rospy.init_node('Emociones_imagenes_baxter')
    rospy.Subscriber('/emociones_baxter', Twist, callback)
    rospy.Subscriber('/voice_message', String, listenVoice)
    rospy.spin()
if __name__ == '__main__':	
    main()
