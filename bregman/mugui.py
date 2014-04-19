from Tkinter import *
import tkMessageBox
from tkFileDialog import askopenfilename
import tkHyperlinkManager
import scipy.io.wavfile as sci
import numpy as np
import mumusic
import mumatch
import muplot
import mumfcc
import mudb

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
	
	# Example:        "TITLE", "900x600"
	def __init__(self, title, resolution):
		# Create window #
		self.main_window = Tk()
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
		tmp = mudb.MusicData(mumusic.getFilename(filename), mumfcc.extractMFCC(filename))
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
		print "   Selected file: " + self.music_list[int(index[0])].name
		targetTOTAL=Frame(self.main_window, relief=GROOVE, bd=1)
		targetTOTAL.place(x=10, y=240)
		self.targetTFrame = targetTOTAL

		targetFrame = Frame(targetTOTAL, relief=GROOVE, width=780, height=150, bd=1)
		targetFrame.grid(row=0, column=0)
		targetTitleFixed = Label(targetFrame, text="Targed sound")
		targetTitleFixed.grid(row=0,column=0)
		targetTitle = Label(targetFrame, text=" ")
		targetTitle.grid(row=0,column=1)
		targetPlay = Button(targetFrame, text="Play", height=4, width=7, command=lambda:self.playButton(int(index[0]), targetTitle))
		targetPause = Button(targetFrame, text="Pause", command=lambda:self.pauseButton(int(index[0]), targetTitle), height=4, width=7)
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
		print "Opening MATCH frame..."
		self.openMatchFrame(self.matchIndex)
	
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
	
	###################################################### Main loop ##
	def startLoop(self):
		self.main_window.mainloop()
