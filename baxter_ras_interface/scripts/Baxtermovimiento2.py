#!/usr/bin/env python

import argparse
import sys
import copy
import struct
import numpy as np
import yaml
import operator
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
def right(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,camara):
	m_1=4
	n_1=9
	m_2=0
	n_2=0
	beta=0
	for i in xrange(m_1):
    		for j in xrange(n_1):
			if j==4:
				if camara[i][j]==0 and beta==0:
					x=matriz[i][j][0]
					y=matriz[i][j][1]
					m_2=i
					n_2=j
					beta=1
	if beta==0:
		for i in xrange(m_1):
	    		for j in xrange(n_1):
				if j==5:
					if camara[i][j]==0 and beta==0:
						x=matriz[i][j][0]
						y=matriz[i][j][1]
						m_2=i
						n_2=j
						beta=1
	posinicialx_1=y
	posinicialy_1=x
	block_poses.append(Pose(
	position=Point(x=posinicialx_1+0.01, y=posinicialy_1, z=posinicialz),
	orientation=overhead_orientation))
	Cub.place(block_poses[idx])
	idx=idx+1
	posinicialz=0
	block_poses.append(Pose(
	position=Point(x=posinicialx_1+0.01, y=posinicialy_1, z=posinicialz),
	orientation=overhead_orientation))
	Cub.up(block_poses[idx])
	idx=idx+1
	Cub.move_to_start(starting_joint_angles)
	x=matriz[m_2][n_2][0]
	y=matriz[m_2][n_2][1]
	posinicialx_1=y
	posinicialy_1=x
	posinicialz=-0.20
	block_poses.append(Pose(
	position=Point(x=posinicialx_1+0.01, y=posinicialy_1, z=posinicialz),
	orientation=overhead_orientation))
	Cub2.pick(block_poses[idx])
	idx=idx+1
	posinicialz=-0.195
	block_poses.append(Pose(
	position=Point(x=posinicialx+0.01, y=posinicialy, z=posinicialz),
	orientation=overhead_orientation))
	Cub2.place(block_poses[idx])
	idx=idx+1
	posinicialz=0
	block_poses.append(Pose(
	position=Point(x=posinicialx+0.01, y=posinicialy, z=posinicialz),
	orientation=overhead_orientation))
	Cub2.up(block_poses[idx])
	Cub2.move_to_start(starting_joint_angles2)
def notright(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,x,y):
	block_poses.append(Pose(
	position=Point(x=posinicialx+0.01, y=posinicialy, z=posinicialz),
	orientation=overhead_orientation))
	Cub.place(block_poses[idx])
	idx=idx+1
	posinicialx=y-0.0005
	posinicialy=x
	posinicialz=0
	block_poses.append(Pose(
	position=Point(x=posinicialx+0.01, y=posinicialy, z=posinicialz),
	orientation=overhead_orientation))
	Cub.up(block_poses[idx])
	Cub.move_to_start(starting_joint_angles)


