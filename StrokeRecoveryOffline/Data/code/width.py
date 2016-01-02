#!/usr/bin/env python

import os, sys, time
import Image
import numpy as np

def calculateNeighbour (pixels, j, i, size):
	neighbour = []
	for a1 in range(-1,2):			#[-1, 0, 1]
		for b1 in range(-1,2):
			if a1 == b1 == 0: continue
			if pixels[(j + a1) * size[0] + i + b1] > 0:
				neighbour.append(1)
			else:
				neighbour.append(0)
	return neighbour

def rotate(l1, l2):
	rotator = [3, 0, 1, 5, 2, 6, 7, 4]
	l3 = []; l4 = []
	for index, term in enumerate(rotator):
		l3.append( l1[term] )
		l4.append( l2[term] )
	return l3, l4

def listdoer(toplist, neighbour):
	eliminate = 1
	for standard, term in zip(toplist, neighbour):
		if standard == 2: #No Matching required
			continue
		elif term != standard:
			eliminate = 0
			break
	if eliminate == 1: return True
	else: return False

#thincaller function:
#If this function returns True, we need to change the value from 0 -> 1
#Else not so
def thincaller(neighbour, debug = False):
	list1 = [1, 1, 1, 2, 2, 0, 0, 0]
	list2 = [2, 1, 1, 0, 1, 2, 0, 2]
	for index in range(7):
		if debug == True : print "neighbour == ", neighbour
		if debug == True : print "Lists == ", list1, list2
		
		if listdoer(list1, neighbour) == True : return True
		elif listdoer(list2, neighbour) == True : return True	
		else:
			list1, list2 = rotate(list1, list2)
			continue
	return False

def thickcaller(neighbour, debug = False):
	list1 = [1, 1, 1, 2, 2, 0, 0, 0]
	list2 = [2, 1, 2, 0, 1, 0, 0, 2]
	for index in range(7):
		if debug == True : print "neighbour == ", neighbour
		if debug == True : print "Lists == ", list1, list2
		
		if listdoer(list1, neighbour) == True : return True
		elif listdoer(list2, neighbour) == True : return True	
		else:
			list1, list2 = rotate(list1, list2)
			continue
	return False

def prunecaller(neighbour, debug = False):
	list1 = [1, 2, 2, 1, 1, 1, 1, 1]
	list2 = [2, 2, 1, 1, 1, 1, 1, 1]
	for index in range(7):
		if debug == True : print "neighbour == ", neighbour
		if debug == True : print "Lists == ", list1, list2
		
		if listdoer(list1, neighbour) == True : return True
		elif listdoer(list2, neighbour) == True : return True	
		else:
			list1, list2 = rotate(list1, list2)
			continue
	return False


def thinnthick(pixels, size, function, debug = False):
	if debug == True: print pixels
	if debug == True: print size

	for j in range(1, size[1] -1):
		for i in range(1, size[0]- 1):
			if function == "thin" and pixels[j * size[0] + i] == 0:
				neighbour = calculateNeighbour(pixels, j , i ,size)
 				if thincaller(neighbour, False) == True:
 					pixels[j * size[0] + i] = 1
 			elif function == "thick" and pixels[j * size[0] + i] == 1:
 				neighbour = calculateNeighbour(pixels, j , i ,size)
 				if thickcaller(neighbour, False) == True:
 					pixels[j * size[0] + i] = 0
 			elif function == "prune" and pixels[j * size[0] + i] == 0:
 				neighbour = calculateNeighbour(pixels, j , i ,size)
 				if prunecaller(neighbour, False) == True:
 					pixels[j * size[0] + i] = 1
	return pixels