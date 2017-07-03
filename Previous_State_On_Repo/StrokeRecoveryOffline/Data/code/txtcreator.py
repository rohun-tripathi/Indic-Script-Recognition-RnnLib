#!/usr/bin/env python

import os, sys, time
import Image

import numpy as np

import width as WT

from copy import deepcopy

def update(top, bottom, left, right, j ,i):
	if top > j:
		top = j
	if bottom < j:
		bottom = j
	if left > i:
		left = i
	if right < i:
		right = i
	return top, bottom, left, right

def howmuchtocrop(image, path):
	pixels = list(image.getdata())
	size = image.size
	
	#Size ==  (20, 49). Not this was for a long and thin image. So, rows -> size[1] and cols -> size[0]
	top = size[1]; bottom = 0; left = size[0]; right = 0
	#I envision the system is like size[1] rows and size[0] columns

	for j in range(size[1]):
		for i in range(size[0]):		
			if pixels[j * size[0] + i] == 0:
				top, bottom, left, right = update(top, bottom, left, right, j ,i)

	return [left, top, right, bottom]

def imgtotxt (path, outpath,k, debug =False):
	if debug == True : print "In imgtotxt function, path and outpath == ", path, outpath
	if not ".bmp" in path and not ".tiff" in path and not ".tif" in path:
		print "The image obtained is not of format tiff or bmp or tif. Check path == ", path
		print "Exiting"
		sys.exit(0)
	
	image = Image.open(path)
	if ".bmp" in path:
		image = image.convert("L")
	size = image.size
	print >> k, size[1], size[0]
	corners = howmuchtocrop(image, path)

	#sequence in box of crop -> left, upper, right, and lower pixel 
	cropimage = image.crop( ( max(0, corners[0] - 1), max(0, corners[1] -1), min(size[0], corners[2] + 2), min(size[1], corners[3] + 2) ) )
	
	size = cropimage.size
	pixels = list(cropimage.getdata())

	
	# fixedheight = 400
	# fwidth = int( float(size[0]) * float(fixedheight)/float(size[1]) )
	# resizeimage = cropimage.resize( ( fwidth , fixedheight), Image.ANTIALIAS )
	# resizeimage.show()
	# pixels = list(resizeimage.getdata())
	# size = resizeimage.size
	
	
	lastcopy = deepcopy(pixels)
	for x in range(100):
		pixels = WT.thinnthick(pixels, size, "thin", False)
		if lastcopy == pixels:
			#print "Thin exited at x == ", x
			break
		else:
			lastcopy = deepcopy(pixels)


	# lastcopy = deepcopy(pixels)
	# for x in range(100):
	# 	pixels = WT.thinnthick(pixels, size, "thick", False)
	# 	if lastcopy == pixels:
	# 		print "Thick exited at x == ", x
	# 		break
	# 	else:
	# 		lastcopy = deepcopy(pixels)
	
	# lastcopy = deepcopy(pixels)
	# for x in range(100):
	# 	pixels = WT.thinnthick(pixels, size, "prune", False)
	# 	if lastcopy == pixels:
	# 		print "Prune exited at x == ", x
	# 		break
	# 	else:
	# 		lastcopy = deepcopy(pixels)


	string = '';

	for j in range(size[1]):
		for i in range(size[0]):
			if pixels[j * size[0] + i] < 255:
				string += '0'
			else:
				string += '1'
		string += "\n" 		
	printout = open(outpath,"w")

	print >> printout, string
	printout.close()