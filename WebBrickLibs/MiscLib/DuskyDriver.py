# $Id: DuskyDriver.py 2760 2008-09-19 14:29:53Z graham.klyne $
# This class is responsible for one way communication with the Dusky IR injector that is used to communicate with a Sky boxd
import logging
from struct import *

class DuskyDriver():

#It accepts a string
#Requests to generate a command takes a string describing the command then a dictionary of parameters for the command

    def __init__( self , Ident ):
        self._lights = dict()
        self._ident = Ident      
        self._log = logging.getLogger( "EventHandlers.Serial" )

    #GetEvents is designed to accept a message from the Lutron device and extract any relevant information from it returning a list of dictionaries in the format { "source": X , "type": X, "payload" : X } 
    def GetEvents( self , Message ):
        pass

    def GetCommand( self , Command , Params  = None):
        message = ''
        if Command == "setchannel":
            if Params.has_key("val"):
                chnl = Params["val"]
                if len(chnl) == 3:
                    message = "As01sk%sx" %chnl
                else:
                    self._log.error("Setchannel request incorrectly formatted, channel number should be 3 digits in length, currently is %s" %chnl)
        elif Command == "on":
            message = "As01skx"
        elif Command == "off":
            message = "As01skkpx"
        elif Command == "channelup":
            message = "As01skf+x"
        elif Command =="channeldown":
            message = "As01skf-x"
        return message     

class DuskyProtocolHandler():
#Messages are decoded into a list of strings
#Messages are encoded into a byte list

    def __init__(self):        
        self._log = logging.getLogger( "EventHandlers.Serial" )
        self._buffer = ''
   
    def Decode(self,Message):
        return []
    
    def Encode(self,Message):
        encoded = []
        for x in Message:
            encoded.append(ord(x))    
        return encoded
    
    
    
    
    
    
    
    
    
    
    

# $Id: LutronDriver.py 2760 2008-09-19 14:29:53Z graham.klyne $
