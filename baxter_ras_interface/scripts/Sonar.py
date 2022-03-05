#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import UInt16


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.linear.x)
    global pub
    x=data.linear.x
    y=data.linear.y
    if (x>=150 and x<=250) and (y>150 and y<250):
	    datas=int(4095/2) 
	    print datas
	    pub.publish(datas)
    if x>250 and y>150 and y<250:
	    datas=0 
	    print datas
	    pub.publish(datas)
    if x>250 and y>0 and y<=150:
	    datas=int((4095*1)/5) 
	    print datas
	    pub.publish(datas)
    if x>250 and y>250 and y<=400:
	    datas=int((4095*1)/4)
	    print datas
	    pub.publish(datas)
    if x<150 and y>150 and y<250:
	    datas=4095 
	    print datas
	    pub.publish(datas)
    if x<150 and y>0 and y<=150:
	    datas=int((4095*4)/5) 
	    print datas
	    pub.publish(datas)
    if x<150 and y>250 and y<=400:
	    datas=int((4095*3)/4) 
	    print datas
	    pub.publish(datas)
def talker():
    #pub = rospy.Publisher(/robot/sonar/head_sonar/lights/set_green_level, Float32, queue_size=10)
    rospy.init_node('Luces_cabeza_sonar')
    global pub
    pub=rospy.Publisher("/robot/sonar/head_sonar/set_sonars_enabled",UInt16,queue_size=10)
    rospy.Subscriber('chatter1', Twist, callback)
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
