#!/usr/bin/env python

import numpy

import CreateNCService as LE

noOfLangauges = 2
level = "Char"
dataSource = "Original"

if noOfLangauges == 2:
	labels =  ["hindi", "english"]
else:
	labels =  ["hindi", "bangla", "english"]

def cal(labelName):
	xterms = []
	yterms = []

	xrang = []
	yrang = []
	pendownterms = []
	iters = 0
	rang = 0

	LE.meancal(xterms, yterms, xrang, yrang, pendownterms,labelName, level, dataSource)
	
	xmean = numpy.mean(xterms)
	ymean = numpy.mean(yterms)
	pendownmean = numpy.mean(pendownterms)
	
	xvar = numpy.sqrt(numpy.var(xterms))
	yvar = numpy.sqrt(numpy.var(yterms))
	pendownvar = numpy.sqrt(numpy.var(pendownterms))

	print "For appending == "
	print "inputMeans = array([", xmean, ", ", ymean, ", ", pendownmean, "])"
	print "inputStds = array([", xvar, ", ", yvar, ", ", pendownvar, "])", "\n"

	print "iters = " , len(xterms)
	print "xmean = " , xmean
	print "ymean = " , ymean
	print "pendownmean = " , pendownmean

	print "xvar = " , xvar
	print "yvar = " , yvar
	print "penvar = " , pendownvar
	f1= open("details_test_"+labelName+"_"+level+"_"+dataSource+".txt", 'w')

	print >> f1, "iters = " , len(xterms)
	print >> f1, "xmean = " , xmean
	print >> f1, "ymean = " , ymean
	print >> f1, "pendownmean = " , pendownmean
	
	print >> f1, "xvar = " , xvar
	print >> f1, "yvar = " , yvar
	print >> f1, "penvar = " , pendownvar
	print >> f1, "For appending == "
	print >> f1, "inputMeans = array([", xmean, ", ", ymean, ", ", pendownmean, "])"
	print >> f1, "inputStds = array([", xvar, ", ", yvar, ", ", pendownvar, "])", "\n"

for label in labels:
	cal(label)