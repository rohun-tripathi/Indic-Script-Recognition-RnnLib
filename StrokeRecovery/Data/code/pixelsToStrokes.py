#junction points == function points == junctions = functionPts and so on
import sys,time, os, math
import pixelsToStrokesGraph as GR
import txtcreator as IMTXT
import pprint as pp
from copy import deepcopy
import pixelsToStrokesView as VW


def ConvertToResult(SlopeList, StartList):
	result = [ [] for x in range( len(StartList) )]
	for cnt in range( len(StartList) ):
		for k, m in zip( SlopeList[cnt], StartList[cnt]) :
			result[cnt].append( [ k, m ] )
	return result

def AddToResult(SlopeList, StartList, totalList, index, pointslist):
	startOfStroke = pointslist[1]
	if not startOfStroke in StartList[index]:
		StartList[index].append(pointslist[1])
		SlopeList[index].append( GR.slopeCalc(pointslist) )
		totalList.append( pointslist[:] )
	return SlopeList, StartList, totalList

def FirstPart(lines, functionPts, SlopeTakingPointsLimit, MinLengthPermitted, SlopeList, StartList):
	totalList = []
	for index, junction in enumerate(functionPts):					#For each junction Point
		
		t, normal, j = GR.lookaround(lines, junction[0], junction[1])			#Calculate the Neighbours
		
		skiplist = deepcopy(normal)									#Points to be skipped in middle of trace. Immediate Neighbours
		
		for term in normal:											#Starting up for each neighbour
			pointslist = [ [junction[0] , junction[1] ] ] 			#This Should be done every time, for slope calc

			for count in range(SlopeTakingPointsLimit):				#How long should the length of the slope be? set it to 5
				pointslist.append(term[:])
				
				t, subnormal, j = GR.lookaround(lines, term[0], term[1])		#Moving to next object
				
				if len(subnormal) == 2:  			 				#This is the ideal case, if it is going away, from the junction
					for tempterm in subnormal:
						if not tempterm in pointslist and not tempterm in skiplist:
							term = tempterm[:]
							continue
				elif len(subnormal) == 1 or len(subnormal) > 2: break 			#We are done on this pointslist
			
			if len(pointslist) > MinLengthPermitted:
				SlopeList, StartList, totalList = AddToResult(SlopeList, StartList, totalList, index, pointslist)

	return SlopeList, StartList, totalList

def AddToLists(SlopeList, StartList, index, slope, value):
	SlopeList[index].append(slope)
	StartList[index].append(value[:])

	return SlopeList, StartList

def LoopyPart(lines, functionPts, JunctionPointDistLimit, MinLengthPermitted, SlopeList, StartList):

	for index, junction in enumerate(functionPts):					#For each junction Point
		
		t, normal, j = GR.lookaround(lines, junction[0], junction[1])			#Calculate the Neighbours
		
		skiplist = deepcopy(normal)									#Points to be skipped in middle of trace. Immediate Neighbours
		
		for term in normal:											#Starting up for each neighbour
			if not term in functionPts: continue
			num = functionPts.index(term)

			for slope, value in zip( SlopeList[num], StartList[num]):
				if value in StartList[index]: continue
				if value in skiplist: continue
				if value == junction: continue

				SlopeList, StartList = AddToLists(SlopeList, StartList, index, slope, value)
	return SlopeList, StartList

#skiplist is the list of terms that don't have to discussed in the calculations
def CalFPSlopes(lines, functionPts):
	
	SlopeTakingPointsLimit = 10
	JunctionPointDistLimit = 1
	MinLengthPermitted = 3
	#For each val in FunctionPts, I have to return a list of slopes, along with a list of the starting points on those slopes.
	
	SlopeList = [ [] for x in range( len(functionPts) )]
	StartList = [ [] for x in range( len(functionPts) )]
	
	SlopeList, StartList, totalList = FirstPart(lines, functionPts, SlopeTakingPointsLimit, MinLengthPermitted, SlopeList, StartList)

	#Now for the looring part
	for loopycnt in range(3):
		SlopeList, StartList = LoopyPart(lines, functionPts, JunctionPointDistLimit, MinLengthPermitted, SlopeList, StartList)	

	result = ConvertToResult(SlopeList, StartList)
	return result, totalList


