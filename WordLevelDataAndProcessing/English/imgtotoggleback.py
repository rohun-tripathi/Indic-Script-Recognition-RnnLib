import os, sys, time
import toggler as TG
from os import walk

filereuse = True

dir = os.curdir;

folders = ['Tam', 'Ban', 'Hin', 'Eng']

for folder in folders:
	path = os.path.join(dir, folder)
	print "Working in path == ", path
	# time.sleep(.5)

	filenames = []
	for root, dirs, files in walk(path):
		filenames.extend(files)
		break
	fileNo = 0
	for onefile in filenames:

		filepath = os.path.join(path, onefile)

		if not ".bmp" in filepath and not ".tiff" in filepath and not ".tif" in filepath:
			#Not an image file
			continue
		fileNo += 1
		outpath = "ToggledDATA/" + "black" +  folder.strip("Off") +"/" + onefile
		if not os.path.exists(outpath) and filereuse == True:
			TG.imgtotoggle(filepath, outpath)