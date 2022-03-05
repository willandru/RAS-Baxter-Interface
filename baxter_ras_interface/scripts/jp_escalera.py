#!/usr/bin/env python

import argparse
import sys
import copy
import struct
import numpy as np
import math

import rospy
import cv2
import cv_bridge
import geometry_msgs.msg 
import baxter_interface

from cv_bridge import CvBridge, CvBridgeError
from baxter_interface import Gripper

from std_msgs.msg import (Header, String)
from geometry_msgs.msg import (PoseStamped, Pose, Point, Quaternion)
from baxter_core_msgs.msg import EndEffectorState
from sensor_msgs.msg import Image
from std_msgs.msg import Int32
from geometry_msgs.msg import Pose, PoseStamped
from sensor_msgs.msg import Image
from std_msgs.msg import String
from geometry_msgs.msg import Twist

from baxter_core_msgs.srv import ( SolvePositionIK,
                                   SolvePositionIKRequest )

from jp_baxtertry1.srv import *

class RecojerCubo(object):
    def __init__(self, limb, hover_distance = 0.15, verbose=True):
        self._limb_name = limb # string
        self._hover_distance = hover_distance # in meters
        self._verbose = verbose # bool
        self._limb = baxter_interface.Limb(limb)
        self._gripper = baxter_interface.Gripper(limb)
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
        else:
            rospy.logerr("INVALID POSE - No Valid Joint Solution Found.")
            return False
        return limb_joints


    def _guarded_move_to_joint_position(self, joint_angles):
        if joint_angles:
            self._limb.move_to_joint_positions(joint_angles)
        else:
            rospy.logerr("No Joint Angles provided for move_to_joint_positions. Staying put.")

    def gripper_open(self):
        self._gripper.open()
        rospy.sleep(0.5)

    def gripper_close(self):
        self._gripper.close()
        rospy.sleep(0.5)

    def _approach(self, pose):
        approach = copy.deepcopy(pose)
        # approach with a pose the hover-distance above the requested pose
        approach.position.z = approach.position.z + self._hover_distance
        joint_angles = self.ik_request(approach)
        self._guarded_move_to_joint_position(joint_angles)

    def _retract(self):
        # retrieve current pose from endpoint
        current_pose = self._limb.endpoint_pose()
        ik_pose = Pose()
        ik_pose.position.x = current_pose['position'].x 
        ik_pose.position.y = current_pose['position'].y 
        ik_pose.position.z = current_pose['position'].z + self._hover_distance
        ik_pose.orientation.x = current_pose['orientation'].x 
        ik_pose.orientation.y = current_pose['orientation'].y 
        ik_pose.orientation.z = current_pose['orientation'].z 
        ik_pose.orientation.w = current_pose['orientation'].w
        joint_angles = self.ik_request(ik_pose)
        # servo up from current pose
        self._guarded_move_to_joint_position(joint_angles)
    def _servo_to_pose(self, pose):
        # servo down to release
        joint_angles = self.ik_request(pose)
        self._guarded_move_to_joint_position(joint_angles)

    def pick(self, pose):
        # open the gripper
        self.gripper_open()
        # servo above pose
        self._approach(pose)
        # servo to pose
        self._servo_to_pose(pose)
        # close gripper
        self.gripper_close()
        # retract to clear object
        self._retract()
    def up(self, pose):
        self._approach(pose)
    def place(self, pose):
        # servo above pose
        self._approach(pose)
        # servo to pose
        self._servo_to_pose(pose)
        # open the gripper
        self.gripper_open()
        # retract to clear object
        self._retract()

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber('demoEscalera', Twist, callback)
	rospy.Subscriber('moverAB', Twist, callback)
	rospy.spin()

def callback(data):
	rospy.loginfo(rospy.get_caller_id() + 'I heard from demoEscalera %s', data.linear.x)
    	rospy.loginfo(rospy.get_caller_id() + 'I heard from demoEscalera %s', data.linear.y)
	moverBrazo(data.linear.x,data.linear.y,data.linear.z)



#def callback2(data):
#	rospy.loginfo(rospy.get_caller_id() + 'I heard from moverAB %s', data.linear.x)
#    	rospy.loginfo(rospy.get_caller_id() + 'I heard from moverAB %s', data.linear.y)
#	moverBrazo(data.linear.x,data.linear.y,data.linear.z)

def posicion(P1,P2):
	j=0.36-(0.06*P1)
	k=0.36-(0.06*P2)
	return j,k

def desapilar(P1,P2,block_poses,Cub,overhead_orientation,idx):
	    j,k=posicion(P1,P2)
	    block_poses.append(Pose(
	        position=Point(x=0.72, y=j, z=-0.20),
	        orientation=overhead_orientation))
	    Cub.pick(block_poses[idx])
	    idx=idx+1
	    block_poses.append(Pose(
	        position=Point(x=0.72, y=j, z=-0.20),
	        orientation=overhead_orientation))
	    Cub.up(block_poses[idx])
	    idx=idx+1
	    return idx

def apilar(P1,P2,block_poses,Cub,overhead_orientation,idx):
	    j,k=posicion(P1,P2)
	    block_poses.append(Pose(
	        position=Point(x=0.72, y=k, z=-0.195),
	        orientation=overhead_orientation))
	    Cub.place(block_poses[idx])
	    idx=idx+1
	    block_poses.append(Pose(
	        position=Point(x=0.72, y=k, z=-0.195),
	        orientation=overhead_orientation))
	    Cub.up(block_poses[idx])
	    idx=idx+1	
	    return idx	

