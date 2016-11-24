# -*- coding: utf-8 -*-
"""
@author: Karl C. Goedel (mail@karl-goedel.de)

This module provides gcode parsing functionality for pyGC

"""

import re


# Find the minimal z value	
def zmin(lines):
	z=0
	mini=0
	for l in lines:
		#Check if it is a G0/G1/G2 command (only supported commands)
		if l[:2] != "G0" and l[:2] != "G1" and l[:2] != "G2" and l[:2] != "G3":
			continue
		#Check if z value is changed
		if "Z" in l:
			index = l.find("Z")
			#extract all floats, take the first one (after "Z")
			z=float(re.findall(r"[-+]?\d*\.\d+|\d+", l[index:])[0])
			if z < mini:
				mini = z
	return mini


# Parse Gcode and return coordinates for drawing in different layers for different tools (probably buggy!)
def parsedraw(lines,tooloffset):
	layers = []
	layers_z = []
	x=0
	y=0
	z=0
	step = -1
	setz = False
	mode = 0
	for l in lines:
		#Check if it is a G0/G1/G2 command (only supported commands)
		if l[:2] != "G0" and l[:2] != "G1" and l[:2] != "G2" and l[:2] != "G3" and l[:1] != ">":
			continue
		#Check for vertical and horizontal lines
		if l[:1] == ">":
			if "CTV" in l:
				mode = 1
			if "CTH" in l:
				mode = 2
		#Check if z value is changed
		if "Z" in l:
			index = l.find("Z")
			#extract all floats, take the first one (after "Z")
			z=re.findall(r"[-+]?\d*\.\d+|\d+", l[index:])[0]
			layers.append([])
			if mode == 1:
				layers_z.append(str(float(z)-70))
			elif mode == 2:
				layers_z.append(str(float(z)-80))
			else:
				layers_z.append(z)
			step += 1
			setz = True
		#Add X Y values
		if "X" in l:
			#If in the beginning no z is set, use 0 as first layer
			if setz == False:
				layers.append([])
				layers_z.append(z)
				step += 1
				setz = True
			index = l.find("X")
			#extract all floats, take the first one (after "X")
			x=re.findall(r"[-+]?\d*\.\d+|\d+", l[index:])[0]
			if mode == 1:
				x = str(float(x) + tooloffset[0])
			if mode == 2:
				x = str(float(x) + tooloffset[1])
		if "Y" in l:
			#If in the beginning no z is set, use 0 as first layer
			if setz == False:
				layers.append([])
				layers_z.append(z)
				step += 1
				setz = True
			index = l.find("Y")
			#extract all floats, take the first one (after "Y")
			y=re.findall(r"[-+]?\d*\.\d+|\d+", l[index:])[0]
			if mode == 1:
				y = str(float(y) + tooloffset[2])
			if mode == 2:
				y = str(float(y) + tooloffset[3])
		layers[step].append([x,y])
	return ( layers, layers_z, step )


# general parse (not used, probably buggy deprecated)
def parse(lines):
	layers = []
	layers_z = []
	x=0
	y=0
	z=0
	step = -1
	setz = False
	mode = 0
	for l in lines:
		#Check if it is a G0/G1/G2 command (only supported commands)
		if l[:2] != "G0" and l[:2] != "G1" and l[:2] != "G2" and l[:2] != "G3" and l[:1] != ">":
			continue
		#Check for vertical and horizontal lines
		if l[:1] == ">":
			if "CTV" in l:
				mode = 1
			if "CTH" in l:
				mode = 2
		#Check if z value is changed
		if "Z" in l:
			index = l.find("Z")
			#extract all floats, take the first one (after "Z")
			z=re.findall(r"[-+]?\d*\.\d+|\d+", l[index:])[0]
			layers.append([])
			layers_z.append(z)
			step += 1
			setz = True
		#Add X Y values
		if "X" in l:
			#If in the beginning no z is set, use 0 as first layer
			if setz == False:
				layers.append([])
				layers_z.append(z)
				step += 1
				setz = True
			index = l.find("X")
			#extract all floats, take the first one (after "X")
			x=re.findall(r"[-+]?\d*\.\d+|\d+", l[index:])[0]
			if mode == 1:
				x = str(float(x) + tooloffset[0])
			if mode == 2:
				x = str(float(x) + tooloffset[1])
		if "Y" in l:
			#If in the beginning no z is set, use 0 as first layer
			if setz == False:
				layers.append([])
				layers_z.append(z)
				step += 1
				setz = True
			index = l.find("Y")
			#extract all floats, take the first one (after "Y")
			y=re.findall(r"[-+]?\d*\.\d+|\d+", l[index:])[0]
			if mode == 1:
				y = str(float(y) + tooloffset[2])
			if mode == 2:
				y = str(float(y) + tooloffset[3])
		layers[step].append([x,y])
	return ( layers, layers_z, step )
