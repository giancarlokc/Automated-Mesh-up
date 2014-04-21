# examples_features.py 
# Bregman audio feature analysis
#
# Copyright (C) 2011 Mike Casey
# Dartmouth College, Hanover, NH
# All Rights Reserved
#

from bregman.suite import *
import os
import os.path
from pylab import *

# Examples of using the Features base class to extract features
# and the derived helper classes to extract the same features.

# Return the average for each band in the MFCC
def avgBand(F):
	print "Extracting the average from each band..."
	x = []
	for i in range(len(F.X)):
		x.append(sum(F.X[i])/len(F.X[i]))
	return x

# Get the MFCC from a music and return the feature class
def getMFCC(audio_file):
#	print "Extracting MFCC from ", x, "..."
#	F = LogFrequencyCepstrum(x, nhop=2205)
#	F.feature_plot(normalize=True)
#	title('Mel-Frequency Cepstral Coefficients')
#	# Show F matrix lenght
#	print "   Lines: ", len(F.X)
#	print "   Colums: ", len(F.X[0])
#	return F
	
	
	#print "\nExtracting MFCC from ", x, "..."
	F = LogFrequencyCepstrum(audio_file, nfft=16384, wfft=8192, nhop=2205)
	F.x.close()
	x = []
	stds=0
	for i in range(len(F.X)):
		x.append(np.mean(F.X[i]))
		stds+=np.std(F.X[i])
	x.append(stds/len(F.X))
	return x
	
# Compare 2 avg band arrays
def cmpAvgMFCC(avg1, avg2):
	print "############################################# COMPARING ##"
	print "A: ", avg1
	print "B: ", avg2
	diff = 0
	for i in range(len(avg1)):
		if(avg1[i] - avg2[i] < 0):
			diff+= avg2[i] - avg1[i]
		else:
			diff+= avg1[i] - avg2[i]
	return diff

def extractMFCC(audio_name):
	audio_file = os.path.join(".",audio_name)
	
	avg = getMFCC(audio_file)
	
	string = ""
	for i in range(len(avg)):
		if(i != 0):
			string = string + " "
		string = string + str(avg[i])
	return string

	
	
	
	#features2 = ex_4a(audio_file2)
	#avg2 = avgBand(features2)
	#difference = cmpAvg(avg, avg2)
	#print difference
	
	raw_input()
