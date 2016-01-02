import netcdf_helpers
from scipy import *
from optparse import OptionParser
import sys, time, os
from xml.dom.minidom import parse
from os import walk

def dataShareToUse(NoFiles, function, Level):		#Separation of files for the train/test/val so on
	if Level == "Word": 
		if not function == "Test":
			print "usage of Level: Word only for testing"
			sys.exit(2)
		elif function == "Test":
			return 0, 475

	if function == "Train":
		return 0, int(NoFiles* 3/5) #~550 files
	elif function == "Test":
		return int(NoFiles* 3/5), int(NoFiles* 4/5)
	elif function == "Val":
		return int(NoFiles* 4/5), NoFiles

def getLabelWordFromFoldername(folderName, debug):
	tempFolderName = folderName.strip("txt")
	if debug == True: print tempFolderName, tempFolderName.strip("Word")
	return tempFolderName.strip("Word")

def checkLevel(Level):
	if not Level in ["Word", "Char"]:
		print "usage of Level: Word/Char"
		sys.exit(2)

def getDir(Level, debug):
	if Level == "Word":
		dir = "/media/riot/5127cd94-5f74-45d1-b6e9-d7aeb19bb1d9/SimpleOffline/MBFeatures/Word"
	else:
		dir = "/media/riot/5127cd94-5f74-45d1-b6e9-d7aeb19bb1d9/SimpleOffline/MBFeatures/Char"
	topdir = []
	for (dirpath, dirnames, filenames) in walk(dir):
		topdir.extend(dirnames)
		break
	if debug == True: print topdir
	return dir, topdir
	
def getFunctionToBeExecuted():
	parser = OptionParser()
	(options, args) = parser.parse_args()
	if (len(args)<1):
		print "usage: Test/Train/Val"
		sys.exit(2)
	if not args [0] in ["Test",  "Train", "Val"]:
		print "usage: Test/Train/Val"
		sys.exit(2)
	return args[0]

def getNCFilename(Level, labels, function):
	labelString = ""
	for label in labels:
		labelString += label
	return "Dat" + function + Level + labelString + time.strftime("%d_%m") + ".nc"


Level = "Word"
debug = True

checkLevel(Level)
function = getFunctionToBeExecuted()
labels =  set(['Eng', 'Hin', 'Ban'])
ncFilename = getNCFilename(Level, labels, function)
dir, topdir = getDir(Level, debug)

if debug == True:
	print dir, topdir, ncFilename, function, Level

seqDims = []
seqLengths = []
targetStrings = []
wordTargetStrings = []
seqTags = []
inputs = []

for folder in topdir:
	pathtemp = os.path.join(dir,folder)
	
	f = []
	for (dirpath, dirnames, filenames) in walk(pathtemp):
		f.extend(filenames)
		break
	
	start, end = dataShareToUse( len(f) , function, Level)

	for index, onefile in enumerate(f[start:end]):
		filepath = os.path.join(pathtemp,onefile)

		word = getLabelWordFromFoldername(folder, debug)
		wordmod = word
		
		oldlen = len(inputs)
		
		for line in file(filepath).readlines():
			line = line.strip()
			coor = line.split()
			if len(coor) < 1: continue
			inputs.append(coor)
		
		seqLengths.append(len(inputs) - oldlen)
		seqDims.append([seqLengths[-1]])
		seqTags.append(word+"/"+onefile)
		wordTargetStrings.append(word) 
		targetStrings.append(wordmod)
		print word+"/"+onefile + "\n"

file = netcdf_helpers.NetCDFFile(ncFilename, 'w')
print shape(inputs)
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