def left(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,camara):
	m_1=4
	n_1=9
	m_2=0
	n_2=0
	beta=0
	for i in xrange(m_1):
    		for j in xrange(n_1):
			if j==4:
				if camara[i][j]==0 and beta==0:
					x=matriz[i][j][0]
					y=matriz[i][j][1]
					m_2=i
					n_2=j
					beta=1
	if beta==0:
		for i in xrange(m_1):
	    		for j in xrange(n_1):
				if j==3:
					if camara[i][j]==0 and beta==0:
						x=matriz[i][j][0]
						y=matriz[i][j][1]
						m_2=i
						n_2=j
						beta=1
	posinicialx_1=y
	posinicialy_1=x
    	block_poses.append(Pose(
     	position=Point(x=posinicialx_1+0.01, y=posinicialy_1, z=posinicialz),
      	orientation=overhead_orientation))
    	Cub2.place(block_poses[idx])
    	idx=idx+1
	posinicialz=0
    	block_poses.append(Pose(
     	position=Point(x=posinicialx_1+0.01, y=posinicialy_1, z=posinicialz),
      	orientation=overhead_orientation))
    	Cub2.up(block_poses[idx])
    	idx=idx+1
	Cub2.move_to_start(starting_joint_angles2)
	x=matriz[m_2][n_2][0]
	y=matriz[m_2][n_2][1]
	posinicialx_1=y
	posinicialy_1=x
	posinicialz=-0.20
    	block_poses.append(Pose(
     	position=Point(x=posinicialx_1-0.01+0.01, y=posinicialy_1, z=posinicialz),
      	orientation=overhead_orientation))
    	Cub.pick(block_poses[idx])
    	idx=idx+1
	posinicialz=-0.195
    	block_poses.append(Pose(
     	position=Point(x=posinicialx-0.01+0.01, y=posinicialy, z=posinicialz),
      	orientation=overhead_orientation))
    	Cub.place(block_poses[idx])
    	idx=idx+1
	posinicialz=0
    	block_poses.append(Pose(
     	position=Point(x=posinicialx-0.01+0.01, y=posinicialy, z=posinicialz),
      	orientation=overhead_orientation))
    	Cub.up(block_poses[idx])
	Cub.move_to_start(starting_joint_angles)
def notleft(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,x,y):
    	block_poses.append(Pose(
     	position=Point(x=posinicialx+0.01, y=posinicialy, z=posinicialz),
      	orientation=overhead_orientation))
    	Cub2.place(block_poses[idx])
    	idx=idx+1
	posinicialx=y
	posinicialy=x
	posinicialz=0
    	block_poses.append(Pose(
     	position=Point(x=posinicialx+0.01, y=posinicialy, z=posinicialz),
      	orientation=overhead_orientation))
    	Cub2.up(block_poses[idx])
	Cub2.move_to_start(starting_joint_angles2)
