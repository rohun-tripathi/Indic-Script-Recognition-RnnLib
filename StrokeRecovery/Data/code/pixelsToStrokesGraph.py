import numpy as np
import sys,time
import math
import pprint as pp
from copy import deepcopy

#Update the lines values, for a point that has been traversed in a particular iteration of the algorithm
def updategraph(lentotal, x, y, lines, path, rejects):
	if not lines[x][y] == 0:
		print "Error in updategraph in graph. lines[x][y] != 0, Exiting\n\n\n"
		print "X,Y, value == ", x, y, lines[x][y]
		print "path -- ", path
		print >> rejects, path
		return [], False
	if lentotal > 2:
		lines[x][y] = 2
	else:
		lines[x][y] = -1
	return lines, True


#lookaround - scans neighbours and returns a list of all unvisited, valid neighbours and a list of surrounding visited functional points
#Our system actually just deals with one functional point neighbour but anyway returnning a list.
def lookaround(lines, rowindex, colindex, debug = False):
	normallist = []
	functlist = []
	totallist = []
	list1 = [-1,-1,-1,0,0,1,1,1]
	list2 = [-1,0,1,-1,1,-1,0,1]
	
	for l in range(8):
		if not lines[ rowindex + list1[l] ] [colindex + list2[l] ] == 1:
			
			totallist.append([rowindex + list1[l], colindex + list2[l]  ])

			if lines[ rowindex + list1[l] ] [colindex + list2[l] ] == 0:
				normallist.append([rowindex + list1[l], colindex + list2[l]  ])
			elif lines[ rowindex + list1[l] ] [colindex + list2[l] ] > 1:
				functlist.append([rowindex + list1[l], colindex + list2[l]  ])
	
	return totallist, normallist, functlist

#Checks is a point has already been visited
def AlreadyVisited(lines, term):
	if lines[ term[0] ][ term[1] ] == 0:
		return False #Not AlreadyVisited
	return True

#Increases the number of times a stroke led to junction. This is for the junctions that have already been traversed by another stroke.
#Thus only their value has to be increased, no addition to this particular stroke.
def IncreaseJunctionTouch(junction, lines):
	for term in junction:
		if lines[ term[0] ][ term[1] ] == 0:
			print "Error! In IncreaseJunctionTouch and the value to be increased is still zero"
		lines[ term[0] ][ term[1] ] += 1

###########
#Complements OtherEndPoints. The final points are arranged in ascending distance from top corner
def	appendtoOrder(lines, normal, order):
	k = orderEndPts(normal, [])					#WATCH THIS CHANGE
	
	k.extend(order)
	
	return k

############
#You could add a strategy to remove the smallest group of the endpoints
#The policy could be - Every endpoint that is at a distance lesser than the mean/2 of all the distances of all the endpoints to their respective closest functional points
#For now this function returns the list of end point along with information on its distance from the top corner and the distance from the nearest functional point
def orderEndPts(endPts, functionPts, debug = False):
	order = []
	for endpt in endPts:
		distancefromtopcorner, distancefromClosestFunctionalPt = DistEndpoints(endpt, functionPts)
		order.append([endpt[0], endpt[1], distancefromtopcorner, distancefromClosestFunctionalPt])

	order = sorted(order,key=lambda x: x[2])
	return order

def DistEndpoints(endpt, functionPts):
	val = 23434					#High Value, as it has to be substituted
	for functionalpt in functionPts:
		sqrt1 = np.sqrt( (endpt[0] - functionalpt[0]) * (endpt[0] - functionalpt[0]) + (endpt[1] - functionalpt[1]) * (endpt[1] - functionalpt[1]) )
		if sqrt1 < val:
			val = sqrt1
	distancefromtopcorner = np.sqrt(endpt[0]*endpt[0] + endpt[1]*endpt[1])
	return distancefromtopcorner, val

def CalculateRandomPoint(lines):
	randompoint = [0, 0]
	InitialDistance = 23435
	for rindex, line in enumerate(lines[1:-1]):
		for cindex, term in enumerate(line[1:-1]):
			if int(term) == 0:
				rowindex = rindex + 1		#Account for the offset from the boundary
				colindex = cindex + 1
				distancefromtopcorner, distancefromClosestFunctionalPt = DistEndpoints( [rowindex, colindex] , [] )
				if distancefromtopcorner < InitialDistance:
					randompoint = [rowindex, colindex]
					InitialDistance = distancefromtopcorner
	return randompoint, CalContinuity(randompoint[0], randompoint[1], 0, 0, 0)


