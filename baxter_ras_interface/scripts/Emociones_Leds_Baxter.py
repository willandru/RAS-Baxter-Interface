#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.linear.x)
    global pub,pub2
    x=((data.linear.x*100)/400)
    y=100-((data.linear.x*100)/400)
    rate = rospy.Rate(10) # 10hz
    datas=x
    pub.publish(datas)
    datas1=y
    pub2.publish(datas1)
def talker():
    #pub = rospy.Publisher(/robot/sonar/head_sonar/lights/set_green_level, Float32, queue_size=10)
    rospy.init_node('Emociones_Leds_Baxter')
    global pub,pub2
    pub=rospy.Publisher("/robot/sonar/head_sonar/lights/set_green_level",Float32,queue_size=10)
    pub2=rospy.Publisher("/robot/sonar/head_sonar/lights/set_red_level",Float32,queue_size=10)
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
