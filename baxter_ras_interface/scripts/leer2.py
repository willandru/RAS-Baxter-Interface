#!/usr/bin/env python

import argparse
import sys
import copy
import struct
import numpy as np

import rospy
import cv2
import cv_bridge
import geometry_msgs.msg 
import baxter_interface

from cv_bridge import CvBridge, CvBridgeError
from baxter_interface import Gripper

from std_msgs.msg import (Header, String)
from geometry_msgs.msg import (PoseStamped, Pose, Point, Quaternion)
from baxter_core_msgs.msg import EndpointState,JointCommand
from sensor_msgs.msg import Image
from std_msgs.msg import Int32
from geometry_msgs.msg import Pose, PoseStamped

from baxter_core_msgs.srv import ( SolvePositionIK,
                                   SolvePositionIKRequest )

import message_filters
from jp_baxtertry1.srv import *
import baxter_interface
class RecojerCubo(object):
    def __init__(self, limb, hover_distance = 0.15, verbose=True):
        self._limb_name = limb # string
        self._hover_distance = hover_distance # in meters
        self._verbose = verbose # bool
        self._limb = baxter_interface.Limb(limb)
        self._gripper = baxter_interface.Gripper(limb)
        global vel
	self._speed=vel
        ns = "ExternalTools/" + limb + "/PositionKinematicsNode/IKService"
        self._iksvc = rospy.ServiceProxy(ns, SolvePositionIK)
        rospy.wait_for_service(ns, 5.0)
        # verify robot is enabled
        #print("Getting robot state... ")
        self._rs = baxter_interface.RobotEnable(baxter_interface.CHECK_VERSION)
        self._init_state = self._rs.state().enabled
        #print("Enabling robot... ")
        self._rs.enable()
    def move_to_start(self, start_angles=None):
        #print("Moving the {0} arm to start pose...".format(self._limb_name))
        if not start_angles:
            start_angles = dict(zip(self._joint_names, [0]*7))
        self._guarded_move_to_joint_position(start_angles)
        self.gripper_open()
        #rospy.sleep(1.0)
        print("Running. Ctrl-c to quit")

    def ik_request(self, pose):
	global valid_pose
        hdr = Header(stamp=rospy.Time.now(), frame_id='base')
        ikreq = SolvePositionIKRequest()
        ikreq.pose_stamp.append(PoseStamped(header=hdr, pose=pose))
        try:
            resp = self._iksvc(ikreq)
        except (rospy.ServiceException, rospy.ROSException), e:
            rospy.logerr("Service call failed: %s" % (e,))
            return False
        # Check if result valid, and type of seed ultimately used to get solution
        # convert rospy's string representation of uint8[]'s to int's
        resp_seeds = struct.unpack('<%dB' % len(resp.result_type), resp.result_type)
        limb_joints = {}
        if (resp_seeds[0] != resp.RESULT_INVALID):
            seed_str = {
                        ikreq.SEED_USER: 'User Provided Seed',
                        ikreq.SEED_CURRENT: 'Current Joint Angles',
                        ikreq.SEED_NS_MAP: 'Nullspace Setpoints',
                       }.get(resp_seeds[0], 'None')
            if self._verbose:
                print("IK Solution SUCCESS - Valid Joint Solution Found from Seed Type: {0}".format(
                         (seed_str)))
            # Format solution into Limb API-compatible dictionary
            limb_joints = dict(zip(resp.joints[0].name, resp.joints[0].position))
            if self._verbose:
                #print("IK Joint Solution:\n{0}".format(limb_joints))
                print("------------------")
		valid_pose=1
        else:
	    valid_pose=0
            rospy.logerr("INVALID POSE - No Valid Joint Solution Found.")
            return False
        return limb_joints


    def _guarded_move_to_joint_position(self, joint_angles):
        if joint_angles:
	    self._limb.set_joint_position_speed(self._speed)
            self._limb.move_to_joint_positions(joint_angles)
	    self._limb.set_joint_position_speed(self._speed)
        else:
            rospy.logerr("No Joint Angles provided for move_to_joint_positions. Staying put.")

    def gripper_open(self):
        self._gripper.open()
        rospy.sleep(0.5)

    def gripper_close(self):
        self._gripper.close()
        rospy.sleep(0.5)
    def gripper_calibrate(self):
        self._gripper.calibrate()
        rospy.sleep(0.5)
