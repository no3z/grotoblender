#!/usr/bin/env python
#coding: iso-8859-1

"""Documentation for bullet.py

Contains the bullet class which 
follow enemies and destroys them

project -- Rez: The Clone
author -- Edwood Grant
organization -- Binhex Tw. 
version -- 1.00
since -- 7/07/2007 13:33:42
"""

#Panda specific imports for this module
from pandac.PandaModules import * 
#To handle events
from direct.showbase import DirectObject

#User imports
import globals

class Bullet(DirectObject.DirectObject):
    def __init__(self, actorEnd, pos):
        """Constructor
        
        We are not doing anything special here, only when we decide to init  
        right here we are only creating some variables     
        """
        #The actor we want to reach to
        self.actorGoal = actorEnd
        self.pos = pos
        #Given a position (the first bullet, the sedond, the third, etc...
        #We initialize the bullet function with init function
        taskMgr.doMethodLater(pos * 0.42, self.init, 'init') 
        
    def init(self, task):
        """Init Function
        
        Initializes and runs everything related to mouse
        """
        #Tries to load that sound according to its postition,
        #However its not necessary to have all sund so if it fails, 
        #load the one that would correspond to its position
        try:
            self.snd = loader.loadSfx(globals.SHOOTSOUNDS[self.pos]) 
        except:
            sndToLoad = self.pos % len(globals.SHOOTSOUNDS)
            self.snd = loader.loadSfx(globals.SHOOTSOUNDS[sndToLoad]) 
        self.snd.play()
        
        # Defines and loads the model...
        self.node = render.attachNewNode("Bullet") 
        self.node.setPos(0, 0, 0)
        self.model = loader.loadModelCopy(globals.BULLETEGG) 
        self.model.setScale(0.2)
        #Enables transparency to the model
        self.model.setTransparency(1)
        self.node.setTransparency(1)
        #Make it visible
        self.model.setPos(self.node.getPos())
        self.model.reparentTo(self.node)

        #Initializes the collision handler event
        #Enabling 'into-%in' collision types
        self.colEvent = CollisionHandlerEvent() 
        self.colEvent.addInPattern('into-%in')
        #Defining a collision node, a shpere of 20 units diameter
        self.colNode = CollisionNode('Bullet') 
        #Seting "from" bitmask to 0
        self.colNode.setFromCollideMask(BitMask32.bit(0)) 
        self.colNode.addSolid(CollisionSphere(0, 0, 0, 20)) 
        self.colNodePath = self.model.attachNewNode(self.colNode)
        #Adding the collider to the main traverser, and assign its event handler     
        base.cTrav.addCollider(self.colNodePath, self.colEvent) 
        #We add an accept to chekeck every time our collision into-%in occurs
        self.accept('into-enemyCol', self._enemyCol)
        
        #Update Task
        self.updateTask = taskMgr.add(self._update, 'Bullet-Update') 
        self.updateTask.last = 0
        #Since this is a task return as task.done
        return task.done
    
    def _enemyCol(self, collEntry):
        """EnemyCol event
        
        Trigger every time this bullet collide with something inside enemyCol
        """
        #We obtain the tag fo the object and attempt to find it
        obj = collEntry.getIntoNodePath().getParent()
        enemy_name = obj.getNetTag('enemy')
        obj = globals.ENEMIES[enemy_name]
        #If it was found, then kill the enemy
        if obj != None and hasattr(obj, 'die'):
            obj.die()
            
    def _update(self, task):
        #Dt handling to make movement independent of framerate
        dt = task.time - task.last
        task.last = task.time
        #Check if actor node is empty, if its not, update position
        #If it is empy, then it was destroyed, so theres no reason to be here anymore
        if not self.actorGoal.node.isEmpty():
            #Look towards him and move relative
            self.model.lookAt(self.actorGoal.node.getPos())
            self.model.setPos(self.model, 0, 50000 * 0.21 * dt, 0)
        else:
            #Remove node, delete self and end task
            self.node.removeNode()
            del self
            return task.done
        return task.cont