def moverBrazo(x,y,z):
#    rospy.init_node('baxter_moverderrst')	
    limb1 = 'left'
    limb2 = 'right'
    hover_distance = 0.15 # meters

    # Starting Joint angles for left arm
    starting_joint_angles1 = {'left_w0': 0.0,
                             'left_w1': 0.0,
                             'left_w2': 0.0,
                             'left_e0': 0.0,
                             'left_e1': 1.9539080285690458,
                             'left_s0': -0.5,
                             'left_s1': -0.7988204952913293}
#   Starting Joint angles for right arm
    starting_joint_angles2 = {'right_w0': 0.0,
                             'right_w1': 0.0,
                             'right_w2': 0.0,
                             'right_e0': 0.0,
                             'right_e1': 1.9539080285690458,
                             'right_s0': 0.5,
                             'right_s1': -0.7988204952913293}

    overhead_orientation = Quaternion(
                             x=1.0,
                             y=1.0,
                             z=0.00,
                             w=0.00)

    Cub=RecojerCubo(limb1, hover_distance)
    Cub.move_to_start(starting_joint_angles1)
    Cub=RecojerCubo(limb2, hover_distance)
    Cub.move_to_start(starting_joint_angles2)
    block_poses = list()
    idx=0
    while not rospy.is_shutdown():
        try:	
		if z==0:
		    # Starting Joint angles for left arm
		    starting_joint_angles1 = {'left_w0': 0.0,
				             'left_w1': 0.0,
				             'left_w2': 0.0,
				             'left_e0': 0.0,
				             'left_e1': 1.9539080285690458,
				             'left_s0': -0.5,
				             'left_s1': -0.7988204952913293}
		#   Starting Joint angles for right arm
		    starting_joint_angles2 = {'right_w0': 0.0,
				             'right_w1': 0.0,
				             'right_w2': 0.0,
				             'right_e0': 0.0,
				             'right_e1': 1.9539080285690458,
				             'right_s0': 0.5,
				             'right_s1': -0.7988204952913293}
		if z==1:
			if math.fabs(x-y)<=2 and x<5:
			    Cub=RecojerCubo(limb1, hover_distance)
			    Cub.move_to_start(starting_joint_angles1)
			elif math.fabs(x-y)<=2 and x>=5:
			    Cub=RecojerCubo(limb2, hover_distance)
			    Cub.move_to_start(starting_joint_angles2)  
			idx=desapilar(x,y,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(x,y,block_poses,Cub,overhead_orientation,idx)
			Cub=RecojerCubo(limb1, hover_distance)
			Cub.move_to_start(starting_joint_angles1)
			Cub=RecojerCubo(limb2, hover_distance)
			Cub.move_to_start(starting_joint_angles2)
		        z=0
			break
		if z==2:
			Cub=RecojerCubo(limb1, hover_distance)
			Cub.move_to_start(starting_joint_angles1)
#			Cambio Posicion V4-5
			idx=desapilar(4,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,5,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V6-4   
			idx=desapilar(6,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,4,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V7-6   
			idx=desapilar(7,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,6,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V5-7   
			idx=desapilar(5,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,7,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V3-5   
			idx=desapilar(3,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,5,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V4-3   
			idx=desapilar(4,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,3,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V6-4   
			idx=desapilar(6,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,4,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V5-6   
			idx=desapilar(5,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,6,block_poses,Cub,overhead_orientation,idx)
#			Posicion de inicio
			Cub=RecojerCubo(limb1, hover_distance)
			Cub.move_to_start(starting_joint_angles1)
			Cub=RecojerCubo(limb2, hover_distance)
			Cub.move_to_start(starting_joint_angles2)
			z=0
			break
#			Cambio Posicion V2-3   
			idx=desapilar(2,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,3,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V4-2   
			idx=desapilar(4,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,2,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V6-4   
			idx=desapilar(6,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,4,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V8-6   
			Cub=RecojerCubo(limb2, hover_distance)
			Cub.move_to_start(starting_joint_angles2)
			idx=desapilar(8,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,6,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V9-8   
			idx=desapilar(9,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,8,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V7-9   
			idx=desapilar(7,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,9,block_poses,Cub,overhead_orientation,idx)
			Cub=RecojerCubo(limb1, hover_distance)
			Cub.move_to_start(starting_joint_angles1)
#			Cambio Posicion V5-7   
			idx=desapilar(5,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,7,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V3-5   
			idx=desapilar(3,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,5,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V1-3   
			idx=desapilar(1,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,3,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V2-1   
			idx=desapilar(2,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,1,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V4-2   
			idx=desapilar(4,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,2,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V6-4   
			idx=desapilar(6,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,4,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V8-6   
			Cub=RecojerCubo(limb2, hover_distance)
			Cub.move_to_start(starting_joint_angles2)
			idx=desapilar(8,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,6,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V7-8   
			idx=desapilar(7,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,8,block_poses,Cub,overhead_orientation,idx)
			Cub=RecojerCubo(limb1, hover_distance)
			Cub.move_to_start(starting_joint_angles1)
#			Cambio Posicion V5-7   
			idx=desapilar(5,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,7,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V3-5   
			idx=desapilar(3,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,5,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V4-3   
			idx=desapilar(4,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,3,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V6-4   
			idx=desapilar(6,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,4,block_poses,Cub,overhead_orientation,idx)
#			Cambio Posicion V5-6   
			idx=desapilar(5,0,block_poses,Cub,overhead_orientation,idx)
			idx=apilar(0,6,block_poses,Cub,overhead_orientation,idx)
			z=0
			break
        except rospy.ServiceException, e:
            print "Service call failed: %s" % e

if __name__ == '__main__':
    listener()
