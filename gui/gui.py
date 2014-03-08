from Tkinter import *
import music
import tkMessageBox
from tkFileDialog import askopenfilename
import tkHyperlinkManager
import plot
import sys
import numpy as np
import random as rand
import matplotlib.pylab as plt
import cmath as m
import scipy.io.wavfile as sci

# Create window #
top = Tk()
top.title("Window")
top.geometry("900x600")

links = list()

###################################################### Global variables ##
# Music TARGET volume control #
global targetVolume
# Music MATCH volume control #
global matchVolume
# Target #
targetIndex = -1
targetON = False
global targetTFrame
# Match #
matchON = False
matchIndex = -1
global matchTFrame


###################################################### Gui functions ##
# Target volume button #
def createTargetVolume(name, window, index):
	print index
	tmp = Scale(window, label=name, to=0, from_=100, command=links[int(index)].changeVolume)
	tmp.grid(row=0, column=2)
	
# Match volume button #
def createMatchVolume(name, window):
	global matchVolume
	matchVolume = Scale( window, label=name, to=0, from_=100)
	matchVolume.grid(row=0, column=2)
	
# Get real file name #
def getFilename(filedir):
	end = len(filedir)
	while(filedir[end-1] != "/"):
		end = end - 1
	return filedir[end:]

# Get the name of the file to be open #
FILEOPENOPTIONS = dict(defaultextension='.wav', filetypes=[('Wav file','*.wav'), ('All files','*.*')])
def openfile():
	filename = askopenfilename(parent=top, **FILEOPENOPTIONS)
	if(filename):
		sample_music = music.Music(filename)
		links.append(sample_music)
		listbox.insert(END, sample_music.name)
		return filename
	else:
		tkMessageBox.showerror("Error", "Could not open wav file!")
		return False;

# Destroy main window #
def exitWin():
	#if tkMessageBox.askokcancel("Quit","You want to quit now?"):
	top.destroy()

# Dummy fuction #
def donothing():
   filewin = Toplevel(top)
   button = Button(filewin, text="Do nothing button")
   button.pack()
	
###################################################### Main menu ##
menubar = Menu(top)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=openfile)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=top.quit)
menubar.add_cascade(label="File", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)
editmenu.add_separator()
editmenu.add_command(label="Cut", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=donothing)
editmenu.add_command(label="Select All", command=donothing)
menubar.add_cascade(label="Edit", menu=editmenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)
top.config(menu=menubar)

###################################################### Play/Stop Sound ##
def playButton(index, targetTitle):
	print "Playing: " + str(links[index].name)
	links[index].playWav()
	targetTitle.config(text="(Playing)")
	
def pauseButton(index, targetTitle):
	links[index].pauseWav()
	targetTitle.config(text="(Stopped)")

###################################################### Open window frame for the target/match music ##
# Open frame for the target sound
def openTargetFrame(index):
	global targetTFrame
	print "   Selected file: " + links[int(index[0])].name
	targetTOTAL=Frame(top,relief=GROOVE,bd=1)
	targetTOTAL.place(x=10,y=240)
	targetTFrame = targetTOTAL

	targetFrame=Frame(targetTOTAL,relief=GROOVE,width=780,height=150,bd=1)
	targetFrame.grid(row=0, column=0)
	targetTitleFixed = Label(targetFrame, text="Targed sound")
	targetTitleFixed.grid(row=0,column=0)
	targetTitle = Label(targetFrame, text=" ")
	targetTitle.grid(row=0,column=1)
	targetPlay = Button(targetFrame, text="Play", height=4, width=7, command=lambda:playButton(int(index[0]), targetTitle))
	targetPause = Button(targetFrame, text="Pause", command=lambda:pauseButton(int(index[0]), targetTitle), height=4, width=7)
	targetPlay.grid(row=1, column=0)
	targetPause.grid(row=1, column=1)

	targetFrame2=Frame(targetTOTAL,relief=GROOVE,width=780,height=150,bd=1)
	targetFrame2.grid(row=0, column=1)
	
	(rate, sample) = sci.read(links[int(index[0])].directory)
	
	st = np.linspace(0, sample.size/rate, sample.size)
	
#	print sample[400]


#	div = 1000
#	print sample.size
#	for i in range(sample.size):
#		if(i/div > 0):
#			print i
#			div=div*2
#		if(sample[i] > 0):
#			sample[i] = sample[i]**2/10000
#			sample[i] = -sample[i]
#		else:
#			sample[i] = -(sample[i]**2/10000)
#			sample[i] = -sample[i]
	
