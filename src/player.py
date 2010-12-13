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
        self.z = 50
        self.jump = 0
        self.jumping = False
        self.TIMES = 1000000
    def init(self):
        """Init Function
        
        Initializes and runs everything related to actor
        """
        ## Variables
        self.start = Point3(0, 0, 50)
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
        self.actor.setScale(0.5, 0.5, 0.5)
        self.actor.setPos(self.node.getPos())
        self.actor.setH(90)
        self.actor.reparentTo(self.node)

#        self.boxBody.setQuaternion(self.actor.getQuat())
#        self.boxBody.setPosition(self.start)
#        #Update task
#        self.camTask = taskMgr.add(self._update, 'Player-Follow', priority=35)
#

    def _update(self, task):
        if (globals.KEYBOARD.keyMap["left"]!=0): self.y =1 * self.TIMES
        elif (globals.KEYBOARD.keyMap["right"]!=0): self.y =-1 * self.TIMES
        elif (globals.KEYBOARD.keyMap["forward"]!=0): self.x =1 * self.TIMES
        elif (globals.KEYBOARD.keyMap["backward"]!=0): self.x =-1 * self.TIMES

        self.actor.setHpr(90,0,0)
        #self.boxBody.setQuaternion(self.actor.getQuat())
        #self.boxBody.addForce(self.x,self.y,0.0)
        #self.boxBody.setPosition(float(self.x),float(self.y),float(self.z))
        self.x = 0
        self.y = 0
        self.z = 0
        print self.boxBody.getPosition()
        return task.cont
