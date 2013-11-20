# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: LutronDriver.py 2760 2008-09-19 14:29:53Z graham.klyne $
# This class is responsible for decoding and encoding information using the Lutron RS232 protocol. The driver class presents an easy to use interface which generates appropriate messages for the lutron
# the driver class also processeses messsages from the lutron and puts them into event format
# The protocol handler class ensures the message is encoded to a byte list correctly, or decoded it into a string correctly
# it is designed to accept a continous byte stream and only produce messages when a valid message is decoded


import logging


class LutronLightDriver():

#It accepts a string
#Requests to generate a command takes a string describing the command then a dictionary of parameters for the command

    def __init__( self , Ident):
        self._lights = dict()
        self._ident = Ident            
        self._log = logging.getLogger( "LutronLightDriver" )

    #GetEvents is designed to accept a message from the Lutron device and extract any relevant information from it returning a list of dictionaries in the format { "source": X , "type": X, "payload" : X } 
    def GetEvents( self , Message ):
        events = []
        if Message != None:
            if Message.find("KLS, [") != -1:
                events.extend(self.GetLightUpdates(Message))
        return events        
    
    def GetLightUpdates(self,KLS):
        self._log.debug("KLS IS %s" %KLS)
        events = []
        infoIndex = KLS.find("[")
        infoIndex += 1         
        self._log.debug("Index of index is %s" %infoIndex)
        processor = str(KLS[infoIndex:infoIndex+2])
        link = str(KLS[infoIndex+3:infoIndex+5])
        keypad = str(KLS[infoIndex+6:infoIndex+8])
        self._log.debug("Processor:%s , Link:%s , Keypad:%s" %(processor,link,keypad))
        lightsindex = KLS.find("], ")
        lightsindex += 3
        lights  = KLS[lightsindex:lightsindex+24]
        self._log.debug("Lights :%s" %lights)
        for light in range(0 , len(lights)):
            if light < 9:
                light = '0%s' %(light+1)
            else:
                light = '%s' %(light+1)
            if self._lights.has_key( processor ):
                if self._lights[processor].has_key( link):
                    if self._lights[processor][link].has_key(keypad):
                        if self._lights[processor][link][keypad].has_key(light):
                            if self._lights[processor][link][keypad][light] != lights[int(light)-1]:
                                self._lights[processor][link][keypad][light] = lights[int(light)-1]
                                event = {'source': 'Lutron/Device/Id/%s/Processor_%s/Link_%s/Keypad_%s/Light_%s' %(self._ident,processor,link,keypad,light) , 'type' : 'Lutron/Lighting/Update' , 'payload' : {'val' : lights[int(light)-1]} }
                                events.append(event)     
                        else:
                            self._lights[processor][link][keypad][light] = lights[int(light)-1]
                            event = {'source': 'Lutron/Device/Id/%s/Processor_%s/Link_%s/Keypad_%s/Light_%s' %(self._ident,processor,link,keypad,light) , 'type' : 'Lutron/Lighting/Update' , 'payload' : {'val' : lights[int(light)-1]} }
                            events.append(event)
                    else:
                        self._lights[processor][link][keypad] = dict()
                        self._lights[processor][link][keypad][light] = lights[int(light)-1]   
                        event = {'source': 'Lutron/Device/Id/%s/Processor_%s/Link_%s/Keypad_%s/Light_%s' %(self._ident,processor,link,keypad,light) , 'type' : 'Lutron/Lighting/Update' , 'payload' : {'val' : lights[int(light)-1]} }
                        events.append(event)                       
                else:
                    self._lights[processor][link] = dict()
                    self._lights[processor][link][keypad] = dict()
                    self._lights[processor][link][keypad][light] = lights[int(light)-1]       
                    event = {'source': 'Lutron/Device/Id/%s/Processor_%s/Link_%s/Keypad_%s/Light_%s' %(self._ident,processor,link,keypad,light) , 'type' : 'Lutron/Lighting/Update' , 'payload' : {'val' : lights[int(light)-1]} }
                    events.append(event)            
                    
            else:
                self._lights[processor] = dict()
                self._lights[processor][link] = dict()
                self._lights[processor][link][keypad] = dict()    
                self._lights[processor][link][keypad][light] = lights[int(light)-1]            
                event = {'source': 'Lutron/Device/Id/%s/Processor_%s/Link_%s/Keypad_%s/Light_%s' %(self._ident,processor,link,keypad,light) , 'type' : 'Lutron/Lighting/Update' , 'payload' : {'val' : lights[int(light)-1]} }
                events.append(event)
        return events                    
        
    def GetCommand( self , Command , Params ):        
        message = []
        if Command == "togglelight":
            if Params.has_key("processor") & Params.has_key("link") & Params.has_key("keypad") & Params.has_key("light"):
                message = "KBP, [%s:%s:%s], %s" %(Params["processor"],Params["link"],Params["keypad"],Params["light"])
        return message        

class LutronProtocolHandler():
#Messages are decoded into a list of strings
#Messages are encoded into a byte list

    def __init__(self):        
        self._log = logging.getLogger( "LutronProtocolHandler" )
        self._buffer = ''
        
    def Decode(self,Message):
        messages = []
        self._buffer = self._buffer + Message        
        if self._buffer.count("\r") != -1:
            messagecount = self._buffer.count("\r")
            splitmessage = self._buffer.split("\r")
            for x in range(0,messagecount):
                messagestring = ''
                for y in range(0,len(splitmessage[x])):
                    messagestring += chr(ord(splitmessage[x][y]))
                messages.append(messagestring)
            
            self._buffer = ''
            self._buffer += splitmessage[messagecount]
        return messages     
    def Encode(self,Message):
        encoded = []
        for x in Message:
            encoded.append(ord(x))
        if encoded != None:
            encoded.append(ord('\r'))
        return encoded
    
    
    
    
    
    
    
    
    
    
    
    

# $Id: LutronDriver.py 2760 2008-09-19 14:29:53Z graham.klyne $
