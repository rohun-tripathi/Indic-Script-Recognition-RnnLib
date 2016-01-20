import sys, time, os
from os import walk

def dataShareToUse(NoFolders, function, labelName = ""):		#Separation of files for the train/test/val so on
	if labelName == "bangla":
		if function == "train":
			return 0, int(NoFolders * 10 / 11) 
		elif function == "test":					#This folder is all for testing
			return 0, NoFolders						#~100
	if labelName == "english":
		if function == "train":
			return 0, int(NoFolders * 10 / 11) 
		elif function == "test":					#This folder is all for testing
			return 0, NoFolders						#~100
	if labelName == "hindi":
		if function == "train":
			return 0, int(NoFolders * 10 / 11) 
		elif function == "test":					#This folder is all for testing
			return 0, NoFolders						#~100
		
def getPathName(labelName):
	defPath = "/media/riot/5127cd94-5f74-45d1-b6e9-d7aeb19bb1d9/DataSets/OfflineCharLevelStrokesRetrieved/"
	if labelName == "bangla":
		return defPath + "strokesBan/"
	if labelName == "english":
		return defPath + "strokesEng/"
	if labelName == "hindi":
		return defPath + "strokesHin/"

def main(function, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputs, labelName = "", debug = False):
	pathname = getPathName(labelName)

	print "pathname and LabelName == ", pathname, labelName
	time.sleep(2)

	f = []
	for (dirpath, dirnames,filenames) in walk(pathname):	
		f.extend(filenames)
		break
	start,end = dataShareToUse(len(f),function, labelName)
	print start, end

	for index, onefile in enumerate(f[start:end]):				#Running for each data file
		
		#Reason: There are files with no data for training. They are named usrX.txt and are to be avoided
		if not "txt" in onefile: continue

		if debug == True: print onefile
		
		word = labelName
		wordmod = labelName
		
		firstlinechk = 0 			# To make sure that the lines of code before the data lines are avoided when necessary
		oldlen = len(inputs)
		thirdval = 0.0

		AtleastsomeDataFlag = False

		k = open(pathname + onefile).readlines()
		for line in k:
			line = line.strip()
			parts = line.split()
			if len(parts) == 0: continue
			
			if firstlinechk == 0 and line != ".PEN_DOWN":		#Skip these lines as they donot have needed info
				continue
			elif line == ".PEN_DOWN":
				firstlinechk = 1 			#Nolonger the firstlines part, now all the information is relevant
				thirdval = 1.0 				#Stores the value for the third column of the first point in the stroke to signify "PENDOWN"
			elif line == ".PEN_UP":
				continue
			else:
				coor = line.split();
				inputs.append([float(coor[0]), float(coor[1]), thirdval])	#append the point to the others of this stroke
				thirdval = 0.0
				AtleastsomeDataFlag = True

		if 	AtleastsomeDataFlag == True:
			seqTags.append(onefile)#appending to seqtags
			wordTargetStrings.append(word)
			targetStrings.append(wordmod)
			seqLengths.append(len(inputs) - oldlen)
			seqDims.append([seqLengths[-1]])
			if debug == True: print "Sequence lengths ", [seqLengths[-1]], "\n"
			if seqLengths[-1] == 0:
				raw_input("The seqLengths for this instance is zero.\nThis should not have happened and will cause errors later (core dump while training).\nProceed with caution.")
		else:
			print onefile, " has no data at all\n"
		#here the iteration for this file ends

def meancal(xterms, yterms, xrang, yrang, pendownterms, labelName = "", debug = False):
	pathname = getPathName(labelName)

	f = []
	for (dirpath, dirnames,filenames) in walk(pathname):	
		f.extend(filenames)
		break#only one iteraion cause all lines are same
	for index, onefile in enumerate(f):				#Running for each data file
			
		#if debug == True: print onefile
		
		firstlinechk = 0 			# To make sure that the lines of code before the data lines are avoided when necessary
		thirdval = 0.0
		
		ymin = 50000
		xmin = 50000
		xmax = 0
		ymax = 0
		
		k = open(pathname + onefile).readlines()
		for line in k:
			line = line.strip()
			coor = line.split()
			if len(coor) == 0: continue
			
			if firstlinechk == 0 and line != ".PEN_DOWN":		#Skip these lines as they donot have needed info
				continue
			elif line == ".PEN_DOWN":
				firstlinechk = 1 			#Nolonger the firstlines part, now all the information is relevant
				thirdval = 1.0 				#Stores the value for the third column of the first point in the stroke to signify "PENDOWN"
			elif line == ".PEN_UP":
				continue
			else:
				xterms.append(float(coor[0]))
				yterms.append(float(coor[1]))	
				pendownterms.append(thirdval)

				if xmax < float(coor[0]): xmax = float(coor[0])
				if xmin > float(coor[0]): xmin = float(coor[0])

				if ymax < float(coor[1]): ymax = float(coor[1])
				if ymin > float(coor[1]): ymin = float(coor[1])

				thirdval = 0.0
		
		xrang.append( xmax - xmin )
		yrang.append( ymax - ymin )
		
		