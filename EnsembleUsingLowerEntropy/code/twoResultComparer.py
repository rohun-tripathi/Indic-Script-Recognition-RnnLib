import linecache as lc
import Classification
import sys, re, math

SPACE = " "
EMPTY = ""
labelMap = dict()
debug = False;
#Sorting free solution

class ClassificationObject(object):
    tag = ""
    prediction = -1
    confidence = -1
    def __init__(self, tag="Unknown name", prediction = -1, confidence = -1):
        self.tag = tag
        self.prediction = prediction
        self.confidence = confidence

    def getTag(self):
    	return self.tag

def readAndGetResult(fileName):
	result = []
	for rowIndex, row in enumerate(open(fileName, "r").readlines()):
		if row.strip() != "data sequence:":
			continue
		tagLine = lc.getline(fileName, rowIndex + 4)
		errorLine = lc.getline(fileName, rowIndex + 9)
		errorTags = errorLine.strip().split(SPACE)
		if int(errorTags[1]) == 1:
			crossEntropyLine = lc.getline(fileName, rowIndex + 12)
		elif int(errorTags[1]) == 0:
			crossEntropyLine = lc.getline(fileName, rowIndex + 11)
		label = retrieveLabel(errorLine)
		classification = ClassificationObject(retrieveTag(tagLine, label), errorTags[1], retrieveConf(crossEntropyLine))
		result.append(classification)
	return sorted(result, key=getTag)

def getTag(classification):
	return classification.tag

def retrieveTag(tagLine, label):
	tokensToRemove = [".txt", ".tif", "Eng/", "Hin/", SPACE]
	parts = tagLine.split()
	for token in tokensToRemove:
		parts[2] = parts[2].strip().replace(token,EMPTY)
	return label + "_" + parts[2]

def retrieveLabel(errorLine):
	parts = errorLine.split()
	label = parts[0].replace("_",EMPTY).strip()
	if label in labelMap:
		return labelMap.get(label)
	return label

def retrieveConf(crossEntropyLine):
	parts = crossEntropyLine.split()
	return parts[1].strip()

def calculateOppConfidence(x):
	eRaisedToMinusX = math.exp(-1 * float(x))
	return -1 * math.log(1 - eRaisedToMinusX)

def validateLists(list1, list2):
	if len(list1) == 0 or len(list2)== 0:
		print "One of the Lists has length zero, list1 and list 2 == ", list1, list2
		sys.exit()

def finishIteration(counter1, counter2):
	return counter1 + 1, counter2 + 1

def updateResult(predictions, firstClassification, secondClassification):
	if firstClassification.prediction == secondClassification.prediction:
		predictions.append(int(firstClassification.prediction))
		if debug ==True:
			print "firstClass == ", firstClassification.tag
			print "secondClass == ", secondClassification.tag
			print predictions
			raw_input()
		return
	if int(firstClassification.prediction) == 0:
		correct = float(firstClassification.confidence)
		inCorrect = float(secondClassification.confidence)
	else:
		correct = float(secondClassification.confidence)
		inCorrect = float(firstClassification.confidence)
	
	oppConfiddence = calculateOppConfidence(inCorrect)
	print correct, oppConfiddence
	if correct < oppConfiddence:
		predictions.append(0)
	else :
		predictions.append(1)
	if debug ==True:
		print "firstClass == ", firstClassification.tag
		print "secondClass == ", secondClassification.tag
		print correct, oppConfiddence
		print predictions
		raw_input()

def main(firstFile, secondFile):
	initialize()
	missAndFail = open("miss_" + firstFile + "_" + secondFile + ".txt", "w")

	sortedResultFirst = readAndGetResult(firstFile);
	sortedResultSecond = readAndGetResult(secondFile)
	
	validateLists(sortedResultFirst, sortedResultSecond)
	lenFirst = 0
	lenSecond = 0

	# filesList = open("lsi","w")

	predictions=[]
	while(withinLimit(lenFirst, lenSecond, sortedResultFirst, sortedResultSecond)):
		# print >> filesList, "file : ", sortedResultFirst[lenFirst].getTag(), "\t\t", sortedResultSecond[lenSecond].getTag()
		# lenFirst, lenSecond = finishIteration(lenFirst, lenSecond)
		# continue
		if(sortedResultFirst[lenFirst].getTag() == sortedResultSecond[lenSecond].getTag()):
			updateResult(predictions, sortedResultFirst[lenFirst], sortedResultSecond[lenSecond])
			lenFirst, lenSecond = finishIteration(lenFirst, lenSecond)

		else:
			print >> missAndFail, "Missed for : ", sortedResultFirst[lenFirst].getTag(), "\t\t", sortedResultSecond[lenSecond].getTag()
			lenFirst, lenSecond = incrementLongerCounter(lenFirst, lenSecond, sortedResultFirst, sortedResultSecond)
			if(sortedResultFirst[lenFirst].getTag() == sortedResultSecond[lenSecond].getTag()):
				updateResult(predictions, sortedResultFirst[lenFirst], sortedResultSecond[lenSecond])
				lenFirst, lenSecond = finishIteration(lenFirst, lenSecond)
			else:
				while (sortedResultFirst[lenFirst].getTag() != sortedResultSecond[lenSecond].getTag()):
					lenFirst, lenSecond = incrementLongerCounter(lenFirst, lenSecond, sortedResultFirst, sortedResultSecond)
					if(sortedResultFirst[lenFirst].getTag() == sortedResultSecond[lenSecond].getTag()):
						updateResult(predictions, sortedResultFirst[lenFirst], sortedResultSecond[lenSecond])
						lenFirst, lenSecond = finishIteration(lenFirst, lenSecond)
			# else:
			# 	#If it comes here, means it missed twice.
			# 	print >> missAndFail, "Major Miss for : ", sortedResultFirst[lenFirst].getTag(), "\t\t", sortedResultSecond[lenSecond].getTag()
			# 	print "Major Miss for : ", sortedResultFirst[lenFirst].getTag(), "\t\t", sortedResultSecond[lenSecond].getTag()
			# 	sys.exit()

	finalResult = open("resultFor_" + firstFile + "_" + secondFile + ".txt", "w")
	printResult(predictions, finalResult)
	#printResultForEach(sortedResultFirst, sortedResultSecond)

def printResult(prediction, finalResult):
	total ,correct, accuracy = calculateResults(prediction)
	if total == 0:
		print "total == 0. How?"
		sys.exit()

	print "\nTotal inputs Classified == ", total
	print "\nInputs Correctly classified == ", correct
	print "\nAccuracy == ", accuracy, "\n"
	print >> finalResult, "Total inputs Classified == ", total
	print >> finalResult, "Inputs Correctly classified == ", correct
	print >> finalResult, "Accuracy == ", accuracy

def calculateResults(prediction):
	return len(prediction), len(prediction) - getSum(prediction), float(len(prediction) - getSum(prediction))/float(len(prediction))

def getSum(list1):
	value = 0
	for term in list1:
		value += int(term)
	return value

def initialize():
	labelMap["Eng"] = "english"
	labelMap["Hin"] = "hindi"

def withinLimit(lenFirst, lenSecond, list1, list2):
	if lenFirst < len(list1) and lenSecond < len(list2):
		return True
	return False

def incrementLongerCounter(lenFirst, lenSecond, list1, list2):
	if len(list1) > len(list2):
		return lenFirst + 1, lenSecond
	elif len(list2) > len(list1):
		return lenFirst, lenSecond + 1
	else:
		return lenFirst + 1, lenSecond + 1