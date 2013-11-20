# $Id: Discovery.py 2610 2008-08-11 20:08:49Z graham.klyne $
#
"""
WebBrick discovery
"""

import logging
import threading
import socket
import httplib
import urllib
import struct
import select
import time

from ExterityTools import GetStreamUrl
from StartechWrapper import StartechWrapper
from SiteplayerWrapper import SitePlayer
from MiscLib.Logging import Trace
from WebBrickLibs.Wb6Config import Wb6Config
from MiscLib.DomHelpers import getDictFromXmlString

def UPnPDiscoverCheck():
    discovered = []
    log = logging.getLogger( "WebBrickGwConfig.Discovery.UpnpDiscoverCheck" )
    try:        
        address = "http://10.100.100.14:8080/eventstate/upnp/device/count"
        devicecount = urllib.urlopen(address)
        devicecount = devicecount.read()   
        devicecount = getDictFromXmlString(devicecount)
        log.debug(devicecount)
        devicecount = int(devicecount["value"]["val"]['']) 
        if devicecount > 0:
            for x in range(1,devicecount+1):
                address = "http://10.100.100.14:8080/eventstate/upnp/device/%i?attr=udn" %x
                udn  = urllib.urlopen(address)
                udn = udn.read()
                udn = getDictFromXmlString(udn)
                udn = str(udn["value"]["val"][''])
                
                address = "http://10.100.100.14:8080/eventstate/upnp/device/%i?attr=model" %x
                model  = urllib.urlopen(address)
                model = model.read()
                model = getDictFromXmlString(model)
                model = str(model["value"]["val"][''])
                
                discovered.append({"udn" : udn , "model" : model , "devicenumber" : x})
    except Exception , e:       
        log.exception( e )
    return discovered            
    
def WbDiscoverCheck(ipadrs,wb=None):
    """
    Return directory of WebBrick properties given an IP address, or None
    If a dictionary is supplied the new values are added to that, 
    otherwise a new dictionary is created.
    """
    Trace(ipadrs,"WbDiscoverCheck")
    try:
        wbcfg = Wb6Config(ipadrs)
        if wbcfg.getConfigXml():
            wb = {} 
            wb["ipAdr"]     = ipadrs
            wb["macAdr"]    = wbcfg.getMacAddress()
            wb["nodeNum"]   = wbcfg.getNodeNumber()
            wb["nodeName"]  = wbcfg.getNodeName()
            wb["attention"] = False
        else:
            wb = None
    except Exception, ex:
        log = logging.getLogger( "WebBrickGwConfig.Discovery.WbDiscoverCheck" )
        log.error( "Wb6Config from %s" % ( ipadrs ) )
        log.exception( ex )
        wb = None
    return wb

class SpDiscoverCheck(threading.Thread):
    def __init__(self ,Addresses,User,Password,Callback):
        threading.Thread.__init__(self)
        self._log = logging.getLogger( "WebBrickGWConfig.Discovery.SpDiscoverCheck" )
        self._log.debug("Finding Siteplayers")
        self.callback = Callback
        self.setDaemon( True )
        self.addresses = Addresses
        self.user = User
        self.password = Password
        self.callback = Callback
        threading.Thread.start(self)
        
   
    def run(self):
        """
        Will terminate after trying all ips
        """        
        players = []
        for address in self.addresses:
            sp = SitePlayer(address,self.user,self.password)
            try:
                player = {}
                if sp.SitePlayerAvailable():
                    player['name'] = sp.GetName()
                    player['ipAdr'] = address
                    player['username'] = self.user
                    player['password'] = self.password
                    self._log.debug("Found siteplayer on IP: %s" % address)

            except Exception , ex:
                #no player as we got an exception
                self._log.error(ex)
                continue
            if player != {}:
                players.append(player)                    
        for spt in players:            
            self.callback(spt)
                
