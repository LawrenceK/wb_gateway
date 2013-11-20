# $Id$
#
#  Class to generate HTML 5 compliant manifest files for skins
#
#  Tom Bushby
#
#
import logging
from os.path import join, split, abspath, exists
from os import rename, remove, listdir

import pkg_resources
pkg_resources.require("TurboGears")

from shutil import copy

import threading
import time
import fnmatch
import md5
import os


from xml.sax.saxutils import escape, unescape

from MiscLib.DomHelpers          import *

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred
from EventHandlers.BaseHandler import BaseHandler

_log = logging.getLogger( "EventHandlers.GenerateManifest" )

class GenerateManifest( BaseHandler, threading.Thread ):
    """
    TODO: Comments
    """

    def __init__ (self, localRouter):
        super(GenerateManifest,self).__init__(localRouter)
        # TODO: Do we need these?
        self._isUpdate = False
        self._subscribeTime = 30
        self._locked = threading.Lock()
        self._log = _log
        _log.debug( 'init complete' )   
        threading.Thread.__init__(self)
        self.setDaemon( True )
        _log.debug( 'thread init' )

    def configure( self, cfgDict ):
        if cfgDict.has_key("skin"):
            self.skinDirectory = cfgDict["skin"]["directory"]
            _log.debug("using custom skin directory: " + self.skinDirectory)
        else:
            self.skinDirectory = pkg_resources.resource_filename("WebBrickRes", "../resources/skins")       
            _log.debug("using skin directory: " + self.skinDirectory)
        pass
   
    def start(self):
        _log.debug( 'start' )
        BaseHandler.start(self)
        self.__running = True
    
        # subscribe to runtime so we can update manifest
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/time/runtime' )
        _log.debug( 'subscribed to runtime' )
        
        threading.Thread.start(self)        

    def stop(self):
        _log.debug( 'stop' )
        self.__running = False
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/time/runtime', '' )
       
    def makeManifest( self ):
        _log.debug( 'starting manifest' )
        # Configuration variables, should go in configure
        self.skinDict = {}
        self.templateFileDict = {}
        self.skinStaticPrefix = "/static/"  
        self.skinCustomPrefix = "/static/custom" 
        self.skinCustomPath = "/opt/webbrick/site/static"
        self.static = pkg_resources.resource_filename("WebBrickRes", "../resources/static")
        self.templatesDir = "/opt/webbrick/site/templates"  
        # Execute manifest functions
        self.findSkins()
        self.findFiles()
        self.findTemplates()
        self.publish()
                
    def doHandleEvent( self, handler, inEvent ):
        if inEvent.getType() == "http://id.webbrick.co.uk/events/time/runtime" :
            if int(inEvent.getPayload()["elapsed"]) == 5:
                _log.debug( 'caught runtime event' )
                self.makeManifest()

        return makeDeferred(StatusVal.OK)

    def run(self):
        _log.debug( 'thread running' )
        
    def publish(self):
        # Publish manifest files to disk and to the event system
    
        # Generate MD5 hashes only for /opt/webbrick/site/templates
        templateMd5 = ""
        for item in self.templateFileDict:
                templateMd5 = md5.new(templateMd5 + self.templateFileDict[item]).hexdigest()
                _log.debug("Template MD5 of " + item + " is " + self.templateFileDict[item] )
                
        # Generate cache for template files and content
        for skin in self.skinDict:
            skinMd5 = ""
            manifest = ""
            hasFiles = False
            # Generate Md5 hashes for all files in the skin directory
            for item in self.skinDict[skin]:
                hasFiles = True
                skinMd5 = md5.new(skinMd5 + self.skinDict[skin][item]).hexdigest()
                _log.debug("MD5 of " + item + " is " + self.skinDict[skin][item] )
                manifest = manifest + item + "\n"
            
            # If there are files in the skin directory, then publish and write the manifest
            if hasFiles:
                finalMd5 = md5.new(skinMd5 + templateMd5).hexdigest()
                
                # Manifest headers
                manifest = manifest + "\nNETWORK:\n*"
                manifest = "CACHE MANIFEST\n" + "#version-" + finalMd5 + "\n" + manifest           
                
                # publish manifest
                savePath = os.path.join(self.skinDirectory, skin, "static", "manifest", skin + ".manifest")
                fileHandle = open(savePath, 'w')
                fileHandle.write(manifest)
                fileHandle.close()
                _log.debug( ' saving skin ' + skin + ' in ' + savePath)        
                # publish md5
                if skin == "round":
                    activeskin = "activeskin"
                else:
                    activeskin = skin + "skin"
                evPayload = {"val": skinMd5}
                
                # publish event
                self.sendEvent( Event ( "http://id.webbrick.co.uk/events/manifest/publish", "manifest/publish/" + activeskin, evPayload ) )
                    
    def findFiles(self):
        # loop through each skin directory, find files and then put in list
        for skin in self.skinDict:
            # Legacy: round is actually called activeskin, whereas all other skins have a suffix of skin
            skinPath = os.path.join(self.skinDirectory, skin, 'static')
            if skin == "round":
                activeskin = "activeskin"
            else:
                activeskin = skin + "skin"
                
            # include static javascript in the manifest file
            self.walk(self.static, skin, "javascript", self.skinStaticPrefix + "")
            
            # include custom static files in the manifest file
            if os.path.isdir( self.skinCustomPath ):
                _log.debug("Custom static path in site directory exists")
                for item in os.listdir ( self.skinCustomPath ):
                    self.walk(self.skinCustomPath, skin, item, self.skinCustomPrefix + "/")            

            # include all standard skin files in the manifest file
            for dir in os.listdir (skinPath):                
                if dir != "manifest" and dir != "notcached": 
                    _log.debug("File walk information: " + skinPath + " --- " + skin + " --- " + dir + " --- " + self.skinStaticPrefix + activeskin + "/")   
                    self.walk(skinPath, skin, dir, self.skinStaticPrefix + activeskin + "/")
        
    def findTemplates(self):
        # Find all template based files in the /opt/webbrick/site/templates (default) folder
        # and use them as a salt for the MD5 hash
        if os.path.isdir( self.templatesDir ):
            for dir in os.listdir (self.templatesDir):
                self.walkTemplates(self.templatesDir, dir, self.templatesDir + "/")
    
    def walkTemplates(self, skinPath, entry, prefix):
        # if is directory
        if os.path.isdir( os.path.join(skinPath, entry) ):
            for item in os.listdir ( os.path.join(skinPath, entry) ):
                _log.debug("is item - " + item)
                self.walkTemplates(os.path.join(skinPath, entry), item, prefix + entry + "/")
        # if is file
        else:
            webPath = prefix + entry
            fileHandle = open(os.path.join(skinPath, entry), 'rb')
            content = fileHandle.read()
            fileHandle.close()
            strMd5 = md5.new(content).hexdigest()
            self.templateFileDict[webPath] = strMd5
            _log.debug("walkTemplates - in walk - MD5 of file " + webPath + " is " + strMd5 )
        
           
    def walk(self, skinPath, skin, entry, prefix):
        # Walk through skinPath and add files to dict
    
        # if is directory
        if os.path.isdir( os.path.join(skinPath, entry) ):
            for item in os.listdir ( os.path.join(skinPath, entry) ):
                self.walk(os.path.join(skinPath, entry), skin, item, prefix + entry + "/")
        else:
            # TODO: Add file filter to remove any unwanted files.
            webPath = prefix + entry
            fileHandle = open(os.path.join(skinPath, entry), 'rb')
            content = fileHandle.read()
            fileHandle.close()
            strMd5 = md5.new(content).hexdigest()
            self.skinDict[skin][webPath] = strMd5
            _log.debug("in walk - MD5 of file " + webPath + " is " + strMd5)
        # if is file
            
    def findSkins(self):
        # Locate all skins in the resources directory
        
        _log.debug( 'find skins start' )
        # loop through skin directory
        for skin in os.listdir ( self.skinDirectory):
            css = False
            images = False
            javascript = False
            _log.debug( 'found skin:' + skin )
            for skinItems in os.listdir ( self.skinDirectory + "/" + skin + "/static/"):
                _log.debug( 'skinItems in skin ' + skin + ' is: ' + skinItems )
                # Python switch statements are a pain when you want to embed a variable assignment
                # => using elif instead
                if skinItems == 'css':
                    css = True
                elif skinItems == 'images':
                    images = True
                elif skinItems == 'javascript':
                    javascript = True
            
            # The definition of a skin is that the css, images and javascript folder must exist                      
            if css == True and images == True and javascript == True:
                _log.debug( 'added skin ' + skin + ' to dict' )
                self.skinDict[skin] = {}
            else:
                self._log.debug( 'Item found in skin directory but is not a valid skin: ' + skin )
            

    


# End.       
# $Id$
