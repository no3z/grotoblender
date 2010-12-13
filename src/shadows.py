#!/usr/bin/env python
#coding: iso-8859-1

"""Documentation for shadows.py

This file contains a very, very small, tiny,
almost microscopical change from the file shadowDemo.py
found in Panda3D, I just put it here to use it on the player

project -- Rez: The Clone
author -- Edwood Grant
organization -- Binhex Tw. 
version -- 1.00
since -- 8/07/2007 0:12:41
"""
    
#Panda specific imports for this module
from pandac.PandaModules import * 

class ShadowCaster:
    texXSize = 128
    texYSize = 128
    
    def __init__(self, lightPath, objectPath):
        self.lightPath = lightPath
        self.objectPath = objectPath
        self.groundPath = None

        # Create an offscreen buffer to render the view of the avatar
        # into a texture.
        self.buffer = base.win.makeTextureBuffer(
            'shadowBuffer', self.texXSize, self.texYSize)

        # The background of this buffer--and the border of the
        # texture--is pure white.
        clearColor = VBase4(1, 1, 1, 1) 
        self.buffer.setClearColor(clearColor)
        
        self.tex = self.buffer.getTexture()
        self.tex.setBorderColor(clearColor)
        self.tex.setWrapU(Texture.WMBorderColor) 
        self.tex.setWrapV(Texture.WMBorderColor) 

        # Set up a display region on this buffer, and create a camera.
        dr = self.buffer.makeDisplayRegion()
        self.camera = Camera('shadowCamera') 
        self.cameraPath = self.lightPath.attachNewNode(self.camera)
        self.camera.setScene(self.objectPath)
        dr.setCamera(self.cameraPath)

        # Use a temporary NodePath to define the initial state for the
        # camera.  The initial state will render everything in a
        # flat-shaded gray, as if it were a shadow.
        initial = NodePath('initial') 
        initial.setColor(0.5, 0.5, 0.5, 1, 1)
        initial.setTextureOff(2)
        self.camera.setInitialState(initial.getState())

        # Use an orthographic lens for this camera instead of the
        # usual perspective lens.  An orthographic lens is better to
        # simulate sunlight, which is (almost) orthographic.  We set
        # the film size large enough to render a typical avatar (but
        # not so large that we lose detail in the texture).
        self.lens = OrthographicLens() 
        self.lens.setFilmSize(100, 100)
        self.camera.setLens(self.lens)

        # Finally, we'll need a unique TextureStage to apply this
        # shadow texture to the world.
        self.stage = TextureStage('shadow') 

        # Make sure the shadowing object doesn't get its own shadow
        # applied to it.
        self.objectPath.setTextureOff(self.stage)

    def setGround(self, groundPath):
        """ Specifies the part of the world that is to be considered
        the ground: this is the part onto which the rendered texture
        will be applied. """
        
        if self.groundPath:
            self.groundPath.clearProjectTexture(self.stage)

        self.groundPath = groundPath
        self.groundPath.projectTexture(self.stage, self.tex, self.cameraPath)

    def clear(self):
        """ Undoes the effect of the ShadowCaster. """
        if self.groundPath:
            self.groundPath.clearProjectTexture(self.stage)
            self.groundPath = None

        if self.lightPath:
            self.lightPath.detachNode()
            self.lightPath = None

        if self.cameraPath:
            self.cameraPath.detachNode()
            self.cameraPath = None
            self.camera = None
            self.lens = None

        if self.buffer:
            base.graphicsEngine.removeWindow(self.buffer) 
            self.tex = None
            self.buffer = None


def avatarShadow(actor):
    # Turn off the existing drop shadow.
    #actor.dropShadow.hide()

    # Set up a new node to hold the "light": this is an abitrary point
    # somewhere above the avatar, looking down, as if from the sun.
    objectPath = actor.getGeomNode()
    shadowCamera = objectPath.attachNewNode('shadowCamera')
    lightPath = objectPath.attachNewNode('lightPath')

    # We can change this position at will to change the angle of the
    # sun.
    lightPath.setPos(0, 0, 200)

    # We need a task to keep the shadowCamera rotated in the same
    # direction relative to render (otherwise, the shadow seems to
    # rotate when you rotate your avatar, which is strange).  We can't
    # just use a compass effect, since that doesn't work on cameras.
    def shadowCameraRotate(task, shadowCamera=shadowCamera):
        shadowCamera.setHpr(render, 0, 0, 0) 
        lightPath.lookAt(shadowCamera, 0, 0, 3)
        return Task.cont 

    #taskMgr.remove('shadowCamera')
    taskMgr.add(shadowCameraRotate, 'shadowCamera')    

          
    sc = ShadowCaster(lightPath, objectPath)

    # Naively, just apply the shadow to everything in the world.  It
    # would probably be better to use a little restraint.
    #(Like only the world's ground node)
    sc.setGround(render) 

    return sc
