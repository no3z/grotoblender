#!/usr/bin/env python
#coding: iso-8859-1

"""Documentation for globals.py

Contains various global variables, 
mostly for localization and to keep all loading string in one place.

project -- Rez: The Clone
author -- Edwood Grant
organization -- Binhex Tw. 
version -- 1.00
since -- 7/07/2007 10:03:02
"""
from pandac.PandaModules import *
"""STRING GLOBALS"""
#XML WORLDS
LEVEL_1_DIR = "../data/lvl/level1"
LEVEL_1_XML = "../data/lvl/level1/rezExample.xml"

"""SOUND GLOBALS"""
#SOUND CONTAINERS
CLICKSOUND = None
LOCKSOUND = None
SHOOTSOUNDS = []
NUMBERTRACKS = []
TEMPO = 0
"""GAME GLOBALS"""
#GAME FLOW GLOBALS
RATE = 1.0
MAXSTACK = 10
SCORE = 0
#CLASS CONTAINERS
ENEMIES_MOUSE = {}
ENEMIES = {}
NOTESGRO = []
WORLD = None
PhysicsBox = None
PhysicsSpace = None
STAGE = None
PLAYER = None
KEYBOARD = None
MOUSE = None
#EGG MODELS
MOUSEEGG = None
LOCKEGG = None
BULLETEGG = None
CHAREGG = None

colors = [  VBase4(0   , 0.0, 1.0, 1.0),
            VBase4(0.0 , 1.0, 1.0, 1.0),
            VBase4(1   , 0.0, 1.0, 1.0),
            VBase4(1   , 0.0, 0.33, 1.0),
            VBase4(1   , 0.330, 0.0, 1.0),
            VBase4(1   , 0.0, 0.0, 1.0),
            VBase4(0.33   , 0.033, 0.0, 1.0),
            VBase4(0.2   , 0.90, 0.20, 1.0),
            VBase4(0.33   , 0.053, 0.60, 1.0),
            VBase4(1   , 0.330, 0.70, 1.0),
            VBase4(0.1   , 0.30, .70, 1.0),
            VBase4(0.37   , 0.013, 1.0, 1.0),
            VBase4(0.55   , 0.20, 0.20, 1.0),
            VBase4(0.17   , 0.53, 0.60, 1.0)
            ]