#!/usr/bin/env python

import sys, time, os, numpy
from optparse import OptionParser

# import tamil_extract as TE
# import bangla_extract as BE

import hindi_extract as HE
import english_extract as EE

import engword_extract as EWE
import hinword_extract as HWE
import banword_extract as BWE

def cal():
	f1= open("details_test.txt", 'w')
		
	#for name in ["EngWord", "tamil", "hindi", "bangla", "english"]:
	for name in ["HinWord", "EngWord", "BanWord"]:
		xterms = []
		yterms = []

		xrang = []
		yrang = []
		pendownterms = []
		iters = 0
		rang = 0
		if name == "BanWord":
			BWE.meancal(xterms, yterms, xrang, yrang, pendownterms)
		elif name == "HinWord":
			HWE.meancal(xterms, yterms, xrang, yrang, pendownterms)
		elif name == "EngWord":
			EWE.meancal(xterms, yterms, xrang, yrang, pendownterms)
		elif name == "hindi":
			HE.meancal(xterms, yterms, xrang, yrang, pendownterms)
		elif name == "english":
			EE.meancal(xterms, yterms, xrang, yrang, pendownterms)
		else:
			print "Language out of scope "
			print name
			sys.exit(1)

		print "\n\n",name, "\n\n"
		print >> f1, "\n\n",name, "\n\n"

		xmean = numpy.mean(xterms)
		ymean = numpy.mean(yterms)
		pendownmean = numpy.mean(pendownterms)
		#this is because our system is diff from the one created by the example python code
		
		xvar = numpy.sqrt(numpy.var(xterms))
		yvar = numpy.sqrt(numpy.var(yterms))
		pendownvar = numpy.sqrt(numpy.var(pendownterms))

		print "inputMeans = array([", xmean, ", ", ymean, ", ", pendownmean, "])"
		print "inputStds = array([", xvar, ", ", yvar, ", ", pendownvar, "])", "\n"
		print >> f1, "For appending == ", "inputMeans = array([", xmean, ", ", ymean, ", ", pendownmean, "])"
		print >> f1, "For appending == ", "inputStds = array([", xvar, ", ", yvar, ", ", pendownvar, "])"
	
		print "iters = " , len(xterms)
		print "xmean = " , xmean
		print "ymean = " , ymean
		print "pendownmean = " , pendownmean
		print "xvar = " , xvar
		print "yvar = " , yvar
		print "penvar = " , pendownvar

		print >> f1, "iters = " , len(xterms)
		print >> f1, "xmean = " , xmean
		print >> f1, "ymean = " , ymean
		print >> f1, "pendownmean = " , pendownmean
		print >> f1, "xvar = " , xvar
		print >> f1, "yvar = " , yvar
		print >> f1, "penvar = " , pendownvar
	

cal()