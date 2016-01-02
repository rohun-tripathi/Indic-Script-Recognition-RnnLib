import sys, time, os
from os import walk

def unnecessaryfunc(d, function):		#Separation of files for the train/test/val so on
	if function == "train":
		return 0,90
	elif function == "test":
		return 90,110

def main(function, labels, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputs, debug = False):

	path = "/home/riot/Videos/scriptrecog/HinData/"
	topdir = []
	for (dirpath, dirnames, filenames) in walk(path):
		topdir.extend(dirnames)
		break
	if debug == True: print "Topdir = \n", topdir

	#For now I have two sets. The first-> function = train and second function  = test. Later we can add more for val and so on
	start,end = unnecessaryfunc(topdir,function)

	for k in topdir[start:end]:
		print "Directory == ", k
		pathname = path.rstrip("/") + "/" + k + "/"
		
		f = []
		for (dirpath, dirnames,filenames) in walk(pathname):	
			f.extend(filenames)
			break#only one iteraion cause all lines are same

		for onefile in f:				#Running for each data file
			seqTags.append(onefile)#appending to seqtags
			if debug == True: print onefile

			
			# Same for now
			word = "hindi"
			wordmod = "hindi"
			#they are appended here as they have to be done for each stroke file
			wordTargetStrings.append(word)
			targetStrings.append(wordmod)
				
			if ".txt" in onefile: continue
			
			firstlinechk = 0 			# To make sure that the lines of code before the data lines are avoided when necessary
			strokeline = []				#Will store the strokes in the data
			oldlen = len(inputs)
			thirdval = 0.0

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

			seqLengths.append(len(inputs) - oldlen)
			seqDims.append([seqLengths[-1]])
			if debug == True: print "Sequence lengths ", [seqLengths[-1]], "\n"
			##and this is the point it shud stop inside the folder

			##here the loop for the respective folder shud stop
			

			############################
			if index == 1:
				break
			#This to reduce the size of the file ryt now for easy check out