from Tkinter import *
import tkMessageBox
from tkFileDialog import askopenfilename
import tkHyperlinkManager
import scipy.io.wavfile as sci
from bregman.suite import *
import numpy as np
import mumusic
import mumatch
import muplot
import mumfcc
import mudb
import os
import pygame
from PIL import Image
from PIL import ImageTk

class Interface:
	music_list = list()
	music_box = []
	main_window = []
	# TARGET
	targetON = []
	targetIndex = []
	targetFrame = []
	targetTFrame = []
	# MATCH
	matchON = []
	matchIndex = []
	matchTFrame = []
	meshupSource1Label = 0
	meshupSource2Label = 0
	
	# Example:        "TITLE", "900x600"
	def __init__(self, title, resolution):
		# Create window #
		self.main_window = Tk()
		image2 =Image.open("image.gif")
		image1 = ImageTk.PhotoImage(image2)
		background_label = Label(self.main_window, image=image1)
		background_label.photo=image1
		background_label.place(x=0, y=0, relwidth=1, relheight=1)
		self.main_window.configure(background='grey')
		self.main_window.title(title)
		self.main_window.geometry(resolution)
	
	###################################################### Gui functions ##
	# Target volume button #
	def createTargetVolume(self, name, window, index):
		print index
		tmp = Scale(window, label=name, to=0, from_=100, command=self.music_list[int(index)].changeVolume)
		tmp.set(100)
		tmp.grid(row=0, column=1)
	
	# Match volume button #
	def createMatchVolume(self, name, window):
		global matchVolume
		matchVolume = Scale( window, label=name, to=0, from_=100)
		matchVolume.grid(row=0, column=2)
		
	# Dummy fuction #
	def donothing(self):
	   filewin = Toplevel(self.main_window)
	   button = Button(filewin, text="Do nothing button")
	   button.pack()
	   
	# Check if music was already loaded
	def checkMusicDB(self, filename, music_data):
		print "   Searching database for: ", mumusic.getFilename(filename)
		for i in range(len(music_data)):
			tmp = list(music_data[i].name)
			tmp = tmp[:len(tmp)-1]
			a = "".join(tmp)
			if(mumusic.getFilename(filename) == music_data[i].name):
				print "   Music found, loading music information..."
				self.music_list[-1].data = music_data[i]
				print "   Information uploaded:"
				print "      - Name:", self.music_list[-1].name
				print "      - MFCC:", self.music_list[-1].data.MFCC_features
				return
				
		print "   Music NOT found, extracting music information..."
		
		# Calls beat-tracking command
		os.system("ibt %s" % filename)
		# Calls MFCC extraction algorithm
		os.system("python extract.py %s %s" % (filename,mumusic.getFilename(filename)))
		# Reads the output of both programs
		t = open('%s_medianTempo.txt' % mumusic.getFilename(filename)[:-4],'r')
		m = open('%s.txt' % mumusic.getFilename(filename)[:-4],'r')
		feats = m.readline()
		
		tmp = mudb.MusicData(mumusic.getFilename(filename), feats, int(t.readline()))
		os.remove('%s_medianTempo.txt' % mumusic.getFilename(filename)[:-4])
		os.remove('%s.txt' % mumusic.getFilename(filename)[:-4])
		music_data.append(tmp)
		self.music_list[-1].data = music_data[-1]
		mudb.syncDB(music_data)
		return
	   
	def openfile(self, music_data):
		FILEOPENOPTIONS = dict(defaultextension='.wav', filetypes=[('Wav file','*.wav'), ('All files','*.*')])
		filename = askopenfilename(parent=self.main_window, **FILEOPENOPTIONS)
		print "Openning file..."
		if(filename):
			sample_music = mumusic.Music(filename)
			self.music_list.append(sample_music)
			self.checkMusicDB(filename, music_data)
			self.music_box.insert(END, sample_music.name)
			return filename
		else:
			tkMessageBox.showerror("Error", "Could not open wav file!")
			return False;
	
	###################################################### Play/Stop Sound ##
	def playButton(self, index, targetTitle):
		print "Playing: " + str(self.music_list[index].name)
		self.music_list[index].playWav()
		targetTitle.config(text="(Playing)")
		
	def pauseButton(self, index, targetTitle):
		self.music_list[index].pauseWav()
		targetTitle.config(text="(Stopped)")
	
	###################################################### Open window frame for the target/match music ##
	def openTargetFrame(self, index):
		print "   Selected file: " + self.music_list[int(index)].name
		targetTOTAL=Frame(self.main_window, relief=GROOVE, bd=1)
		targetTOTAL.place(x=10, y=240)
		self.targetTFrame = targetTOTAL

		targetFrame = Frame(targetTOTAL, relief=GROOVE, width=780, height=150, bd=1)
		targetFrame.grid(row=0, column=0)
		targetTitleFixed = Label(targetFrame, text="Targed sound")
		targetTitleFixed.grid(row=0,column=0)
		targetTitle = Label(targetFrame, text=" ")
		targetTitle.grid(row=0,column=1)
		targetPlay = Button(targetFrame, text="Play", height=4, width=7, command=lambda:self.playButton(int(index), targetTitle))
		targetPause = Button(targetFrame, text="Pause", command=lambda:self.pauseButton(int(index), targetTitle), height=4, width=7)
		targetPlay.grid(row=1, column=0)
		targetPause.grid(row=1, column=1)
		targetFrame2=Frame(targetTOTAL,relief=GROOVE,width=120,height=150,bd=1)
		targetFrame2.grid(row=0, column=1)
		
		self.createTargetVolume("Volume", targetTOTAL, index)
		
	# Open frame for the match sound
	def openMatchFrame(self, index):
		print "   Oppening file: " + str(self.music_list[index].name)
		matchTOTAL=Frame(self.main_window, relief=GROOVE, width=780, height=150, bd=1)
		matchTOTAL.place(x=10, y=410)
		self.matchTFrame = matchTOTAL
	
		matchFrame=Frame(matchTOTAL,relief=GROOVE, width=780, height=150,bd=1)
		matchFrame.grid(row=0, column=0)
		matchTitleFixed = Label(matchFrame, text="Match sound")
		matchTitleFixed.grid(row=0,column=0)
		matchTitle = Label(matchFrame, text=" ")
		matchTitle.grid(row=0,column=1)
		matchPlay = Button(matchFrame, text="Play", height=4, width=7, command=lambda:self.playButton(index, matchTitle))
		matchPause = Button(matchFrame, text="Pause", command=lambda:self.pauseButton(index, matchTitle), height=4, width=7)
		matchPlay.grid(row=1, column=0)
		matchPause.grid(row=1, column=1)
		matchFrame2=Frame(matchTOTAL,relief=GROOVE,width=120,height=150,bd=1)
		matchFrame2.grid(row=0, column=1)
		
		self.createTargetVolume("Volume", matchTOTAL, index)
	
	###################################################### Action functions for the buttons ##
	def selectTarget(self):
		# Get the selected music
		a = self.music_box.curselection()
		# Check if there was a selected music, if not show error.
		if(len(a) == 0):
			print "Can not open TARGET frame: Music was NOT selected!"
			tkMessageBox.showwarning("Error", "Music was not selected!")
			return
		if(self.targetON == True):
			self.targetTFrame.destroy()
		# Set TARGET global variables
		self.targetON = True
		self.targetIndex = a[0]
		self.meshupSource1Label.config(text=("Target: "+self.music_list[int(self.targetIndex)].name))
		# Open target music frame
		print "Opening TARGET frame..."
		self.openTargetFrame(self.targetIndex)
		
	def selectMatch(self):
		# If the music list is empty, show error and return
		if(len(self.music_list) == 0):
			print "Can not open MATCH frame: Empty music list!"
			tkMessageBox.showwarning("Error", "Music list is empty!")
			return
		if(self.targetON == False):
			print "Can not open MATCH frame: TARGET was not selected yet!"
			tkMessageBox.showwarning("Error", "Select the target music first!")
			return
		if(self.matchON == True):
			self.matchTFrame.destroy()
		# Set MATCH global variables
		self.matchON = True
		# Find a MATCH for the TARGET music
		self.matchIndex = mumatch.avgBandMFCC(self.targetIndex, self.music_list)
		self.meshupSource2Label.config(text=("Match: "+self.music_list[int(self.matchIndex)].name))
		print "Opening MATCH frame..."
		self.openMatchFrame(self.matchIndex)
		
	def playMeshup(self, period):
		if(len(self.targetIndex) > 0):
			if(int(self.targetIndex) >= len(self.music_list)):
				print "Target and Match musics are not selected."
				tkMessageBox.showwarning("Error", "Target and Match musics are not selected.")
				return
		else:
			print "Target music is not selected."
			tkMessageBox.showwarning("Error", "Target music is not selected.")
			return
		if(self.matchIndex >= len(self.music_list)):
			print "Match music is not selected."
			tkMessageBox.showwarning("Error", "Match music is not selected.")
			return
		music_dir = mumusic.meshupSongs(self.music_list[int(self.targetIndex)].directory, self.music_list[self.matchIndex].directory, period)
		
		if(music_dir != False):
			pygame.mixer.music.pause()
			print "Openning: ", music_dir
			pygame.mixer.music.load(music_dir)
			pygame.mixer.music.play()
			time.sleep(2)
			pygame.mixer.music.set_volume(1)
		else:
			tkMessageBox.showwarning("Error", "Songs could not be meshup because they have different number of channels.")
			return False
		
		return True
	
	###################################################### Main menu ##
	def startMenu(self, music_data):
		menubar = Menu(self.main_window)
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="New", command=self.donothing)
		filemenu.add_command(label="Open", command=lambda:self.openfile(music_data))
		filemenu.add_command(label="Save", command=self.donothing)
		filemenu.add_command(label="Save as...", command=self.donothing)
		filemenu.add_command(label="Close", command=self.donothing)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=self.main_window.quit)
		menubar.add_cascade(label="File", menu=filemenu)
		editmenu = Menu(menubar, tearoff=0)
		editmenu.add_command(label="Undo", command=self.donothing)
		editmenu.add_separator()
		editmenu.add_command(label="Cut", command=self.donothing)
		editmenu.add_command(label="Copy", command=self.donothing)
		editmenu.add_command(label="Paste", command=self.donothing)
		editmenu.add_command(label="Delete", command=self.donothing)
		editmenu.add_command(label="Select All", command=self.donothing)
		menubar.add_cascade(label="Edit", menu=editmenu)
		helpmenu = Menu(menubar, tearoff=0)
		helpmenu.add_command(label="Help Index", command=self.donothing)
		helpmenu.add_command(label="About...", command=self.donothing)
		menubar.add_cascade(label="Help", menu=helpmenu)
		self.main_window.config(menu=menubar)
	
	###################################################### Scrollbox of musics ##
	def startScrollBox(self):
		myframe = Frame(self.main_window, relief=GROOVE, width=400, height=100, bd=1)
		myframe.place(x=10, y=10)
		scrollbar = Scrollbar(myframe)
		scrollbar.pack(side=RIGHT, fill=Y)
		self.music_box = Listbox(myframe, yscrollcommand=scrollbar.set, selectmode=BROWSE)
		for i in range(len(self.music_list)):
		    self.music_box.insert(END, self.music_list[i])
		self.music_box.pack(side=LEFT, fill=BOTH)
		scrollbar.config(command=self.music_box.yview)
	
	###################################################### Action Buttons ##
	# Target button #
	def startTargetButton(self):
		# Target button #
		myframe2=Frame(self.main_window, relief=GROOVE, width=400, height=100, bd=1)
		myframe2.place(x=10, y=180)
		b1 = Button(myframe2, text="Target", command=lambda:self.selectTarget(), anchor="e")
		b1.pack()
		
	# Match button #
	def startMatchButton(self):
		myframe3=Frame(self.main_window, relief=GROOVE, width=400, height=100, bd=1)
		myframe3.place(x=122, y=180)
		b2 = Button(myframe3, text="Match", command=lambda:self.selectMatch(), anchor="w")
		b2.pack()
		
	def startMeshupPlay(self):
		# MAIN FRAME
		meshupFrame = Frame(self.main_window, relief=GROOVE, width=690, height=200, bd=1)
		meshupFrame.place(x=200, y=10)
		mainLabelFrame = Frame(meshupFrame, relief=GROOVE, width=400, height=30, bd=1)
		mainLabelFrame.place(x=0, y=0)
		labelMain = Label(mainLabelFrame, text="Meshup Menu")
		labelMain.pack()
		# SOURCES PANEL
		sourcesFrame = Frame(meshupFrame, relief=GROOVE, width=365, height=80, bd=1)
		sourcesFrame.place(x=7, y=112)
		labelSFrame = Frame(sourcesFrame, relief=GROOVE, width=145, height=100, bd=1)
		labelSFrame.place(x=0, y=0)
		labelSources = Label(labelSFrame, text="Sources")
		labelSources.pack()
		musicSourceFrame = Frame(sourcesFrame, relief=GROOVE, width=120, height=115, bd=0)
		musicSourceFrame.place(x=10, y=30)
		self.meshupSource1Label = Label(musicSourceFrame, height=1, width=14, text="Target: None", anchor="nw")
		self.meshupSource1Label.grid(row=0)
		self.meshupSource2Label = Label(musicSourceFrame, height=1, width=14, text="Match: None", anchor="nw")
		self.meshupSource2Label.grid(row=1)
		# ENTRY FRAME
		meshupFrameEntry = Frame(meshupFrame, relief=GROOVE, width=100, height=30, bd=1)
		meshupFrameEntry.place(x=380, y=142)
		periodEntry = Entry(meshupFrameEntry, width=11, bd=5)
		periodEntry.pack()
		labelEntry = Label(meshupFrameEntry, text="(Segmentation in secs)")
		labelEntry.pack()
		# MESHUP BUTTON
		meshupButtonFrame = Frame(meshupFrame, relief=GROOVE, width=100, height=30, bd=3)
		meshupButtonFrame.place(x=535, y=142)
		b = Button(meshupButtonFrame, text="Play Meshup", width=14, height=2,command=lambda:self.playMeshup(periodEntry.get()), anchor="center")
#		b = Button(meshupButtonFrame, text="Play Meshup", anchor="w")
		
		b.pack()
	
	###################################################### Main loop ##
	def startLoop(self):
		self.main_window.mainloop()