##############
#Returns a list of junctionPts, end points, modifies the lines to remove spurious points and returns total number of points in image
def CalculateEndpoints(lines):

	functionPts = []
	endPts = []
	totalPts = 0
	randompoint = [0, 0]
	for rindex, line in enumerate(lines[1:-1]):
		for cindex, term in enumerate(line[1:-1]):
			if int(term) == 0:
				rowindex = rindex + 1		#Account for the offset from the boundary
				colindex = cindex + 1
				sum = sumneighbour(rowindex, colindex, lines)
				if sum == 0:			#spurious point
					lines[rowindex][colindex] = 1
					continue
				if sum == 1:
					#Endpoint
					endPts.append( [rowindex, colindex])
				if sum > 2:
					#functionPts.append( [rowindex, colindex, sum])
					functionPts.append( [rowindex, colindex])
				totalPts += 1

	return functionPts, endPts, lines, totalPts

def sumneighbour(rowindex, colindex, lines):
	list1 = [-1,-1,-1,0,0,1,1,1]
	list2 = [-1,0,1,-1,1,-1,0,1]
	sum = 8
	for l in range(8):
		sum -= lines[ rowindex + list1[l] ] [colindex + list2[l] ]
	return sum

def converttoint(text):
	complete = []
	for line in text.readlines():
		line = line.strip()
		
		coor = line.split()
		if not len(coor) >0: continue
		
		linebyline = []
		for term in line:
			linebyline.append( int(term) )
		complete.append(linebyline)
	return zeroOutCorner(complete)

def printing(printout, printtoouttext):
	if printout == []:
		pass
		#print "The printout came out blank. Nevertheless, continuing the evaluation."
	if len(printout) < 4:
		pass
		#print "The printout came out with only one term. Nevertheless, continuing the evaluation."
	else:
		printtoouttext.append( deepcopy(printout) )
	return printtoouttext, []

def finalprint(printtoouttext, outtext, cutatthird):
	for index,printout in  enumerate(printtoouttext):

		print >> outtext, ".PEN_DOWN"
		for term in printout:
			print >> outtext, term[0], term[1], 1
		print >> outtext, ".PEN_UP"
		
#Turns the boundary to 1
#Necessary for input data that sticks to the boundary
def zeroOutCorner(lines):

	for k in range( len(lines[0]) ):
		lines[0][k] = 1
		lines[-1][k] = 1

	for k in range( len(lines) ):
		lines[k][0] = 1
		lines[k][-1] = 1
	return lines

#Find the next term in the normal case of a point in the middle of a stroke and at the end. but not at a junction point
def nextTermNormal(normal, oldx, oldy, continuity, lines, debug = False):
	if debug == True: print "In nextTermNormal"
	continueflag = 0
	for term in normal: 										#There is only one possible way to go. One of the terms will be already visited.
		if AlreadyVisited(lines, term) == False:
			x = term[0]
			y = term[1]
			continueflag = 1
			continuity = CalContinuity(x, y, oldx, oldy, continuity)
			return 1, x, y , term, continuity
	
	return continueflag, -1, -1, -1, continuity 	 		#Same continuity returned, Might be not be useful tho

#Find the next term in the junction case of a point, at a junction point
def ChecknextTermJunction(pastvector, normal, oldx, oldy, continuity, lines, functionPts, functionPtsSlopes, printout, debug = False):
	
	if debug == True: print "In ChecknextTermJunction"
	
	for term in normal: 										#There is only one possible way to go. One of the terms will be already visited.
		if term == pastvector: continue
		if not term in functionPts: continue

		#Now I have the term. Time to work.
		num = functionPts.index(term)
		result = functionPtsSlopes[index]
		printout.append(term)

		k = printout[ max(-10 , -1 * len(printout)) : ]
		ArrayForSlope = [ k[len(k) - x - 1] for x in range( len(k) )]
		slope = slopeCalc(ArrayForSlope)

		val = 122323						#High Value
		chosen = None
		for term in result:
			if AlreadyVisited(lines , term[1]) == False:
				if abs( term[0] - slope) < val:
					chosen = term[1]
					val = abs( term[0] - slope)
		if not chosen == None:
			continuity = CalContinuity(chosen[0], chosen[1], oldx, oldy, continuity)
			return 1, chosen[0], chosen[1], chosen, continuity

	return -1, -1, -1, -1, -1

