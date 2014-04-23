from bregman.suite import *
import numpy

audio_file_1 = os.path.join("/home/gkc/Music/wav","george.wav")


#gen = GeneralAudioSegmentor()
#gen.extract("/home/gkc/Music/wav/gbs1.wav" , 3)

#gen.segmentation_plot()

#raw_input()

#gen.play_segs(0)

#print "SECOND:"

#gen.play_segs(1)

#print "THIRD:"

#gen.play_segs(2)


def meshupSongs(audio1, audio2, step):
	x, y, z = wavread(audio1)
	x1, y1, z1 = wavread(audio2)

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

	while(x_end < len(x) or x1_end < len(x1)):
		if(x_end >= len(x)):
			x_end = len(x) - 1
		if(x1_end >= len(x1)):
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
		

	if(y != y1):
		print "Concatenating with different sample rates..."
	else:
		print "Concatenating with equal sample rates..."
	
	print "Saving as: test.wav" 
	wavwrite(result, "test.wav", y)
	return "test.wav"
	
meshupSongs("/home/gkc/Music/wav/rock2.wav", "/home/gkc/Music/wav/rock1.wav", 1000000)




