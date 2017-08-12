from scipy import *

DATASET_HOME = "/media/riot/5127cd94-5f74-45d1-b6e9-d7aeb19bb1d9/versions_of_projects/scriptRepo_DataSets/"

def getPathName(labelName, level, dataSource):
	if dataSource == "Original":
		return getPathNameForOriginal(labelName, level)
	else:
		return getPathNameForStrRecov(labelName, level)

def getPathNameForOriginal(labelName, level):
	if level == "Char":
		return getPathNameForCharForOriginal(labelName)
	else:
		return getPathNameForWordForOriginal(labelName)

def getPathNameForStrRecov(labelName, level):
	if level == "Char":
		return getPathNameForCharForStrRecov(labelName)
	else:
		return getPathNameForWordForStrRecov(labelName)

def getPathNameForCharForOriginal(labelName):
	#Done
	defPath = DATASET_HOME + "OnlineCharLevel/"
	if labelName == "bangla":
		pathName = defPath + "DataBan/"
		inputMeans = array([ 653.324493254 ,  709.853922885 ,  0.0312360125328 ])
		inputStds = array([ 278.299333669 ,  200.679098723 ,  0.173954948346 ]) 
	if labelName == "english":
		pathName = defPath + "DataEng/"
		inputMeans = array([ 325.727175665 ,  388.192835692 ,  0.0201181255074 ])
		inputStds = array([ 91.9722164008 ,  76.7254244735 ,  0.140404367928 ]) 
	if labelName == "hindi":
		pathName = defPath + "DataHin/"
		inputMeans = array([ 5356.81911165 ,  3673.50562983 ,  0.0317493008247 ])
		inputStds = array([ 2505.79381351 ,  2112.95077319 ,  0.17533192157 ]) 
	return pathName, inputMeans, inputStds

def getPathNameForWordForOriginal(labelName):
	#Done
	defPath = DATASET_HOME + "OnlineWordLevel/"
	if labelName == "bangla":
		pathName = defPath + "txtBanWord/"
		inputMeans = array([ 41.6739496193 ,  92.1837437729 ,  0.02120500047 ])
		inputStds = array([ 24.9476536852 ,  58.9613775415 ,  0.144067166367 ]) 
	if labelName == "english":
		pathName = defPath + "txtEngWord/"
		inputMeans = array([ 3280.09081913 ,  3525.5072691 ,  0.0396606079223 ])
		inputStds = array([ 1451.50131834 ,  1704.37143443 ,  0.195160559796 ])
	if labelName == "hindi":
		pathName = defPath + "txtHinWord/"
		inputMeans = array([ 5373.91794672 ,  3464.31656682 ,  0.0315004541232 ])
		inputStds = array([ 2844.88270614 ,  2047.47960179 ,  0.174665896814 ])
	return pathName, inputMeans, inputStds
	
def getPathNameForCharForStrRecov(labelName):
	
	defPath = DATASET_HOME + "OfflineCharLevelStrokesRetrieved/"
	if labelName == "bangla":
		pathName = defPath + "strokesBan/"
		inputMeans = array([ 29.9574801796 ,  39.3277184539 ,  0.0171024643878 ])
		inputStds = array([ 21.682325964 ,  23.5297621524 ,  0.129653268758 ])
	if labelName == "english":
		pathName = defPath + "strokesEng/"
		inputMeans = array([ 20.1197738962 ,  18.102001324 ,  0.0201660131385 ])
		inputStds = array([ 14.078078879 ,  13.190027056 ,  0.140567937498 ])
	if labelName == "hindi":
		pathName = defPath + "strokesHin/"
		inputMeans = array([ 131.496914426 ,  134.551279828 ,  0.0062047164797 ])
		inputStds = array([ 96.342533732 ,  90.7312127862 ,  0.0785252696468 ])
	return pathName, inputMeans, inputStds

def getPathNameForWordForStrRecov(labelName):
	#Done
	defPath = DATASET_HOME + "OfflineWordLevelStrokesRetrieved/"
	if labelName == "bangla":
		pathName = defPath + "strokesBanWord/"
		inputMeans = array([ 39.3020429273 ,  64.3542876398 ,  0.0174984915094 ])
		inputStds = array([ 24.220588125 ,  45.5887552493 ,  0.131119389505 ])
	if labelName == "english":
		pathName = defPath + "strokesEngWord/"
		inputMeans = array([ 44.2994163835 ,  68.7957830052 ,  0.01821566173 ])
		inputStds = array([ 24.4149708067 ,  70.159852713 ,  0.133730517825 ])
	if labelName == "hindi":
		pathName = defPath + "strokesHinWord/"
		inputMeans = array([ 43.5716277755 ,  72.728701988 ,  0.0151754027826 ])
		inputStds = array([ 27.3972575236 ,  51.9577234449 ,  0.122250194 ])
	return pathName, inputMeans, inputStds

