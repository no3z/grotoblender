#!/usr/bin/env python
#coding: iso-8859-1

"""Documentation for world.py

The file world.py represents the first event that is executed by main.py.
This one does all the heavy-duty job here, not main ;).

project -- Rez: The Clone
author -- Edwood Grant
organization -- Binhex Tw. 
version -- 1.00
since -- 7/07/2007 19:30:33
"""

#Default Imports
import sys

from pandac.PandaModules import loadPrcFileData
loadPrcFileData("", "audio-cache-limit 128") #Audio Cache Limit
loadPrcFileData("", "win-size 640 480") #Audio Cache Limit
#loadPrcFileData("", "fullscreen 1") #Fullscreen

#Panda specific imports for this module
from pandac.PandaModules import *
#To handle events
from direct.showbase import DirectObject 
#To handle OnScreen Text
from direct.gui.DirectGui import OnscreenText 

#Other Imports
#To handle XML (SAX)
from xml.sax import make_parser

#User imports
import camera
import globals
import xmlr
import score
import notesGRO

class World(DirectObject.DirectObject):
    """Class world.
    
    The class that really runs and manages everything
    """
    def __init__(self):
        """Constructor"""
        #Create a Tittle
        self.title = OnscreenText(text="deBlock2 experimental",
                                  style=1, fg=(1, 1, 1, 1),
                                  pos=(0.95, -0.95), scale=.05)
        
#        self.credits = OnscreenText(text='Credits:\nCreated by Italo F. Capasso B. AKA "Edwood Grant"\n no3productionz@gmail.com,
#                                    style=1, fg=(1, 1, 1, 1),
#                                    pos=(-1.25, -0.725), scale=.05, align=TextNode.ALeft)

        #Set the framerate meter, uncomment this if you want to see fps
        base.setFrameRateMeter(True) 
        #Change Background Color to black
        base.setBackgroundColor(0, 0, 0) 
        
        #Disable Standard Mouse
        base.disableMouse() 
        props = WindowProperties()
        props.setCursorHidden(True)
        #Set a title for the window
        props.setTitle('deBlock2')
        base.win.requestProperties(props) 
        
        
#        self.world = OdeWorld.OdeWorld()
#        globals.WORLD = self.world
#        self.world.setGravity(0, 0, -9.81)
#
#        self.world.initSurfaceTable(1)
#        self.world.setSurfaceEntry(0, 0, 1500, 0.6, 9.1, 0.9, 0.00001, 0, 0.002)
#
#        self.space = OdeHashSpace.OdeHashSpace()
#        self.space.setAutoCollideWorld(self.world)
#        self.contactgroup = OdeJointGroup()
#        self.space.setAutoCollideJointGroup(self.contactgroup)
#
#        globals.PhysicsSpace = self.space
#
#        self.cm = CardMaker("ground")
#        self.cm.setFrame(-5000, 5000, -5000, 5000)
#        self.ground = render.attachNewNode(self.cm.generate())
#        self.ground.setPos(0, 0, 0); self.ground.lookAt(0, 0, -1)
#        self.ground = OdePlaneGeom(self.space, Vec4(0, 0, 1, 0))
#        self.ground.setCollideBits(BitMask32(0x00000001))
#        self.ground.setCategoryBits(BitMask32(0x00000002))
        #Enable Particles
        base.enableParticles()
        
        #Recreate a simple Fog
        self.fog = Fog('distanceFog') 
        self.fog.setColor(0, 0, 0)
        self.fog.setExpDensity(.0003)
        #Assign fog to render
        render.setFog(self.fog) 
        
        #Set camera lens Far distance
        base.camLens.setFar(7500) 
        #Initialize traverser
        base.cTrav = CollisionTraverser()         

        #Initializes the XML parser and loads level1       
        handler = xmlr.RezHandler(globals.LEVEL_1_DIR)
        parser = make_parser()
        parser.setContentHandler(handler)
        parser.parse(open(globals.LEVEL_1_XML))  
                           
        #Setup Camera       
        cam = camera.Camera()
        cam.setToFollow(globals.PLAYER.actor)
        
        #Setup Score
        score.Score()
        
        #taskMgr.doMethodLater(0.2, self.physicsCollision, "Physics Simulatior")
        
        #Accept Events
         
        
    def physicsCollision(self, task):
        self.space.autoCollide()
        self.world.quickStep(globalClock.getDt())
        for np, body in globals.PhysicsBox:
            np.setPosQuat(render, body.getPosition(), Quat(body.getQuaternion()))
            #print body.getPosition()
        self.contactgroup.empty()
        #print render.getNumChildren(),render.getNumNodes()
        return task.cont
    
    def run(self):
        """Manages and runs everything."""
        #Action
        run() 
