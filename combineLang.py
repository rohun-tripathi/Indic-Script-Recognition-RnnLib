#!/usr/bin/env python

import netcdf_helpers
from scipy import *
from optparse import OptionParser
from xml.dom.minidom import parse
import sys, time, os

import CreateNCService as LE

def getNCFilename(level, labels, function, dataSource):
	labelString = ""
	for label in labels:
		labelString += label
	return "Data" + function + level + dataSource + labelString + time.strftime("%d_%m") + ".nc"


labels =  ["hindi", "bangla", "english"]
level = "Word"
dataSource = "StrokeRecov"

#command line options
parser = OptionParser()
(options, args) = parser.parse_args()
if (len(args)<1):
	print "usage: test/train/val"
	sys.exit(2)
function = args [0]
if not function in ["test",  "train", "val"]:
	print "usage: test/train/val"
	sys.exit(2)

seqDims = []
seqLengths = []
targetStrings = []
wordTargetStrings = []
seqTags = []
inputs = []

for label in labels:
	inputlanguage = []
	inputMeans, inputStds = LE.main(function, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputlanguage, label, level, dataSource, False)
	inputlanguage = ((array(inputlanguage)-inputMeans)/inputStds).tolist()
	inputs.extend(inputlanguage)

#create a new .nc file
ncFilename = getNCFilename(level, labels, function, dataSource)
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
