#!/usr/bin/env python

import argparse
import sys
import copy
import struct
import numpy as np
import yaml
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
def countgreen(matriz):
	count=0
	count1=0
	for x in range(len(matriz)):
		if matriz[x]==1:
			count=count+1
		if matriz[x]==0:
			count1=count1+1
	return count,count1

def yaml_loader(filepath):
	"""Loads a yaml file"""
	with open(filepath, "r") as file_descriptor:
		data =yaml.load(file_descriptor)
	return data

def yaml_dump(filepath, data):
	"""Dumps data to a yaml file"""
	with open(filepath, "w") as file_descriptor:
		yaml.dump(data, file_descriptor)
def traer_ficha(i,j,m,n,camara,data,color):
	aux = 0
	bandera_mov=0	
	for k in xrange(m):
		for l in xrange(n):
			if camara[k][l] == data['inicial1'][k][l]:
				pass
			elif camara[k][l] == color: # si encuentre un cubo de color 1(verde), lo llev a donde necesito
				print ("traer ficha de [k][l] a [i][j]")
				global valid_pose
				puntoa=(k,l)
				puntob=(i,j)
				moverbaxter(puntoa,puntob)
				aux = camara[i][j]
				camara[i][j]=camara[k][l]
				camara[k][l]=aux
				break
			else:
				pass
		if camara[i][j] == color:
			break

def quitar_ficha(i,j,m,n,camara,data,color):
	aux = 0
	bandera_mov=0
	for k in xrange(m): # busco si esta ficha se necesita en algun otro lado
		for l in xrange(n):
			if k <= i and l <= j: # no muevo lo que ya esta organizado
				pass
			elif camara[k][l] == 0 and data['inicial1'][k][l]==color: # si encuentre un espacio vacio y que la necesite,traigo la otra ficha
				print ("quitar ficha de [i][j] a [k][l]")
				puntoa=(i,j)
				puntob=(k,l)
				moverbaxter(puntoa,puntob)
				aux = camara[i][j]
				camara[i][j]=camara[k][l]
				camara[k][l]=aux
				bandera_mov=1;
				break
			else:
				pass
		if camara[i][j] == 0:
			break
	if bandera_mov==0:
		for k in xrange(m): # si no se necesita en otro lado la pongo en un sitio vacio
			for l in xrange(n):
				if k <= i and l <= j: # no muevo lo que ya esta organizado
					pass
				elif camara[k][l] == 0: # si encuentre un espacio vacio, traigo la otra ficha
					print ("5mover ficha de [i][j] a [k][l]")
					puntoa=(i,j)
					puntob=(k,l)
					moverbaxter(puntoa,puntob)
					aux = camara[i][j]
					camara[i][j]=camara[k][l]
					camara[k][l]=aux
					break
				else:
					pass
			if camara[i][j] == 0:
				break