def main():
    rospy.init_node('baxter_mover__cubos_node2')
    #rospy.Subscriber("/robot/limb/left/endpoint_state",EndpointState,callback)
    #rospy.Subscriber("/robot/limb/right/endpoint_state",EndpointState,callback2)
    #rospy.Subscriber("/robot/limb/left/joint_command",JointCommand,callback)
    limb = baxter_interface.Limb('right')	
    limb2 = baxter_interface.Limb('left')
    print 'right'
    print limb.joint_angles()
    print 'left'
    print limb2.joint_angles()	 
    valoresiniciales()
    initialpose()
    girar()
    subirBrazo()
    estirar()		
    rospy.spin()


def valoresiniciales():
    global vel
    vel=3
    global initial_right,Cub2
    hover_distance = 0.15 # meters
    # Starting Joint angles for left arm
    initial_right={'right_s0': -0.6810874698211237, 'right_s1': -0.8295001110490375, 'right_w0': -1.8308060703412412, 'right_w1': -1.0009224640952326, 'right_w2': 3.0181072001645517, 'right_e0': 0.16106798272796843, 'right_e1': 2.328582836010058}    
    limb2= 'right'
    Cub2=RecojerCubo(limb2, hover_distance)
def initialpose():
    global initial_right,Cub2 
    Cub2.gripper_calibrate()
    Cub2.move_to_start(initial_right)
def girar():
    global initial_right,Cub2
    Cub2.gripper_close()
    giro_right2={'right_s0': -0.3896311201228951, 'right_s1': -0.7861651537912745, 'right_w0': -1.9853546347206967, 'right_w1': -1.4281361135213202, 'right_w2': -1.9853546347206967, 'right_e0': -0.33172334538022075, 'right_e1': 2.316694484903946}
    Cub2.move_to_start(giro_right2)
    Cub2.move_to_start(initial_right)
def subirBrazo():
    global initial_right,Cub2
    Cub2.gripper_close()
    giro_right2={'right_s0': -0.7761942786700193, 'right_s1': -1.4227671807637212, 'right_w0': -1.9508400669932748, 'right_w1': -1.4066603824909245, 'right_w2': 3.0269275896948926, 'right_e0': -0.009587379924283835, 'right_e1': 2.513811016147222}
    Cub2.move_to_start(giro_right2)
    giro_right3={'right_s0': -0.7386117493668267, 'right_s1': -0.03528155812136451, 'right_w0': -1.708854597704351, 'right_w1': -1.5696458412037497, 'right_w2': 3.0200246761494083, 'right_e0': -0.12732040539448933, 'right_e1': 1.6037769137342002}
    Cub2.move_to_start(giro_right3)
    Cub2.move_to_start(initial_right)
def estirar():
    global initial_right,Cub2
    Cub2.gripper_close()
    giro_right2={'right_s0': -0.3854126729562102, 'right_s1': -0.4233786974563742, 'right_w0': -1.1466506389443467, 'right_w1': -0.7424467013365402, 'right_w2': 3.027311084891864, 'right_e0': 0.5150340495325276, 'right_e1': 1.8833449123263166}
    Cub2.move_to_start(giro_right2)
    giro_right3={'right_s0': -0.922305948716105, 'right_s1': 0.09088836168221076, 'right_w0': -1.6586167269011036, 'right_w1': -1.4442429117941171, 'right_w2': 2.7247333744814664, 'right_e0': 1.2559467700811826, 'right_e1': 1.9355002591144208}
    Cub2.move_to_start(giro_right3)
    Cub2.move_to_start(initial_right)
if __name__ == '__main__':
    main()