#	sci.write(links[int(index[0])].directory + "NEW.wav", rate, sample)
	
	plot.showPlot(targetFrame2, st, sample.real)

	#####################
	#
	#	Here is where you use the music data (rate and sample.real)
	#
	#####################
	
	createTargetVolume("Volume", targetTOTAL, index)

# Open frame for the match sound
def openMatchFrame(index):
	global matchTFrame
	print "   Oppening file: " + str(links[index].name)
	matchTOTAL=Frame(top,relief=GROOVE,width=780,height=150,bd=1)
	matchTOTAL.place(x=10,y=410)
	matchTFrame = matchTOTAL
	
	matchFrame=Frame(matchTOTAL,relief=GROOVE, width=780, height=150,bd=1)
	matchFrame.grid(row=0, column=0)
	matchTitleFixed = Label(matchFrame, text="Match sound")
	matchTitleFixed.grid(row=0,column=0)
	matchTitle = Label(matchFrame, text=" ")
	matchTitle.grid(row=0,column=1)
	matchPlay = Button(matchFrame, text="Play", height=4, width=7, command=lambda:playButton(index, matchTitle))
	matchPause = Button(matchFrame, text="Pause", command=lambda:pauseButton(index, matchTitle), height=4, width=7)
	matchPlay.grid(row=1, column=0)
	matchPause.grid(row=1, column=1)

	matchFrame2=Frame(matchTOTAL,relief=GROOVE,width=780,height=150,bd=1)
	matchFrame2.grid(row=0, column=1)
	
	(rate, sample) = sci.read(links[index].directory)
	st = np.linspace(0, sample.size/rate, sample.size)
	plot.showPlot(matchFrame2, st, sample.real)
	
	#####################
	#
	#	Here is where you use the music data (rate and sample.real)
	#
	#####################
	
	createMatchVolume("Volume", matchTOTAL);

###################################################### Matching funtions ##
# Find a random match for the TARGET music
def randomMatch(links):
	from random import randint
	a = randint(0,len(links)-1)
	return a
	
###################################################### Action functions for the buttons ##
def selectTarget():
	# Get global variables
	global targetON
	global targetIndex
	global targetTFrame
	# Get the selected music
	a = listbox.curselection()
	# Check if there was a selected music, if not show error.
	if(len(a) == 0):
		print "Can not open TARGET frame: Music was NOT selected!"
		tkMessageBox.showwarning("Error", "Music was not selected!")
		return
	if(targetON == True):
		targetTFrame.destroy()
	# Set TARGET global variables
	targetON = True
	targetIndex = a[0]
	# Open target music frame
	print "Opening TARGET frame..."
	openTargetFrame(targetIndex)
	
def selectMatch():
	# Get global variables
	global targetON
	global targetIndex
	global matchON
	global matchIndex
	global matchTFrame
	# If the music list is empty, show error and return
	if(len(links) == 0):
		print "Can not open MATCH frame: Empty music list!"
		tkMessageBox.showwarning("Error", "Music list is empty!")
		return
	if(targetON == False):
		print "Can not open MATCH frame: TARGET was not selected yet!"
		tkMessageBox.showwarning("Error", "Select the target music first!")
		return
	if(matchON == True):
		matchTFrame.destroy()
	# Set MATCH global variables
	matchON = True
	# Find a MATCH for the TARGET music
	matchIndex = randomMatch(links)
	print "Opening MATCH frame..."
	openMatchFrame(matchIndex)
	
	
###################################################### Scrollbox of musics ##
myframe=Frame(top,relief=GROOVE,width=400,height=100,bd=1)
myframe.place(x=10,y=10)

scrollbar = Scrollbar(myframe)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(myframe, yscrollcommand=scrollbar.set, selectmode=BROWSE)
for i in range(len(links)):
    listbox.insert(END, links[i])
listbox.pack(side=LEFT, fill=BOTH)

scrollbar.config(command=listbox.yview)

###################################################### Action Buttons ##
# Target button #
myframe2=Frame(top,relief=GROOVE,width=400,height=100,bd=1)
myframe2.place(x=10,y=180)
b1 = Button(myframe2, text="Target", command=lambda:selectTarget(), anchor="e")
b1.pack()

# Match button #
myframe3=Frame(top,relief=GROOVE,width=400,height=100,bd=1)
myframe3.place(x=122,y=180)
b2 = Button(myframe3, text="Match", command=selectMatch, anchor="w")
b2.pack()

###################################################### Main loop ##

top.mainloop()