def moverbaxter(puntoa,puntob):
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
		der_noy1=0.11
		der_noy2=0.23
		der_noy3=0.23
		der_noy4=0.23
		izq_noy1=-0.11
		izq_noy2=-0.22
		izq_noy3=-0.22
		izq_noy4=-0.22		
		if x_1<0:
  	  		block_poses = list()
    			idx=0
			Cub2.move_to_start(starting_joint_angles2)
	  	    	block_poses.append(Pose(
		     	position=Point(x=posinicialx, y=posinicialy, z=posinicialz),
		      	orientation=overhead_orientation))
	  	    	Cub2.pick(block_poses[idx])
	  	    	idx=idx+1
	  		x=matriz[puntob[0]][puntob[1]][0]
	  		y=matriz[puntob[0]][puntob[1]][1]
	  		posinicialx=y
	  		posinicialy=x
	  		posinicialz=-0.18
			if y>=nox1:	
				print '1'
				if x>=der_noy1:
					x=matriz[1][4][0]
					y=matriz[1][4][1]
					posinicialx_1=y
	  				posinicialy_1=x
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.up(block_poses[idx])
			  	    	idx=idx+1
					Cub2.move_to_start(starting_joint_angles2)
					x=matriz[1][4][0]
					y=matriz[1][4][1]
					posinicialx_1=y
	  				posinicialy_1=x
					posinicialz=-0.20
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1-0.01, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.pick(block_poses[idx])
			  	    	idx=idx+1
					posinicialz=-0.18
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx-0.01, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx-0.01, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.up(block_poses[idx])
					Cub.move_to_start(starting_joint_angles)
				else:
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
					Cub2.move_to_start(starting_joint_angles2)
			elif y>=nox2 and y<nox1:
				print '2'
				print x
				if x>=der_noy2:
					x=matriz[1][4][0]
					y=matriz[1][4][1]
					posinicialx_1=y
	  				posinicialy_1=x
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.up(block_poses[idx])
			  	    	idx=idx+1
					Cub2.move_to_start(starting_joint_angles2)
					x=matriz[1][4][0]
					y=matriz[1][4][1]
					posinicialx_1=y
	  				posinicialy_1=x
					posinicialz=-0.20
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1-0.01, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.pick(block_poses[idx])
			  	    	idx=idx+1
					posinicialz=-0.18
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx-0.01, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx-0.01, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.up(block_poses[idx])
					Cub.move_to_start(starting_joint_angles)
				else:
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
					Cub2.move_to_start(starting_joint_angles2)
			elif y>=nox3 and y<nox1 and y<nox2:
				print '3'
				if x>=der_noy3:
					x=matriz[1][4][0]
					y=matriz[1][4][1]
					posinicialx_1=y
	  				posinicialy_1=x
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.up(block_poses[idx])
			  	    	idx=idx+1
					Cub2.move_to_start(starting_joint_angles2)
					x=matriz[1][4][0]
					y=matriz[1][4][1]
					posinicialx_1=y
	  				posinicialy_1=x
					posinicialz=-0.20
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1-0.01, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.pick(block_poses[idx])
			  	    	idx=idx+1
					posinicialz=-0.18
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx-0.01, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx-0.01, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.up(block_poses[idx])
					Cub.move_to_start(starting_joint_angles)
				else:
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
					Cub2.move_to_start(starting_joint_angles2)
			elif y>=nox4 and y<nox1 and y<nox2 and y<nox3:
				print '4'
				print x,abs(izq_noy4)
				if x>=der_noy4:
					x=matriz[1][4][0]
					y=matriz[1][4][1]
					posinicialx_1=y
	  				posinicialy_1=x
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.up(block_poses[idx])
			  	    	idx=idx+1
					Cub2.move_to_start(starting_joint_angles2)
					x=matriz[1][4][0]
					y=matriz[1][4][1]
					posinicialx_1=y
	  				posinicialy_1=x
					posinicialz=-0.20
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1-0.01, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.pick(block_poses[idx])
			  	    	idx=idx+1
					posinicialz=-0.18
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx-0.01, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx-0.01, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.up(block_poses[idx])
					Cub.move_to_start(starting_joint_angles)
				else:
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
					Cub2.move_to_start(starting_joint_angles2)
			
			else:			
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
					Cub2.move_to_start(starting_joint_angles2)
			del block_poses[:]
		if x_1>0:
    			block_poses = list()
    			idx=0
			Cub.move_to_start(starting_joint_angles)
	  	    	block_poses.append(Pose(
		     	position=Point(x=posinicialx-0.01, y=posinicialy, z=posinicialz),
		      	orientation=overhead_orientation))
	  	    	Cub.pick(block_poses[idx])
	  	    	idx=idx+1
	  		x=matriz[puntob[0]][puntob[1]][0]
	  		y=matriz[puntob[0]][puntob[1]][1]
	  		posinicialx=y-0.01
	  		posinicialy=x
	  		posinicialz=-0.18
			if y>=nox1:
				if abs(x)>= abs(izq_noy1) and x<0:
					x=matriz[1][4][0]
					y=matriz[1][4][1]
					posinicialx_1=y
	  				posinicialy_1=x
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1-0.01, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1-0.01, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.up(block_poses[idx])
			  	    	idx=idx+1
					Cub.move_to_start(starting_joint_angles)
					x=matriz[1][4][0]
					y=matriz[1][4][1]
					posinicialx_1=y
	  				posinicialy_1=x
					posinicialz=-0.20
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.pick(block_poses[idx])
			  	    	idx=idx+1
					posinicialz=-0.18
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.up(block_poses[idx])
					Cub2.move_to_start(starting_joint_angles2)
				else:
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx-0.01, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialx=y-0.0005
			  		posinicialy=x
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx-0.01, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.up(block_poses[idx])
					Cub.move_to_start(starting_joint_angles)
			elif y>=nox2 and y<nox1:
				if abs(x)>= abs(izq_noy2) and x<0:
					x=matriz[1][4][0]
					y=matriz[1][4][1]
					posinicialx_1=y
	  				posinicialy_1=x
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1-0.01, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1-0.01, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.up(block_poses[idx])
			  	    	idx=idx+1
					Cub.move_to_start(starting_joint_angles)
					x=matriz[1][4][0]
					y=matriz[1][4][1]
					posinicialx_1=y
	  				posinicialy_1=x
					posinicialz=-0.20
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.pick(block_poses[idx])
			  	    	idx=idx+1
					posinicialz=-0.18
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.up(block_poses[idx])
					Cub2.move_to_start(starting_joint_angles2)
				else:
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx-0.01, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialx=y-0.0005
			  		posinicialy=x
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx-0.01, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.up(block_poses[idx])
					Cub.move_to_start(starting_joint_angles)
			elif y>=nox3 and y<nox1 and y<nox2:
				if abs(x)>= abs(izq_noy3) and x<0:
					x=matriz[1][4][0]
					y=matriz[1][4][1]
					posinicialx_1=y
	  				posinicialy_1=x
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1-0.01, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1-0.01, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.up(block_poses[idx])
			  	    	idx=idx+1
					Cub.move_to_start(starting_joint_angles)
					x=matriz[1][4][0]
					y=matriz[1][4][1]
					posinicialx_1=y
	  				posinicialy_1=x
					posinicialz=-0.20
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.pick(block_poses[idx])
			  	    	idx=idx+1
					posinicialz=-0.18
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.up(block_poses[idx])
					Cub2.move_to_start(starting_joint_angles2)
				else:
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx-0.01, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialx=y-0.0005
			  		posinicialy=x
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx-0.01, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.up(block_poses[idx])
					Cub.move_to_start(starting_joint_angles)
			elif y>=nox4 and y<nox1 and y<nox2 and y<nox3:
				print x,abs(izq_noy4)
				if abs(x)>= abs(izq_noy4) and x<0:
					x=matriz[1][4][0]
					y=matriz[1][4][1]
					posinicialx_1=y
	  				posinicialy_1=x
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1-0.01, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1-0.01, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.up(block_poses[idx])
			  	    	idx=idx+1
					Cub.move_to_start(starting_joint_angles)
					x=matriz[1][4][0]
					y=matriz[1][4][1]
					posinicialx_1=y
	  				posinicialy_1=x
					posinicialz=-0.20
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx_1, y=posinicialy_1, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.pick(block_poses[idx])
			  	    	idx=idx+1
					posinicialz=-0.18
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub2.up(block_poses[idx])
					Cub2.move_to_start(starting_joint_angles2)
				else:
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx-0.01, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.place(block_poses[idx])
			  	    	idx=idx+1
			  		posinicialx=y-0.0005
			  		posinicialy=x
			  		posinicialz=0
			  	    	block_poses.append(Pose(
				     	position=Point(x=posinicialx-0.01, y=posinicialy, z=posinicialz),
				      	orientation=overhead_orientation))
			  	    	Cub.up(block_poses[idx])
					Cub.move_to_start(starting_joint_angles)
			else:
		  	    	block_poses.append(Pose(
			     	position=Point(x=posinicialx-0.01, y=posinicialy, z=posinicialz),
			      	orientation=overhead_orientation))
		  	    	Cub.place(block_poses[idx])
		  	    	idx=idx+1
		  		posinicialx=y-0.0005
		  		posinicialy=x
		  		posinicialz=0
		  	    	block_poses.append(Pose(
			     	position=Point(x=posinicialx-0.01, y=posinicialy, z=posinicialz),
			      	orientation=overhead_orientation))
		  	    	Cub.up(block_poses[idx])
				Cub.move_to_start(starting_joint_angles)
			del block_poses[:]
		

