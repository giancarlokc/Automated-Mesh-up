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
def ex_4a(x):
	print "Extracting MFCC from ", x, "..."
	F = LogFrequencyCepstrum(x, nhop=2205)
#	F.feature_plot(normalize=True)
#	title('Mel-Frequency Cepstral Coefficients')
	# Show F matrix lenght
	print "   Lines: ", len(F.X)
	print "   Colums: ", len(F.X[0])
	return F
	
# Compare 2 avg band arrays
def cmpAvg(a, b):
	diff = 0
	for i in range(len(a)):
		if(a[i] - b[i] < 0):
			diff+= b[i] - a[i]
		else:
			diff+= a[i] - b[i]
	return diff

if __name__ == "__main__":
	#audio_file = os.path.split(bregman.__file__)[0]+os.sep+'audio'+os.sep+'gmin.wav'
	audio_file = os.path.join(".","rock1.wav")
	audio_file2 = os.path.join(".","beet3.wav")
	
	features = ex_4a(audio_file)
	avg = avgBand(features)
	features2 = ex_4a(audio_file2)
	avg2 = avgBand(features2)
	difference = cmpAvg(avg, avg2)
	print difference
	
	raw_input()
