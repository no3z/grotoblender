#!/usr/bin/env python
#coding: iso-8859-1

"""Documentation for tunnel.py

This file contains the class tunnel for handling world maps

project -- Rez: The Clone
author -- Edwood Grant
organization -- Binhex Tw. 
version -- 1.00
since -- 7/07/2007 23:04:41
"""

#Panda specific imports for this module
import direct.directbase.DirectStart  
from pandac.PandaModules import * 

#Librerias propias
import globals

class Tunnel:
    def __init__(self):
        """Constructor
        
        We are not doing anything special here, only when we decide to init  
        right here we are only creating some variables     
        """
        self.models = []
        self.bgMusic = []
        self.name = []
        self.changer = []
        self.changingUp = None
        self.changingDown = None
        self.actStage = 0
        self.transp = 0
        self.moved = 0
        self.loop = None
        self.backMusic = None
        
    def init(self, lvl):
        """Init Function
        
        Initializes and runs everything related to tunnel and maps
        """
        #If the parameter lvl if bigger than 
        #the amount of levels, we wont do anything
        if lvl >= len(self.models):
            return
        #Loads sound, according to lvl parameter 
        #and if there any sounds in the correspondant level
        if not (self.bgMusic[lvl] == "" or self.bgMusic[lvl] == None):
            #Try to stop the previous music, if we are in the middle of a
            #level this must exist already, or it is None if its the beggining
            if self.backMusic != None:
                self.backMusic.stop()
            #Load music, set it to lopp if requested, and play
            self.backMusic = base.loadMusic(self.bgMusic[lvl]) 
            self.backMusic.setVolume(.8)
            if self.loop == True:
                self.backMusic.setLoop(True)
            self.backMusic.setPlayRate(globals.RATE)
            self.backMusic.play()
    
        #Define and load everything
        if lvl == 0: #The node hasnt been created
            self.node = render.attachNewNode(self.name[lvl]) 
            #Enable transparency
            self.node.setAlphaScale(self.transp)
            
        #We try to remove these nodes. If we are in the middle of a level
        #These node must exist already
        if lvl != 0:
            self.model.removeNode()
            self.model2.removeNode()
            self.model3.removeNode()
        
        #We are going to move this and look like the infinite tunnel demo from panda 3D
        #So we are loading two other instances of this model
        self.model = loader.loadModelCopy(self.models[lvl]) 
        self.model2 = loader.loadModelCopy(self.models[lvl]) 
        self.model3 = loader.loadModelCopy(self.models[lvl]) 
        #We will enable transaparency on these model as well
        self.model.setTransparency(1)
        self.model2.setTransparency(1)
        self.model3.setTransparency(1)
        self.node.setTransparency(1)
        
        #This changing size and scaling and rotating, are just 
        #a horrible blatant hack, im puttin them just to make 
        #the models fit well in the screen
        self.model.setScale(50, 100, 100)
        self.model.setR(90)
        self.model2.setScale(50, 100, 100)
        self.model2.setR(90)
        self.model3.setScale(50, 100, 100)
        self.model3.setR(90)
        #We set it accordin to a nice position for our player, another hack again
        self.node.setZ(222)
        self.node.setY(222)
        self.node.setX(1225)

        #And our thir horrible hack, we put each one next to the other so 
        #they end next to the other so it looks seamless
        self.model2.setPos(self.node.getPos())
        self.model2.setPos(self.model2, 0, 0, 50)
        
        self.model3.setPos(self.node.getPos())
        self.model3.setPos(self.model3, 0, 0, 100)
        
        self.model.setPos(self.node.getPos())

        #Make it visible
        self.model.reparentTo(self.node)
        self.model2.reparentTo(self.node)
        self.model3.reparentTo(self.node)
        
        #And we put it in the place where the previous tunnel was
        #on relation to itself, if this is the fires self.moved = 0
        self.node.setPos(self.node, self.moved, 0, 0)        

        #Special configuration if this is the first level loaded
        if lvl == 0:
            #Turn of all lights
            self.lightAttrib = LightAttrib.makeAllOff() 
            #ambient light
            self.ambientLight = AmbientLight("ambientLight") 
            self.ambientLight.setColor(Vec4(0.6, 0.6, 0.6, 1)) 
            ambientLightNP = render.attachNewNode(self.ambientLight.upcastToPandaNode())       
            render.setLight(ambientLightNP) 
            
            #Point light
            self.plight = PointLight("sunLight") 
            # set the numbers here for Red, Green, Blue for light color
            self.plight.setColor(Vec4(0.5, 0.5, 0.5, 1)) 
            plightNP = render.attachNewNode(self.plight) 
            plightNP.setPos(-10, 0, 50)
            render.setLight(plightNP) 

            #Update Task
            self.updateTask = taskMgr.add(self._update, 'Update-Tunnel') 
            self.updateTask.last = 0
            #This task is to make the map movement return to where it was before,
            #so the illusion of a seamlees world is mantained
            taskMgr.doMethodLater(10, self._returnToStart, 'Return-Tunnel') 
        
        #Our model if fading from black now, so its 'changingUp'
        self.changingUp = True
    
    def _returnToStart(self, task):
        """Task Function
        
        It will return to the beginning the whole tunnel, and will reset this task
        """
        self.node.setX(self.node, -self.moved)
        self.moved = 0
        taskMgr.doMethodLater(10, self._returnToStart, 'Return-Tunnel') 
        return task.done

    def _update(self, task):
        """Task function
        
        This will update the state of the tunnel
        """
        #Dt handling to make movement independent of framerate
        dt = task.time - task.last
        task.last = task.time
        
        #Tunnel constanly keep monitoring enemy changers,
        #so if changer node is empty, it means it was destroyed,
        #So we change to a new level if we have more levels
        if not self.actStage >= len(self.models) - 1:
            if self.changer[self.actStage].node.isEmpty():
                self._change(self.actStage + 1)
        
        #If we are 'changing down', we are doing a fade to black
        #We do that by changing its transparency
        if self.changingDown == True:
            #If we are done then we call _initlvl
            if self.transp < 0:
                self.transp = 0
                self._initLvl(self.actStage)
            self.node.setAlphaScale(self.transp)
            self.transp -= 0.01
        
        #If we are 'changing down', we are undoing the fade to black
        #We do that by changing its transparency
        if self.changingUp == True:
            if self.transp > 1:
                self.transp = 1
                self.changingUp = False
            self.node.setAlphaScale(self.transp)
            self.transp += 0.01
        
        #The world is always moving backwards to make look that the player is moving   
        self.node.setPos(self.node, -500 * dt, 0, 0)        
        self.moved -= 500 * dt 
        return task.cont

    def startLevel(self):
        """Start Level function
        
        This will start this level
        """
        self._change(0)
            
    def _change(self, lvl):
        """Change function
        
        This will issue a change to a specific level
        """
        self.actStage = lvl
        #If the level is different from 0, we only 
        #have to make a changedown-up setting. (this assumes level 0 is loaded already)
        #but if it is 0, then we intialize everything normaly
        if lvl != 0:
            self.changingDown = True
            self.changingUp = False
            self.transp = 1
        else:
            self._initLvl(lvl)

    def _initLvl(self, lvl):
        """Init Level function
        
        This function will intialize enemies and maps to render
        """
        #We must disable changing down, we start from black
        self.changingDown = False
        #We load all the enemies related to this stage
        #And we are good to go and init()
        for i in globals.ENEMIES:
            obj = globals.ENEMIES[i]
            if obj.stageBelong == lvl:
                obj.init()
        self.init(lvl)
