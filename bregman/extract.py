# 
# MFCC Extractor
#
# Given a path to a .wav file,
# extracts MFCC and writes the 
# average values in a file.
#

from bregman.suite import *
import os
import os.path
import time
import numpy as np
from pylab import *

# Get the MFCC from a song
def getMFCC(x):
	#print "\nExtracting MFCC from ", x, "..."
	F = LogFrequencyCepstrum(x, nfft=16384, wfft=8192, nhop=2205)
	F.x.close()
	x = []
	stds=0
	for i in range(len(F.X)):
		x.append(np.mean(F.X[i]))
		stds+=np.std(F.X[i])
	x.append(stds/len(F.X))
	return x

# Get the Chromagram values from a song
def getChroma(x):
	#print "\nExtracting MFCC from ", x, "..."
	F = Chromagram(x, nfft=16384, wfft=8192, nhop=2205)
	F.x.close()
	x = []
	stds=0
	for i in range(len(F.X)):
		x.append(np.mean(F.X[i]))
		stds+=np.std(F.X[i])
	x.append(stds/len(F.X))
	return x

if __name__ == "__main__":
	filename = "%s.txt" % sys.argv[2][:-4]
	f = open(filename,'w')
	print "Extracting MFCC..."
	mfcc = getMFCC(sys.argv[1])
	print "Done!"
	chroma = getChroma(sys.argv[1])
	f.write("%s " % ' '.join(str(x) for x in mfcc))
	f.write("%s\n" % ' '.join(str(x) for x in chroma))
	f.close()
