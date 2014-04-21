import pygame
import time
import mudb
from bregman.suite import *
from numpy import *
pygame.init()

# Mesh to songs
def meshupSongs(audio1, audio2, step):
	
	x, y, z = wavread(audio1)
	x1, y1, z1 = wavread(audio2)
	
	step = int(int(step)*y)
	print "STEP: ", step
	
	print "Song 1:"
	print "   Size: ", len(x)
	print "   Sample Rate: ", y
	print x

	print "Song 2:"
	print "   Size: ", len(x1)
	print "   Sample Rate: ", y1
	print x1
	
	# Concatenate songs
	result = numpy.concatenate([x, x1])
	x_begin = 0
	x_end = step
	x1_begin = 0
	x1_end = step
	final_begin = 0
	final_end = step
	while(x_end < len(x) and x1_end < len(x1)):
		diff = 0
		if(x_end >= len(x)):
			diff = x_end - len(x) + 1
			x_end = len(x) - 1
		if(x1_end >= len(x1)):
			diff = x1_end - len(x1) + 1
			x1_end = len(x1) - 1
		
		result[final_begin:final_end] = x[x_begin:x_end]
		final_begin = final_begin + step
		final_end = final_end + step
		result[final_begin:final_end] = x1[x1_begin:x1_end]
		final_begin = final_begin + step
		final_end = final_end + step
		
		x_begin = x_begin + step
		x_end = x_end + step
		x1_begin = x1_begin + step
		x1_end = x1_end + step
		final_x = False
		final_x1 = False
		

	if(y != y1):
		print "Concatenating with different sample rates..."
	else:
		print "Concatenating with equal sample rates..."
	
	print "Saving as: tmp.wav" 
	wavwrite(result, "tmp.wav", y)
	return "tmp.wav"

# Get real file name #
def getFilename(filedir):
	end = len(filedir)
	while(filedir[end-1] != "/"):
		end = end - 1
	return filedir[end:]

class Music:
	directory = ""
	paused = False
	started = False
	name = ""
	pointer = []
	channel = []
	data = mudb.MusicData(name, "", "")

	def __init__(self, directory):
		self.directory = directory
		self.name = getFilename(directory)

	# Play music #
	def playWav(self):
		if(self.paused == True):
			pygame.mixer.music.unpause()
			self.paused = False
		else:
#			audio_file = os.path.join(".",self.directory)
#			x,sr,fmt = wavread(audio_file) # load the audio file
#			play(x, sr) # play it

			pygame.mixer.music.load(self.directory)
			pygame.mixer.music.play()
			time.sleep(2)
			pygame.mixer.music.set_volume(1)
			self.started = True

	# Pause music #
	def pauseWav(self):
		pygame.mixer.music.pause()
		self.paused = True

	# Change volume #
	def changeVolume(self, volume):
		pygame.mixer.music.set_volume(float(float(volume)/100))