class StartechDiscovery(threading.Thread):
    def __init__(self):
        self._log = logging.getLogger ("WebBrickGwConfig.Startechdiscovery")
        threading.Thread.__init__(self)
        self.setDaemon( True ) 
        # Retrive default timeout
        timeout = socket.getdefaulttimeout()
        self._log.debug("Default time out is set to: %s" % timeout)
        self._socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        self._socket.setsockopt( socket.SOL_SOCKET, socket.SO_BROADCAST, 1 )
        self._socket.bind(('10.100.100.14', 0))        
        self._socket.setblocking(0)
        self._callbacks = {}
        
        
    def subscribe(self, name, callback):
        """ 
        Subscribes a callback for an event.

        @param name: name of the event. At the moment may only be: 
             "new_exterity_event" 
        
        @param callback: callback

        @type name: string
        @type callback: callable
        """
        self._callbacks.setdefault(name, []).append(callback)
    
    def unsubscribe(self, name, callback):
        """ 
        Unsubscribes a callback for an event.

        @param name: name of the event
        @param callback: callback

        @type name: string
        @type callback: callable
        """
        callbacks = self._callbacks.get(name, [])
        [callbacks.remove(c) for c in callbacks]
        self._callbacks[name] = callbacks
    
    def doCallback(self, name, *args):
        """ 
        Performs callbacks for events.
        """
        for callback in self._callbacks.get(name, []):
            callback(*args)
     
    def start(self):
        """ 
        Starts the Exterity Listener on its own Thread
        """
        self._log.debug("Starting Exterity Listener Thread")
        threading.Thread.start(self)
    
    def stop(self):
        """ 
        Will 'gracefully' stop the Exterity Listener 
        """
        self._running = False
        self._log.debug("Stop of Exterity Listener main loop requested")
        
    def run(self):
        """
        Called on new thread, when the Tread.start() is called
        Will termintate after socket has timed 4 times.
        """
        buff = ''
        discovermessage = ''
        startechhi = (67, 33, 48, 57, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        for x in startechhi:
            discovermessage += chr(x)
        self._running = True
        timeout_count = 0
        discoveredlist = {}
        while self._running:
        
                ready_to_read , ready_to_write , in_error = select.select([self._socket],[self._socket],[self._socket],1)
                
                if self._socket in ready_to_read:
                    #we have stuff from what is hopefully a startech box
                    #they send their data in 20 byte chunks
                    buff += self._socket.recv( 200 )
                    if len(buff) >= 20:
                        #got enough to process a packet
                        ip = self.quickIp(buff[0:20])
                        
                        if not discoveredlist.has_key(ip):
                            params = self.getParams(buff[0:20])
                            buff = buff[20:]
                            if params:
                                discoveredlist[ params["settings"]["IP"] ] = 1
                                self.doCallback("new_startech_event" , params)
                                self._log.debug("Received UDP from startech box on IP: %s" %params["settings"]["IP"])
                                #print "FOUND STARTECH %s" %params                 
                                    
                elif timeout_count > 4:
                    self._running = False
                    
                elif self._socket in ready_to_write:
                    self._socket.sendto(discovermessage , ("255.255.255.255",36))
                    timeout_count += 1
                    time.sleep(2)               
                
                else:
                    time.sleep(2)
                    timeout_count += 1
                      
        self._socket.close()
        self._log.debug("Startech discovery main loop has stopped") 
    def quickIp(self , message):
        return "%s.%s.%s.%s" %( ord( message[4] ) , ord( message[5] ) , ord( message[6] ) , ord( message[7] ) )
    def getParams(self , message):
        """
        function to return a dictonary of parameters of the exeterity box on the 
        given address.
        
        @params ipaddr: The IP address
        
        @type ipaddr: string 
        """
        
        result = None
        try:
            if message[0:4] == "C!09":
                ip = "%s.%s.%s.%s" %( ord( message[4] ) , ord( message[5] ) , ord( message[6] ) , ord( message[7] ) )
                subnet = "%s.%s.%s.%s" %( ord( message[8] ) , ord( message[9] ) , ord( message[10] ) , ord( message[11] ) )
                MAC = ''
                MAC += hex(ord( message[12] )).split('x')[1] 
                MAC += ':' + hex(ord( message[13] )).split('x')[1] 
                MAC += ':' + hex(ord( message[14] )).split('x')[1] 
                MAC += ':' + hex(ord( message[15] )).split('x')[1] 
                MAC += ':' + hex(ord( message[16] )).split('x')[1] 
                MAC += ':' + hex(ord( message[17] )).split('x')[1]
                DeviceID = "%s" %struct.unpack("!h",message[18:20])
                
                startech = StartechWrapper(ip , "")
                settings = startech.GetSettings()
                if settings["DeviceID"] == DeviceID:
                    result = { 'settings' : settings , 'MAC' : MAC }
                else:
                    self._log.error("Device Ids do not match , something is wrong ! Startechs settings : %s , UDP contents : %s" %(settings,DeviceID))
        except Exception, e:
            self._log.error(e)   
        return result
        
        
class ExterityDiscovery(threading.Thread):
    def __init__(self):
        self._log = logging.getLogger ("WebBrickGwConfig.ExterityDiscovery")
        threading.Thread.__init__(self)
        self.setDaemon( True )
        self._recievePort = 162
        # Retrive default timeout
        timeout = socket.getdefaulttimeout()
        self._log.debug("Default time out is set to: %s" % timeout)
        self._socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        self._socket.bind(('', self._recievePort))
        self._socket.setsockopt( socket.SOL_SOCKET, socket.SO_BROADCAST, 1 )
        
        self._callbacks = {}
        
        
    def subscribe(self, name, callback):
        """ 
        Subscribes a callback for an event.

        @param name: name of the event. At the moment may only be: 
             "new_exterity_event" 
        
        @param callback: callback

        @type name: string
        @type callback: callable
        """
        self._callbacks.setdefault(name, []).append(callback)
    
    def unsubscribe(self, name, callback):
        """ 
        Unsubscribes a callback for an event.

        @param name: name of the event
        @param callback: callback

        @type name: string
        @type callback: callable
        """
        callbacks = self._callbacks.get(name, [])
        [callbacks.remove(c) for c in callbacks]
        self._callbacks[name] = callbacks
    
    def doCallback(self, name, *args):
        """ 
        Performs callbacks for events.
        """
        for callback in self._callbacks.get(name, []):
            callback(*args)
     
    def start(self):
        """ 
        Starts the Exterity Listener on its own Thread
        """
        self._log.debug("Starting Exterity Listener Thread")
        threading.Thread.start(self)
    
    def stop(self):
        """ 
        Will 'gracefully' stop the Exterity Listener 
        """
        self._running = False
        self._log.debug("Stop of Exterity Listener main loop requested")
        
    def run(self):
        """
        Called on new thread, when the Tread.start() is called
        Will termintate after socket has timed 4 times.
        """
        self._running = True
        timeout_count = 0
        alreadyDiscovered = {}
        while self._running:
            try:
                (data,addr) = self._socket.recvfrom( 100 )
                if addr not in alreadyDiscovered:
                    params = self.getParams(addr[0])
                    if params:
                        if params["type"] == "encoder":
                            self._log.debug("Received UDP from Exterity Encoder Box on IP: %s , Name : %s , Location : %s" %(addr[0],params["name"],params["location"]))
                            self.doCallback("new_exterity_encoder_event", params)
                            
                        elif params["type"] == "decoder":
                            self._log.debug("Received UDP from Exterity Decoder Box on IP: %s , Name : %s , Location:  %s" %(addr[0],params["name"],params["location"]))
                            self.doCallback("new_exterity_decoder_event", params)
                        alreadyDiscovered[addr] = ''    
                    else:
                        self._log.debug("Received UDP from an unknown device on IP: %s" % addr[0])
                else:
                    self._log.debug("Received UDP from an already discovered device on IP: %s" % addr[0])
            except Exception, ex: 
                if str(ex) == "timed out": 
                    self._log.debug("Socket timeout, lets try again ")
                    if timeout_count > 4:
                        self._running = False;      
                    else:
                        timeout_count += 1
                else: 
                    self._log.exception(ex)
                      
        self._socket.close()
        self._log.debug("Exterity Listener main loop has stopped") 
    
    def getParams(self, ipaddr):
        """
        function to return a dictonary of parameters of the exeterity box on the 
        given address.
        
        @params ipaddr: The IP address
        
        @type ipaddr: string 
        """
        
        result = None
        
        auth = 'Basic ' + 'YWRtaW46bGFicmFkb3I=\n'  # to obsure the default details
        conn = httplib.HTTPConnection(ipaddr)
        conn.putrequest("GET", "/cgi-bin/general.cgi")
        conn.putheader("Authorization", auth)
        conn.endheaders()
        response = conn.getresponse()
        general_html = None
        if response.status == 200:
            self._log.debug("Got /cgi-bin/general.cgi")
            general_html = response.read()
        else:
            #for newer exterity models general.cgi 404s so we have to do this
            conn.putrequest("GET", "/cgi-bin/general")
            conn.putheader("Authorization", auth)
            conn.endheaders()
            response = conn.getresponse()            
            if response.status == 200:
                self._log.debug("Got /cgi-bin/general")
                general_html = response.read()
        
        if general_html:
                
            result = dict()
            #encconf only exists on older SD encoders
            conn.putrequest("GET" , "/cgi-bin/encconf.cgi")
            conn.putheader("Authorization", auth)
            conn.endheaders()
            encoder_response = conn.getresponse()
            #decconf only exists on decoders
            conn.putrequest("GET" , "/cgi-bin/decconf.cgi")
            conn.putheader("Authorization", auth)
            conn.endheaders()
            decoder_response = conn.getresponse()
            #encoding_enc only exists on newer HD encoders
            conn.putrequest("GET" , "/cgi-bin/encoding_enc")
            conn.putheader("Authorization", auth)
            conn.endheaders()
            hd_encoder_response = conn.getresponse()
            self._log.debug("Page status on device : %s \n\t\t\tencconf.cgi : %s \n\t\t\tdecconf.cgi : %s \n\t\t\tencoding_enc : %s" %(ipaddr,encoder_response.status,decoder_response.status,hd_encoder_response.status))
            if encoder_response.status == 200:
                #general.cgi from an encoder is malformed on some firmware versions and has technically unsafe html in it
                #so we have to look for strings
                try:
                    temp_data = getDictFromXmlString(general_html)
                    result["name"] = temp_data["html"]["body"]["form"]["table"]["tr"][0]["td"][1]["input"]["value"]
                    result["location"] = temp_data["html"]["body"]["form"]["table"]["tr"][1]["td"][1]["input"]["value"]
                    result["ip"] = ipaddr
                    result["type"] = "encoder"
                except:
                    self._log.debug("Extertity encoder generated an unsafe html page, resorting to string searching")
                    #self._log.debug("HTML is %s" %general_html)
                    name_startstring = """<TD><INPUT NAME=Name TYPE=TEXT value="""
                    name_endstring = """"></TD>
</TR>
<TR>
<TD>Location:</TD>"""
                    namestart = general_html.find(name_startstring) + 1 #add one before there is a quotation mark after this THEN the name
                    nameend = general_html.find(name_endstring)
                    result["name"] = general_html[namestart + len(name_startstring):nameend]
                    
                    location_startstring = """<TD><INPUT NAME=Location TYPE=TEXT value="""
                    location_endstring = """"></TD>
</TR>
<TR>
<TD></TD>
<TD align=center><INPUT type="submit" value="Apply"></TD>
"""
                    locationstart = general_html.find(location_startstring) + 1 #add one before there is a quotation mark after this THEN the name
                    locationend = general_html.find(location_endstring)
                    result["location"] = general_html[locationstart + len(location_startstring):locationend]
                    #self._log.debug("Got encconf.cgi , general.cgi is %s" %general_html[bodystart:bodyend+7])
                result["ip"] = ipaddr
                result["type"] = "encoder"
                result["streamUrl"] = GetStreamUrl(ipaddr)
                
            elif decoder_response.status == 200:
                temp_data = getDictFromXmlString(general_html)
                result["name"] = temp_data["html"]["body"]["form"]["table"]["tr"][0]["td"][1]["input"]["value"]
                result["location"] = temp_data["html"]["body"]["form"]["table"]["tr"][1]["td"][1]["input"]["value"]
                result["ip"] = ipaddr
                result["type"] = "decoder"
            elif hd_encoder_response.status == 200:
                bodystart = general_html.find("<body")
                bodyend = general_html.find("</body>")
                temp_data = getDictFromXmlString(general_html[bodystart:bodyend+7])
                result["name"] = temp_data["body"]["form"]["table"][1]["tr"][0]["td"]["input"]["value"]
                result["location"] = temp_data["body"]["form"]["table"][1]["tr"][1]["td"]["input"]["value"]
                result["ip"] = ipaddr
                result["type"] = "encoder"
                result["streamUrl"] = GetStreamUrl(ipaddr)
            else:
                #neither page exist so this is an unencountered type of exterity device
                result = None
        return result
        
        
        
    


# End. $Id: Discovery.py 2610 2008-08-11 20:08:49Z graham.klyne $
