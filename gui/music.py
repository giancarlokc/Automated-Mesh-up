import pygame
import time
pygame.init()

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

	def __init__(self, directory):
		self.directory = directory
		self.name = getFilename(directory)

	# Play music #
	def playWav(self):
		if(self.paused == True):
			pygame.mixer.music.unpause()
			self.paused = False
		else:
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
