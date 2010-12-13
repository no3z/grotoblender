#!/usr/bin/env python
#coding: iso-8859-1

"""Documentation for xmlr.py

This file contains the XML SAX reader for the game

project -- Rez: The Clone
author -- Edwood Grant
organization -- Binhex Tw. 
version -- 1.00
since -- 7/07/2007 0:42:55
"""

#Panda specific imports for this module
from pandac.PandaModules import Point3 #@UnresolvedImport

#Other Imports
#XML Handling
#from xml.sax import SAXException
from xml.sax.handler import ContentHandler

#User imports
import globals
import player
import enemy
import mouse
import tunnel
import keyb


class RezHandler(ContentHandler):
    """Class runner.
    
    Handles everything XML Related, inherits from content handler
    This class uses the python built in XML SAX reader
    Search google for "XML SAX" if you need more information
    """    
    def __init__(self,path):
        """Constructor"""
        #We create some elements to use with our SAX reader
        self.path = path
        self.tmpEnemy = None
        self.tmpTunnel = tunnel.Tunnel()
        self.changer = None
        
        self.numEnemy = 0
        self.actStage = 0

    ##Inicio de elemento    
    def startElement(self,name,attrs):
        """startEkement function, overridden from contentHandler
        
        This method triggers when a new XML element has been found.
        Here we'll find which element name is, and then we proceed to
        either create a new object or assign a value.
        """
        #If its the character, we initialize it and the mouse, and assign
        #the char model (which is an atribute inside the element)
        if name == 'character':
            globals.PLAYER = player.rezChar()
            #globals.MOUSE = mouse.Mouse()
            globals.KEYBOARD = keyb.Keyboard()
            globals.CHAREGG = self.path + "/cha/" + attrs.get('model')
            
        #The weapon element contains two attributes, the stack,
        #(how many times can i accumulate my weapon to fire)
        #And the bullet model
        #elif name == 'weapon':
            #globals.MAXSTACK = int(attrs.get('stack'))
            #globals.BULLETEGG = self.path + "/cha/" + attrs.get('model')
            
        #The cursor element contains two attrbiutes, the click sound
        #and the cursor model (it is loaded as a texture card egg)
        #elif name == 'cursor':
            #globals.CLICKSOUND = self.path + "/snd/" + attrs.get('sound')
            #globals.MOUSEEGG = self.path + "/cha/" + attrs.get('model')
            
        #Same as cursor, the lock element contains a lock sound
        #and the cursor model (again loaded as a texture card egg)
        #elif name == 'lock':
            #globals.LOCKSOUND = self.path + "/snd/" + attrs.get('sound')
            #globals.LOCKEGG = self.path + "/cha/" + attrs.get('model')
            
        #The shoot element contains juat a shoot sound, these are loaded in order
        #it can be more than one and they do NOT need to be the same ammount 
        #as the stack number. The game will cycle through all these sounds without problems
        #elif name == 'shoot':
            #globals.SHOOTSOUNDS.append(self.path + "/snd/" + attrs.get('sound'))
            
        #The stage element holds as attributes, the name of the map, the model of the map, 
        #a background music for that map (if it has), and if its loopable or not (the music).
        #We append it to the temp tunnel we have as attribute, this tunnel 
        #will end up containing all stages from the XML archive
        elif name == 'stage':
            self.tmpTunnel.name.append(attrs.get('name'))
            self.tmpTunnel.models.append(self.path + "/map/" + attrs.get('model'))
            if attrs.get('bgmusic') != "":
                self.tmpTunnel.bgMusic.append(self.path + "/mus/" + attrs.get('bgmusic'))
            else:
                self.tmpTunnel.bgMusic.append("")
                
            if attrs.get('loop') != "":
                self.tmpTunnel.loop = attrs.get('loop')
            else:
                self.tmpTunnel.loop = ""
                
        #The enemy element handles all the attributes of a determined enemy, we create
        #a temp enemy in our attibute, an we assing to which stage this enemy belongs
        #then we set his model, his time when he appears, his start position, and
        #his sound whenever he is defeated, and the socre point he gives when dead
        #TODO: Make flag for hostile enemies
        elif name == 'enemy':
            self.tmpEnemy = enemy.Enemy()
            self.tmpEnemy.stageBelong = self.actStage
            self.tmpEnemy.model = self.path + "/ene/" + attrs.get('model')
            self.tmpEnemy.time = float(attrs.get('time'))
            self.tmpEnemy.startPos = Point3(float(attrs.get('startX')),float(attrs.get('startY')),float(attrs.get('startZ')))
            self.tmpEnemy.sound = self.path + "/snd/" + attrs.get('sound')
            self.tmpEnemy.scorePoints = int(attrs.get('points'))
            
        #Each enemy move withtin these point elements, the application creates intervals
        #that move between these points at a certain speed, we assign it to the current 
        #temporary enemy at the moment
        elif name == 'point':
            tmpPoint = Point3(float(attrs.get('x')),float(attrs.get('y')),float(attrs.get('z')))
            self.tmpEnemy.points.append(tmpPoint)
            time = float(attrs.get('time'))
            self.tmpEnemy.times.append(time)

        #Changer is an enemy that can make the player change to the next world, 
        #all worlds but the last have changers. It has the same attributes of an enemy
        #the enemy has an special attribute called loop, it makes the enemy to keep looping
        #betwen his set of point if hes not destroyed. By definition a changer musto loop.
        #Otherwise the payer could miss it and never beable to advance
        elif name == 'changer':
            self.changer = enemy.Enemy()
            self.changer.stageBelong = self.actStage
            self.changer.model = self.path + "/ene/" + attrs.get('model')
            self.changer.time = float(attrs.get('time'))
            self.changer.startPos = Point3(float(attrs.get('startX')),float(attrs.get('startY')),float(attrs.get('startZ')))
            self.changer.sound = self.path + "/snd/" + attrs.get('sound')
            self.changer.scorePoints = int(attrs.get('points'))
            self.changer.loop = True
        #The Cpoit element is the same as point but it is ofr changers, 
        #its attributes are assigned to the current changer, which are 
        #the point itself and the time it takes to get to that point
        elif name == 'Cpoint':
            tmpPoint = Point3(float(attrs.get('x')),float(attrs.get('y')),float(attrs.get('z')))
            self.changer.points.append(tmpPoint)
            time = float(attrs.get('time'))
            self.changer.times.append(time)
            
    def endElement(self,name):
        """endEkement function, overridden from contentHandler
        
        This method triggers when an XML element has ended.
        Here we'll do things need to be done when certain elements close
        """
        #If the element is Stage we must set the actual stage to be the next stage
        #this is importat for enemys and changer to know in which stage they are
        if name == 'stage':
            self.actStage += 1
            
        #If the element is enemy we must "complete" that enemy by assigning to
        #The global variables to be used for colision between bullets and the mouse
        #Then we set to None our temp enemy for the next creation.
        elif name == 'enemy':
            tmpName = 'malo'+str(self.numEnemy)
            self.tmpEnemy.actor.setTag('enemy',tmpName)
            globals.ENEMIES[tmpName] = self.tmpEnemy
            globals.ENEMIES_MOUSE[tmpName] = self.tmpEnemy
            self.numEnemy += 1
            self.tmpEnemy = None
        
        #If the element is changer, we do almost the same thing as we did to enemy
        #Remebe changer is an enemy, just a special and different one
        elif name == 'changer':
            tmpName = 'changer'+str(self.numEnemy)
            self.changer.actor.setTag('enemy',tmpName)
            globals.ENEMIES[tmpName] = self.changer
            globals.ENEMIES_MOUSE[tmpName] = self.changer
            self.numEnemy += 1
            self.tmpTunnel.changer.append(self.changer)
            self.changer = None
        
    def endDocument(self):
        """endDocument function, overridden from contentHandler
        
        This method triggers when an XML document has ended.
        Here we initialize everything, set our tmpTunnel as the stage
        and trigger a change of our tunnel to begin with our game
        """
        for it in globals.NOTESGRO:
                #print it
                self.tmpEnemy = enemy.Enemy()
                self.tmpEnemy.stageBelong = "test"
                self.tmpEnemy.model = self.path + "/ene/" + "ene01.egg"
                self.tmpEnemy.time = it.start 
                #self.tmpEnemy.startPos = Point3( float(500), float(-100) ,float(-100) )
                #self.tmpEnemy.startPos = Point3(1000, float(it.pitch-48)*10, float(it.channel+1)*20 )
                self.tmpEnemy.duration = it.duration 
                self.tmpEnemy.init()
                
                self.tmpEnemy.sound = self.path + "/snd/" + "dene01.mp3"
                self.tmpEnemy.scorePoints = 100
                self.tmpEnemy.channel = it.channel
                self.tmpEnemy.velocity = it.velocity
                self.tmpEnemy.pitch = it.pitch

                tmpPoint = Point3( 500-float(it.duration*2000.0), float(it.channel-8)*100 ,float(0) )
                #tmpPoint = Point3( float(1000), float(100) ,float(100) )
                self.tmpEnemy.points.append(tmpPoint)
                time = it.duration 
                self.tmpEnemy.times.append(time)
                
                tmpName = 'malo'+str(self.numEnemy)
                self.tmpEnemy.actor.setTag('enemy',tmpName)

                globals.ENEMIES[tmpName] = self.tmpEnemy
                globals.ENEMIES_MOUSE[tmpName] = self.tmpEnemy
                self.numEnemy += 1
                self.tmpEnemy = None
            
        globals.PLAYER.init()
        #globals.MOUSE.init()
        globals.STAGE = self.tmpTunnel
        #Start Level and game
        globals.STAGE.startLevel()
        del self