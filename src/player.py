#!/usr/bin/env python
#coding: iso-8859-1

"""Documentation for player.py

This file contains the player class,
with everything he needs to work.

project -- Rez: The Clone
author -- Edwood Grant
organization -- Binhex Tw. 
version -- 1.00
since -- 7/07/2007 10:16:25
"""

#Panda specific imports for this module
from pandac.PandaModules import *
from direct.actor import Actor
#To handle Actors
#To handle intervals
from direct.interval.IntervalGlobal import * 
from pandac.PandaModules import CollisionNode, CollisionSphere

#User imports
import shadows #@UnusedImport
import globals

class rezChar:
    """Class rezChar.
    
    Defines and implements a RezChar. Nothing special just a character 
    in 0 position and animated, so it looks like its running
    """
    def __init__(self):
        """Constructor
        
        We are not doing anything special here, only when we decide to init        
        """
        self.x = 0
        self.y = 0
        self.z = 0
        self.jump = 960
        self.jumping = 176
        self.TIMES = 1000000
        self.color = 0

    def init(self):
        """Init Function
        
        Initializes and runs everything related to actor
        """
        ## Variables
        self.start = Point3(0, 0, 25)
        self.playrate = 1.5
        
        # Loading and creating the actor
        self.node = render.attachNewNode("Jugador") 
        self.node.setPos(self.start)
        self.actor = Actor.Actor()
        self.actor.loadModel(globals.CHAREGG)
        self.actor.loadAnims({"Run":globals.CHAREGG})
        self.actor.bindAnim('Run')
        self.actor.loop('Run')
        #Setting the actor playrate to match with music and everything
        self.actor.setPlayRate(self.playrate + (globals.RATE - 1), 'Run')
        # Create a collsion node for this object.
        self.cNode = CollisionNode('frowney')
        # Attach a collision sphere solid to the collision node.
        self.cNode.addSolid(CollisionTube(0, 0, -35,0.0,0.0, 100,35))
        # Attach the collision node to the object's model.
        self.frowneyC = self.actor.attachNewNode( self.cNode)
        # Set the object's collision node to render as visible.
        #self.frowneyC.show()

#        self.boxBody = OdeBody(globals.WORLD)
#        self.mass = OdeMass()
#        self.mass.setBoxTotal(1980,100.0,100.0,100.0)
#
#        self.boxBody.setMass(self.mass)
#        self.boxBody.setPosition(self.start)
#
#        self.boxGeom = OdeBoxGeom(globals.PhysicsSpace, 100.0,100.0,100.0)
#        self.boxGeom.setCollideBits(BitMask32(0x00000002))
#        self.boxGeom.setCategoryBits(BitMask32(0x00000001))
#        self.boxGeom.setBody(self.boxBody)
#        globals.PhysicsBox.append( (self.actor, self.boxBody) )

        #Setting scale and position to the model
        self.actor.setScale(1.0, 1.0, 1.0)
        self.actor.setPos(self.node.getPos())
        self.actor.setH(90)
        self.actor.reparentTo(self.node)

        self.parallel = self.actor.posInterval(1.0,Point3(0.0,0.0,0.0))
#        self.boxBody.setQuaternion(self.actor.getQuat())
#        self.boxBody.setPosition(self.start)
#        #Update task


        base.cTrav.addCollider( self.frowneyC, globals.PhysicsBox)
        self.z = 0

        malament = max(globals.NUMBERTRACKS)
        self.jump = 480
        for t in malament:
            self.numtracks = int(t)
        print self.numtracks
        self.camTask = taskMgr.add(self._update, 'Player-Follow', priority=20)
#

    def _update(self, task):
        if not self.parallel.isPlaying():
            if (globals.KEYBOARD.keyMap["left"]!=0):
                if self.y < self.numtracks:
                    self.y += 1
                    self.parallel = self.actor.posInterval(float(globals.TEMPO/self.jump),Point3(self.x*100,self.y*100,self.z))
                    self.parallel.start()

            elif (globals.KEYBOARD.keyMap["right"]!=0):
                if self.y > 0:
                    self.y -= 1
                    self.parallel = self.actor.posInterval(float(globals.TEMPO/self.jump),Point3(self.x*100,self.y*100,self.z))
                    self.parallel.start()

                ##
                ##
        ##
        ##
        if (globals.KEYBOARD.keyMap["forward"]!=0):
            print "yerp"
            if self.z < 1:
                self.z += 1
                self.myparallel = Sequence(
                                        ProjectileInterval(self.node,startPos = Point3(self.x,self.y,(self.z)),endPos = Point3(self.x+self.jumping,self.y,(self.z)+self.jumping),duration =float(globals.TEMPO/self.jump), gravityMult = 1),
                                        ProjectileInterval(self.node,startPos = Point3(self.x+self.jumping,self.y,(self.z)+self.jumping), endPos = Point3(self.x,self.y,(self.z)),duration =float(globals.TEMPO/self.jump), gravityMult = 1))
                self.z = 0
                self.myparallel.start()
        elif (globals.KEYBOARD.keyMap["backward"]!=0):
            self.color += 1
            if self.color <= self.numtracks:
                self.actor.setColor(float(globals.colors[self.color].getX()),
                        float(globals.colors[self.color].getY()),
                        float(globals.colors[self.color].getZ()),
                        float(1.0))
            else:
                self.color = 0

        #print self.x,self.y,self.z, self.numtracks, globals.KEYBOARD.keyMap


        #self.boxBody.setQuaternion(self.actor.getQuat())
        #self.boxBody.addForce(self.x,self.y,0.0)
        #self.boxBody.setPosition(float(self.x),float(self.y),float(self.z))
        return task.cont