#######DataShare#######

def dataShareToUseForStrokeRecovForChar(NoFolders, function, labelName):		#Separation of files for the train/test/val so on
	#Done
	if labelName == "bangla":
		if function == "train":
			return 0, int(NoFolders * 10 / 11) 
		elif function == "test":					#This folder is all for testing
			return 0, NoFolders						#~100
	if labelName == "english":
		if function == "train":
			return 0, int(NoFolders * 10 / 11) 
		elif function == "test":					#This folder is all for testing
			return 0, NoFolders						#~100
	if labelName == "hindi":
		if function == "train":
			return 0, int(NoFolders * 10 / 11) 
		elif function == "test":					#This folder is all for testing
			return 0, NoFolders						#~100

def dataShareToUseForStrokeRecovforWord(NoFolders, function, labelName):		#Separation of files for the train/test/val so on
	#Done
	if labelName == "bangla":
		if function == "train":
			return 0, int(NoFolders * 10 / 11) 
		elif function == "test":					#This folder is all for testing
			return 0, NoFolders/2					#~250
		elif function == "val":					
			return NoFolders/2, NoFolders						#~100
	if labelName == "english":
		if function == "train":
			return 0, int(NoFolders * 10 / 11) 
		elif function == "test":					#This folder is all for testing
			return 0, NoFolders/2					#~500
		elif function == "val":					
			return NoFolders/2, NoFolders
	if labelName == "hindi":
		if function == "train":
			return 0, int(NoFolders * 10 / 11) 
		elif function == "test":					#This folder is all for testing
			return 0, NoFolders/2					#~250
		elif function == "val":					
			return NoFolders/2, NoFolders					#~100

def dataShareToUseForOriginalForChar(NoFolders, function, labelName):		#Separation of files for the train/test/val so on
	#Done
	if labelName == "bangla":
		if function == "train":
			return 0, int(NoFolders * 1.5 / 10) #~2000 files
		elif function == "val":
			return NoFolders - int(NoFolders * 1.5 / 100), NoFolders
	if labelName == "english":
		if function == "train":
			return 0, int( (NoFolders/17 )* 10 )	#~2000 files
		elif function == "test":
			return int(NoFolders * 12 / 17), NoFolders
		elif function == "val":
			return int( (NoFolders/17 )* 10 ), int( (NoFolders/17 )* 12 )
	if labelName == "hindi":
		if function == "train":
			return 0, int(NoFolders * 1 / 11) #~2000 files
		elif function == "test":
			return int(NoFolders * 1 / 11), int(NoFolders * 3 / 22)
		elif function == "val":
			return  int(NoFolders * 3 / 22), int((NoFolders * 3/22) + NoFolders * 1/55) #~200 Files

def dataShareToUseForOriginalForWord(NoFolders, function, labelName):		#Separation of files for the train/test/val so on
	#Done
	if labelName == "bangla":
		print "Unsupported Language for Word Original -> bangla"
		if function == "train":
			return 0, int(NoFolders * 10 / 11) 
		elif function == "test":					#This folder is all for testing
			return 0, NoFolders/2					#~250
		elif function == "val":					
			return NoFolders/2, NoFolders					
	if labelName == "english":
		if function == "train":
			return 0, int(NoFolders * 1 / 3) 		#~12000/3 -> 4000
		elif function == "val":					#This folder is all for testing
			return int(NoFolders * 1 / 3) , int(NoFolders * 4500 / 12000) 					#~500
		elif function == "test":					
			return int(NoFolders * 2 / 3), int(NoFolders * 3 / 4) #~1000 
	if labelName == "hindi":
		if function == "train":
			return 0, int(NoFolders * 1 / 6) 		#~27000/6 -> 4500
		elif function == "val":					#This folder is all for testing
			return int(NoFolders * 1 / 6) , int(NoFolders * 5000 / 28000) 					#~500
		elif function == "test":					
			return int(NoFolders * 1 / 3), int(NoFolders * 3 / 8) #~1000 					


def dataShareToUse(NoFolders, function, labelName, level, dataSource):
	if dataSource == "Original":
		return dataShareToUseForOriginal(NoFolders, function, labelName, level)
	else:
		return dataShareToUseForStrokeRecov(NoFolders, function, labelName, level)

def dataShareToUseForOriginal(NoFolders, function, labelName, level):
	if level == "Char":
		return dataShareToUseForOriginalForChar(NoFolders, function, labelName)
	else:
		return dataShareToUseForOriginalForWord(NoFolders, function, labelName)

def dataShareToUseForStrokeRecov(NoFolders, function, labelName, level):
	if level == "Char":
		return dataShareToUseForStrokeRecovForChar(NoFolders, function, labelName)
	else:
		return dataShareToUseForStrokeRecovforWord(NoFolders, function, labelName)

