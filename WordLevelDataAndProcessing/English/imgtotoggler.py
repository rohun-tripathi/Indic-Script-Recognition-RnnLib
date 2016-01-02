import os, sys, time
import toggler as TG
from os import walk

def FilesFromEach (num, MaxForthisFolder):
	if num == 0:
		print "The number of folders is zero somewhere. Exiting"
		sys.exit(0)
	return MaxForthisFolder / num

MaxFilesFromEachLang = 10000
#This is to be kept true whenever the format of data has not been changed. Then we will only ADD to the existing txt files
filereuse = True

dir = os.curdir;

folders = ['words']

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
			for onefile in filenames:

				if fileNo == max(NumberInEachSub, 1):
					#Time to move to next subFolder
					break

				filepath = os.path.join(pathsubfol, onefile)

				if not ".png" in filepath:
					#Not an image file
					continue
				fileNo += 1
				outpath = "ToggledDATA/file" + str(index1) + "_" + str(index2) + "_" + str(fileNo) + ".tiff"
				# if not os.path.exists(outpath) and filereuse == False:
				TG.imgtotoggle(filepath, outpath)
			
			
		