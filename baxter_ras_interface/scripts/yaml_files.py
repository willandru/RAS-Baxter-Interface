#!/usr/bin/env python
import yaml

def yaml_loader(filepath):
	"""Loads a yaml file"""
	with open(filepath, "r") as file_descriptor:
		data =yaml.load(file_descriptor)
	return data

def yaml_dump(filepath, data):
	"""Dumps data to a yaml file"""
	with open(filepath, "w") as file_descriptor:
		yaml.dump(data, file_descriptor)

if __name__ == "__main__":
	filepath = "/home/z420/ros_ws/src/jp_baxtertry1/scripts/test.yaml"
	data = yaml_loader(filepath)
	#print data

	values = data.values()
	#keys = data.keys()
	
	print values[0][3]
	#print keys
	#print values[0][0]
	
	
