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
    def gripper_calibrate(self):
        self._gripper.calibrate()
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
        #self.gripper_calibrate()
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
def main2():
    rospy.init_node('baxter_mover__cubos_node')
    limb = 'left'
    Coordinates_service = rospy.ServiceProxy("Coordinates_service", Coordinates)
    rospy.wait_for_service('Coordinates_service')
    response = Coordinates_service.call(CoordinatesRequest())
    print response
def matriz1(x,y):
	matriz = [range(9) for i in range(4)]
	xaux=0.06
	yaux=0.082
        x_1=x
	y_1=y
	for x_2 in range(4):
		y=y_1-(x_2*yaux)
		for y_2 in range(9):
			matriz[x_2][y_2]=(x-(y_2*xaux)),y
	return matriz
def main():
    rospy.init_node('baxter_mover__cubos_node')
    rospy.sleep(10)
    Coordinates_service = rospy.ServiceProxy("Coordinates_service", Coordinates)
    rospy.wait_for_service('Coordinates_service')
    response = Coordinates_service.call(CoordinatesRequest())
    xdesfase=-0.004
    ydesfase=0.4547
    x=response.xc1[0]+xdesfase
    y=response.yc1[0]+ydesfase+0.035
    matriz=matriz1(x,y)
    a_1=((0,8),(1,8))
    x=matriz[a_1[0][0]][a_1[0][1]][0]
    y=matriz[a_1[0][0]][a_1[0][1]][1]
    hover_distance = 0.15 # meters
    # Starting Joint angles for left arm
    initial_left={'left_w0': -1.4289031039152629, 'left_w1': 1.41394679123338, 'left_w2': -0.2684466378799474, 'left_e0': -0.09088836168221076, 'left_e1': 1.6961992562042962, 'left_s0': 0.8709175923219437, 'left_s1': -0.28877188331942916}
    initial_right={'right_s0': -0.6810874698211237, 'right_s1': -0.8295001110490375, 'right_w0': -1.8308060703412412, 'right_w1': -1.0009224640952326, 'right_w2': 3.0181072001645517, 'right_e0': 0.16106798272796843, 'right_e1': 2.328582836010058}

    starting_joint_angles = {'left_w0': 0.7781117546548761, 'left_w1': 1.1217234511412089, 'left_w2': 0.7696748603215063, 'left_e0': -1.1424321917776619, 'left_e1': 1.797825483401705, 'left_s0': -0.16835439147042416, 'left_s1': -0.8153107887610974}


    starting_joint_angles2 ={'right_s0': 0.02914563496982286, 'right_s1': -0.7815632114276183, 'right_w0': -0.7923010769428162, 'right_w1': 1.1106020904290395, 'right_w2': 2.107306107357587, 'right_e0': 1.1010147105047556, 'right_e1': 1.7249613959771477}
    
    limb1 = 'left'
    Cub=RecojerCubo(limb1, hover_distance)
    Cub.gripper_calibrate()
    overhead_orientation = Quaternion(
	                     x=1.0,
	                     y=1.0,
	                     z=0.00,
	                     w=0.00)
    Cub.move_to_start(initial_left)
    limb2= 'right'
    Cub2=RecojerCubo(limb2, hover_distance)
    Cub2.gripper_calibrate()
    overhead_orientation = Quaternion(
	                     x=1.0,
	                     y=1.0,
	                     z=0.00,
	                     w=0.00)
    Cub2.move_to_start(initial_right)
    block_poses = list()
    idx=0
    a=0
    while not rospy.is_shutdown():
        try:
          if a==0:
  		posinicialx=y
  		posinicialy=x
  		posinicialz=-0.20
		if x>=0:
			Cub.move_to_start(starting_joint_angles)
	  	    	block_poses.append(Pose(
		     	position=Point(x=posinicialx, y=posinicialy, z=posinicialz),
		      	orientation=overhead_orientation))
	  	    	Cub.pick(block_poses[idx])
	  	    	idx=idx+1
	  		x=matriz[a_1[1][0]][a_1[1][1]][0]
	  		y=matriz[a_1[1][0]][a_1[1][1]][1]
	  		posinicialx=y
	  		posinicialy=x
	  		posinicialz=-0.18
	  	    	block_poses.append(Pose(
		     	position=Point(x=posinicialx, y=posinicialy, z=posinicialz),
		      	orientation=overhead_orientation))
	  	    	Cub.place(block_poses[idx])
	  	    	idx=idx+1
	  		posinicialx=y
	  		posinicialy=x
	  		posinicialz=0
	  	    	block_poses.append(Pose(
		     	position=Point(x=posinicialx, y=posinicialy, z=posinicialz),
		      	orientation=overhead_orientation))
	  	    	Cub.up(block_poses[idx])
	  	    	idx=idx+1
			Cub.move_to_start(starting_joint_angles)
			Cub.move_to_start(initial_left)
		if x<0:
			Cub2.move_to_start(starting_joint_angles2)
	  	    	block_poses.append(Pose(
		     	position=Point(x=posinicialx, y=posinicialy, z=posinicialz),
		      	orientation=overhead_orientation))
	  	    	Cub2.pick(block_poses[idx])
	  	    	idx=idx+1
	  		x=matriz[a_1[1][0]][a_1[1][1]][0]
	  		y=matriz[a_1[1][0]][a_1[1][1]][1]
	  		posinicialx=y
	  		posinicialy=x
	  		posinicialz=-0.18
	  	    	block_poses.append(Pose(
		     	position=Point(x=posinicialx, y=posinicialy, z=posinicialz),
		      	orientation=overhead_orientation))
	  	    	Cub2.place(block_poses[idx])
	  	    	idx=idx+1
	  		posinicialx=y
	  		posinicialy=x
	  		posinicialz=0
	  	    	block_poses.append(Pose(
		     	position=Point(x=posinicialx, y=posinicialy, z=posinicialz),
		      	orientation=overhead_orientation))
	  	    	Cub2.up(block_poses[idx])
	  	    	idx=idx+1
			Cub2.move_to_start(starting_joint_angles2)
			Cub2.move_to_start(initial_right)

  	        rospy.sleep(1)
      		a=a+1      
        except rospy.ServiceException, e:
            print "Service call failed: %s" % e

if __name__ == '__main__':
    main()
