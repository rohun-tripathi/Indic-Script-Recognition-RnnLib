import sys, time, os, numpy
from optparse import OptionParser

import code.lang_extract_recStrokes as LE

def cal():
	f1 = open("details_mean_lang" + ".txt", 'w')
	
	for label in ["bangla", "english", "hindi"]:
		xterms = []
		yterms = []
		xrang = []
		yrang = []
		pendownterms = []
		iters = 0
		rang = 0

		LE.meancal(xterms, yterms, xrang, yrang, pendownterms, label)
		
		xmean = numpy.mean(xterms)
		ymean = numpy.mean(yterms)
		pendownmean = numpy.mean(pendownterms)
		xvar = numpy.sqrt(numpy.var(xterms))
		yvar = numpy.sqrt(numpy.var(yterms))
		pendownvar = numpy.sqrt(numpy.var(pendownterms))

		print "if label == \"" + label + "\":"
		print >> f1, "\n\n", label, "\n\n"
		
		print "inputMeans = array([", xmean, ", ", ymean, ", ", pendownmean, "])"
		print "inputStds = array([", xvar, ", ", yvar, ", ", pendownvar, "])"
		print >> f1, "For appending == ", "inputMeans = array([", xmean, ", ", ymean, ", ", pendownmean, "])"
		print >> f1, "For appending == ", "inputStds = array([", xvar, ", ", yvar, ", ", pendownvar, "])"
	
		#print "iters = " , len(xterms)
		print >> f1, "iters = " , len(xterms), "\n"
		f1.close()
cal()
