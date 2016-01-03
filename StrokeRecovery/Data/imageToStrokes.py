#STROKE RECOVERY
#This is the start point of our stroke recovery code.
#This calls the file which recursively enters folders and generates the Strokes for each image file

import code.wordToTxt as MN
inputdir = "/media/riot/5127cd94-5f74-45d1-b6e9-d7aeb19bb1d9/DataSets/OfflineCharLevel/"
outputdir = "/media/riot/5127cd94-5f74-45d1-b6e9-d7aeb19bb1d9/DataSets/OfflineCharLevelStrokesRetrieved/"
MN.resursiveStrokeRecovery(inputdir, outputdir)