def OrdenCub():
    alpha=0
    filepath = "/home/z420/ros_ws/src/jp_baxtertry1/scripts/test.yaml"
    data = yaml_loader(filepath)
    values = data.values()
    keys= data.keys()
    # cont_color 0=vacio 1=verde 2=rojo
    cont_color = [0,0,0]
    cont_color2 = [0,0,0]
    aux = 0
    posact = [0,0]
    #rospy.sleep(10)
    InfoCoor_service = rospy.ServiceProxy("InfoCoor_service", InfoCoor)
    rospy.wait_for_service('InfoCoor_service')
    response = InfoCoor_service.call(InfoCoorRequest())
    #print response
    camara=      [[0,0,2,0,0,0,1,0,0],
		 [0,0,0,2,0,0,0,0,0],
		 [0,1,0,2,1,0,0,2,0],
		 [0,0,0,0,0,1,0,0,0]]
    camara2=[response.matriz_5,response.matriz_6,response.matriz_7,response.matriz_8]
    n=9
    m=4
    for i in xrange(m):
    	for j in xrange(n):
		camara[i][j]=camara2[i][j]
    print camara
    for i in xrange(m):
    	for j in xrange(n):
        	if data['inicial1'][i][j] == 0:
			cont_color[0] = cont_color[0] + 1
		elif data['inicial1'][i][j] == 1:
			cont_color[1] = cont_color[1] + 1
		elif data['inicial1'][i][j] == 2:
			cont_color[2] = cont_color[2] + 1
		else:
			print("color no valido")

    for i in xrange(m):
    	for j in xrange(n):
        	if camara[i][j] == 0:
			cont_color2[0] = cont_color2[0] + 1
		elif camara[i][j] == 1:
			cont_color2[1] = cont_color2[1] + 1
		elif camara[i][j] == 2:
			cont_color2[2] = cont_color2[2] + 1
		else:
			print("color no valido")
    print cont_color
    print cont_color2
    if cont_color == cont_color2:
	for i in xrange(m):
    		for j in xrange(n):
			print "camara antes de movimiento"
			print camara
			if data['inicial1'][i][j] == camara[i][j]: # este elif se agranda si hay mas colores!!!!
				print "nada"					
				pass
			elif data['inicial1'][i][j] == 0:  #necesito quitar la ficha
				print "quitar"					
				quitar_ficha(i,j,m,n,camara,data,camara[i][j])

			elif data['inicial1'][i][j] == 1: #necesito color 1(verde)
				print "traer verde"
				bandera_mov=0					
				if camara[i][j] ==0: # y esta vacio (se agrega elif si hay mas colores!!!!!)
					traer_ficha(i,j,m,n,camara,data,data['inicial1'][i][j])
				else: # sino esta vacio necesito quitar la ficho y poner la correcta
					quitar_ficha(i,j,m,n,camara,data,camara[i][j])				
					traer_ficha(i,j,m,n,camara,data,data['inicial1'][i][j])
			else: #necesito color 2(roja)  
				print "traer rojo"
				bandera_mov=0					
				if camara[i][j] ==0: # y esta vacio (se agrega elif si hay mas colores!!!!!)
					traer_ficha(i,j,m,n,camara,data,data['inicial1'][i][j])
				else: # si no esta vacio debo quitar la que esta 
					quitar_ficha(i,j,m,n,camara,data,camara[i][j])				
					traer_ficha(i,j,m,n,camara,data,data['inicial1'][i][j])
			#print camara
			print " final pos"
			alpha=1

    if (cont_color[2] < cont_color2[2]) or (cont_color[1] < cont_color2[1]) or (cont_color[2] > cont_color2[2]) or (cont_color[1] > cont_color2[1]):
		if (cont_color[1] < cont_color2[1]):
			print("hay "+str(cont_color2[1]-cont_color[1])+" verdes de mas")
		if (cont_color[2] < cont_color2[2]):
			print("hay "+str(cont_color2[2]-cont_color[2])+" rojos de mas")
		if (cont_color[1] > cont_color2[1]):
			print("hay "+str(cont_color[1]-cont_color2[1])+" verdes de menos")
		if (cont_color[2] > cont_color2[2]):
			print("hay "+str(cont_color[2]-cont_color2[2])+" rojos de menos")
		if (cont_color[1] == cont_color2[1]):
			print("esta la cantidad suficiente de cubos verdes")
		if (cont_color[2] == cont_color2[2]):
			print("esta la cantidad suficiente de cubos rojos")
    return alpha	
def main():
    rospy.init_node('baxter_mover__cubos_node')
    rospy.sleep(10)
    #print matriz_1_1
    Coordinates_service = rospy.ServiceProxy("Coordinates_service", Coordinates)
    InfoCoor_service = rospy.ServiceProxy("InfoCoor_service", InfoCoor)
    rospy.wait_for_service('Coordinates_service')
    response = Coordinates_service.call(CoordinatesRequest())
    xdesfase=-0.004
    ydesfase=0.4547
    x=response.xc1[0]+xdesfase
    y=response.yc1[0]+ydesfase+0.035
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
    while not rospy.is_shutdown():
        try:
		alpha=OrdenCub()
		if alpha==1:
			Cub2.move_to_start(initial_right)
			Cub.move_to_start(initial_left)
			break
        except rospy.ServiceException, e:
            print "Service call failed: %s" % e

if __name__ == '__main__':
    global valid_pose	
    main()
