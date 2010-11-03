import Blender
from Blender import Mesh
import bpy
import BPyAddMesh

fh = open("/home/no3z/popo.gro","r")

igot = fh.readlines()

midistuffers = []

    
for line in igot:
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
                        info = [T,V,K,P,U,L]
                        print info
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
			print self


		
d = {}
time = 0.0
duration = 0.0
vel = 0.0
pitch = 0
channel = 0

count = 0
for track in midistuffers:
	midinote = myMidiNote()		
	name = str(track[1]),'-',track[0],track[5],track[3],track[4]
	print(track)
	midinote.create(name, 0,0,0, float(track[0]),int(track[1]),float(track[2]),int(track[3]),float(track[4]),float(track[5]))
	d[name] = midinote	
	count += 1
		
	print(count, midinote)	


def add_mymesh(x1,x2,y1,y2):
	verts = []
	faces = []		
	verts.append([x1,y1,0])
	verts.append([x1,y2,0.0])
	verts.append([x2,y2,0.0])
	verts.append([x2,y1,0.0])
	faces.append([0,1,2,3])
	return verts, faces


mat = Blender.Material.New("newMat")
mat.rgbCol = [0.97,0.88,0.88]
mat.setAlpha(0.33)
mat.emit = 0.7
mat.setAdd(0.8)


sce = bpy.data.scenes.active
for k,v in d.items():
	y = 0.0 
	x = 0.0
	z = 0.0
	x2 = v.duration
	y2 = v.velocity/64;
	str = ''
	for n in v.name:
		str += n
	

	 #print(x,x2,y,y2,str,v.name)
	verts, faces = add_mymesh(x,x2,y,y2)
	BPyAddMesh.add_mesh_simple(str, verts, [], faces) 
	
	timeline = v.start
	time = v.start * 25
	duration = 	v.duration * 25
	vel = v.velocity
	pitch = 		v.pitch
	channel = v.channel

		
					
	obj = Blender.Object.Get(str)
	if obj:
		temp = obj.getLocation()
		temp = [timeline + temp[0], ((channel-1))*2.169 + temp[1], v.velocity/127]
		print temp
		
		obj.setMaterials([mat])
		obj.colbits = (1<<0)
		obj.setLocation(temp)
		obj.addProperty("channel",channel,'INT')
		obj.addProperty("time",time,'FLOAT')
		obj.addProperty("vel",vel,'FLOAT')
		obj.addProperty("pitch",pitch,'INT')
		obj.addProperty("duration",duration,'FLOAT')
		obj.rbFlags = 81924

		action = Blender.Ipo.New('Object',str)
#				
		action.addCurve('LocY')
		action.addCurve('LocZ')
#		action.addCurve('RotX')
#				
		posY = action.getCurve('LocY')
		posZ = action.getCurve('LocZ')
#		Spin = action.getCurve('RotX')

#			
		

		posY[0] = temp[1]
#		posY[time] = vel + temp[1]
#		posY[time+duration] = posY[time]
#		posY[time+duration+vel] = posY[0] #0 - dist

		posZ[0] = temp[2]
		posZ[time-0.2] =	posZ[0]
		posZ[time] = pitch/16.0
		posZ[time+duration] = posZ[time]
		posZ[time+duration+(vel/127)*(pitch/127)] = posZ[0]
				
#		Spin[0] = 0
#		Spin[time] = vel 
#		Spin[time+duration] = Spin[time]
#		Spin[time+duration+vel+pitch/320] = 0
				
		obj.setIpo(action)

Blender.Redraw()

				
		
