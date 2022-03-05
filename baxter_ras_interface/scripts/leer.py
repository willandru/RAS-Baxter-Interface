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
    rospy.init_node('baxter_mover__cubos_node')
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
    global initial_left,Cub
    hover_distance = 0.15 # meters
    # Starting Joint angles for left arm
    initial_left={'left_w0': -1.4289031039152629, 'left_w1': 1.41394679123338, 'left_w2': -0.2684466378799474, 'left_e0': -0.09088836168221076, 'left_e1': 1.6961992562042962, 'left_s0': 0.8709175923219437, 'left_s1': -0.28877188331942916}   
    limb1 = 'left'
    Cub=RecojerCubo(limb1, hover_distance)
def initialpose():
    global initial_left,Cub 
    Cub.gripper_calibrate()
    Cub.move_to_start(initial_left)
def girar():
    global initial_left,initial_right,Cub,Cub2
    Cub.gripper_close()
    giro_left2={'left_w0': -1.4841264122791378, 'left_w1': 1.2893108522176902, 'left_w2': 3.046869339937403, 'left_e0': -0.0038349519697135344, 'left_e1': 2.0125827937056626, 'left_s0': 0.745514662912311, 'left_s1': -0.44753889486556947}
    Cub.move_to_start(giro_left2)
    Cub.move_to_start(initial_left)
def subirBrazo():
    global initial_left,Cub
    Cub.gripper_close()
    giro_left2={'left_w0': -1.8461458782200955, 'left_w1': 1.6609176980829317, 'left_w2': -0.48205346259299126, 'left_e0': 0.15454856437945544, 'left_e1': 2.1966604882519123, 'left_s0': 0.591349593729827, 'left_s1': -1.4135632960364088}
    Cub.move_to_start(giro_left2)
    giro_left3={'left_w0': -1.7268788719620045, 'left_w1': 1.7939905314319913, 'left_w2': -0.2703641138648042, 'left_e0': 0.2044029399857314, 'left_e1': 1.6938982850224682, 'left_s0': 0.5437961893053792, 'left_s1': -0.09587379924283836}
    Cub.move_to_start(giro_left3)
    Cub.move_to_start(initial_left)
def estirar():
    global initial_left,Cub
    Cub.gripper_close()
    giro_left2={'left_w0': -1.580767201915919, 'left_w1': 0.5691068723054885, 'left_w2': -0.4019029664259784, 'left_e0': -0.6599952339876992, 'left_e1': 1.2118448224294769, 'left_s0': 0.336325287743877, 'left_s1': -0.10929613113683573}
    Cub.move_to_start(giro_left2)
    giro_left3={'left_w0': -1.4189322287940078, 'left_w1': 2.0931167850696473, 'left_w2': -0.07708253459124204, 'left_e0': -1.131694326262464, 'left_e1': 1.8545827725534652, 'left_s0': 0.9955535313376335, 'left_s1': 0.04563592843959106}
    Cub.move_to_start(giro_left3)
    Cub.move_to_start(initial_left)
if __name__ == '__main__':
    main()
