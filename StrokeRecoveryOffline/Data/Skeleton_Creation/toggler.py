#!/usr/bin/env python

import os, sys, time
import Image

import numpy as np

def imgtotoggle (path, outpath):
	image = Image.open(path)
	image = image.convert("L")

	pixels = image.load()
	size = image.size
	
	for j in range(size[0]):
		for i in range(size[1]):
			if pixels[j, i] == 0:
				pixels[j, i] = 255
			else:
				pixels[j, i] = 0


	image.save(outpath)