from scipy import *

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
	defPath = "/media/riot/5127cd94-5f74-45d1-b6e9-d7aeb19bb1d9/DataSets/OnlineCharLevel/"
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
	defPath = "/media/riot/5127cd94-5f74-45d1-b6e9-d7aeb19bb1d9/DataSets/OnlineWordLevel/"
	if labelName == "bangla":
		pathName = defPath + "blackBanWord/"
		inputMeans = array([ 41.6739496193 ,  92.1837437729 ,  0.02120500047 ])
		inputStds = array([ 24.9476536852 ,  58.9613775415 ,  0.144067166367 ]) 
	if labelName == "english":
		pathName = defPath + "blackEngWord/"
		inputMeans = array([ 46.330696446 ,  129.470081799 ,  0.0190522590902 ])
		inputStds = array([ 25.3159868775 ,  181.098511472 ,  0.136708706796 ]) 
	if labelName == "hindi":
		pathName = defPath + "blackHinWord/"
		inputMeans = array([ 46.3485867625 ,  93.3273084061 ,  0.0180196154922 ])
		inputStds = array([ 28.1631435006 ,  64.7344452375 ,  0.133022212242 ])
	return pathName, inputMeans, inputStds
	
def getPathNameForCharForStrRecov(labelName):
	#Done
	defPath = "/media/riot/5127cd94-5f74-45d1-b6e9-d7aeb19bb1d9/DataSets/OfflineCharLevelStrokesRetrieved/"
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
	defPath = "/media/riot/5127cd94-5f74-45d1-b6e9-d7aeb19bb1d9/DataSets/OfflineWordLevelStrokesRetrieved/"
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

def dataShareToUse(NoFolders, function, labelName, level, dataSource):
	if dataSource == "Original":
		return dataShareToUseForOriginal(NoFolders, function, labelName, level)
	else:
		return dataShareToUseForStrokeRecov(NoFolders, function, labelName, level)

def dataShareToUseForOriginal(NoFolders, function, labelName, level):
	if level == "Char":
		return dataShareToUseForOriginalForChar(NoFolders, function, labelName)
	else:
		return dataShareToUseForOriginalforWord(NoFolders, function, labelName)

def dataShareToUseForStrokeRecov(NoFolders, function, labelName, level):
	if level == "Char":
		return dataShareToUseForStrokeRecovForChar(NoFolders, function, labelName)
	else:
		return dataShareToUseForStrokeRecovforWord(NoFolders, function, labelName)

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
	if labelName == "bangla":
		if function == "train":
			return 0, int(NoFolders * 1.5 / 10) #~2000 files
		elif function == "val":
			return NoFolders - int(NoFolders * 1.5 / 100), NoFolders
	if labelName == "english":
		if function == "train":
			return 0, int( (NoFolders/17 )* 10 )	#~2000 files
			# return 0, int(NoFolders * 6.5 / 11) 
		elif function == "test":
			return int(NoFolders * 10 / 11), NoFolders
		elif function == "val":
			return NoFolders - int( (NoFolders/170 ) * 10), NoFolders
	if labelName == "hindi":
		if function == "train":
			return 0, int(NoFolders * 1 / 11) #~2000 files
		elif function == "test":
			return int(NoFolders * 10 / 11), NoFolders
		elif function == "val":
			return  NoFolders - int(NoFolders *  1 / 80), NoFolders #~200 Files

def dataShareToUseForOriginalForWord(NoFolders, function, labelName):		#Separation of files for the train/test/val so on
	if labelName == "bangla":
		if function == "train":
			return 0, int(NoFolders * 10 / 11) 
		elif function == "test":					#This folder is all for testing
			return 0, NoFolders/2					#~250
		elif function == "val":					
			return NoFolders/2, NoFolders					
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
			return NoFolders/2, NoFolders					