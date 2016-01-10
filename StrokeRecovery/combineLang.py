#!/usr/bin/env python

import netcdf_helpers
from scipy import *
from optparse import OptionParser
from xml.dom.minidom import parse
import sys, time, os

import code.lang_extract_recStrokes as LE

def getNCFilename(Level, labels, function):
	labelString = ""
	for label in labels:
		labelString += label
	return "Data" + function + Level + labelString + time.strftime("%d_%m") + ".nc"

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

labels =  ["hindi", "bangla", "english"]
Level = "Char"

seqDims = []
seqLengths = []
targetStrings = []
wordTargetStrings = []
seqTags = []
inputs = []

for label in labels:

	if label == "bangla":
		inputMeans = array([ 29.9574801796 ,  39.3277184539 ,  0.0171024643878 ])
		inputStds = array([ 21.682325964 ,  23.5297621524 ,  0.129653268758 ])
	elif label == "english":
		inputMeans = array([ 20.1197738962 ,  18.102001324 ,  0.0201660131385 ])
		inputStds = array([ 14.078078879 ,  13.190027056 ,  0.140567937498 ])
	elif label == "hindi":
		continue
		inputMeans = array([ 131.496914426 ,  134.551279828 ,  0.0062047164797 ])
		inputStds = array([ 96.342533732 ,  90.7312127862 ,  0.0785252696468 ])
 
	inputlanguage = []
	LE.main(function, labels, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputlanguage, label, False)
	inputlanguage = ((array(inputlanguage)-inputMeans)/inputStds).tolist()
	inputs.extend(inputlanguage)

#create a new .nc file
ncFilename = getNCFilename(Level, labels, function)
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
