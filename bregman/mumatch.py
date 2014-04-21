###################################################### Matching funtions ##

from numpy import *

# Find a random match for the TARGET music
def randomMatch(targetIndex, music_list):
	from random import randint
	print "################# MATCHING ##"
	print "Using random selection..."
	print "   Target: ", music_list[int(targetIndex[0])].name
	a = randint(0,len(music_list)-1)
	print "   Match: ", music_list[a].name
	print "#############################"
	return a
	
def euclDist(a,b):
	dist = [float((a[i]-b[i])**2) for i in range(len(a))]
	return sqrt(sum(dist))
	
# Find the closest match to the TARGET using an average for a 10-Band MFCC
def avgBandMFCC(targetIndex, music_list):
	import mumfcc
	print "################# MATCHING ##"
	print "Using average band MFCC..."
	print "   Target: ", music_list[int(targetIndex[0])].name
	print "   TARGET MFCC: ", music_list[int(targetIndex[0])].data.MFCC_features.split(" ")
	smallestDiff = 10000
	index = 0
	for i in range(len(music_list)):
		if(int(targetIndex[0]) != i):
			a = music_list[int(targetIndex[0])].data.MFCC_features.split(" ")
			for j in range(len(a)):
				a[j] = float(a[j])
			b = music_list[i].data.MFCC_features.split(" ")
			for j in range(len(b)):
				b[j] = float(b[j])
		
			#diff = mumfcc.cmpAvgMFCC(a, b)
			diff = euclDist(a, b)
			if(diff < smallestDiff):
				smallestDiff = diff
				index = i
	print "   Match: ", music_list[index].name
	print "#############################"
	return index
