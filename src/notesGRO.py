
#User imports
import globals
import player
import enemy
import mouse
import tunnel

from pandac.PandaModules import Point3 #@UnresolvedImport

fh = open(globals.LEVEL_1_DIR+ "/newdoneit.gro","r")
igot = fh.readlines()

track = 0
midistuffers = []
numtracks = []



for line in igot:
    	if "tempor" in line:
                tempo = line.lstrip("T0.0000 -tempor:")[:]
                print "tempo: " + tempo
                globals.TEMPO = float(tempo)
	if "track" in line:
		print line
                track = line.lstrip("#track ")[:2]
		track.strip()
		numtracks.append({int(track):str(line.lstrip("#track ")[2:])})
	if "T" in line:
		tokens = line.split()
		for tok in tokens:
			if "T" in tok:
				T = tok.lstrip("T")
			elif "V" in tok:
				V =  tok.lstrip("V")
			elif "K" in tok:
				K =  tok.lstrip("K")
			elif "P" in tok:
				P =  tok.lstrip("P")
			elif "U" in tok:
				U =  tok.lstrip("U")
			elif "L" in tok:
				L  = tok.lstrip("L")
				info = [T,track,K,P,U,L]
				midistuffers.append(info)
	else:
		continue

class myMidiNote:
	def __init__(self):
		self.file = None
		self.x = 0
		self.y = 0
		self.z = 0
		self.start = None
		self.ob = None
		self.channel = 0
		self.velocity = 0
		self.pitch = 0
		self.duration = 0
		self.name = "empty"

	def __repr__(self):
		return "myMidiNote:"+str(self.start)

	def create(self, name, posx, posy, posz,time,channel,key,pitch,duration,vel):
		self.name = name
		self.x = posx
		self.y = posy
		self.z = posz
		self.channel = channel
		self.velocity = vel
		self.pitch = pitch
		self.start = time
		self.duration = duration
		#print self

		
time = 0.0
duration = 0.0
vel = 0.0
pitch = 0
channel = 0
d = []


count = 0
for track in midistuffers:
	midinote = myMidiNote()		

        name = str(track[1]),'-',track[0],track[5],track[3],track[4]
	midinote.create(name, 0,0,0, float(track[0]),int(track[1]),float(track[2]),int(track[3]),float(track[4]),float(track[5]))
	d.append(midinote)
	count += 1

	#print(count, midinote)


d.sort(key = lambda myMidiNote:myMidiNote.start)
globals.NOTESGRO = d
globals.NUMBERTRACKS = numtracks

class notesGRO():
	def __init__(self,path):
		"""Constructor"""
		#We create some elements to use with our SAX reader
		self.path = globals.LEVEL_1_DIR
		self.tmpEnemy = None
		self.changer = None
		self.numEnemy = 0
		self.actStage = 0

	def Create(self):
		for it in globals.NOTESGRO:
			#print it
			self.tmpEnemy = enemy.Enemy()
			self.tmpEnemy.stageBelong = "test"
			self.tmpEnemy.model = self.path + "/ene/" + "ene01.egg"
			self.tmpEnemy.time = it.start
			self.tmpEnemy.startPos = Point3( float(500), float(-100) ,float(100) )
			#self.tmpEnemy.startPos = Point3(float(it.pitch), float(10), float(1) )
			
			self.tmpEnemy.sound = self.path + "/snd/" + "dene01.mp3"
			self.tmpEnemy.scorePoints = 100

			tempo = float(it.pitch + it.velocity)
			
			#tmpPoint = Point3( float(tempo), float(10) ,float(1) )
			tmpPoint = Point3( float(1), float(1) ,float(1) )
			self.tmpEnemy.points.append(tmpPoint)
			time = it.duration
			self.tmpEnemy.times.append(time)
			
			tmpName = 'malo'+str(self.numEnemy)
			self.tmpEnemy.actor.setTag('enemy',tmpName)
			globals.ENEMIES[tmpName] = self.tmpEnemy
			globals.ENEMIES_MOUSE[tmpName] = self.tmpEnemy
			self.numEnemy += 1
			self.tmpEnemy = None
	


