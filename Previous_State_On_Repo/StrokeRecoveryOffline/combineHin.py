#!/usr/bin/env python

import netcdf_helpers
from scipy import *
from optparse import OptionParser
from xml.dom.minidom import parse
import sys, time, os

# import tamil_extract as TE
import bangla_extract as BE

import hindi_extract as HE
import english_extract as EE

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

labels =  ["hindi", "bangla"]

seqDims = []
seqLengths = []
targetStrings = []
wordTargetStrings = []
seqTags = []
inputs = []

# inputenglish = []
# EE.main(function, labels, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputenglish, True)

# inputMeans = array([ 20.3063709272 ,  18.1954686218 ,  0.0207776395543 ])
# inputStds = array([ 14.4594023607 ,  13.4718222236 ,  0.142639157488 ]) 

# inputenglish = ((array(inputenglish)-inputMeans)/inputStds).tolist()
# inputs.extend(inputenglish)


inputhindi = []
HE.main(function, labels, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputhindi, True)
inputMeans = array([ 115.204268789 ,  118.781161714 ,  0.0306033398908 ])
inputStds = array([ 94.3599554363 ,  86.7815331607 ,  0.172240458309 ]) 

inputhindi = ((array(inputhindi)-inputMeans)/inputStds).tolist()
inputs.extend(inputhindi)



inputbangla = []
BE.main(function, labels, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputbangla, True)
inputMeans = array([ 27.7758812741 ,  38.49031808 ,  0.0171472934505 ])
inputStds = array([ 20.952996415 ,  23.1016430872 ,  0.129820120851 ]) 
inputbangla = ((array(inputbangla)-inputMeans)/inputStds).tolist()
inputs.extend(inputbangla)

#create a new .nc file
ncFilename = "combine" + function + ".nc"
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
