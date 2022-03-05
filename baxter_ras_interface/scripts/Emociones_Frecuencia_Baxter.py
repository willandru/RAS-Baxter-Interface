#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import UInt16
from baxter_ras_interface.srv import *

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.linear.x)
    infoxyz_service = rospy.ServiceProxy("infoxyz_service", infoxyz)
    global pub
    while not rospy.is_shutdown():
	    rospy.wait_for_service('infoxyz_service')
	    response = infoxyz_service.call(infoxyzRequest())
	    ratef=10.1-((response.x*10)/400)
	    x_1=0x8000
            x_2=0x0fff
	    rate = rospy.Rate(ratef) # 10hz
	    datas=x_2
	    pub.publish(datas)
            rate.sleep()
	    rate = rospy.Rate(ratef) # 10hz
	    datas=x_1
	    pub.publish(datas)
            rate.sleep()
def talker():
    #pub = rospy.Publisher(/robot/sonar/head_sonar/lights/set_green_level, Float32, queue_size=10)
    rospy.init_node('Emociones_Frecuencia_Baxter')
    global pub,pub2
    pub=rospy.Publisher("/robot/sonar/head_sonar/lights/set_lights",UInt16,queue_size=10)
    infoxyz_service = rospy.ServiceProxy("infoxyz_service", infoxyz)
    rospy.Subscriber('/emociones_baxter', Twist, callback)
    #rate = rospy.Rate(10) # 10hz
    #data=0
    #rospy.loginfo(data)
    #pub.publish(data)
    #rate.sleep()
    rospy.spin()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
