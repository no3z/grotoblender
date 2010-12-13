#!/usr/bin/env python
#coding: iso-8859-1

"""Documentation for enemy.py

Details and summary here.

project -- Rez: The Clone
author -- Edwood Grant
organization -- Binhex Tw. 
version -- 1.00
since -- 7/07/2007 11:20:27
"""

#Standard imports
from random import random

#Panda specific imports for this module
from pandac.PandaModules import *

#To handle actors
from direct.actor import Actor

#To handle intervals
from direct.interval.IntervalGlobal import * 

#To handle particles
from direct.particles.Particles import Particles 
from direct.particles.ParticleEffect import ParticleEffect 


colors = [  VBase4(0   , 0.0, 1.0, 1.0),
            VBase4(0.0 , 1.0, 1.0, 1.0),
            VBase4(1   , 0.0, 1.0, 1.0),
            VBase4(1   , 0.0, 0.33, 1.0),
            VBase4(1   , 0.330, 0.0, 1.0),
            VBase4(1   , 0.0, 0.0, 1.0),
            VBase4(0.33   , 0.033, 0.0, 1.0),
            VBase4(0.2   , 0.90, 0.20, 1.0),
            VBase4(0.33   , 0.053, 0.60, 1.0),
            VBase4(1   , 0.330, 0.70, 1.0),
            VBase4(0.1   , 0.30, .70, 1.0),
            VBase4(0.37   , 0.013, 1.0, 1.0),
            VBase4(0.55   , 0.20, 0.20, 1.0),
            VBase4(0.17   , 0.53, 0.60, 1.0)
            ]

#User imports
import globals #@UnusedImport

class Enemy:
    def __init__(self):
        """Constructor
        We are not doing anything special here, only when we decide to init  
        right here we are only creating some variables     
        """
        self.model = None
        self.time = None
        self.startPos = None
        self.stageBelong = None
        self.points = []
        self.times = []
        self.sound = None
        self.pos = None
        self.dead = False
        self.scorePoints = 0
        self.actor = Actor.Actor();
        self.node = render.attachNewNode("Enemy") 
        self.loop = False
        self.duration = 0
        self.channel = 0
        self.velocity = 0
        self.pitch = 0

    def init(self):
        """Init Function
        
        Initializes and runs everything related to enemy
        """

        #Creates a task that will begin according to the time imposed in xmlR
        taskMgr.doMethodLater(self.time, self._init, 'Start-Later-Enemy') 

    def _particle(self, pos):
        """Particle function
        
        This function will create particles when the enemy 
        is destroyed, just a fancy visual effect. Takes pos 
        as the argument from where to start the effect
        """
        #This code was created from the particle panel example in Panda
        #Then it was tweaked a little to handle random colors
        #TODO:It would still be good to comment this code so you can understand the meaning of all these functions 
        self.part = ParticleEffect()
        self.part.reset()
        self.part.setPos(pos)
        self.part.setHpr(0.000, 0.000, 0.000)
        self.part.setScale(75.000, 75.000, 75.000)
        p0 = Particles('particles-1')
        # Particles parameters
        p0.setFactory("PointParticleFactory")
        p0.setRenderer("LineParticleRenderer")
        p0.setEmitter("SphereVolumeEmitter")
        p0.setPoolSize(500)
        p0.setBirthRate(0.010)
        p0.setLitterSize(500)
        p0.setLitterSpread(0)
        p0.setSystemLifespan(10.0000)
        p0.setLocalVelocityFlag(1)
        p0.setSystemGrowsOlderFlag(0)
        # Factory parameters
        p0.factory.setLifespanBase(2.0000)
        p0.factory.setLifespanSpread(0.0000)
        p0.factory.setMassBase(1.0000)
        p0.factory.setMassSpread(0.0000)
        p0.factory.setTerminalVelocityBase(300.0000)
        p0.factory.setTerminalVelocitySpread(0.0000)
        # Point factory parameters
        # Renderer parameters
        p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT) 
        p0.renderer.setUserAlpha(1.00)
        #Some extra light parameters for random colors
        #This is NOT part of the generated code from particle panel
        self.lightR = random()
        self.lightG = random()
        self.lightB = random()
        # Line parameters we also set the random color here
        p0.renderer.setHeadColor(Vec4(self.lightR, self.lightG, self.lightB, 1.00)) 
        p0.renderer.setTailColor(Vec4(self.lightR, self.lightR, self.lightB, 1.00)) 
        p0.renderer.setLineScaleFactor(10.00)
        # Emitter parameters
        p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE) 
        p0.emitter.setAmplitude(1.0000)
        p0.emitter.setAmplitudeSpread(0.0000)
        p0.emitter.setOffsetForce(Vec3(0.0000, 0.0000, 0.0000)) 
        p0.emitter.setExplicitLaunchVector(Vec3(1.0000, 0.0000, 0.0000)) 
        p0.emitter.setRadiateOrigin(Point3(0.0000, 0.0000, 0.0000)) 
        # Sphere Volume parameters
        p0.emitter.setRadius(1.0000)
        self.part.addParticles(p0)
        
        #The code from particle panel ends here, no we create a 
        #sequence for the particle (they star and then disappear
        t = ParticleInterval(self.part, render, 0, 0, 2.0) 
        u = Sequence(t, Func(self.part.removeAllParticles)) 
        u.start()
        
        #we also create a point light with the same random color to make it look nicer
        #In the same position of course
        self.plight = PointLight('Particle-Light')
        self.plight.setColor(VBase4(self.lightR, self.lightG, self.lightB, 1))
        self.dlnp = render.attachNewNode(self.plight) 
        self.dlnp.setPos(pos)
        render.setLight(self.dlnp) 
        taskMgr.add(self._dimLight, 'DimLight') 
        
    def _dimLight(self, task):
        """Task function
        
        It will dim the particle light until its off.
        """
        #If the colors are all dimmed remove the light and end task
        if self.lightR <= 0 and self.lightG <= 0 and self.lightB <= 0:
            render.clearLight(self.dlnp) 
            return task.done
        else:
        #Otherwise... dim
            if self.lightR > 0:
                self.lightR -= 0.01
            if self.lightG > 0:
                self.lightG -= 0.01
            if self.lightB > 0:
                self.lightB -= 0.01
        #Set color and continue
        self.plight.setColor(VBase4(self.lightR, self.lightG, self.lightB, 1)) 
        return task.cont


    def _init(self, Task):
        """Task function
        
        This will be executed after the time parameter, 
        it will start all of his models, intervals and move on.
        """        
        # Defining and loading the actor
        self.actor.loadModel(self.model)

        #Enable transparency to the enemy
        self.actor.setTransparency(1)
        self.node.setTransparency(1)
        
        #Loading its destruction sound
        self.snd = loader.loadSfx(self.sound) 
        
        #Make it visible
        self.actor.setPos(self.node.getPos())
        self.actor.reparentTo(self.node) 
        
        #Collisions
        #Create a collision solid for this model
        self.cNode = CollisionNode('enemyCol')
        #Setting "from" bitmask to 0
        self.cNode.setFromCollideMask(BitMask32.bit(0))
        self.cNode.addSolid(CollisionSphere(0, 0, 0, 35))
        self.cNodePath = self.actor.attachNewNode(self.cNode)
        #Show collision solid
        self.startPos = Point3(2000, float(self.channel)*100, 50 + float(self.pitch)/127*2.27 )


