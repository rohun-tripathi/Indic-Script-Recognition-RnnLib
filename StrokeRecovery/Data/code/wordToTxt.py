#STROKE RECOVERY
#This is the start point of our stroke recovery code.
#This calls the file which recursively enters folders and generates the Strokes for each image file

import os, sys, time, re
import pixelsToStrokes as MN
from os import walk

def FilesFromEach (num, MaxForthisFolder):
	if num == 0:
		print "The number of folders is zero somewhere. Exiting"
		sys.exit(0)
	return MaxForthisFolder/num

def resursiveStrokeRecovery(inputdir, outputdir):
	MaxFilesFromEachLang = 50000
	#This is to be kept true whenever the format of data has not been changed. Then we will only ADD to the existing txt files
	filereuse = True

	dir = inputdir;

	folders = ['blackBan', 'blackHin', 'blackEng']
	# folders = ['blackEngWord', "blackHinWord"]
	
	sizes = open("sizes.txt", "w")
	rejects = open("rejects.txt", "w")

	for folder in folders:
		path = os.path.join(dir, folder)
		print "Working in path == ", path
		time.sleep(.5)

		#Now we enter each folder
		distribution = []
		
		for root, dirs, files in walk(path):
			distribution.extend(dirs)
			break
		
		NumberinEach = FilesFromEach( len(distribution), MaxFilesFromEachLang )
		for index1, subfolder in enumerate(distribution):
			pathfol = os.path.join(path, subfolder)

			dirnames = []
			for root, dirs, files in walk(pathfol):
				dirnames.extend(dirs)
				break

			NumberInEachSub = FilesFromEach (len(dirnames), NumberinEach)
			for index2, subsubfol in enumerate(dirnames):
				pathsubfol = os.path.join(pathfol, subsubfol)

				filenames = []
				for root, dirs, files in walk(pathsubfol):
					filenames.extend(files)
					break
				fileNo = 0
				filenames = sorted(filenames)
				for onefile in filenames:

					if fileNo == max(NumberInEachSub, 1):
						#Time to move to next subFolder
						break

					filepath = os.path.join(pathsubfol, onefile)

					if not ".bmp" in filepath and not ".tiff" in filepath and not ".tif" in filepath:
						continue
					fileNo += 1
					outpath = outputdir.rstrip("/") + "/" + "strokes" +  folder.strip("black") + "/" + onefile + ".txt"
					print onefile
					if not os.path.exists(outpath) or filereuse == False:
						# print filepath
						MN.trial (filepath, outpath, sizes, rejects)
	sizes.close()