#!/usr/bin/env python
#coding: iso-8859-1

"""Documentation for "filename"

Just a small texto node to set a simple score

project -- Rez: The Clone
author -- Edwood Grant
organization -- Binhex Tw. 
version -- 1.00
since -- 8/07/2007 0:57:02
"""

#Panda specific imports for this module
from pandac.PandaModules import * 

#User imports
import globals

class Score:
    """Score class
    
    Creates a simple score, that sits on the 
    corner waiting to be updated
    """
    def __init__(self):
        """Constructor
        
        We set some properties here
        """
        #We create the text an set some properties like color and position
        self.text = TextNode('node name') 
        txt = "SCORE: " + str(globals.SCORE)
        self.text.setText(txt)
        self.text.setTextColor(1, 0, 0, 1)
        self.text.setShadow(0.05, 0.05)
        self.text.setShadowColor(0, 0, 0, 1)
                                  
        self.textNodePath = aspect2d.attachNewNode(self.text) 
        self.textNodePath.setPos(0.90, 0, 0.90)
        self.textNodePath.setScale(0.07) 
        
        #Update Task
        self.updateTask = taskMgr.add(self._update, 'Update-Score') 
        
    def _update(self, task):
        """Task function
        
        Updates the state of the score
        """
        txt = "SCORE: " + str(globals.SCORE)
        self.text.setText(txt)
        return task.cont
    