def moverbaxter(puntoa,puntob,velocidad,camara):
		main(velocidad)
		global initial_left,initial_right,starting_joint_angles,starting_joint_angles2,Cub,Cub2,matriz,overhead_orientation 
	        x_1=matriz[puntoa[0]][puntoa[1]][0]
	        y=matriz[puntoa[0]][puntoa[1]][1]
	        posinicialx=y
	        posinicialy=x_1
	        posinicialz=-0.20
		nox1=0.75
		nox2=0.67
		nox3=0.59
		nox4=0.51
		der_noy1=0.01
		der_noy2=0.23
		der_noy3=0.23
		der_noy4=0.23
		izq_noy1=-0.01
		izq_noy2=-0.22
		izq_noy3=-0.22
		izq_noy4=-0.22
		if puntoa[1]==4:
			if puntob[1]>4:
	  	  		block_poses = list()
	    			idx=0
				Cub2.move_to_start(starting_joint_angles2)
		  	    	block_poses.append(Pose(
			     	position=Point(x=posinicialx+0.01, y=posinicialy, z=posinicialz),
			      	orientation=overhead_orientation))
		  	    	Cub2.pick(block_poses[idx])
		  	    	idx=idx+1
		  		x=matriz[puntob[0]][puntob[1]][0]
		  		y=matriz[puntob[0]][puntob[1]][1]
		  		posinicialx=y
		  		posinicialy=x
		  		posinicialz=-0.195
			    	block_poses.append(Pose(
			     	position=Point(x=posinicialx+0.01, y=posinicialy, z=posinicialz),
			      	orientation=overhead_orientation))
			    	Cub2.place(block_poses[idx])
			    	idx=idx+1
				posinicialx=y
				posinicialy=x
				posinicialz=0
			    	block_poses.append(Pose(
			     	position=Point(x=posinicialx+0.01, y=posinicialy, z=posinicialz),
			      	orientation=overhead_orientation))
			    	Cub2.up(block_poses[idx])
				Cub2.move_to_start(starting_joint_angles2)
				del block_poses[:]
			if puntob[1]<4:
	    			block_poses = list()
	    			idx=0
				Cub.move_to_start(starting_joint_angles)
		  	    	block_poses.append(Pose(
			     	position=Point(x=posinicialx-0.01+0.01, y=posinicialy, z=posinicialz),
			      	orientation=overhead_orientation))
		  	    	Cub.pick(block_poses[idx])
		  	    	idx=idx+1
		  		x=matriz[puntob[0]][puntob[1]][0]
		  		y=matriz[puntob[0]][puntob[1]][1]
		  		posinicialx=y-0.01
		  		posinicialy=x
		  		posinicialz=-0.195
				block_poses.append(Pose(
				position=Point(x=posinicialx+0.01, y=posinicialy, z=posinicialz),
				orientation=overhead_orientation))
				Cub.place(block_poses[idx])
				idx=idx+1
				posinicialx=y-0.0005
				posinicialy=x
				posinicialz=0
				block_poses.append(Pose(
				position=Point(x=posinicialx+0.01, y=posinicialy, z=posinicialz),
				orientation=overhead_orientation))
				Cub.up(block_poses[idx])
				Cub.move_to_start(starting_joint_angles)
				del block_poses[:]
		else:				
			if x_1<0:
	  	  		block_poses = list()
	    			idx=0
				Cub2.move_to_start(starting_joint_angles2)
		  	    	block_poses.append(Pose(
			     	position=Point(x=posinicialx+0.01, y=posinicialy, z=posinicialz),
			      	orientation=overhead_orientation))
		  	    	Cub2.pick(block_poses[idx])
		  	    	idx=idx+1
		  		x=matriz[puntob[0]][puntob[1]][0]
		  		y=matriz[puntob[0]][puntob[1]][1]
		  		posinicialx=y
		  		posinicialy=x
		  		posinicialz=-0.195
				if y>=nox1:	
					print '1'
					if x>=der_noy1:
						Cub.move_to_start(starting_joint_angles)
						left(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,camara)
					else:
						notleft(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,x,y)
				elif y>=nox2 and y<nox1:
					print '2'
					print x
					if x>=der_noy2:
						Cub.move_to_start(starting_joint_angles)
						left(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,camara)
					else:
				  	    	notleft(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,x,y)
				elif y>=nox3 and y<nox1 and y<nox2:
					print '3'
					if x>=der_noy3:
						Cub.move_to_start(starting_joint_angles)
						left(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,camara)
					else:
				  	    	notleft(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,x,y)
				elif y>=nox4 and y<nox1 and y<nox2 and y<nox3:
					print '4'
					print x,abs(izq_noy4)
					if x>=der_noy4:
						Cub.move_to_start(starting_joint_angles)
						left(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,camara)
					else:
				  	    	notleft(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,x,y)
			
				else:			
				  	    	notleft(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,x,y)
				del block_poses[:]
			if x_1>0:
	    			block_poses = list()
	    			idx=0
				Cub.move_to_start(starting_joint_angles)
		  	    	block_poses.append(Pose(
			     	position=Point(x=posinicialx-0.01+0.01, y=posinicialy, z=posinicialz),
			      	orientation=overhead_orientation))
		  	    	Cub.pick(block_poses[idx])
		  	    	idx=idx+1
		  		x=matriz[puntob[0]][puntob[1]][0]
		  		y=matriz[puntob[0]][puntob[1]][1]
		  		posinicialx=y-0.01
		  		posinicialy=x
		  		posinicialz=-0.195
				if y>=nox1:
					if abs(x)>= abs(izq_noy1) and x<0:
						Cub2.move_to_start(starting_joint_angles2)
						right(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,camara)
					else:
				  	    	notright(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,x,y)
				elif y>=nox2 and y<nox1:
					if abs(x)>= abs(izq_noy2) and x<0:
						Cub2.move_to_start(starting_joint_angles2)
						right(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,camara)
					else:
				  	    	notright(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,x,y)
				elif y>=nox3 and y<nox1 and y<nox2:
					if abs(x)>= abs(izq_noy3) and x<0:
						Cub2.move_to_start(starting_joint_angles2)
						right(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,camara)
					else:
				  	    	notright(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,x,y)
				elif y>=nox4 and y<nox1 and y<nox2 and y<nox3:
					print x,abs(izq_noy4)
					if abs(x)>= abs(izq_noy4) and x<0:
						Cub2.move_to_start(starting_joint_angles2)
						right(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,camara)
					else:
				  	    	notright(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,x,y)
				else:
			  	    	notright(matriz,block_poses,posinicialz,overhead_orientation,idx,Cub2,Cub,starting_joint_angles,starting_joint_angles2,posinicialx,posinicialy,x,y)
				del block_poses[:]
