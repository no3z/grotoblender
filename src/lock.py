#!/usr/bin/env python
#coding: iso-8859-1

"""Documentation for lock.py

This file contains the lock class, used for displaying
locks over selected enemies.

project -- Rez: The Clone
author -- Edwood Grant
organization -- Binhex Tw. 
version -- 1.00
since -- 7/07/2007 10:06:55
"""

#Panda specific imports for this module
from pandac.PandaModules import *
#User Imports
import globals


class Lock:
    """Class Lock.
    
    Defines and implements a lock, which is a simple model that 
    locks and follows a predefined actor, it will be destroyed 
    when the selected actor "dies"
    """
    def __init__(self, actor):
        """Constructor
        
        Requires an actor class so the lock can follow it
        """
        # Assign the actor from the constructor
        self.enemy = actor
        # Create a node with the lock model
        self.node = loader.loadModelCopy(globals.LOCKEGG) 
        self.node.setScale(0.1, 1, 0.125)
        # Make sure it points to the camera
        self.node.setBillboardPointEye()
        # And reparent to render2D, it will render above everything in render
        self.node.reparentTo(render2d) 
        # Update task
        self.moveTask = taskMgr.add(self._update, 'Update-Lock') 

    def _update(self, task):
        """Task function
        
        Updates the lock state
        """
        # Check if the node still exists
        if not self.enemy.node.isEmpty():
            # Compute the 2D postition and place it if its posible
            punto = self._compute2dPosition(self.enemy.node)
            if punto != None:
                x = punto[0]
                y = punto[1]
                self.node.setPos(x, 0, y)
        else:
            # If it does not exist, just delete yourself and finish
            self.node.removeNode()
            del self
            return task.done
        return task.cont


    def _compute2dPosition(self, nodePath, point=Point3(0, 0, 0)): 
        """Computes a 3-d point, relative to the indicated node, into a
        2-d point as seen by the camera.  
        
        The range of the returned value
        is based on the len's current film size and film offset, which is
        (-1 .. 1) by default. 
        This code has been borrowed from somewhere else.
        """
        # Convert the point into the camera's coordinate space
        p3d = base.cam.getRelativePoint(nodePath, point) 
        # Ask the lens to project the 3-d point to 2-d.
        p2d = Point2() 
        if base.camLens.project(p3d, p2d): 
            # Got it!
            return p2d
        # If project() returns false, it means the point was behind the
        # lens.
        return None
