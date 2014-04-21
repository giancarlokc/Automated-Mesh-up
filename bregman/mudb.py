# MESH-UP
#
# SIMPLE DATABASE IMPLEMENTED USING A FILE (music.db)

# Load db file
def loadDB():
	music_data = []
	f = open("music.db", "r")
	n_samples = int(f.readline())
	for i in range(n_samples):
		name = f.readline()
		name = name[:len(name)-1]
		features = f.readline()
		#features = features[:len(features)-1]
		tempo = int(f.readline())
		p = MusicData(name, features, tempo)
		music_data.append(p)
	f.close()
	return music_data

# Display current db in memmory
def showDB(music_data):
	for i in range(len(music_data)):
		print music_data[i].name
		print music_data[i].MFCC_features
		
# Save changes in the db file
def syncDB(music_data):
	f = open("music.db", "w")
	f.write(str(len(music_data)))
	for i in range(len(music_data)):
		f.write("\n")
		f.write(music_data[i].name)
		f.write("\n")
	#	for j in range(len(music_data[i].MFCC_features)):
#			print music_data[i].MFCC_features[j]
	#		f.write(str(music_data[i].MFCC_features[j]))
		f.write("%s" % music_data[i].MFCC_features)
		f.write("%s" % music_data[i].tempo)
#		f.write("\n")
	f.close()
	
class MusicData:
	name = ""
	MFCC_features = []
	tempo = 0
	
	def __init__(self, name, features, tempo):
		self.name = name
		self.MFCC_features = features
		self.tempo = tempo
