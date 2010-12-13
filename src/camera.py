#!/usr/bin/env python
#coding: iso-8859-1

"""Documentation for camera.py

Contain the camera class, manages 
everything related to camer movement

project -- Rez: The Clone
author -- Edwood Grant
organization -- Binhex Tw. 
version -- 1.00
since -- 7/07/2007 12:31:50
"""

#Default imports
from math import pi, sin

import globals
import keyb

class Camera:
    def __init__(self, actor=None):        
        ########################################
        # Cargar Actores
        ########################################
    
        #Set actor to follow
        self.actor = actor
        self.resetCamera()
        #Camera Task
        self.camTask = taskMgr.add(self.cameraUpdate, 'Camera-Follow', priority=35) 
        self.camTask2 = taskMgr.add(self.move, 'move') 

    def setToFollow(self, actor):
        """Set To follow
        
        Set an actor to be followed by the camera
        """
        self.actor = actor
        
    #Camara
    def resetCamera(self):
        """Reset camera function
        
        Resets the camera postition, 
        if theres an actor to follow of course
        """
        #Standard variables
        self.min_dist = 150.0
        self.dist = 1070
        self.max_dist = 850.0
        self.ang_cam_z = 45.5
        self.offset_z = 0.0
        self.ang_cam_x = 0.0
        self.ang_cam_y = 274

    def cameraUpdate(self, task):  
        """Task function
        
        Updates the camera state
        """   
        if self.actor == None:
            return task.cont
        #Calcular x, y y z
        x = (self.actor.getX(render) - self.dist)
        y = (self.actor.getY(render) + sin(self.ang_cam_y * (pi / 180)) * 700)
        z = (self.actor.getZ(render) + sin(self.ang_cam_z * (pi / 180)) * 700)
        #Colocamos la pocision final de la camara
        camera.setX(x) 
        camera.setY(y) 
        camera.setZ(z) 
        camera.lookAt(self.actor, 0, 0, 125) 
        #print self.ang_cam_z,self.ang_cam_y,self.dist
        #and done...
        return task.cont

    def move(self, task):
        if (globals.KEYBOARD.keyMap["cam-left"]!=0):
            self.ang_cam_z += 1.5
        if (globals.KEYBOARD.keyMap["cam-right"]!=0):
            self.ang_cam_y += 1.5
        if (globals.KEYBOARD.keyMap["cam-up"]!=0):
            self.dist += -10.5
        if (globals.KEYBOARD.keyMap["cam-down"]!=0):
            self.dist += 10.5

        #print globals.KEYBOARD.keyMap
        return task.cont