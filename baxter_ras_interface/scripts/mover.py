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
from baxter_core_msgs.msg import EndEffectorState
from sensor_msgs.msg import Image
from std_msgs.msg import Int32
from geometry_msgs.msg import Pose, PoseStamped

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
        #self._approach(pose)
        # servo to pose
        self._servo_to_pose(pose)
        # close gripper
        self.gripper_close()
        # retract to clear object
        #self._retract()
        # servo above pose
        #self._approach(pose)
    def pickcubo(self, pose):
        # open the gripper
        #self.gripper_open()
        # servo above pose
        self._approach(pose)
        # servo to pose
        #self._servo_to_pose(pose)
        # close gripper
        self.gripper_open()
        # retract to clear object
        #self._retract()
        # servo above pose
        #self._approach(pose)
    def inicial(self, pose):
        # open the gripper
        self.gripper_open()
        # servo above pose
        self._approach(pose)
        # servo to pose
        #self._servo_to_pose(pose)
        # close gripper
        #self.gripper_close()
        # retract to clear object
        #self._retract()

    def mover(self, pose):
        # open the gripper
        #self.gripper_open()
        # servo above pose
        self._servo_to_pose(pose)
        self.gripper_close()
	self.gripper_open()

def main2():
    rospy.init_node('baxter_mover__cubos_node')
    limb = 'left'
    Coordinates_service = rospy.ServiceProxy("Coordinates_service", Coordinates)
    rospy.wait_for_service('Coordinates_service')
    response = Coordinates_service.call(CoordinatesRequest())
    print response
def defmatriz(response,xdesfase,ydesfase):
	matriz = [range(9) for i in range(4)]
	for x in range(4):
		for y in range(9):
			if x==0:
				xcor=response.xc1[y]+xdesfase
    				ycor=response.yc1[y]+ydesfase+0.05
				matriz[x][y]=xcor,ycor
			if x==1:
				xcor=response.xc2[y]+xdesfase
    				ycor=response.yc2[y]+ydesfase+0.05
				matriz[x][y]=xcor,ycor
			if x==2:
				xcor=response.xc3[y]+xdesfase
    				ycor=response.yc3[y]+ydesfase+0.05
				matriz[x][y]=xcor,ycor
			if x==3:
				xcor=response.xc4[y]+xdesfase
    				ycor=response.yc4[y]+ydesfase+0.05
				matriz[x][y]=xcor,ycor
	return matriz
def main():
    rospy.init_node('baxter_mover__cubos_node')
    Coordinates_service = rospy.ServiceProxy("Coordinates_service", Coordinates)
    rospy.wait_for_service('Coordinates_service')
    response = Coordinates_service.call(CoordinatesRequest())
    xdesfase=-0.004
    ydesfase=0.4547
    matriz=defmatriz(response,xdesfase,ydesfase)
    print matriz[0][0]
    x=matriz[0][0][0]
    y=matriz[0][0][1]
    hover_distance = 0.15 # meters
    # Starting Joint angles for left arm
    starting_joint_angles = {'left_w0': 0.7781117546548761, 'left_w1': 1.1217234511412089, 'left_w2': 0.7696748603215063, 'left_e0': -1.1424321917776619, 'left_e1': 1.797825483401705, 'left_s0': -0.16835439147042416, 'left_s1': -0.8153107887610974}


    starting_joint_angles2 ={'right_s0': 0.02914563496982286, 'right_s1': -0.7815632114276183, 'right_w0': -0.7923010769428162, 'right_w1': 1.1106020904290395, 'right_w2': 2.107306107357587, 'right_e0': 1.1010147105047556, 'right_e1': 1.7249613959771477}

    if x>=0:
	    limb = 'left'
	    Cub=RecojerCubo(limb, hover_distance)
	    overhead_orientation = Quaternion(
		                     x=1.0,
		                     y=1.0,
		                     z=0.00,
		                     w=0.00)

    	    Cub.move_to_start(starting_joint_angles)
    if x<0:
	    limb = 'right'
	    Cub=RecojerCubo(limb, hover_distance)
	    overhead_orientation = Quaternion(
		                     x=1.0,
		                     y=1.0,
		                     z=0.00,
		                     w=0.00)

	    Cub.move_to_start(starting_joint_angles2)


    block_poses = list()
    idx=0
    while not rospy.is_shutdown():
        try:	    
		print x,y
		posinicialx=y
		posinicialy=x
		posinicialz=-0.18
	    	block_poses.append(Pose(
           	position=Point(x=posinicialx, y=posinicialy, z=posinicialz),
            	orientation=overhead_orientation))
	    	Cub.mover(block_poses[idx])
	    	idx=idx+1
		rospy.sleep(5.0)
		if x>=0:
			Cub.move_to_start(starting_joint_angles)
		if x<0:
			Cub.move_to_start(starting_joint_angles2)
	        rospy.sleep(1)
        except rospy.ServiceException, e:
            print "Service call failed: %s" % e

if __name__ == '__main__':
    main()
