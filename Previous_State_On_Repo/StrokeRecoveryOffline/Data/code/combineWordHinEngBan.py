#!/usr/bin/env python

import netcdf_helpers
from scipy import *
from optparse import OptionParser
from xml.dom.minidom import parse
import sys, time, os

# import tamil_extract as TE
# import bangla_extract as BE

import hindi_extract as HE
import english_extract as EE
import engword_extract as EWE
import hinword_extract as HWE
import banword_extract as BWE

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

labels =  ["hindi", "english", "bangla"]

seqDims = []
seqLengths = []
targetStrings = []
wordTargetStrings = []
seqTags = []
inputs = []

#Here begins the module functional call for each of the respective indic scripts



inputhinword = []
HWE.main(function, labels, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputhinword, True)
inputMeans = array([ 43.5716277755 ,  72.728701988 ,  0.0151754027826 ])
inputStds = array([ 27.3972575236 ,  51.9577234449 ,  0.122250194 ]) 

inputhinword = ((array(inputhinword)-inputMeans)/inputStds).tolist()
inputs.extend(inputhinword)

inputbanword = []
BWE.main(function, labels, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputbanword, True)
inputMeans = array([ 39.3020429273 ,  64.3542876398 ,  0.0174984915094 ])
inputStds = array([ 24.220588125 ,  45.5887552493 ,  0.131119389505 ]) 

inputbanword = ((array(inputbanword)-inputMeans)/inputStds).tolist()
inputs.extend(inputbanword)

inputengword = []
EWE.main(function, labels, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputengword, True)
inputMeans = array([ 44.2994163835 ,  68.7957830052 ,  0.01821566173 ])
inputStds = array([ 24.4149708067 ,  70.159852713 ,  0.133730517825 ]) 


inputengword = ((array(inputengword)-inputMeans)/inputStds).tolist()
inputs.extend(inputengword)



# inputenglish = []
# EE.main(function, labels, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputenglish, True)
# inputMeans = array([ 21.5401437051 ,  19.095532646 ,  0.0197438300531 ])
# inputStds = array([ 15.2712299058 ,  14.35175744 ,  0.139118694746 ]) 
# inputenglish = ((array(inputenglish)-inputMeans)/inputStds).tolist()
# inputs.extend(inputenglish)


# inputhindi = []
# HE.main(function, labels, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputhindi, True)
# inputMeans = array([ 116.181545791 ,  117.589252273 ,  0.0311165710348 ])
# inputStds = array([ 95.3247873525 ,  86.246804645 ,  0.173632744728 ]) 

# inputhindi = ((array(inputhindi)-inputMeans)/inputStds).tolist()
# inputs.extend(inputhindi)



# inputbangla = []
# BE.main(function, labels, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputbangla, True)
# inputMeans = array([ 26.1452919339 ,  38.2040724491 ,  0.0170435369558 ])
# inputStds = array([ 19.3466051312 ,  23.8909551492 ,  0.129433592254 ]) 

# inputbangla = ((array(inputbangla)-inputMeans)/inputStds).tolist()
# inputs.extend(inputbangla)

# inputtamil = []
# TE.main(function, labels, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputtamil, True)
# inputMeans = array([ 57.8497793792 ,  78.1069514634 ,  0.00850420629953 ])
# inputStds = array([ 32.9270365136 ,  59.0435324226 ,  0.0918252948525 ]) 

# inputtamil = ((array(inputtamil)-inputMeans)/inputStds).tolist()
# inputs.extend(inputtamil)

# print inputs
# print len(labels), labels
# print labels

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
