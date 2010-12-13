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

import globals
import sys

class Keyboard(DirectObject):
    """Class Mouse.
    
    Defines and implements mouse handling, like clicks and stacking enemies
    """
    def __init__(self):
        self.keyMap = {"left":0, "right":0, "forward":0,"backward":0, "cam-up":0, "cam-down":0, "cam-left":0, "cam-right":0}

        #Click sound and lock sound
        #self.clicksound = loader.loadSfx(globals.CLICKSOUND) 
        #self.locksound = loader.loadSfx(globals.LOCKSOUND)                
        
        self.accept("escape", sys.exit)
        self.accept("arrow_left", self.setKey, ["left",1])
        self.accept("arrow_right", self.setKey, ["right",1])
        self.accept("arrow_up", self.setKey, ["forward",1])
        self.accept("arrow_down", self.setKey, ["backward",1])
        self.accept("a", self.setKey, ["cam-left",1])
        self.accept("d", self.setKey, ["cam-right",1])
        self.accept("w", self.setKey, ["cam-up",1])
        self.accept("s", self.setKey, ["cam-down",1])

        self.accept("arrow_left-up", self.setKey, ["left",0])
        self.accept("arrow_right-up", self.setKey, ["right",0])
        self.accept("arrow_up-up", self.setKey, ["forward",0])
        self.accept("arrow_down-up", self.setKey, ["backward",0])
        self.accept("a-up", self.setKey, ["cam-left",0])
        self.accept("s-up", self.setKey, ["cam-down",0])
        self.accept("d-up", self.setKey, ["cam-right",0])
        self.accept("w-up", self.setKey, ["cam-up",0])

        #The stack, just a simple array
        self.stack = []        
            #Update Task

    #Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value
    
    
    
            