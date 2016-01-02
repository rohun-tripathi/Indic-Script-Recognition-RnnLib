#!/usr/bin/env python

import netcdf_helpers
from scipy import *
from optparse import OptionParser
import sys, time
import os
from xml.dom.minidom import parse

from os import walk

def location(path, function):
	datapath = path + "word_samples/" + function + "/"
	labelpath = path + "Label/" + function + "/"
	return labelpath, datapath

debug = False

#command line options
parser = OptionParser()

#parse command line options
(options, args) = parser.parse_args()
if (len(args)<1):
	print "usage: Test/Train/Val"
	sys.exit(2)

function = args [0]
if not function in ["Test",  "Train", "Val"]:
	print "usage: Test/Train/Val"
	sys.exit(2)


ncFilename = "combine" + function + ".nc"
path = "/home/riot/Videos/Student/"

topdir = []
for (dirpath, dirnames, filenames) in walk(path):
	topdir.extend(dirnames)
	break
if debug == True: print topdir

#later
# inputMeans = array([1054.11664783, 1455.79299719, 0.0196859027344])
# inputStds = array([413.688579765, 643.506710495, 0.138918565959])

labels =  set(['BA', 'DH', 'YA', 'DA', 'FA', 'JH', 'DW', 'HA', 'JA', 'DQ', 'LA', 'PZ', 'NA', 'TR', 'NZ', 'PA', 'RA', 'TH', 'LZ', 'TA', 'VA', 'CH', 'AE', 'EA', 'OM', 'CZ', 'EX', 'GA', 'KZ', 'AY', 'AX', 'SZ', 'KA', 'MA', 'UX', 'KH', 'OA', 'QA', 'SH', 'OX', 'QH', 'SA', 'UA', 'SE', 'MZ'])

seqDims = []
seqLengths = []
targetStrings = []
wordTargetStrings = []
seqTags = []
inputs = []

NoLabel = [] 
NoLabcnt = 0

#Now for inside each folder

#For now I have two sets. The first-> function = train and second function  = test. Later we can add more for val and so on
for folder in topdir[0:1]:
	pathtemp = path + str(folder) + "/"
	labelpath, datapath = location(pathtemp, function)
	if debug == True: print labelpath, datapath
	
	#Now in this folder we have word_samples and Label
	#We want to enter both together
	
	f = []
	for (dirpath, dirnames, filenames) in walk(datapath):
		f.extend(filenames)
		break
	if debug == True: print f

	for index, k in enumerate(f):
		data = datapath + k
		label = labelpath + k.strip(".pbm") + ".lab"	#Converting the name to account for the correct format
		
		onefile = k
		print onefile 			#This will always be printed, just to check the working and how far it got
		
		#Here is the code to extract the correct word and target strings for the word
		word = ""; 		wordmod = None		
		for line in open(label).readlines():
			wordmod = line.strip()
			chars = line.split()
			if wordmod != "":
				for char in chars:
					#labels.add( char.strip() )
					word += char.strip()
				break
				#There is a break here because only first line with info is to be considered
			else:
				print "There is a file for which the label entry is 0, that is - ", onefile
				print line
				print chars
				
		if word == "":
			NoLabel.append(onefile)
			NoLabcnt += 1
			continue
			#These are real problem cases
		#they are appended here as they have to be done for each stroke file
		seqTags.append(onefile)				#appending to seqtags
		wordTargetStrings.append(wordmod[:]) #For the instance in June4
		targetStrings.append(wordmod[:])

		firstlinechk = 0;
		#to make the first points have output 1.0 instead of 0.0
		oldlen = len(inputs)
		thirdval = 0.0
		for line in file(data).readlines():
			line= line.strip()
			coor = line.split()
			if debug == True : print line

			if len(coor) < 3:
				continue
				#The only way I know of dealing with trailing empty lines at the end :P
			if firstlinechk == 0:
				inputs.append([float(coor[0]), float(coor[1]), 1])
				if debug == True : print "inputted : ", float(coor[0]), float(coor[1]), 1
				firstlinechk = 1
			else:
				inputs.append([float(coor[0]), float(coor[1]), 0])
				if debug == True : print "inputted : ", float(coor[0]), float(coor[1]), 0
				if int (coor[2]) == 0:
					firstlinechk = 0
					
		seqLengths.append(len(inputs) - oldlen)
		seqDims.append([seqLengths[-1]])
		
		if debug == True: print "Input = " , inputs, "\n\n\n\n"
		if debug == True: print "Sequence lengths ", [seqLengths[-1]], "\n"
		if debug == True: print "wordTargetStrings == ", wordTargetStrings
		if debug == True: print "\n\n One iteration is over, check it out\n\n"
		if debug == True: break
	
		##and this is the point it shud stop inside the folder

#Later
#inputs = ((array(inputs)-inputMeans)/inputStds).tolist()

# print len(labels), labels

#create a new .nc file
file = netcdf_helpers.NetCDFFile(ncFilename, 'w')

#create the dimensions
netcdf_helpers.createNcDim(file,'numSeqs',len(seqLengths))
netcdf_helpers.createNcDim(file,'numTimesteps',len(inputs))
netcdf_helpers.createNcDim(file,'inputPattSize',len(inputs[0]))
netcdf_helpers.createNcDim(file,'numDims',1)
netcdf_helpers.createNcDim(file,'numLabels',len(labels))

#create the variables
netcdf_helpers.createNcStrings(file,'seqTags',seqTags,('numSeqs','maxSeqTagLength'),'sequence tags')
netcdf_helpers.createNcStrings(file,'labels',labels,('numLabels','maxLabelLength'),'labels')
netcdf_helpers.createNcStrings(file,'targetStrings',targetStrings,('numSeqs','maxTargStringLength'),'target strings')
netcdf_helpers.createNcStrings(file,'wordTargetStrings',wordTargetStrings,('numSeqs','maxWordTargStringLength'),'word target strings')
netcdf_helpers.createNcVar(file,'seqLengths',seqLengths,'i',('numSeqs',),'sequence lengths')
netcdf_helpers.createNcVar(file,'seqDims',seqDims,'i',('numSeqs','numDims'),'sequence dimensions')
netcdf_helpers.createNcVar(file,'inputs',inputs,'f',('numTimesteps','inputPattSize'),'input patterns')

#write the data to disk
print "closing file", ncFilename
file.close()

print "NoLabel == ", NoLabel
print "NoLabcnt == ", NoLabcnt