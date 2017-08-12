#Command to Use:
#Input a command like : python networkStateBackupCreator.py /media/riot/5127cd94-5f74-45d1-b6e9-d7aeb19bb1d9/IndicScriptRecogProject/charScriptRecog/TrainingInstances/Feb14/ /media/riot/5127cd94-5f74-45d1-b6e9-d7aeb19bb1d9/IndicScriptRecogProject/charScriptRecog/TrainingInstances/Feb14/networkBackupStates 2.5
#It will look for the last.save file in the Input folder and save it on the outputFolder


import os, sys, time, re, shutil
from os import walk
from optparse import OptionParser
from xml.dom.minidom import parse

def getDest(fileName, outputDir):
	return os.path.join(outputDir, time.strftime("%M_%H_%d_%m") + fileName)

inputDir = "/media/riot/5127cd94-5f74-45d1-b6e9-d7aeb19bb1d9/IndicScriptRecogProject/charScriptRecog/TrainingInstances/Feb14b/"
outputDir = "/media/riot/5127cd94-5f74-45d1-b6e9-d7aeb19bb1d9/IndicScriptRecogProject/charScriptRecog/TrainingInstances/Feb14b/networkBackupStates"
sleepTime = 30 * 60	#30 mins

debug = False

parser = OptionParser()
(options, args) = parser.parse_args()
if (len(args)<3):
	print "usage: inputDir outputDir epochTime (in minutes). Exiting"
	sys.exit(0)
else:
	inputDir = args[0]
	outputDir = args [1]
	sleepTime = float(args[2]) * 10 * 60

files = []
for r, d, f in walk(inputDir):
	files.extend(f)
	break;

if debug == True:
	print "files == ", files
for oneFile in files:
	if "last.save" not in oneFile:
		continue
	while (1):
		print "Copying file : ", oneFile
		
		destination = getDest(oneFile, outputDir)
		inputFile = os.path.join(inputDir, oneFile)
		shutil.copy(inputFile, destination)

		if debug == True:
			time.sleep(5)
		else:
			print "Off to sleep for sleepTime == ", sleepTime
			time.sleep(sleepTime)
			#time.sleep takes seconds as input.