def trial(path, strokepath, k, rejects, debug = False):
	outpath = "abc.txt"
	#outpath = strokepath.strip(".txt") + "_stroke.txt"					#temppath
	IMTXT.imgtotxt (path, outpath, k)
	text = open(outpath, "r")
	
	lines = GR.converttoint(text)			#lines is 2D int array, with boundary values == 1
	functionPts, endPts, lines, totalPts = GR.CalculateEndpoints(lines)		#correct. Checked
	order = GR.orderEndPts(endPts, functionPts)
	covered = 0
	
	functionPtsSlopes, totalList = CalFPSlopes(deepcopy(lines), functionPts)

	term, x, y, continuity = GR.getendpoints(order, lines, functionPts)
	if term == -1:
		randompoint, randompointContinuity = GR.CalculateRandomPoint(lines)
		x = randompoint[0]
		y = randompoint[1]
		continuity = randompointContinuity
		term = randompoint[:]
	
	printtoouttext = []
	printout = []
	DoNotPrintAnyData = False

	pastlist = []

	cutatthird = 1

	while 1:

		covered += 1 					#tracks the number of text points covered in the image
		printout.append([x,y])
		pastlist.append([x,y])
		# print x,y
		# # if (x,y) in [(35,1)]: debug = True
		# else: debug = False

		total, normal, junction = GR.lookaround(lines, x, y)
		if debug == True: print "total, normal, junction == ",  total, normal, junction


		lines, valid = GR.updategraph(len(total), x, y, lines, path, rejects)
		if valid == False:
			DoNotPrintAnyData = True
			break

		if len(total) > 2:			#Junction
			continueflag, x, y, term, continuity = GR.nextTermJunction(normal, x, y, continuity, lines, functionPts, functionPtsSlopes, printout, False)
			order = GR.appendtoOrder(lines, normal, order)	#Only the points around the Junction that are left over are appended to order. In priority
			for onelist in totalList:
				if onelist[1] == [x,y]:
					covered += 1 
					printout.append([x,y])
					pastlist.append([x,y])
					lines, valid = GR.updategraph(2, x, y, lines,path, rejects)
					if valid == False:
						DoNotPrintAnyData = True
						break

					x = onelist[2][0]
					y = onelist[2][1]

					break
		else:
			continueflag, x, y, term, continuity = GR.nextTermNormal(normal,x, y ,continuity, lines,  debug)
			if continueflag == -1:
				continueflag, x, y, term, continuity = GR.ChecknextTermJunction(pastlist[-2], normal, oldx, oldy, continuity, lines, functionPts, functionPtsSlopes, printout)
		
		if continueflag == 1: continue
			
		#If we reached here, that means that the path has hit a stop, possibly at an endpoint or a junction point #Checking the Junction POint theory
		printtoouttext , printout = GR.printing(printout, printtoouttext);							#Later we will implement a better model
		if len(junction) > 0:
			GR.IncreaseJunctionTouch(junction, lines)
			#I could try and start from a point around the junction, even it has been visited, when another stroke reaches here
			#There are two optimizations left. This and the one improving continuity

		if covered == totalPts- len(functionPts):
			if debug == True: print "Atleast totalPts - len(functionPts) == ", totalPts- len(functionPts), " are covered." 
			break
		term, x, y, continuity = GR.getendpoints(order, lines, functionPts)
		if debug == True: print "Ordesmbedbhjr == ", order
		if debug == True: print "Total points have not been covered, so next term from the endpoints == ", term

		if term == -1: break
		else: continue
	
	if covered >= totalPts- len(functionPts):
		if debug == True:print "Atleast totalPts - len(functionPts) == ", totalPts- len(functionPts), " are covered." 
		#pp.pprint(lines)
	if DoNotPrintAnyData == False:
		print "here"
		outtext = open(strokepath, "w")
		GR.finalprint(printtoouttext, outtext,cutatthird)
		outtext.close()
		
		#VW.mainview(strokepath)

	text.close()

# filename = "file0_0_1.tif"

# sizes = open("AAtempsizes.txt", "w")
# rejects = open("AAtemprejects.txt", "w")
# trial(filename, filename.rstrip(".tif") + "_stroke.txt", sizes, rejects )