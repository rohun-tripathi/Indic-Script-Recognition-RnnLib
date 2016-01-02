#!/usr/bin/env python

import os, sys, time
import Image
import pprint
import numpy as np

def converttype(path, outpath):
	image = Image.open(path)
	image.save(outpath)	

def imgtotoggle (path, outpath):
	print outpath
	image = Image.open(path)
	image = image.convert("L")
	pixels = image.load()
	size = image.size

	for j in range(size[0]):
		for i in range(size[1]):
			if pixels[j, i] < 100:
				pixels[j, i] = 0
			else:
				pixels[j, i] = 355


	image.save(outpath)