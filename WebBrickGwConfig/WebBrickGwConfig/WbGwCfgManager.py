# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: WbGwCfgManager.py 3136 2009-04-15 10:17:29Z philipp.schuster $

"""
Module to handle get and post requests for the WebBrick Gateway configurator
"""


import turbogears
import cherrypy
from macromaker import CreateMacros
from spike import BuildUI
import logging
import httplib

from urllib                 import urlencode , urlopen 
from os.path                import join, split, abspath, exists
from MiscLib.DomHelpers     import *
from threading              import Lock
from xml.etree.ElementTree import *
from xml.dom.minidom import parseString

from Discovery        import WbDiscoverCheck, ExterityDiscovery, SpDiscoverCheck , StartechDiscovery , UPnPDiscoverCheck
from StartechWrapper import StartechWrapper
from SiteplayerWrapper import SitePlayer
from MiscLib.Functions  import formatIntList, formatInt
from MiscLib.Logging    import Trace, Info, Warn, Error


class WbGwCfgManager(object):
    """
    Class to handle requests for WebBrick configuration management resources
    """

    def __init__(self):        
        self._log = logging.getLogger ("WebBrickGwConfig.WbGwCfgManager")
        self._usedIds = []
        
        self._locked = Lock()
        
        #newSiteplayers is used exclusivley to store skybox Tx and skybox Rx devices, as these should not be put into newDevices untill we have discovered a pair of them.
        self._newSkyboxes = {}
        # newDevices are devices that are prenst on the network, 
        # BUT which are not yet provisioned
        self._newDevices = {}
       
        # knownDevices are devies for which a xml configuration exists 
        # NOTE: This does not mean they are available on the network
        self._knownDevices = self.loadKnownDevices()
        
        # presentDevices are devices that are present on the network 
        # AND are already provisioned, i.e. are part of knownDevices 
        self._presentDevices = self.checkPresentDevices()
        
        #TODO: Compare known and present devices and issue warnign if a device is 
        #      If a device is not present
        
        # Setup Exterity Discovery on a Seperate Thread
        self._exterityListener = ExterityDiscovery()
        self._exterityListener.subscribe("new_exterity_decoder_event", self.exterityDecoderDiscovered)
        self._exterityListener.subscribe("new_exterity_encoder_event", self.exterityEncoderDiscovered)
        self._exterityListener.start()
         
        self._startechFinder = StartechDiscovery()
        self._startechFinder.subscribe("new_startech_event" , self.startechDiscovered)
        self._startechFinder.start()
                     
          
    def loadKnownDevices(self):
        """
        Function that checks whether a gateway device configuration file 
        (WebBrickGatewayDeviceConfig.xml) exists:
       
        - If one exists we try to load it and return a dict of known devices, 
          keyed by their id
        - If no file exists an empty dictonary is returned
        """
        result = {}
        configFile = self.SITE_CONFIG_LOCATION
        if not configFile.lower().endswith( ".xml" ):
            configFile = "%s.xml" % (configFile)
        configFile = abspath(configFile)   
          
        
        if exists(configFile):
            self._log.debug("Found Gateway Device Configuration file ")
            deviceConfig = getDictFromXmlFile( configFile )
            if "devices" in deviceConfig:
                for device in deviceConfig["devices"]:
                    #TODO: Prevent over writing and log warning!
                    result[device["id"]["val"]] = device
                    self._usedIds.append(device["id"]["val"])
                self._log.debug("The following devices are known: %s" %result)  
            else: 
                self._log.debug("No Devices tag found in config: %s" %deviceConfig) 
        else:
            self._log.debug("No Gateway Device Configuration file found")
        
        return result 
    
    def persistConfiguration( self ):
        """
        Function to write change in knownDevices to file to persist the 
        configuration
        """
        
        # write configuration change to Xml file.
        while not self._locked.acquire():
            _log.info( "Already writing persisted data " )
            time.sleep(0.5)  
        out = []
        for deviceid in self._knownDevices:
            out.append(self._knownDevices[deviceid])
            
        xmlDom = getXmlDomFromDict( out  , "devices")
        self._log.debug( "Xml to persist  %s" % (getElemPrettyXml(xmlDom)) )
        saveXmlToFilePretty( self.SITE_CONFIG_LOCATION_WRITE , xmlDom )
        self._locked.release()
    
    def checkPresentDevices(self):
        """
        Function that checks which of the known devices are present.
        
        At the moment this is done in a very crude way, by pinging devices
        TODO: Come up with a better way, that check the 'right' device is
              actually present on that IP. 
       
        Returns a dict of present devices keyed by id. 
        """
        #TODO: 
        #   - come up with a way of 'pinging' devices or actually 
        #     checkign if the right devices are present
         
        self._log.debug("DEBUG CHEAT!!: Assumed that all known devices are present")
        self._presentDevices = self._knownDevices
    
    def getNewId(self):
        notsuitable = True
        deviceId = 1
        while notsuitable:
            if len(str(deviceId)) == 1:
                result = "00%s" % deviceId
            elif len(str(deviceId)) == 2:
                result = "0%s" % deviceId
            if result in self._usedIds:
                deviceId += 1
            else:
                notsuitable = False;
        self._usedIds.append(result)
        return result
        
    def upnpDiscovered(self,device):
        """
        Function that checks whether the upnp device was previously
        discovered. If it was not discovered previously it is added
        to new devices
        
        @param params: name, location, ip

        @type params: dict 
        """
        
        alreadyDiscovered = False
        for d in self._knownDevices:
            if self._knownDevices[d].has_key("udn"):
                # This key check has to be in here to cope with skyboxes which have "rxip" and "txip"
                # but no "ip"
                if self._knownDevices[d]["udn"]["val"] == device["udn"]:
                    alreadyDiscovered = True
                    self._log.debug("Upnp Device (udn: %s) is already part of knownDevices" % device["udn"])  
        
        for d in self._newDevices:
            if self._newDevices[d].has_key("udn"):
                if self._newDevices[d]["udn"]["val"] == device["udn"]:
                    alreadyDiscovered = True
                    self._log.debug("Upnp Device (udn: %s) is already part of newDevices" % device["udn"])
        
        if not alreadyDiscovered:
            newId = self.getNewId()
            self._log.debug("Trying to add new upnp device : %s" %device)
            if device["model"].find("s3000") != -1:
                #imerge3000
                try:
                    address = "http://10.100.100.14:8080/eventstate/upnp/device/%i/1?attr=udn" %device["devicenumber"]
                    renderudn1  = urlopen(address)
                    renderudn1 = renderudn1.read()
                    renderudn1 = getDictFromXmlString(renderudn1)
                    renderudn1 = str(renderudn1["value"]["val"][''])

                    address = "http://10.100.100.14:8080/eventstate/upnp/device/%i/2?attr=udn" %device["devicenumber"]
                    renderudn2  = urlopen(address)
                    renderudn2 = renderudn2.read()
                    renderudn2 = getDictFromXmlString(renderudn2)
                    renderudn2 = str(renderudn2["value"]["val"][''])

                    address = "http://10.100.100.14:8080/eventstate/upnp/device/%i/3?attr=udn" %device["devicenumber"]
                    renderudn3  = urlopen(address)
                    renderudn3 = renderudn3.read()
                    renderudn3 = getDictFromXmlString(renderudn3)
                    renderudn3 = str(renderudn3["value"]["val"][''])

                    address = "http://10.100.100.14:8080/eventstate/upnp/device/%i/4?attr=udn" %device["devicenumber"]
                    renderudn4  = urlopen(address)
                    renderudn4 = renderudn4.read()
                    renderudn4 = getDictFromXmlString(renderudn4)
                    renderudn4 = str(renderudn4["value"]["val"][''])
                    
                    
                    configFile = self.DEVICE_CONFIG_LOCATION + "imerge_s3000.xml"
                    
                    if exists(configFile):
                        self._newDevices[newId] = getDictFromXmlFile( configFile )["device"]
                        self._newDevices[newId]["id"]["val"] = newId

                        for c in self._newDevices[newId]["connections"]:
                            if "sources" in c:
                                for s in c['sources']:
                                    s["id"]["val"] = newId + s["id"]["val"]

                            if "sinks" in c:
                                for s in c['sinks']:
                                    s["id"]["val"] = newId + s["id"]["val"] 
                                    if s["name"]["val"] == "Imerge Media 1":
                                        s["udn"]['val'] = renderudn1
                                    
                                    elif s["name"]["val"] == "Imerge Media 2":
                                        s["udn"]['val'] = renderudn2
                                    
                                    elif s["name"]["val"] == "Imerge Media 3":
                                        s["udn"]['val'] = renderudn3
                                    
                                    elif s["name"]["val"] == "Imerge Media 4":
                                        s["udn"]['val'] = renderudn4            
                        
                        self._newDevices[newId]["udn"]["val"] = device["udn"]
                        
                        self._log.debug("Added new Imerge box (udn: %s) to newDevices" % device["udn"])
                        self._log.debug("Device Des: %s " % self._newDevices[newId])
                    else:
                        self._log.debug("Imerge s3000 Config file does not exist!!!")
                except Exception , e:
                    self._log.error(e)
                
            elif device["model"].find("sonos") != -1:
               
                #sonosbox only has one renderer on it
                try:
                    address = "http://10.100.100.14:8080/eventstate/upnp/device/%i/1?attr=udn" %device["devicenumber"]
                    renderudn1  = urlopen(address)
                    renderudn1 = renderudn1.read()
                    renderudn1 = getDictFromXmlString(renderudn1)
                    renderudn1 = str(renderudn1["value"]["val"][''])
                    
                    configFile = self.DEVICE_CONFIG_LOCATION + "sonos_z90.xml"
                    if exists(configFile):
                        self._newDevices[newId] = getDictFromXmlFile( configFile )["device"]
                        self._newDevices[newId]["id"]["val"] = newId
                        for c in self._newDevices[newId]["connections"]:
                            if "sources" in c:
                                for s in c['sources']:
                                    s["id"]["val"] = newId + s["id"]["val"]
                                    
                            if "sinks" in c:
                                for s in c['sinks']:
                                    if s["name"]["val"] == "Sonos Media 1":
                                        s["udn"]['val'] = renderudn1
                                    s["id"]["val"] = newId + s["id"]["val"] 
                        
                        self._newDevices[newId]["udn"]["val"] = device["udn"]
                        self._log.debug("Added new Sonos box (udn: %s) to newDevices" % device["udn"])
                        self._log.debug("Device Des: %s " % self._newDevices[newId])
                    else:
                        self._log.debug("Sonos Config file does not exist!!!")
                except Exception , e:
                    self._log.error(e)
                    
                    
        pass
        
        
        
    def exterityEncoderDiscovered(self,params):
        """
        Function that checks whether the Exterity Box was previously
        discovered. If it was not discovered previously it is added
        to new devices
        
        @param params: name, location, ip

        @type params: dict 
        """
        
        alreadyDiscovered = False
        for d in self._knownDevices:
            if self._knownDevices[d].has_key("ip"):
                # This key check has to be in here to cope with skyboxes which have "rxip" and "txip"
                # but no "ip"
                if self._knownDevices[d]["ip"]["val"] == params["ip"]:
                    alreadyDiscovered = True
                    self._log.debug("Exterity Encoder (ip: %s) is already part of knownDevices" % params["ip"])  
        
        for d in self._newDevices:
            if self._newDevices[d]["ip"]["val"] == params["ip"]:
                alreadyDiscovered = True
                self._log.debug("Exterity Encoder (ip: %s) is already part of newDevices" % params["ip"])
        
        if not alreadyDiscovered:
            newId = self.getNewId() 
            configFile = self.DEVICE_CONFIG_LOCATION + "exterity_encoder.xml"
            if exists(configFile):
                self._newDevices[newId] = getDictFromXmlFile( configFile )["device"]
                self._newDevices[newId]["id"]["val"] = newId
                for c in self._newDevices[newId]["connections"]:
                    if "sources" in c:
                        for s in c['sources']:
                            s["id"]["val"] = newId + s["id"]["val"]
                            if s["type"]["val"] == "ExterityIP":
                                s["parameters"]["streamUrl"] = params["streamUrl"]
                    if "sinks" in c:
                        for s in c['sinks']:
                            s["id"]["val"] = newId + s["id"]["val"] 
                self._newDevices[newId]["ip"]["val"] = params["ip"]
                self._newDevices[newId]["location"]["val"] = params["location"]
                self._newDevices[newId]["name"]["val"] = params["name"]
                self._log.debug("Added new Exterity Encoder(ip: %s) to newDevices" % params["ip"])
                self._log.debug("Device Des: %s " % self._newDevices[newId])
            else:
                self._log.debug("Exterity Encoder Config file does not exist!!!")        
        pass
    def exterityDecoderDiscovered(self,params):
        """
        Function that checks whether the Exterity Box was previously
        discovered. If it was not discovered previously it is added
        to new devices
        
        @param params: name, location, ip

        @type params: dict 
        """
        
        alreadyDiscovered = False
        for d in self._knownDevices:
            if self._knownDevices[d].has_key("ip"):
                # This key check has to be in here to cope with skyboxes which have "rxip" and "txip"
                # but no "ip"
                if self._knownDevices[d]["ip"]["val"] == params["ip"]:
                    alreadyDiscovered = True
                    self._log.debug("Exterity Box (ip: %s) is already part of knownDevices" % params["ip"])  
        
        for d in self._newDevices:
            if self._newDevices[d]["ip"]["val"] == params["ip"]:
                alreadyDiscovered = True
                self._log.debug("Exterity Box (ip: %s) is already part of newDevices" % params["ip"])
        
        if not alreadyDiscovered:
            newId = self.getNewId() 
            configFile = self.DEVICE_CONFIG_LOCATION + "exterity_decoder.xml"
            if exists(configFile):
                self._newDevices[newId] = getDictFromXmlFile( configFile )["device"]
                self._newDevices[newId]["id"]["val"] = newId
                for c in self._newDevices[newId]["connections"]:
                    if "sources" in c:
                        for s in c['sources']:                         
                            s["id"]["val"] = newId + s["id"]["val"] 
                    if "sinks" in c:
                        for s in c['sinks']:                            
                            s["id"]["val"] = newId + s["id"]["val"]             
                self._newDevices[newId]["ip"]["val"] = params["ip"]
                self._newDevices[newId]["location"]["val"] = params["location"]
                self._newDevices[newId]["name"]["val"] = params["name"]
                self._log.debug("Added new Exterity encoder Box (ip: %s) to newDevices" % params["ip"])
                self._log.debug("Device Des: %s " % self._newDevices[newId])
            else:
                self._log.debug("Exterity encoder Config file does not exist!!!")    
   
        
    
    def siteplayerDiscovered(self, siteplayer):
        """
        Function that checks whether the Telnet Siteplayer was previously
        discovered. If it was not discovered previously it is added
        to new devices
        
        @param params: name, ip

        @type params: dict 
        """
           
        alreadyDiscovered = False
        for d in self._knownDevices:
            if self._knownDevices[d]["ip"]["val"] == siteplayer["ipAdr"]:
                alreadyDiscovered = True
                self._log.debug("Telnet Siteplayer (ip: %s) is already part of knownDevices" % siteplayer["ipAdr"])  
        
        for d in self._newDevices:
            if self._newDevices[d]["ip"]["val"] == siteplayer["ipAdr"]:
                alreadyDiscovered = True
                self._log.debug("Telnet Siteplayer (ip: %s) is already part of newDevices" % siteplayer["ipAdr"])
        
        if not alreadyDiscovered:
            newId = self.getNewId()
            self._log.debug("New Siteplayer discovered name is %s" %siteplayer["name"])
            if siteplayer["name"].find("NAD5") != -1:
                configFile = self.DEVICE_CONFIG_LOCATION + "nad_visio_5.xml"
                if exists(configFile):
                    self._newDevices[newId] = getDictFromXmlFile( configFile )["device"]
                    self._newDevices[newId]["id"]["val"] = newId 
                    self._newDevices[newId]["ip"]["val"] = siteplayer["ipAdr"]
                    self._newDevices[newId]["location"]["val"] = "livingroom"
                    self._newDevices[newId]["name"]["val"] = siteplayer["name"]
                    for c in self._newDevices[newId]["connections"]:
                        if "sources" in c:
                            for s in c['sources']:
                                s["id"]["val"] = newId + s["id"]["val"] 
                        if "sinks" in c:
                            for s in c['sinks']:
                                s["id"]["val"] = newId + s["id"]["val"] 
                    self._log.debug("Added new NAD5 Via Telnet Siteplayer (ip: %s) to newDevices" % siteplayer["ipAdr"])
                    self._log.debug("Device Des: %s " % self._newDevices[newId])
                else:
                    self._log.error("NAD5 Config file does not exist!")  
            
         
            
            elif siteplayer["name"].find("SKYRX") != -1:
                self._log.debug("Sky RX found checking for pairs or previous discovery")
                skytx = None
                paired = False
                for d in self._newDevices:
                    if self._newDevices[d].has_key("rxip"):
                        if self._newDevices[d]["rxip"]["val"] == siteplayer["ipAdr"]:
                            alreadyDiscovered = True
                            self._log.debug("Telnet Siteplayer (ip: %s) is already part of newDevices" % siteplayer["ipAdr"])
                
                if not alreadyDiscovered:
                    for d in self._newSkyboxes:
                        if self._newSkyboxes[d]["ipAdr"] == siteplayer["ipAdr"]:
                            alreadyDiscovered = True
                            self._log.debug("Telnet Siteplayer (ip: %s) is already part of newSkyboxes" % siteplayer["ipAdr"])
                
                        elif self._newSkyboxes[d]["name"].find("SKYTX") != -1:
                            skytx = self._newSkyboxes[d]
                            paired = True                        
                            self._log.debug("Paired siteplayer with skyTX siteplayer ")
                                
                if not alreadyDiscovered and not paired:
                    self._newSkyboxes[newId] = siteplayer
                    self._newSkyboxes[newId]["id"] = newId
                    self._log.debug("Telnet Siteplayer (ip: %s) is skyRX , no skyTX discovered yet , storing" % siteplayer["ipAdr"])
                
                
                if not alreadyDiscovered and paired:
                    self._log.debug("Telnet Siteplayer (ip: %s) Sky RX and TX pair discovered, adding to available devices" % siteplayer["ipAdr"])
                
                    configFile = self.DEVICE_CONFIG_LOCATION + "skybox.xml"
                    if exists(configFile):
                        skyboxid = self.getNewId()
                        self._newDevices[skyboxid] = getDictFromXmlFile( configFile )["device"]
                        self._newDevices[skyboxid]["rxid"]["val"] = newId
                        self._newDevices[skyboxid]["txid"]["val"] = skytx["id"] 
                        self._newDevices[skyboxid]["rxip"]["val"] = siteplayer["ipAdr"]
                        self._newDevices[skyboxid]["txip"]["val"] = skytx["ipAdr"]
                        self._newDevices[skyboxid]["txname"]["val"] = skytx["name"]
                        self._newDevices[skyboxid]["rxname"]["val"] = siteplayer["name"]
                        self._newDevices[skyboxid]["location"]["val"] = "Rack"
                        self._newDevices[skyboxid]["name"]["val"] = "New Skybox"
                        self._log.debug("Added new Lutron Processor Via Telnet Siteplayer (ip: %s) to newDevices" % siteplayer["ipAdr"])
                        self._log.debug("Device Des: %s " % self._newDevices[skyboxid])
                    else:
                        self._log.debug("Skybox Config file does not exist!")
             
            elif siteplayer["name"].find("SKYTX") != -1:
                self._log.debug("Sky TX found checking for pairs or previous discovery")
                skyrx = None
                paired = False
                for d in self._newDevices:
                    if self._newDevices[d].has_key("txip"):
                        if self._newDevices[d]["txip"]["val"] == siteplayer["ipAdr"]:
                            alreadyDiscovered = True
                            self._log.debug("Telnet Siteplayer (ip: %s) is already part of newDevices" % siteplayer["ipAdr"])
                
                if not alreadyDiscovered:
                    for d in self._newSkyboxes:
                        if self._newSkyboxes[d]["ipAdr"] == siteplayer["ipAdr"]:
                            alreadyDiscovered = True
                            self._log.debug("Telnet Siteplayer (ip: %s) is already part of newSkyboxes" % siteplayer["ipAdr"])
                
                        elif self._newSkyboxes[d]["name"].find("SKYRX") != -1:
                            skyrx = self._newSkyboxes[d]
                            paired = True                        
                            self._log.debug("Paired siteplayer with skyRX siteplayer ")
                                
                if not alreadyDiscovered and not paired:
                    self._newSkyboxes[newId] = siteplayer
                    self._newSkyboxes[newId]["id"] = newId
                    self._log.debug("Telnet Siteplayer (ip: %s) is skyTX , no skyRX discovered yet , storing" % siteplayer["ipAdr"])
                
                
                if not alreadyDiscovered and paired:
                    self._log.debug("Telnet Siteplayer (ip: %s) Sky RX and TX pair discovered, adding to available devices" % siteplayer["ipAdr"])                
                    configFile = self.DEVICE_CONFIG_LOCATION + "skybox.xml"

                    if exists(configFile):
                        skyboxid = self.getNewId()
                        self._newDevices[skyboxid] = getDictFromXmlFile( configFile )["device"]                     
                        self._newDevices[skyboxid]["txid"]["val"] = newId                       
                        self._newDevices[skyboxid]["rxid"]["val"] = skyrx["id"]               
                        self._newDevices[skyboxid]["txip"]["val"] = siteplayer["ipAdr"]                        
                        self._newDevices[skyboxid]["rxip"]["val"] = skyrx["ipAdr"]
                        self._newDevices[skyboxid]["txname"]["val"] = siteplayer["name"]
                        self._newDevices[skyboxid]["rxname"]["val"] = skyrx["name"]                       
                        self._newDevices[skyboxid]["location"]["val"] = "Rack"                       
                        self._newDevices[skyboxid]["name"]["val"] = "New Skybox"
                       
                        self._log.debug("Added new Skybox Via Telnet Siteplayer (ip: %s) to newDevices" % siteplayer["ipAdr"])
                      
                        self._log.debug("Device Des: %s " % self._newDevices[skyboxid])
                    else:
                        
                        self._log.debug("Skybox Config file does not exist!")                          
            
            
            else:
                self._log.error("Unknown Device")
    def startechDiscovered(self,startech):

        """
        Function that checks whether the Startech device was previously
        discovered. If it was not discovered previously it is added
        to new devices
        
        @param startech: startech description        
        """
        
        alreadyDiscovered = False   
        self._log.debug("Checking discovered starcheck device against currently found ones : %s" %startech)    
        for d in self._newDevices:
            if self._newDevices[d].has_key("txip"):
                if self._newDevices[d]["txip"]["val"] == startech["settings"]["IP"]:
                    alreadyDiscovered = True
                    self._log.debug("Startech (ip: %s) is already part of newDevices" %startech["settings"]["IP"]  )    
            if self._newDevices[d].has_key("rxip"):
                if self._newDevices[d]["rxip"]["val"] == startech["settings"]["IP"]:
                    alreadyDiscovered = True
                    self._log.debug("Startech (ip: %s) is already part of newDevices" %startech["settings"]["IP"]  )            
            if self._newDevices[d].has_key("ip"):
                if self._newDevices[d]["ip"]["val"] == startech["settings"]["IP"]:
                    alreadyDiscovered = True
                    self._log.debug("Startech (ip: %s) is already part of newDevices" %startech["settings"]["IP"]  )    
        
        for d in self._knownDevices:
            if self._knownDevices[d].has_key("txip"):
                if self._knownDevices[d]["txip"]["val"] == startech["settings"]["IP"]:
                    alreadyDiscovered = True
                    self._log.debug("Startech (ip: %s) is already part of knownDevices" %startech["settings"]["IP"]  )    
            if self._knownDevices[d].has_key("rxip"):
                if self._knownDevices[d]["rxip"]["val"] == startech["settings"]["IP"]:
                    alreadyDiscovered = True
                    self._log.debug("Startech (ip: %s) is already part of knownDevices" %startech["settings"]["IP"]  )            
            if self._knownDevices[d].has_key("ip"):
                if self._knownDevices[d]["ip"]["val"] == startech["settings"]["IP"]:
                    alreadyDiscovered = True
                    self._log.debug("Startech (ip: %s) is already part of knownDevices" %startech["settings"]["IP"]  )    
                      
        if not alreadyDiscovered:        
            newId = self.getNewId() 
            self._newDevices[newId] = {u'name': {u'val': u''}, u'number': {u'val': u''}, u'ip': {u'val': u''}, u'location': {u'val': u''}, u'type': {u'subtype': {u'val': u''}, u'val': u'Startech'}, u'id': {u'val': u''}}
            self._newDevices[newId]["id"]["val"] = newId
            partialMAC = startech["MAC"].split(':')[4:]
            self._newDevices[newId]["type"]["val"] = "Startech"
            self._newDevices[newId]["name"]["val"] = "Startech : %s (%s:%s)" %(startech["settings"]["IP"] , partialMAC[0] , partialMAC[1])
            self._newDevices[newId]["ip"]["val"] = startech["settings"]["IP"]
            self._newDevices[newId]["devicesettings"] = startech["settings"]
            self._log.debug("Added new Startech (ip: %s) to newDevices" % startech["settings"]["IP"])
                   
    def webbrickDiscovered(self, wb):
        """
        Function that checks whether the Webbrick was previously
        discovered. If it was not discovered previously it is added
        to new devices
        
        @param wb: webbrick description

        @type wb: dict
        """
        
        alreadyDiscovered = False   
             
        for d in self._newDevices:
            if self._newDevices[d]["ip"]["val"] == '10.100.100.100':
                alreadyDiscovered = True
                self._log.debug("WebBrick (ip: 10.100.100.100) is already part of newDevices"  )    
                
        if not alreadyDiscovered:        
            configFile = self.DEVICE_CONFIG_LOCATION + "webbrick.xml"
            if exists(configFile):
                newId = self.getNewId()
                self._newDevices[newId] = getDictFromXmlFile( configFile )["device"]
                self._newDevices[newId]["id"]["val"] = newId
                self._newDevices[newId]["name"]["val"] = wb['nodeName']
                self._newDevices[newId]["number"]["val"] = wb["nodeNum"]
                self._newDevices[newId]["location"]["val"] = "Rack"
                self._log.debug("Added new WebBrick (ip: %s) to newDevices" % "10.100.100.100")
                self._log.debug("Device Des: %s " % self._newDevices[newId])
            else:
                self._log.debug("Webbrick Config file does not exist!")
        
            
            
    # Constants
    # ---------
    FRONT_PAGE = "/wbgwcnf/GwConfigWarning"
    DEBUG_DEVICES =  {u'1': {u'name': {u'val': u''}, u'ip': {u'val': u''}, u'connections': [{u'source': {u'connectedto': {u'device': u'', u'sink': u''}, u'type': {u'val': u'analogue'}, u'focus': {u'val': u'local'}, u'name': {u'val': u'ANSignal'}}, u'sink': {u'type': {u'val': u'ExterityIP'}, u'focus': {u'val': u'global'}, u'name': {u'val': u'IPStream'}}}], u'location': {u'val': u''}, u'type': {u'subtype': {u'val': u'Decoder'}, u'val': u'WebBrick'}, u'id': {u'val': u'001'}}, u'2': {u'name': {u'val': u''}, u'ip': {u'val': u''}, u'connections': [{u'source': {u'type': {u'val': u'ExterityIP'}, u'focus': {u'val': u'global'}, u'name': {u'val': u'IPStream'}}, u'sink': {u'connectedto': {u'device': u'', u'sink': u''}, u'type': {u'val': u'analogue'}, u'focus': {u'val': u'local'}, u'name': {u'val': u'ANSignal'}}}], u'location': {u'val': u''}, u'type': {u'subtype': {u'val': u'Encoder'}, u'val': u'Exterity'}, u'id': {u'val': u'002'}}}
    LOCATIONS = ['Rack' , 'Livingroom' , 'Kitchen' , 'Bedroom'] 
    #TODO: need to get this location dynamically (probably passed in on __init__
    SITE_CONFIG_LOCATION = "/opt/webbrick/site/WebBrickGatewayDeviceConfig.xml"
    DEVICE_CONFIG_LOCATION = "/usr/lib/python2.5/site-packages/WebBrickGwConfig-2.0-py2.5.egg/resources/descriptions/"
    SITE_CONFIG_LOCATION_WRITE = "/opt/webbrick/site/WebBrickGatewayDeviceConfig.xml"
    
    # URI dispatching
    # ---------------

    @turbogears.expose()
    def index(self, *args):
        """
        Index page for configuration resources
        """
        requri = cherrypy.request.browserUrl
        raise cherrypy.HTTPRedirect(turbogears.url(self.FRONT_PAGE))
        ### raise cherrypy.HTTPError(404, "Unrecognized index URI: "+requri )
        return ""

    @turbogears.expose()
    def default(self, *args):
        """
        Analyze request URI and invoke the corresponding configuration resource
        """
        cherrypy.response.headerMap["Cache-Control"] = "no-cache"
        requri  = cherrypy.request.browserUrl
        Trace("%s: %s"%(requri,str(args)), "WbCfgManagerForm.default")
        if len(args) > 0:
            # Configuration manager front page
            if args[0] == "GwConfigWarning": return self.GwConfigWarning()
            if args[0] == "GwConfigStep1": return self.GwConfigStep1()
            if args[0] == "GwConfigStep2": return self.GwConfigStep2()
            if args[0] == "GwConfigStep3": return self.GwConfigStep3('None')
            if args[0] == "GwConfigKeypads": return self.GwConfigKeypads()
            # Immediate responses
            if args[0] == "GetXml" and len(args) >= 2:
                return self.GwConfigGetXml(args)
            
            if args[0] == "GwConfigStep1Action":    return self.GwConfigStep1Action()
            if args[0] == "GwConfigStep2Action":    return self.GwConfigStep2Action()
            if args[0] == "GwConfigStep3Action":    return self.GwConfigStep3Action()
            if args[0] == "GwConfigProvisionAction":    return self.GwConfigProvisionAction()
            if args[0] == "GwConfigConfigureAction":    return self.GwConfigConfigureAction()
            if args[0] == "GwConfigKeypadsAction":      return self.GwConfigKeypadsAction()
            if args[0] == "GwConfigKeypadsButtonAction":        return self.GwConfigKeypadsButtonAction()

            

        raise cherrypy.HTTPError(404, "Unrecognized URI: "+requri+", args[0] "+args[0] )
        # cherrypy.response.status = "204 WebBrick command accepted ("+wbaddr+","+wbchan+","+cmd+")"
        return ""

    

    # Main configuration form display and submission processing
    # ---------------------------------------------------------
    
    @turbogears.expose(template="WebBrickGwConfig.templates.GwConfigWarning")
    def GwConfigWarning(self):
        """
        Returns the configuration manager main page.
        """
        #TODO: Why do I have to return an empty dict here... 
        #      There must be a better way. 
        result = {}
        return result
        
    @turbogears.expose(template="WebBrickGwConfig.templates.GwConfigError")
    def GwConfigError(self,errorMsg):
        """
        Returns the Error page with a specific error message
        """
        
        result = {"error": errorMsg}
        return result
    
    @turbogears.expose()
    def GwConfigStep1Action(self):
        """
        Process return from main configuration form
        """

        # Process submission        
        req    = cherrypy.request
        action = req.paramMap["action"]
        if isinstance( action, list ):
            # Internet explorer
            action = req.paramMap["buttonAction"]
        
        if action == "discover":
            
            #TODO:
            #   - Discover Siteplayers
            #   - Discover UPnP
            
            # Discover Exterity Boxes (async!!!) 
            if not self._exterityListener.isAlive(): 
                self._exterityListener.join()
                self._exterityListener = ExterityDiscovery()
                self._exterityListener.subscribe("new_exterity_decoder_event", self.exterityDecoderDiscovered)
                self._exterityListener.subscribe("new_exterity_encoder_event", self.exterityEncoderDiscovered)                
                self._exterityListener.start()
                
            if not self._startechFinder.isAlive():
                self._startechFinder.join()
                self._startechFinder = StartechDiscovery()
                self._startechFinder.subscribe("new_startech_event" , self.startechDiscovered)
                self._startechFinder.start()    
            
           
            upnpDevices = UPnPDiscoverCheck()
            for device in upnpDevices:
                self.upnpDiscovered(device)     
            # Discover WebBricks
            wb = WbDiscoverCheck("10.100.100.100")
            if wb:
                self.webbrickDiscovered(wb)
            
            
            return self.GwConfigStep1()
            
            
        elif action == "provision":
            #Open provisioning page
            if "NewDevicesSelector" in req.paramMap:
                new = req.paramMap["NewDevicesSelector"]
                return self.GwConfigProvision(new, True )
            else:
                return self.GwConfigError(
                """
                No new device was selected, please go back to Step 1 and select 
                a device from the 'New Devices List' prior to clicking 'Provision' 
                """)
            
        elif action == "reprovision":
            #TODO: 
            #      Open provisioning page
            if "KnownDevicesSelector" in req.paramMap:
                known = req.paramMap["KnownDevicesSelector"]
                return self.GwConfigProvision(known, False)
            else:
                return self.GwConfigError(
                    """
                    No known device was selected, please go back to Step 1 and select 
                    a device from the 'Known Devices List' prior to clicking 'Re-Provision' 
                    """)
            
        elif action == "done":
            return self.GwConfigSteps()
    
    @turbogears.expose()
    def GwConfigStep2Action(self):
        """
        Process return from main configuration form
        """
        # Process submission        
        req    = cherrypy.request
        action = req.paramMap["action"]
        if isinstance( action, list ):
            # Internet explorer
            action = req.paramMap["buttonAction"]
        
        if action == "configure":
            if "KnownDevicesSelector" in req.paramMap:
                known = req.paramMap["KnownDevicesSelector"]
                deviceId = known[0:3]
                if deviceId in self._knownDevices:
                    deviceType = self._knownDevices[deviceId]["type"]["val"]
                    if deviceType == "Lutron" or deviceType == "WebBrick":
                        return self.GwConfigKeypads(deviceId)
                    else:                  
                        return self.GwConfigConfigure(known)
            else:
                return self.GwConfigError(
                    """
                    No known device was selected, please go back to Step 2 and select 
                    a device from the 'Known Devices List' prior to clicking 'Setup' 
                    """)
            
        elif action == "done":
            return self.GwConfigSteps()       

    @turbogears.expose()
    def GwConfigStep3Action(self):
        """
        Process return from main configuration form
        """
        # Process submission        
        req    = cherrypy.request
        action = req.paramMap["action"]
        if isinstance( action, list ):
            # Internet explorer
            action = req.paramMap["buttonAction"]
        if action == "buildUI":
            messages = []
            for location in self.LOCATIONS:
                if location != "Rack":
                    BuildUI(self._knownDevices , location)
                    messages.append("Rendered UI for location : %s" %location)
                    CreateMacros(self._knownDevices, location)
                    messages.append("Wrote Eventdispatch for location : %s" %location)

            return self.GwConfigStep3(messages)          
        elif action == "done":
            return self.GwConfigSteps()       

            
    @turbogears.expose()
    def GwConfigGetXml(self, args):
        """
        Process to return a blob of xml
        """
        
        argument1 = args[1]
        
        def makeItems (deviceId, deviceName=None, deviceType=None):
            """
            Function to create a simple xml element
            """
            self._log.debug("Make Items with id: %s    name: %s      type: %s     " %(deviceId,deviceName,deviceType))
            if deviceName:
                return "<item id='%s' name='%s' />" % (deviceId, deviceName)
            elif deviceType:
                return "<item id='%s' name='%s' />" % (deviceId, deviceType)
            else:
                return "<item id='%s' name='Unknown Device'/>" %(deviceId)
		

        result = """<?xml version="1.0" encoding="utf-8" ?>"""      
        items = []        
        if argument1 == "NewDevices":
            for d in self._newDevices:
                if self._newDevices[d]["name"]["val"] != '':
                    items.append( makeItems( d, deviceName = self._newDevices[d]["name"]["val"] ) )
                elif self._newDevices[d]["type"]["val"] != '':
					items.append(makeItems(d, deviceName=self._newDevices[d]["type"]["val"]))
            result = """<?xml version="1.0" encoding="utf-8" ?><items>"""+"\n".join(items)+"""</items>""" 
        
        elif argument1 == "KnownDevices":
            for d in self._knownDevices:
                items.append(makeItems(d, deviceName=self._knownDevices[d]["name"]["val"]))
            result = """<?xml version="1.0" encoding="utf-8" ?><items>"""+"\n".join(items)+"""</items>""" 
                    
        elif argument1 == "DeviceInfo":
            deviceId = args[2]
            
            if deviceId in self._knownDevices:
                items.append("<name value ='%s' />" % (self._knownDevices[deviceId]["name"]["val"]))
                items.append("<location value ='%s' />" % (self._knownDevices[deviceId]["location"]["val"]))
                items.append("<confstatus value ='%s' />" % (self._knownDevices[deviceId]["confstatus"]["val"]))
                items.append("<type value = '%s' />" % (self._knownDevices[deviceId]["type"]["val"]))
                
                if self._knownDevices[deviceId]["type"]["val"] != "Lutron" and self._knownDevices[deviceId]["type"]["val"] != "WebBrick": 
                    sourceTypes = []
                    sinkTypes = []
                    
                    # Obtain number of sinks
                    for c in self._knownDevices[deviceId]["connections"]:
                    
                        if "sources" in c:
                            for s in c['sources']:
                                sourceTypes.append(s["type"]["val"])
                        if "sinks" in c:
                            for s in c['sinks']:
                                sinkTypes.append(s["type"]["val"])
                            

                    items.append("<sourcecount value='%s' />" % len(sourceTypes))
                    items.append("<sinkcount value='%s' />" % len(sinkTypes))
                    items.append("<sourcetypes>")
                    for t in sourceTypes:
                        items.append("<value>%s</value>" % (t))
                    items.append("</sourcetypes>" )
                    items.append("<sinktypes>" )
                    for t in sinkTypes:
                        items.append("<value>%s</value>" % (t))
                    items.append("</sinktypes>" )
                result = """<?xml version="1.0" encoding="utf-8" ?><devices>"""+"\n".join(items)+"""</devices>""" 
        
        elif argument1 == "Keypads":
            deviceId = args[2]
            if deviceId in self._knownDevices:
                for keypad in self._knownDevices[deviceId]["keypads"]:
                    if "location" in keypad and "processor" in keypad and "link" in keypad and "number" in keypad and "buttons" in keypad:
                        items.append("<keypad>")
                        items.append("""<number value = '%s'/>""" %keypad["number"]["val"])
                        items.append("<location value = '%s'/>" %keypad["location"]["val"])
                        items.append("<processor value = '%s'/>" %keypad["processor"]["val"])
                        items.append("<link value = '%s'/>" %keypad["link"]["val"])
                        items.append("<buttons value = '%i'>" %len(keypad["buttons"]))
                        for button in keypad["buttons"]:
                            if "icon" in button and "number" in button:
                                items.append("<button>")
                                items.append("<number value = '%s'/>" %button["number"]["val"])
                                items.append("<icon value = '%s'/>" %button["icon"]["val"])
                                items.append("</button>")
                        items.append("</buttons>")
                        items.append("</keypad>")
            result = """<?xml version="1.0" encoding="utf-8" ?><keypads>"""+"\n".join(items) + "</keypads>"        
                    
        elif argument1 == "Sources":
            deviceId = args[2]
            
            if deviceId in self._knownDevices:
                # Build the list of sources
                for c in self._knownDevices[deviceId]["connections"]:
                    if 'sources' in c:
                        for s in c['sources']:
                            if 'connectedto' in s:
                                items.append("<source>")
                                items.append("<type value='%s' />" % s["type"]["val"])
                                items.append("<name value='%s' />" % s["name"]["val"])
                                items.append("<id value='%s' />" % s["id"]["val"])
                                items.append("<connectedto value='%s' />" % s["connectedto"]["val"])
                                items.append("<status value='%s' />" % s["status"]["val"])
                                items.append("</source>")
                result = """<?xml version="1.0" encoding="utf-8" ?><sources>"""+"\n".join(items)+"""</sources>"""        
        
        
        elif argument1 == "Sinks":
            deviceId = args[2]
            
            if deviceId in self._knownDevices:
                # Build the list of sinks
                for c in self._knownDevices[deviceId]["connections"]:
                    if "sinks" in c:
                        for s in c['sinks']:
                            if "connectedto" in s:
                                items.append("<sink>")
                                items.append("<type value='%s' />" % s["sink"]["type"]["val"])
                                items.append("<name value='%s' />" % s["sink"]["name"]["val"])
                                items.append("<id value='%s' />" % s["sink"]["id"]["val"])
                                items.append("<connectedto value='%s' />" % s["sink"]["connectedto"]["val"])
                                items.append("<status value='%s' />" % s["sink"]["status"]["val"])
                                items.append("</sink>")
                result = """<?xml version="1.0" encoding="utf-8" ?><sinks>"""+"\n".join(items)+"""</sinks>"""
        
        elif argument1 == "Sink":
            connectionId = args[2]
            deviceId = connectionId.split(":")[0]
            if deviceId in self._knownDevices:
                # Find the Sink and build info
                for c in self._knownDevices[deviceId]["connections"]:
                    if "sinks" in c:
                        for s in c['sinks']:
                            if s["id"]["val"] == connectionId:
                                items.append("<device>")
                                items.append("<name value='%s' />" % self._knownDevices[deviceId]["name"]["val"])
                                items.append("<sink>")
                                items.append("<type value='%s' />" % s["type"]["val"])
                                items.append("<name value='%s' />" % s["name"]["val"])
                                items.append("<id value='%s' />" % s["id"]["val"])
                                items.append("<connectedto value='%s' />" % s["connectedto"]["val"])
                                items.append("<status value='%s' />" % s["status"]["val"])
                                items.append("</sink>")
                                items.append("</device>")
                        
                result = """<?xml version="1.0" encoding="utf-8" ?><devices>"""+"\n".join(items)+"""</devices>"""
        
        elif argument1 == "Source":
            connectionId = args[2]
            deviceId = connectionId.split(":")[0]
            if deviceId in self._knownDevices:
                # Find the Source and build info
                for c in self._knownDevices[deviceId]["connections"]:
                    if "sources" in c:
                        for s in c['sources']:
                            if s["id"]["val"] == connectionId:
                                items.append("<device>")
                                items.append("<name value='%s' />" % self._knownDevices[deviceId]["name"]["val"])
                                items.append("<source>")
                                items.append("<type value='%s' />" % s["type"]["val"])
                                items.append("<name value='%s' />" % s["name"]["val"])
                                items.append("<id value='%s' />" % s["id"]["val"])
                                items.append("<connectedto value='%s' />" % s["connectedto"]["val"])
                                items.append("<status value='%s' />" % s["status"]["val"])
                                items.append("</source>")
                                items.append("</device>")
                            
                result = """<?xml version="1.0" encoding="utf-8" ?><devices>"""+"\n".join(items)+"""</devices>"""
        
        
        elif argument1 == "compatible":
            
            if args[2] == "sources":
                # Looking for sources
                
                #Determine the sink to be matched
                deviceId = args[3].split(":")[0]
                sinkId = args[3]
                sink = None
                
                for c in self._knownDevices[deviceId]["connections"]:
                    if "sinks" in c:
                        for s in c['sinks']:
                            if s["id"]["val"] == sinkId:
                                sink = s
                                self._log.debug("Found the sink we are looking for: %s" % sink)
                
                if sink:
                    for dev in self._knownDevices:
                        if self._knownDevices[dev]["id"]["val"] != deviceId:
                            if self._knownDevices[dev]["location"]["val"] == self._knownDevices[deviceId]["location"]["val"]:
                                for c in self._knownDevices[dev]["connections"]:
                                    if "sources" in c:
                                        for s in c['sources']:
                                            if s["type"]["val"] == sink["type"]["val"]:
                                                # We have found a match!!! 
                                                # TODO: 
                                                #   - ATM this generated a whole device for every source 
                                                #     that matches rather than one device with multiple 
                                                #     sources 
                                                items.append("<device>")
                                                items.append("<id value='%s' />" % self._knownDevices[dev]["id"]["val"])
                                                items.append("<name value='%s' />" % self._knownDevices[dev]["name"]["val"])
                                                items.append("<sources>")
                                                items.append("<source>")
                                                items.append("<type value='%s' />" % s["type"]["val"])
                                                items.append("<name value='%s' />" % s["name"]["val"])
                                                items.append("<id value='%s' />" % s["id"]["val"])
                                                items.append("<connectedto value='%s' />" % s["connectedto"]["val"])
                                                items.append("</source>")
                                                items.append("</sources>")
                                                items.append("</device>")
                   
                   
            elif args[2] == "sinks":
                # looking for sinks
                    
                # Determine Source to be matched
                deviceId = args[3].split(":")[0]
                sourceId = args[3]
                source = None
                
                for c in self._knownDevices[deviceId]["connections"]:
                    if "sources" in c:
                        for s in c['sources']:
                            if s["id"]["val"] == sourceId:
                                source = s
                                self._log.debug("Found the source we are looking for: %s" % source)
                
                if source:
                    for dev in self._knownDevices:
                        if self._knownDevices[dev]["id"]["val"] != deviceId:
                            if self._knownDevices[dev].has_key("connections"):
                                if self._knownDevices[dev]["location"]["val"] == self._knownDevices[deviceId]["location"]["val"]:
                                    for c in self._knownDevices[dev]["connections"]:
                                        if "sinks" in c:
                                            for s in c['sinks']:
                                                if s["type"]["val"] == source["type"]["val"]:
                                                    # We have found a match!!! 
                                                    # TODO: 
                                                    #   - ATM this generated a whole device for every sink 
                                                    #     that matches rather than one device with multiple 
                                                    #     sinks 
                                                    items.append("<device>")
                                                    items.append("<id value='%s' />" % self._knownDevices[dev]["id"]["val"])
                                                    items.append("<name value='%s' />" % self._knownDevices[dev]["name"]["val"])
                                                    items.append("<sinks>")
                                                    items.append("<sink>")
                                                    items.append("<type value='%s' />" % s["type"]["val"])
                                                    items.append("<name value='%s' />" % s["name"]["val"])
                                                    items.append("<id value='%s' />" % s["id"]["val"])
                                                    items.append("<connectedto value='%s' />" % s["connectedto"]["val"])
                                                    items.append("</sink>")
                                                    items.append("</sinks>")
                                                    items.append("</device>")
                    
            result = """<?xml version="1.0" encoding="utf-8" ?><devices>"""+"\n".join(items)+"""</devices>"""
        
        
        self._log.debug("Devices: %s" %items) 
        cherrypy.response.headerMap["Content-Type"]  = "application/xml"
        cherrypy.response.headerMap["Cache-Control"] = "no-cache"
        return result
            
                
            
    
    @turbogears.expose(template="WebBrickGwConfig.templates.GwConfigProvision")
    def GwConfigProvision(self, device, isNewDevice=False , startechtype = None):
        """
        Returns the provisioning page.
        """
        result = {}
        #if we are dealing with a skybox which has two rs232 adapters associated with it , we are being passed a disctionary of two IDs , the Tx id and the Rx Id
        if isinstance(device , dict):
            txId = device["txId"]
            rxId = device["rxId"]
            configFile = self.DEVICE_CONFIG_LOCATION + "skybox.xml"
            if exists(configFile):
                skybox = getDictFromXmlFile( configFile )["device"]
                skybox["id"]["val"] = self.getNewId()                     
                skybox["txid"]["val"] = txId                       
                skybox["rxid"]["val"] = rxId               
                skybox["txip"]["val"] = self._newDevices[txId]["ip"]["val"]                        
                skybox["rxip"]["val"] = self._newDevices[rxId]["ip"]["val"]
                skybox["location"]["val"] = "Rack"                       
                skybox["name"]["val"] = "New Skybox"            
                result["device_description"] = skybox
        else:
            deviceId = device[0:3]
            if startechtype:
                result["startechtype"] = startechtype
                result["startechdevices"] = []
                for x in self._newDevices:
                    if self._newDevices[x]["type"]["val"] == "Startech":
                        if x != deviceId: 
                            result["startechdevices"].append(self._newDevices[x])
            if isNewDevice:
                result["device_description"] = self._newDevices[deviceId]            
            else:
                result["device_description"] = self._knownDevices[deviceId]
        return result
        
        
    @turbogears.expose(template="WebBrickGwConfig.templates.GwConfigConfigure")
    def GwConfigConfigure(self, device, message = None):
        """
        Returns the device setup page.
        """
        
        result = dict()
        
        deviceId = device[0:3]
        result["device_description"] = self._knownDevices[deviceId]
        if message: 
            result["message"] = message
        
        return result
    
    @turbogears.expose(template="WebBrickGwConfig.templates.GwConfigSteps")
    def GwConfigSteps(self):
        """
        Returns the configuration manager main page.
        """
        #TODO: Why do I have to return an empty dict here... 
        #      There must be a better way. 
        result = {}
        return result
        
    @turbogears.expose(template="WebBrickGwConfig.templates.GwConfigStep1")
    def GwConfigStep1(self):
        """
        Returns the configuration manager main page.
        """
        #TODO: Why do I have to return an empty dict here... 
        #      There must be a better way. 
        result = {}
        return result
        
    @turbogears.expose(template="WebBrickGwConfig.templates.GwConfigStep2")
    def GwConfigStep2(self):
        """
        Returns the configuration manager main page.
        """
        #TODO: Why do I have to return an empty dict here... 
        #      There must be a better way. 
        result = {}
        return result
        
    @turbogears.expose(template="WebBrickGwConfig.templates.GwConfigStep3")
    def GwConfigStep3(self,message = None):
        """
        Returns the configuration manager main page.
        """
        #TODO: Why do I have to return an empty dict here... 
        #      There must be a better way. 
        result = dict()
        if message: 
            result["message"] = message
        
        return result
        
    @turbogears.expose(template="WebBrickGwConfig.templates.GwConfigKeypads")
    def GwConfigKeypads(self,devid):
        """
        Returns the configuration manager main page.
        """
        #TODO: Why do I have to return an empty dict here... 
        #      There must be a better way. 
        result = dict()
        result["devid"] = devid   
        result["device_description"] = self._knownDevices[devid]
        return result
        
    @turbogears.expose(template = "WebBrickGwConfig.templates.GwConfigKeypadButtons")    
    def GwConfigKeypadButtons(self,devid , keypadid):        
        """
        Returns the button configuration page.
        """        
        #TODO: Why do I have to return an empty dict here... 
        #      There must be a better way. 
        result = dict()
        result["devid"] = devid
        result["device_description"] = self._knownDevices[devid]
        result["keypadid"] = keypadid
        return result
        
    @turbogears.expose()
    def GwConfigKeypadsButtonAction(self):    
        """
        Adds new buttons
        """
        result = ''
        req = cherrypy.request
        action = req.paramMap["action"]
        deviceid = req.paramMap["devid"]
        mergedId = req.paramMap["keypadid"]
        if action == "add":            
            
            processor = mergedId[0:2]
            link = mergedId[2:4]
            number = mergedId[4:6]
            newbutton = req.paramMap["NewButtonSelector"]
            newicon = req.paramMap["NewButtonIconSelect"]
            for keypad in self._knownDevices[deviceid]["keypads"]:

                if processor in keypad["processor"]["val"] and link in keypad["link"]["val"] and number in keypad["number"]["val"]:
                    buttons = keypad["buttons"]

                    for button in buttons:

                        if newbutton in button["number"]["val"]:
                            return "Button already exists"
                    newbuttond = {"number" : {"val":newbutton} , "icon" : {"val" : newicon } }
                    keypad["buttons"].append(newbuttond)
            result = self.GwConfigKeypadButtons(deviceid,mergedId)
        elif action == "done":
            result = self.GwConfigKeypads(deviceid)
            
        self.persistConfiguration()             
        return result
        
    @turbogears.expose()
    def GwConfigKeypadsAction(self):    
        """
        Adds keypads or displays button configuration page for lutron device
        """
        result = dict()
        req = cherrypy.request
        action = req.paramMap["action"]
        if action == "add":
            deviceid = req.paramMap["devid"]
            newprocessor = req.paramMap["NewProcessorSelector"]
            newlink = req.paramMap["NewLinkSelector"]
            newnumber = req.paramMap["NewKeyPadSelector"]
            for keypad in self._knownDevices[deviceid]["keypads"]: 
                if newprocessor in keypad["processor"]["val"] and newlink in keypad["link"]["val"] and newnumber in keypad["number"]["val"]:
                    return "Keypad already exists"     
            newlocation = req.paramMap["location"]        
            keypadId = newprocessor + newlink + newnumber
            newkeypad = { 'buttons' : [] , 'location' : { 'val' : newlocation } , 'link' : { 'val' : newlink } , 'processor' : { 'val' : newprocessor } , 'number' : { 'val' : newnumber } }
            if self._knownDevices[deviceid]["keypads"] == {}:
                self._knownDevices[deviceid]["keypads"] = [] 
                self._knownDevices[deviceid]["keypads"].append(newkeypad)
            else:
                self._knownDevices[deviceid]["keypads"].append(newkeypad)
            result = self.GwConfigKeypads(deviceid)
        
        elif action == "edit_buttons":
            if "KeypadSelector" in req.paramMap:
                deviceid = req.paramMap["devid"]
                kId = req.paramMap["KeypadSelector"]
              
                keypadId = kId[0:2] + kId[5:7] + kId[10:12]

                result = self.GwConfigKeypadButtons(deviceid,keypadId)
            else:
                result =  self.GwConfigError(
                    """
                    No known keypad was selected, please go back to Step 2 and select 
                    a device from the Keypad List prior to clicking 'Edit buttons' 
                    """)
        elif action == "done":
            result = self.GwConfigStep2()
        self.persistConfiguration()     
        return result
    
    @turbogears.expose()
    def GwConfigProvisionAction(self):
        """
        Returns the configuration manager main page.
        """
        # Process submission        
        req    = cherrypy.request
        action = req.paramMap["action"]
        if isinstance( action, list ):
            # Internet explorer
            action = req.paramMap["buttonAction"]
        if action == "Skybox_Paired":
            if req.paramMap["device_one_type"] == req.paramMap["device_two_type"]:
                return self.GwConfigError(
                    """
                    Please select two different types, you cannot provision a skybox with two receivers or two transmitters
                    """)
            else:
                device_one_type = req.paramMap["device_one_type"]
                device_two_type = req.paramMap["device_two_type"]
                
                device_one_id = req.paramMap["device_one_id"]
                device_two_id = req.paramMap["device_two_id"]
                
                txId = None
                rxId = None
                if device_one_type == "skyTx" and device_two_type == "skyRx":
                    txId = device_one_id
                    rxId = device_two_id
                
                if device_one_type == "skyRx" and device_two_type == "skyTx":
                    txId = device_two_id
                    rxId = device_one_id
                    
                if txId and rxId :
                    return self.GwConfigProvision({"txId" : txId , "rxId" : rxId} , True )
                else:
                    return self.GwConfigError(
                        """
                        Please select two valid types
                        """)        
                        
        if action == "Startech_Type_Chosen":
            deviceid = req.paramMap["dev_id"]
            return self.GwConfigProvision(deviceid , True , req.paramMap["devicetype"])
        
        if action == "upnp_done":
            deviceId = None
            newName = None            
            if "new_name" in req.paramMap:
                newName = req.paramMap["new_name"]
            if "dev_id" in req.paramMap:
                deviceId = req.paramMap["dev_id"]
            if "location" in req.paramMap:
                location = req.paramMap["location"]
                    
            self._log.debug("Try to provision UPnP device - UDN : %s, Name: %s" %(self._newDevices[deviceId]["udn"]["val"] , newName) )
            
            if deviceId and newName:
                
                if deviceId in self._newDevices:
                    isNewDevice = True
                elif deviceId in self._knownDevices:
                    isNewDevice = False

                # Set Name
                if isNewDevice:
                    self._newDevices[deviceId]["name"]["val"] = newName
                else:
                    self._knownDevices[deviceId]["name"]["val"] = newName
                    
                #Set location    
                if isNewDevice:
                    self._newDevices[deviceId]["location"]["val"] = location
                else:
                    self._knownDevices[deviceId]["location"]["val"] = location
                
                # Shift device to known devices if it was newly provisioned
                if isNewDevice:
                    self._knownDevices[deviceId] = self._newDevices.pop(deviceId)
                    self._log.debug("Known Devices: %s" %self._knownDevices)  
                                    
        if action == "webbrick_done":
            deviceId = None
            newIp = None
            newName = None
            newNumber = None
            if "dev_id" in req.paramMap:
                deviceId = req.paramMap["dev_id"]
            if "new_ip" in req.paramMap:
                newIp = req.paramMap["new_ip"]
            if "node_name" in req.paramMap:
                newName = req.paramMap["node_name"]
            if "node_number" in req.paramMap:
                newNumber = req.paramMap["node_number"]
            
            self._log.debug("Try to provision WebBrick - ID: %s, IP: %s, Node Name: %s, Node Number: %s " %(deviceId, newIp, newName, newNumber) )
            if deviceId and newIp and newName and newNumber:
                
                if deviceId in self._newDevices:
                    currentIp = self._newDevices[deviceId]["ip"]["val"]
                    isNewDevice = True
                elif deviceId in self._knownDevices:
                    currentIp = self._knownDevices[deviceId]["ip"]["val"]
                    isNewDevice = False

                # Set Name
                conn = httplib.HTTPConnection(currentIp)
                conn.request("GET", "/hid.spi?com=NN;%s:" % newName)
                response = conn.getresponse()
                if response.status == 302:
                    if isNewDevice:
                        self._newDevices[deviceId]["name"]["val"] = newName
                    else:
                        self._knownDevices[deviceId]["name"]["val"] = newName
                # Set Number
                
                conn.request("GET", "/hid.spi?com=SN;%s:" % newNumber)
                response = conn.getresponse()
                if response.status == 302:
                    if isNewDevice:
                        self._newDevices[deviceId]["number"]["val"] = newNumber
                    else:
                        self._knownDevices[deviceId]["number"]["val"] = newNumber
                # Set IP 
                conn.request("GET", "/hid.spi?com=SI;%s:" % newIp.replace(".",";"))
                response = conn.getresponse()
                if response.status == 302:
                    if isNewDevice:
                        self._newDevices[deviceId]["ip"]["val"] = newIp
                    else:
                        self._knownDevices[deviceId]["ip"]["val"] = newIp
                
                
                # Shift device to known devices if it was newly provisioned
                if isNewDevice:
                    self._knownDevices[deviceId] = self._newDevices.pop(deviceId)
                    self._log.debug("Known Devices: %s" %self._knownDevices)  
                
                #create eventdespatch to get scene feedback
                webbrick_feedback_file = open("/opt/webbrick/site/eventdespatch/templates/webbrick_feedback_template.xml")
                webbrick_feedback_template = webbrick_feedback_file.readlines()
                webbrick_feedback = StringListSub({"node" : newNumber} , webbrick_feedback_template)        
                webbrickfile = open("/opt/webbrick/site/eventdespatch/%s_webbrick_feedback.xml" %deviceId , 'w')
                webbrickfile.writelines(webbrick_feedback)
        
        
        elif action == "skybox_done":
            deviceId = None
            newIp = None
            newName = None
            newLocation = None
            if "skyTx" in req.paramMap:
                txId = req.paramMap["skyTx"]
            if "skyRx" in req.paramMap:
                rxId = req.paramMap["skyRx"]
            if "skyRxip" in req.paramMap:
                rxIp = req.paramMap["skyRxip"]
            if "skyTxip" in req.paramMap:
                txIp = req.paramMap["skyTxip"]
            if "name" in req.paramMap:
                deviceName = req.paramMap["name"]
            if "location" in req.paramMap:
                deviceLocation = req.paramMap["location"]
            self._log.debug("Trying to provision Sky Box - RxIp: %s, TxIp Ip: %s, Name: %s, Location: %s " %(txIp, rxIp, deviceName, deviceLocation) )
             
            if txId and rxId and rxIp and txIp and deviceName and deviceLocation:
                self.ProvisionSky(txId , rxId , rxIp , txIp , deviceName , deviceLocation)           
        
        elif action == "lutron_done":
            deviceId = None
            newIp = None
            newName = None
            newLocation = None
            if "dev_id" in req.paramMap:
                deviceId = req.paramMap["dev_id"]
            if "new_ip" in req.paramMap:
                newIp = req.paramMap["new_ip"]
            if "name" in req.paramMap:
                newName = req.paramMap["name"]
            if "location" in req.paramMap:
                newLocation = req.paramMap["location"]
            self._log.debug("Trying to provision Lutron Box - ID: %s, IP: %s, Name: %s, Location: %s " %(deviceId, newIp, newName, newLocation) )
             
            if deviceId and newIp and newName and newLocation:
                self.ProvisionSimpleStartech(self.DEVICE_CONFIG_LOCATION + "lutron_processor.xml" ,  deviceId, newName , newIp , newLocation)
                    
        elif action == "NAD5_done":
            deviceId = None
            newIp = None
            newName = None
            newLocation = None
            if "dev_id" in req.paramMap:
                deviceId = req.paramMap["dev_id"]
            if "new_ip" in req.paramMap:
                newIp = req.paramMap["new_ip"]
            if "name" in req.paramMap:
                newName = req.paramMap["name"]
            if "location" in req.paramMap:
                newLocation = req.paramMap["location"]
            self._log.debug("Trying to provision NAD 5 Box - ID: %s, IP: %s, Name: %s, Location: %s " %(deviceId, newIp, newName, newLocation) )
             
            if deviceId and newIp and newName and newLocation:
                self.ProvisionSimpleStartech(self.DEVICE_CONFIG_LOCATION + "nad_visio_5.xml" ,  deviceId, newName , newIp , newLocation)

        elif action == "exterity_done":
            deviceId = None
            newIp = None
            newName = None
            newLocation = None
            if "dev_id" in req.paramMap:
                deviceId = req.paramMap["dev_id"]
            if "new_ip" in req.paramMap:
                newIp = req.paramMap["new_ip"]
            if "name" in req.paramMap:
                newName = req.paramMap["name"]
            if "location" in req.paramMap:
                newLocation = req.paramMap["location"]
            if "web_url" in req.paramMap:
                newWebUrl = req.paramMap["web_url"]
                
            self._log.debug("Try to provision Exterity Box - ID: %s, IP: %s, Name: %s, Location: %s " %(deviceId, newIp, newName, newLocation) )
            if deviceId and newIp and newName and newLocation and newWebUrl:
                
                if deviceId in self._newDevices:
                    currentIp = self._newDevices[deviceId]["ip"]["val"]
                    isNewDevice = True
                elif deviceId in self._knownDevices:
                    currentIp = self._knownDevices[deviceId]["ip"]["val"]
                    isNewDevice = False
                
                # TODO: 
                # 
                auth = 'Basic ' + 'YWRtaW46bGFicmFkb3I=\n'
                headers = {"Content-type": "application/x-www-form-urlencoded","Authorization": auth}
                
                
                conn = httplib.HTTPConnection(currentIp)
                
                # Set Name
                params = "Name=%s" % newName
                conn.request("POST","/cgi-bin/general.cgi?"+params,None,headers)
                response = conn.getresponse()
                if response.status == 200:
                    if isNewDevice:
                        self._newDevices[deviceId]["name"]["val"] = newName
                    else:
                        self._knownDevices[deviceId]["name"]["val"] = newName
                
                else:
                    params = "Name=%s" % newName
                    conn.request("POST","/cgi-bin/general?"+params,None,headers)
                    response = conn.getresponse()
                    if response.status == 200:
                        if isNewDevice:
                            self._newDevices[deviceId]["name"]["val"] = newName
                        else:
                            self._knownDevices[deviceId]["name"]["val"] = newName
                    
                # Set Location
                params = "Location=%s" % newLocation
                conn.request("POST","/cgi-bin/general.cgi?"+params,None,headers)
                response = conn.getresponse()
                if response.status == 200:
                    if isNewDevice:
                        self._newDevices[deviceId]["location"]["val"] = newLocation
                    else:
                        self._knownDevices[deviceId]["location"]["val"] = newLocation
                else:
                    params = "Location=%s" % newLocation
                    conn.request("POST","/cgi-bin/general?"+params,None,headers)
                    response = conn.getresponse()
                    if response.status == 200:
                        if isNewDevice:
                            self._newDevices[deviceId]["location"]["val"] = newLocation
                        else:
                            self._knownDevices[deviceId]["location"]["val"] = newLocation
                #we need to set up the exterity webpage url
                if isNewDevice:
                    for connection in self._newDevices[deviceId]["connections"]:
                        print "connection is %s" %connection
                        for sink in connection["sinks"]:
                            print "sink is %s" %sink
                            if sink["type"]['val'] == "ExterityWeb":
                                for command in sink["commands"]:
                                    if command["name"] == "selectWeb":
                                        print command["params"]["webUrl"]
                                        command["params"]["webUrl"] = command["params"]["webUrl"] %{"location":newLocation, "webUrl" : newWebUrl}
                else:
                    for connection in self._knownDevices[deviceId]["connections"]:
                        for sink in connection["sinks"]:
                            if sink["type"]['val'] == "ExterityWeb":
                                for command in sink["commands"]:
                                    if command["name"] == "selectWeb":
                                        command["params"]["webUrl"] = command["params"]["webUrl"] %{"location":newLocation , "webuUrl" : newWebUrl}
                # Set IP 
                if currentIp != newIp:
                    #TODO: 
                    #   - Need to properly set all params
                    pDict = {}
                    pDict["Apply"] = "Apply"
                    pDict["DHCP"] = "no"
                    pDict["Subnet"] = "255.255.0.0"
                    pDict["Gateway"] = "192.168.1.254"
                    pDict["IpAddress"] = newIp
                    pDict["Eth0Mode"] = "auto"
                    pDict["DNSPrimary"] = "208.67.222.222"
                    pDict["DNSSecondary"] = "208.67.220.220"    
                    params = urlencode(pDict)
                    conn.request("POST","/cgi-bin/ipconf.cgi?"+params,None,headers)
                    response = conn.getresponse()
                    tempData = response.read()
                    #TODO Proper POST for exterity ENCODERS
                    if isNewDevice:
                        self._newDevices[deviceId]["ip"]["val"] = newIp
                    else:
                        self._knownDevices[deviceId]["ip"]["val"] = newIp

                # Shift device to known devices if it was newly provisioned
                if isNewDevice:
                    self._knownDevices[deviceId] = self._newDevices.pop(deviceId)
                    self._log.debug("Known Devices: %s" %self._knownDevices)
                    
        self.persistConfiguration()           
        return self.GwConfigStep1()

    @turbogears.expose()
    def GwConfigConfigureAction(self):
        """
        Configures the connection between devices.
        """
        
        # Process submission        
        req    = cherrypy.request
        action = req.paramMap["action"]
        if isinstance( action, list ):
            # Internet explorer
            action = req.paramMap["buttonAction"]
            
        if action == "connect":
            deviceId = None
            ConnectionId1 = None
            ConnectionId2 = None
            message = []
            if "dev_id" in req.paramMap:
                deviceId = req.paramMap["dev_id"]
            if "DevConnSelector" in req.paramMap:
                ConnectionId1 = req.paramMap["DevConnSelector"][0:7]
                deviceId1 = ConnectionId1.split(":")[0]
                self._log.debug("Selected Device 1 is:%s" % ConnectionId1)
            if "connOptions" in req.paramMap:
                ConnectionId2 = req.paramMap["connOptions"][0:7]
                deviceId2 = ConnectionId2.split(":")[0]
                self._log.debug("Selected Device 2 is:%s" % ConnectionId2)
                
            if ConnectionId1 and ConnectionId2:
                #   - Make the connection between the devices
                message.append("The following configuration steps were carried out:")
                # Find the first device and set connectedto
                for c in self._knownDevices[deviceId1]["connections"]:
                    if "sinks" in c:
                        for s in c['sinks']:
                            if s["id"]["val"] == ConnectionId1:
                                #Found the one to modify
                                if s["connectedto"]["val"] != "":
                                    # is already connected to need to clear 
                                    # the connection on paired device 
                                    # hence find the other device! 
                                    temp_dev_con = c["sink"]["connectedto"]["val"]
                                    temp_dev = temp_dev_con.split(":")[0]
                                    #message.append("<div class='warning'>Warning:</div> The sink you selected was already connected to the source: %s" % temp_dev_con)
                                    message.append("WARNING: The sink you selected was already connected to the source: %s" % temp_dev_con)
                                    for t_c in self._knownDevices[temp_dev]["connections"]:                
                                        if "sources" in t_c:
                                            for t_c_s in t_c['sources']:
                                                if t_c_s["id"]["val"] == temp_dev_con:
                                                    # found the one to reset
                                                    t_c_s["connectedto"]["val"] = ""
                                                    #message.append("<div class='warning'>Warning:</div> Removed this mapping from the source.")
                                                    message.append("WARNING: Removed this mapping from the source.")
                                # Now set the new connection    
                                s["connectedto"]["val"] = ConnectionId2
                                s["status"]["val"] = "connected"
                                message.append("Info: Created mapping of %s(sink) to %s(source)" % (ConnectionId1, ConnectionId2))
                    if "sources" in c:
                        for s in c['sources']:
                            if s["id"]["val"] == ConnectionId1:
                                # found the one to modify
                                
                                if s["connectedto"]["val"] != "":
                                    # is already connected to need to clear 
                                    # the connection on paired device 
                                    # hence find the other device! 
                                    self._log.debug("The source of device %s is aready connected to %s" % (ConnectionId1,s["connectedto"]["val"]) )
                                    temp_dev_con = s["connectedto"]["val"]
                                    temp_dev = temp_dev_con.split(":")[0]
                                    #message.append("<div class='warning'>Warning:</div> The source you selected was already connected to the sink: %s" % temp_dev_con)
                                    message.append("WARNING: The source you selected was already connected to the sink: %s" % temp_dev_con)
                                    for t_c in self._knownDevices[temp_dev]["connections"]:                
                                        if "sinks" in t_c:
                                            for t_c_s in t_c['sinks']:
                                                if t_c_s["id"]["val"] == temp_dev_con:
                                                    # found the one to reset
                                                    self._log.debug("About to remove mapping %s from device %s" % (t_c_s["connectedto"]["val"] ,temp_dev_con) )    
                                                    t_c_s["connectedto"]["val"] = ""
                                                    #message.append("<div class='warning'>Warning:</div> Removed this mapping from the sink.")
                                                    message.append("WARNING: Removed this mapping from the sink.")
                                                        
                                s["connectedto"]["val"] = ConnectionId2
                                s["status"]["val"] = "connected"
                                message.append("Info: Created mapping of %s(source) to %s(sink)" % (ConnectionId1, ConnectionId2))
                
                # Find the second device and set connectedto
                for c in self._knownDevices[deviceId2]["connections"]:
                    if "sinks" in c:
                        for s in c['sinks']:
                            if s["id"]["val"] == ConnectionId2:
                                #Found the one to modify
                                
                                if s["connectedto"]["val"] != "":
                                    # is already connected to need to clear 
                                    # the connection on paired device 
                                    # hence find the other device! 
                                    temp_dev_con = s["connectedto"]["val"]
                                    temp_dev = temp_dev_con.split(":")[0]
                                    #message.append("<div class='warning'>Warning:</div> The sink you selected was already connected to the source: %s" % temp_dev_con)
                                    message.append("WARNING: The sink you selected was already connected to the source: %s" % temp_dev_con)
                                    for t_c in self._knownDevices[temp_dev]["connections"]:                
                                        if "sources" in t_c:
                                            for t_c_s in t_c['sources']:
                                                if t_c_s["id"]["val"] == temp_dev_con:
                                                    # found the one to reset
                                                    t_c_s["connectedto"]["val"] = ""
                                                    #message.append("<div class='warning'>Warning:</div> Removed this mapping from the source.")
                                                    message.append("WARNING: Removed this mapping from the source.")
                                
                                s["connectedto"]["val"] = ConnectionId1
                                s["status"]["val"] = "connected"
                                message.append("Info: Created mapping of %s(sink) to %s(source)" % (ConnectionId2, ConnectionId1))
                    if "sources" in c:
                        for s in c['sources']:
                            if s["id"]["val"] == ConnectionId2:
                                # found the one to modify
                                
                                if s["connectedto"]["val"] != "":
                                    # is already connected to need to clear 
                                    # the connection on paired device 
                                    # hence find the other device! 
                                    temp_dev_con = s["connectedto"]["val"]
                                    temp_dev = temp_dev_con.split(":")[0]
                                    #message.append("<div class='warning'>Warning:</div> The source you selected was already connected to the sink: %s" % temp_dev_con)
                                    message.append("WARNING: The source you selected was already connected to the sink: %s" % temp_dev_con)
                                    for t_c in self._knownDevices[temp_dev]["connections"]:                
                                        if "sinks" in t_c:
                                            for t_c_s in t_c['sinks']:
                                                if t_c_s["id"]["val"] == temp_dev_con:
                                                    # found the one to reset
                                                    t_c_s["connectedto"]["val"] = ""
                                                    #message.append("<div class='warning'>Warning:</div> Removed this mapping from the sink.")
                                                    message.append("WARNING: Removed this mapping from the sink.")
                                
                                s["connectedto"]["val"] = ConnectionId1
                                s["status"]["val"] = "connected"
                                message.append("Info: Created mapping of %s(source) to %s(sink)" % (ConnectionId2, ConnectionId1))
                self.persistConfiguration() 
                return self.GwConfigConfigure(deviceId, message)
            
            elif deviceId:
                message.append("ERROR: You have not selected a pair of source & sink")  
                self.persistConfiguration() 
                return self.GwConfigConfigure(deviceId, message)

    def ConfigureStartech(self, currentIp , settings):
        
        device = StartechWrapper(currentIp, '')
        cursettings = device.GetSettings()
        for x in settings:
            if cursettings.has_key(x):
                cursettings[x] = settings[x]
        device.SetSettings(cursettings)
            
    def ProvisionSky(self,txId , rxId , rxIp , txIp , deviceName , deviceLocation):
        #TODO Reprovisoning of skyboxes        
        
        configFile = self.DEVICE_CONFIG_LOCATION + "skybox.xml"
        if exists(configFile):
            
            txDescription = self._newDevices.pop(txId)
            rxDescription = self._newDevices.pop(rxId)
            
            deviceId = self.getNewId()
            self._knownDevices[deviceId] = getDictFromXmlFile( configFile )["device"]
            self._knownDevices[deviceId]["txid"]["val"] = txId 
            self._knownDevices[deviceId]["txip"]["val"] = txIp
            
            self._knownDevices[deviceId]["id"]["val"] = deviceId
            self._knownDevices[deviceId]["rxid"]["val"] = rxId 
            self._knownDevices[deviceId]["rxip"]["val"] = rxIp
            
            self._knownDevices[deviceId]["location"]["val"] = deviceLocation
            self._knownDevices[deviceId]["name"]["val"] = deviceName
            if self._knownDevices[deviceId].has_key("connections"):
                    for c in self._knownDevices[deviceId]["connections"]:
                        if "sources" in c:
                            for s in c['sources']:
                                s["id"]["val"] = deviceId + s["id"]["val"] 
                        if "sinks" in c:
                            for s in c['sinks']:
                                s["id"]["val"] = deviceId + s["id"]["val"] 
            
            
            
            self._log.debug("Device Description: %s " % self._knownDevices[deviceId])
            newsettings = { "IP" : self._knownDevices[deviceId]["txip"]["val"]  , 'SioBaud' : "57600" , 'ctSioPort' : '23' }
            self.ConfigureStartech( txDescription["ip"]["val"] , newsettings)
            
            newsettings = { "IP" : self._knownDevices[deviceId]["rxip"]["val"]  , 'SioBaud' : "57600" , 'ctSioPort' : '23'}
            self.ConfigureStartech( rxDescription["ip"]["val"] , newsettings)
            self._log.debug("Simple Startech device provisioned , new knowndevice list is : %s" %self._knownDevices)                
            
            self.MakeSerialConnection(txId , txIp , "Dusky" , "Dusky")
            self.MakeSerialConnection(rxId , rxIp , "Sky" , "Sky")
        else:
            self._log.error("Config file does not exist!") 



                         
    def ProvisionSimpleStartech(self,xmlLocation ,  deviceId, new_deviceName , new_deviceIp , new_deviceLocation):
        #TODO Automatically write/rewrite event dispatch for adding serial connections
        
        if deviceId in self._knownDevices:
            currentIp = self._knownDevices[deviceId]["ip"]["val"]
            isNewDevice = False
        elif deviceId in self._newDevices:
            currentIp = self._newDevices[deviceId]["ip"]["val"]
            self._newDevices.pop(deviceId)
            isNewDevice = True
        
        if isNewDevice:
            configFile = xmlLocation
            if exists(configFile):
                self._knownDevices[deviceId] = getDictFromXmlFile( configFile )["device"]
                self._knownDevices[deviceId]["id"]["val"] = deviceId 
                self._knownDevices[deviceId]["ip"]["val"] = new_deviceIp
                self._knownDevices[deviceId]["location"]["val"] = new_deviceLocation
                self._knownDevices[deviceId]["name"]["val"] = new_deviceName
                if self._knownDevices[deviceId].has_key("connections"):
                    for c in self._knownDevices[deviceId]["connections"]:
                        if "sources" in c:
                            for s in c['sources']:
                                s["id"]["val"] = deviceId + s["id"]["val"] 
                        if "sinks" in c:
                            for s in c['sinks']:
                                s["id"]["val"] = deviceId + s["id"]["val"] 
                    
        
                self._log.debug("Provisoned new device controller (ip: %s) " %new_deviceIp)
                self._log.debug("Device Description: %s " % self._knownDevices[deviceId])
            else:
                self._log.error("Config file does not exist!") 
        else:
            self._knownDevices[deviceId]["ip"]["val"] = new_deviceIp
            self._knownDevices[deviceId]["name"]["val"] = new_deviceName
            self._knownDevices[deviceId]["location"]["val"] = new_deviceLocation
        
        newsettings = { "IP" : self._knownDevices[deviceId]["ip"]["val"]  , 'SioBaud' : self._knownDevices[deviceId]["serial"]["baud"]["val"] , 'ctSioPort' : '23'}
       
        self.ConfigureStartech( currentIp , newsettings)
        self.MakeSerialConnection(deviceId , new_deviceIp , self._knownDevices[deviceId]["serial"]["driver"]["val"] , self._knownDevices[deviceId]["serial"]["protocol"]["val"])
        self._log.debug("Simple Startech device provisioned , new knowndevice list is : %s" %self._knownDevices)                

    
    def MakeSerialConnection(self, deviceId ,Ip , Driver , Protocol):
        #fire event to add a new serial device
        newPort = {'cmd':'NewConnection','port_type':'tcp','id':'lutronTelnet','ipAddress':'10.100.100.151','port':'23','deliminator':'13'}                   
        url = urlencode(newPort)
        a = urlopen("http://127.0.0.1:8080/sendevent/configurator/ui/lutron?type=new/serial/port&%s" %url )      
        #create the eventdispatch to persist the port over to the next session
        
                
        configFile = "/opt/webbrick/site/eventdespatch/serialConnections.xml"
        if exists(configFile):
            tree = ElementTree(file=configFile)
            interface = tree.find("eventInterface")
            ports = interface.find("serialPorts")
            newPort = SubElement(ports , "serialPort")
            newPort.attrib["driver"] = Driver
            newPort.attrib["protocol_handler"] = Protocol
            newPort.attrib["ipAddress"] = Ip
            newPort.attrib["port_type"] = 'tcp'
            newPort.attrib["port"] = "23"
            newPort.attrib["id"] = deviceId
            
            prettyxml = parseString(tostring(tree.getroot())).toprettyxml()
            f = open("/opt/webbrick/site/eventdespatch/serialConnections.xml",'w')
            f.write( prettyxml )
            f.close()
                   
        
# Helper functions
# ----------------

def StringListSub(Args , Stringlist):
    print "STRINGSUB : Args %s , Stringlist %s" %(Args,Stringlist)
    subbed = []
    for line in Stringlist:
        if '%' in line:
            line = line %Args
            print "STRINGSUB : Subbed %s" %line
        subbed.append(line)
    return subbed
    
def wrap(s1,s2): 
    """
    Return a function that wraps a supplied string in a supplied prefix and suffix.
    This is used for constructing XML elements from a list of values.
    """
    return (lambda t: s1+t+s2)

def login(tgtadrs, password):
    if not sendUdpCommand(tgtadrs, ':LG;'+password+':'):
        return "Failed to send login to WebBrick"
    return None

def setIp(tgtadrs, macbytes, ipbytes):
    cmd  = (':SA;'+
        formatIntList(macbytes,sep=";")+";"+
        formatIntList(ipbytes,sep=";")+":")
    if not sendUdpCommand(tgtadrs, cmd):
        return "Failed to send new address to WebBrick"
    return None

# End: $Id: WbGwCfgManager.py 3136 2009-04-15 10:17:29Z philipp.schuster $

