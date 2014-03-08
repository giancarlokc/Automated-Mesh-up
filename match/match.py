#!/usr/bin/python

import matplotlib.pylab as plt
import numpy as np
import scipy.io.wavfile as sci
import sys

# Normalize data with a given granualization #
def normalize(tSample, tRate, granu):
	rNormalized = [0 for x in xrange(tSample.size/granu+2)]
	iNorm=0
	ini = 0
	while(ini < tSample.size):
		# Define the beggining and ending of the piece to normalize #
		end = ini + granu;
		if(end > tSample.size):
			end = tSample.size-1
	
	
		# Normalize piece #
		tsum=0
		i=ini
		while(i<=end):
			if(i == tSample.size):
				tsum = tsum + tSample[i-1]
			else:
				tsum = tsum + tSample[i] 
			i=i+1
		rNormalized[iNorm] = tsum / (end - ini)
		
		ini = ini + granu;
		iNorm = iNorm + 1

	print "Current number of samples: %d" % (len(rNormalized))
	afterSt = np.linspace(0, len(rNormalized)/(tRate/granu), len(rNormalized))
	return (afterSt, rNormalized)
	
# Check arguments #
if(len(sys.argv) < 3):
	print "Usage: match <granualization> <target song> <song list>..."
	quit()

# Open TARGET song #
(tRate, tSample) = sci.read(sys.argv[2])

print "Previous number of samples: %d" % (tSample.size)

#plt.plot(tSt, tSample)
#plt.show()

(tSt, rNormalized) = normalize(tSample, tRate, tRate)

plt.plot(tSt, rNormalized)
plt.show()
	

i=0
# For each song in the song list #
while(i < len(sys.argv)-3):
	# Open song in song list #
	(rate, sample) = sci.read(sys.argv[i+3])
	print sample.size/100
	(st, sample) = normalize(sample, rate, rate)
	
	plt.plot(st, sample)
	plt.show()
	# matrix                          y                                 x #
	matrix = [[0 for x in xrange(len(rNormalized))] for x in xrange(len(sample))]
	
	# Set initial values for y axis #
	j=0
	count = 0
	while(j < len(rNormalized)):
		matrix[0][j] = count
		j=j+1
		count=count+1
	
	# Set initial values for x axis #
	j=0
	count = 0
	while(j < len(sample)):
		matrix[j][0] = count
		j=j+1
		count=count+1
	
	# Fill the matrix #
	j=1

	while(j < len(sample)):
		k=1
		while(k < len(rNormalized)):
#			print "For position [%d][%d]" % (j,k)
			extra = sample[j] - rNormalized[k]
			if(extra < 0):
				extra = extra * (-1)
			matrix[j][k] = min(matrix[j-1][k] + extra, matrix[j-1][k-1] + extra, matrix[j][k-1] + extra)
			k=k+1
		j=j+1
	
	i=i+1
	print "FINAL VALUE:"
	print matrix[len(sample)-1][len(rNormalized)-1]