#        self.boxBody = OdeBody(globals.WORLD)
#        self.mass = OdeMass()
#        self.mass.setSphere(self.velocity/64,2.0)
#        self.boxBody.setMass(self.mass)
#        self.boxBody.setPosition(self.startPos)
#
#        self.boxBody.setLinearVel(float(-self.velocity)*10,float(self.pitch-64),float(-1000))
#        self.boxBody.setAngularVel(float(self.pitch)*100,0.0,float(-self.pitch)*100)
#
#        self.boxGeom = OdeSphereGeom(globals.PhysicsSpace, 50)
#        self.boxGeom.setCollideBits(BitMask32(0x00000001))
#        self.boxGeom.setCategoryBits(BitMask32(0x00000001))
#        self.boxGeom.setBody(self.boxBody)
#        globals.PhysicsBox.append( (self.actor, self.boxBody) )

        self.duration += self.duration * (self.velocity)/32

        self.actor.setColor(float(colors[self.channel].getX()),
                            float(colors[self.channel].getY()),
                            float(colors[self.channel].getZ()),
                            float(self.velocity/127))
        #Set starting position
        self.node.setPos(self.startPos)
        self.endPos = Point3(float(self.pitch)*5, float(self.channel)*100, float(self.pitch)*1.25)
        #self.mySeq = Sequence()
        #We iterate thought the points, creating a lerpPosinterval and
        #appending each one to the sequence, with its respective duration
        #j = 0
        #for i in self.points:
        #    int = LerpPosInterval(self.node, self.times[j], i)
        #    self.mySeq.append(int)
        #    j += 1

        #Since we dont want enemies to "pop up" onto the screen
        #we create a small scale interval
        #self.grow = LerpScaleInterval(self.node, 0.25, 1.0, 0)
        #We create then a parallel with grow to go along with the sequenece

        #self.parallel = Parallel(self.grow, self.mySeq)

        self.parallel = ProjectileInterval(self.node,startPos = self.startPos,endPos = self.endPos,duration = self.duration, gravityMult = 16.9)
        self.parallel.start()
        #If is set to loop, loop the parallel (Usually a changer)
#        if self.loop:
#            self.parallel.loop()
#        else:
#            self.parallel.start()

        #Update task
        self.updateTask = taskMgr.add(self._update, 'Enemy-Update')
        #Since this is a task, we are done here
        return Task.done


#    def _update(self, task):
#        self.duration = float(float(self.duration) - float(globalClock.getDt()))
#        if self.duration < 0:
#            #If we are making fancy colors, we have to
#            # be sure it was killed by the die function
#            if self.dead == True:
#                #Call nice particles and sound
#                self._particle(self.pos)
#                self.snd.play()
#                #Update Score!!
#                globals.SCORE += self.scorePoints
#            #Either way we remove the node and delete ourselves
#            globals.PhysicsBox.remove( (self.actor, self.boxBody) )
#            self.node.removeNode()
#            del self
#            return task.done
#        else:
#            #This is needed by bullets to be able to follow it
#            self.pos = self.node.getPos()
#        return task.cont


    def _update(self, task):
        """Task function

        This will update the state of the enemy
        """
        #print str(globalClock.getDt()),self.duration
        self.duration = float(float(self.duration) - float(globalClock.getDt()))
        #Check if the parallel is still playing
        #print self.duration
        if not self.parallel.isPlaying():
            #Either way we remove the node and delete ourselves
            #globals.PhysicsBox.remove( (self.actor, self.boxBody) )
            #print len(globals.PhysicsBox)
            self.node.removeNode()
            del self
            print "dead"
            return task.done

        return task.cont
    
    def die(self):
        """Task function
        
        Kills the enemy
        """  
        #Finish the interval and set dead to true
        self.dead = True    
        self.parallel.finish()
        
