#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Int32MultiArray

def talker():
    pub = rospy.Publisher('ordenar_fichas_estado_final_problema', Int32MultiArray, queue_size=40)
    rospy.init_node('talker12345_5', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    datos=Int32MultiArray()
    datos.data=[0,0,1,2,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5]
    rospy.loginfo(datos)
    pub.publish(datos)
    rate.sleep()
    rospy.spin()
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
