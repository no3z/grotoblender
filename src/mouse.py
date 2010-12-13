#!/usr/bin/env python
#coding: iso-8859-1

"""Documentation for mouse.py

This file contains the mouse class, manages everything
related to mouse events and movement

project -- Rez: The Clone
author -- Edwood Grant
organization -- Binhex Tw. 
version -- 1.00
since -- 7/07/2007 10:36:51
"""

#Panda specific imports for this module
from pandac.PandaModules import * 
#To handle events
from direct.showbase.DirectObject import DirectObject 

#User imports
import bullet
import lock
import globals

class Mouse(DirectObject):
    """Class Mouse.
    
    Defines and implements mouse handling, like clicks and stacking enemies
    """
    def __init__(self):
        """Constructor
        
        We are not doing anything special here, only when we decide to init        
        """
        pass
        
    def init(self):
        """Init Function
        
        Initializes and runs everything related to mouse
        """
        
        #We load and store some models and sounds neede for our mouse
        self.node = loader.loadModel(globals.MOUSEEGG) 
        self.node.setScale(0.1, 1, 0.125)
        self.node.setBillboardPointEye()
        self.node.reparentTo(render2d) 
        #Click sound and lock sound
        self.clicksound = loader.loadSfx(globals.CLICKSOUND) 
        self.locksound = loader.loadSfx(globals.LOCKSOUND)                
        
        #The stack, just a simple array
        self.stack = []        
        
        #Since we are using collision detection to do picking, we set it up like
        #any other collision detection system with a traverser and a handler
        #Make a traverser
        self.picker = CollisionTraverser() 
        #Make a handler           
        self.pq = CollisionHandlerQueue() 
        #Make a collision node for our picker ray
        self.pickerNode = CollisionNode('mouseRay') 
        #Attach that node to the camera since the ray will need to be positioned
        #relative to it
        self.pickerNP = camera.attachNewNode(self.pickerNode) 
        #Everything to be picked will use bit 1. This way if we were doing other
        #collision we could seperate it
        self.pickerNode.setFromCollideMask(BitMask32.bit(1)) 
        #We dont want any 'into' collisions with this ray, 
        #so we put it somewhere else we'll also stop having the 
        #collide(error): Invalid attempt to detect collision from CollisionSphere into CollisionRay!
        #Since sphere won try to collide into this ray
        self.pickerNode.setIntoCollideMask(BitMask32.bit(2)) 
        
        #Make our ray
        self.pickerRay = CollisionRay()               
        self.pickerNode.addSolid(self.pickerRay)      #Add it to the collision node
        #Register the ray as something that can cause collisions
        self.picker.addCollider(self.pickerNP, self.pq)
        #self.picker.showCollisions(render)
    
        self.accept("mouse1", self.click)
        self.accept("mouse1-up", self.clickUp)
        #Update Task
        self.updateTask = taskMgr.add(self._update, 'Update-Mouse') 

    def _update(self, task):
        """Task function
        
        Updates the mouse state and manages dragging events
        """
        #If we have a mouse
        if base.mouseWatcherNode.hasMouse(): 
            #get the mouse position
            mpos = base.mouseWatcherNode.getMouse() 
            x = mpos.getX()
            y = mpos.getY()
            #Set the position of the ray based on the mouse position
            self.pickerRay.setFromLens(base.camNode, x, y) 
            #Set the position of the node too
            self.node.setPos(x, 0, y)
        
        #Traverse through everything
        self.picker.traverse(render) 
        if self.pq.getNumEntries() > 0:
            #Sort entries, find the first entry, and get his tag so he can be searched
            self.pq.sortEntries()            
            mod = self.pq.getEntry(0).getIntoNodePath().getParent()
            enemy_name = mod.getNetTag('enemy')
            #Try to find the enemy, if not, well nothing happens
            try:
                actor = globals.ENEMIES_MOUSE[enemy_name]
                #Drag must be valid to even consider locking someone
                if len(self.stack) < globals.MAXSTACK and self.drag == True:
                    #Create lock object
                    lock.Lock(actor)
                    #play sound effect
                    self.locksound.play()
                    #Add it to the stack, since we are pressing here the mouse button
                    self.stack.append(actor)
                    #Now we delete from our mouse enemies list, since he's locked already
                    del globals.ENEMIES_MOUSE[enemy_name]
            except:
                pass
        return task.cont
    
    def click(self):
        """click function
        
        Plays a sound and enables drag
        """
        self.drag = True
        self.clicksound.play()

    def clickUp(self):
        """clickUp function
        
        Disables drag and fires bullets
        """
        self.drag = False
        #Goes through that stack and creates bullets
        #Sending the enemy as parameter and the position in the stack
        for i in range(len(self.stack)):
            bullet.Bullet(self.stack[i], i)
        #Since we have fired everything, empty the stack
        self.stack = []