def main(velocidad):
    #rospy.sleep(10)
    #print matriz_1_1
    global vel
    vel=velocidad
    Coordinates_service = rospy.ServiceProxy("Coordinates_service", Coordinates)
    InfoCoor_service = rospy.ServiceProxy("InfoCoor_service", InfoCoor)
    rospy.wait_for_service('Coordinates_service')
    response = Coordinates_service.call(CoordinatesRequest())
    xdesfase=-0.005
    ydesfase=0.357
    x=response.xc1[0]+xdesfase
    y=response.yc1[0]+ydesfase+0.045
    global initial_left,initial_right,starting_joint_angles,starting_joint_angles2,Cub,Cub2,matriz,overhead_orientation 
    matriz=matriz1(x,y)
    hover_distance = 0.15 # meters
    # Starting Joint angles for left arm
    initial_left={'left_w0': -1.4289031039152629, 'left_w1': 1.41394679123338, 'left_w2': -0.2684466378799474, 'left_e0': -0.09088836168221076, 'left_e1': 1.6961992562042962, 'left_s0': 0.8709175923219437, 'left_s1': -0.28877188331942916}
    initial_right={'right_s0': -0.6810874698211237, 'right_s1': -0.8295001110490375, 'right_w0': -1.8308060703412412, 'right_w1': -1.0009224640952326, 'right_w2': 3.0181072001645517, 'right_e0': 0.16106798272796843, 'right_e1': 2.328582836010058}

    starting_joint_angles = {'left_w0': 0.7781117546548761, 'left_w1': 1.1217234511412089, 'left_w2': 0.7696748603215063, 'left_e0': -1.1424321917776619, 'left_e1': 1.797825483401705, 'left_s0': -0.16835439147042416, 'left_s1': -0.8153107887610974}


    starting_joint_angles2 ={'right_s0': 0.02914563496982286, 'right_s1': -0.7815632114276183, 'right_w0': -0.7923010769428162, 'right_w1': 1.1106020904290395, 'right_w2': 2.107306107357587, 'right_e0': 1.1010147105047556, 'right_e1': 1.7249613959771477}
    
    limb1 = 'left'
    Cub=RecojerCubo(limb1, hover_distance)
    overhead_orientation = Quaternion(
	                     x=1.0,
	                     y=1.0,
	                     z=0.00,
	                     w=0.00)

    limb2= 'right'
    Cub2=RecojerCubo(limb2, hover_distance)
    overhead_orientation = Quaternion(
	                     x=1.0,
	                     y=1.0,
	                     z=0.00,
	                     w=0.00)

def initialpose(velocidad):
    main(velocidad)
    global initial_left,initial_right,starting_joint_angles,starting_joint_angles2,Cub,Cub2,matriz,overhead_orientation 
    Cub.gripper_calibrate()
    Cub.move_to_start(initial_left)
    Cub2.gripper_calibrate()
    Cub2.move_to_start(initial_right) 
    print "Ok"
def finalpose(velocidad):
    main(velocidad)
    global initial_left,initial_right,starting_joint_angles,starting_joint_angles2,Cub,Cub2,matriz,overhead_orientation 
    Cub.move_to_start(initial_left)
    Cub2.move_to_start(initial_right)
	