#Calculate the continuity equation, part of the continuity model for calculation
def CalContinuity(x, y, oldx, oldy, continuity):
	oldcontinuityratio = 0.6
	if continuity == 0:
		return math.degrees (math.atan( (float(y-oldy) + 0.01) / (float(x- oldx) + 0.01) ) )
	return oldcontinuityratio * continuity + (1 - oldcontinuityratio) * math.degrees( ( math.atan( (float(y-oldy) + 0.01) / (float(x- oldx) + 0.01) ) ) )

#Find the next term in the junction case of a point, at a junction point
def nextTermJunction(normal, oldx, oldy, continuity, lines, functionPts, functionPtsSlopes, printout, debug = False):
	
	if debug == True: print "In nextTermJunction"
	
	for index, k in enumerate(functionPts):
		
		if k == [oldx, oldy]:
			result = functionPtsSlopes[index]
		
			if len(printout) == 1:				#This means that the stroke has started from a junction point
				slope = CalContinuity(printout[0][0], printout[0][1], 0, 0, 0)			#DirectionFromTop
			else:
				k = printout[ max(-10 , -1 * len(printout)) : ]
				ArrayForSlope = [ k[len(k) - x - 1] for x in range( len(k) )]
				slope = slopeCalc(ArrayForSlope)

				# reverse = [ArrayForSlope[n] for n in range(len(ArrayForSlope)-1, -1, -1)]
				# slope = slopeCalc(reverse)

			val = 122323						#High Value
			chosen = None
			for term in result:
				if AlreadyVisited(lines , term[1]) == False:
					if abs( term[0] - slope) < val:
						chosen = term[1]
						val = abs( term[0] - slope)
			if chosen == None:
				if debug == True: print "Didn't find any stroke from this junction, x,y and lines val == ", oldx, oldy, lines[oldx][oldy]
				
				return -1, -1, -1, -1, -1 				#If it reached here, it is done, with no solution

				return 1, oldx, oldy, [oldx, oldy], CalContinuity(oldx, oldy, 0,0,continuity)
			else:
				continuity = CalContinuity(chosen[0], chosen[1], oldx, oldy, continuity)
				return 1, chosen[0], chosen[1], chosen, continuity

	return -1, -1, -1, -1, -1 				#If it reached here, it is done, with no solution

def SlopeForPoint(x, y, oldx, oldy, debug=False):
	
	return  (float(y-oldy) + 0.01) / (float(x- oldx) + 0.01)

def slopeCalc(pointslist, debug = False):
	sum = 0
	for index in range(1, len(pointslist)):
		continuity = SlopeForPoint(pointslist[index][0], pointslist[index][1], pointslist[index - 1][0], pointslist[index - 1][1])
		# print continuity, pointslist[index][0], pointslist[index][1], pointslist[index - 1][0], pointslist[index - 1][1]
		sum += continuity
	if debug == True : print pointslist

	continuity = SlopeForPoint(pointslist[-1][0], pointslist[-1][1], pointslist[0][0], pointslist[0][1])
	return continuity

	# return float(sum) / float(len(pointslist) - 1)


#When the order points have expired. This is used to retrieve any of the junction points that were untouched to start from those
# Logic : a point next to a junction point will aready have been covered by the order point inclusion it gets.
def expandUsingJunctions(lines, functionPts):
	for index, junc in enumerate(functionPts):
		if lines[junc[0]][junc[1]] == 0:
			return 1, junc[0] , junc[1]
	return -1, -1, -1;										#means there is no junction that is yet to be visited.

#Return the top term on the order list, which dictat= es the order in which the strokes have be started from
def getendpoints(order, lines, functionPts, debug = False):
	lenorder = (len(order))
	while 1:
		try:
			nextterm = order[0]
		except:
			break
		if debug == True: print "Next term from order == ", nextterm
		term = [ nextterm[0], nextterm[1] ]
		order.remove(nextterm)

		if AlreadyVisited(lines, term) == False:
			return nextterm, nextterm[0], nextterm[1], CalContinuity(nextterm[0], nextterm[1], 0, 0, 0)

	if debug == True: print "We have run out of Order Points."
	valid, x,y = expandUsingJunctions(lines, functionPts)		#If we get a -1 for x, means all junction points and endpoints are done. So we are done :D
	if valid == 1:
		return valid, x, y, CalContinuity(x, y, 0, 0, 0)
	else:
		return -1, -1, -1, -1
	
