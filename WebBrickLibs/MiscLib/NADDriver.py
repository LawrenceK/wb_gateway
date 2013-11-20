# $Id: LutronDriver.py 2760 2008-09-19 14:29:53Z graham.klyne $
# This class is responsible for decoding and encoding information using the Lutron RS232 protocol. The driver class presents an easy to use interface which generates appropriate messages for the lutron
# the driver class also processeses messsages from the lutron and puts them into event format
# The protocol handler class ensures the message is encoded to a byte list correctly, or decoded it into a string correctly
# it is designed to accept a continous byte stream and only produce messages when a valid message is decoded


import logging


class NADDriver():

#It accepts a string
#Requests to generate a command takes a string describing the command then a dictionary of parameters for the command

    def __init__( self , Ident):
        self._lights = dict()
        self._ident = Ident            
        self._log = logging.getLogger( "Misclib.NADDriver" )
        self._currentSource = ''
    #GetEvents is designed to accept a message from the Lutron device and extract any relevant information from it returning a list of dictionaries in the format { "source": X , "type": X, "payload" : X } 
    def GetEvents( self , Message ):
        events = []
        
        if Message != None:
            if len(Message) >= 3:
                if Message[0] == 20:
                    if Message[1] == 88:
                        if Message[2] == 0:
                            #stopped
                            event = { 'payload':{ 'stop':1 , 'play' : 0 , 'pause' : 0, 'ff' : 0 , 'rew' : 0} , 'source': 'to_ui/%s/NAD/5/PlayState/Changed' %self._ident, 'type' : 'NAD/5/PlayState' }                            
                            events.append(event)
                        if Message[2] == 1:
                            #playing
                            event = { 'payload':{ 'stop':0 , 'play' : 1 , 'pause' : 0, 'ff' : 0 , 'rew' : 0 } , 'source': 'to_ui/%s/NAD/5/PlayState/Changed' %self._ident, 'type' : 'NAD/5/PlayState' }       
                            events.append(event)
                        if Message[2] == 2:
                            #paused
                            event = { 'payload':{ 'stop':0 , 'play' : 0 , 'pause' : 1 , 'ff' : 0 , 'rew' : 0 } , 'source': 'to_ui/%s/NAD/5/PlayState/Changed' %self._ident, 'type' : 'NAD/5/PlayState' }       
                            events.append(event)
                        if Message[2] == 13:
                            #paused
                            event = { 'payload':{ 'stop':0 , 'play' : 0 , 'pause' : 0 , 'ff' : 1 , 'rew' : 0 } , 'source': 'to_ui/%s/NAD/5/PlayState/Changed' %self._ident, 'type' : 'NAD/5/PlayState' }       
                            events.append(event)
                        if Message[2] == 24:
                            #paused
                            event = { 'payload':{ 'stop':0 , 'play' : 0 , 'pause' : 0 , 'ff' : 0 , 'rew' : 1 } , 'source': 'to_ui/%s/NAD/5/PlayState/Changed' %self._ident, 'type' : 'NAD/5/PlayState' }       
                            events.append(event)
                    
                    elif Message[1] == 81:
                            event = { 'payload':{ 'title': int(Message[2])  , 'chapter':int(Message[3]) } , 'source': 'to_ui/%s/NAD/5/PlayPosition/Changed' %self._ident, 'type' : 'NAD/5/PlayPosition' }
                            events.append(event)
                    
                    elif Message[1] == 21:
                        event = { 'payload':{ 'val':Message[2]} , 'source': 'to_ui/%s/NAD/5/PowerState/Changed' %self._ident, 'type' : 'NAD/5/Power' }
                        events.append(event)
                    
                    elif Message[1] == 93:
                        event = { 'payload':{ 'val':Message[2]} , 'source': 'to_ui/%s/NAD/5/Subs/Changed' %self._ident, 'type' : 'NAD/5/Subs' }
                        events.append(event)
                        
                    elif Message[1] == 23:
                        if Message[2] > 18:
                            vol = Message[2] - 256 + 81
                        else:
                            vol = Message[2] + 81
                        event = { 'payload':{ 'val':vol} , 'source': 'to_ui/%s/NAD/5/VolumeChange' %self._ident , 'type' : 'NAD/5/Volume' }
                        events.append(event)
                        
                    elif Message[1] == 24:
                        event = { 'payload':{ 'val':Message[2]} , 'source': 'to_ui/%s/NAD/5/MuteChanged' %self._ident , 'type' : 'NAD/5/Mute' }
                        events.append(event)
                        
                    elif Message[1] == 53:
                        if Message[2] != self._currentSource:
                            
                            if self._currentSource == 0:
                                events.append({ 'payload':{ 'val': 0 } , 'source': 'to_ui/%s/NAD/5/Source/DVD' %self._ident , 'type' : 'NAD/5/NewSource'}) 
                            elif self._currentSource == 1:
                                events.append({ 'payload':{ 'val': 0 } , 'source': 'to_ui/%s/NAD/5/Source/Satellite' %self._ident , 'type' : 'NAD/5/NewSource'})
                            elif self._currentSource == 2:
                                events.append({ 'payload':{ 'val': 0 } , 'source': 'to_ui/%s/NAD/5/Source/CAB/SAT' %self._ident , 'type' : 'NAD/5/NewSource'})
                            elif self._currentSource == 3:
                                events.append({ 'payload':{ 'val': 0 } , 'source': 'to_ui/%s/NAD/5/Source/VCR' %self._ident , 'type' : 'NAD/5/NewSource'})
                            elif self._currentSource == 4:
                                events.append({ 'payload':{ 'val': 0 } , 'source': 'to_ui/%s/NAD/5/Source/Video/4' %self._ident , 'type' : 'NAD/5/NewSource'})
                            elif self._currentSource == 5:
                                events.append({ 'payload':{ 'val': 0 } , 'source': 'to_ui/%s/NAD/5/Source/Tuner' %self._ident , 'type' : 'NAD/5/NewSource'})
                            elif self._currentSource == 6:
                               events.append({ 'payload':{ 'val': 0 } , 'source': 'to_ui/%s/NAD/5/Source/Ext/5/1' %self._ident , 'type' : 'NAD/5/NewSource'})
                                    
                            if Message[2] == 0:
                                events.append({ 'payload':{ 'val':1} , 'source': 'to_ui/%s/NAD/5/Source/DVD' %self._ident , 'type' : 'NAD/5/NewSource' })
                            elif Message[2] == 1:                    
                                events.append({ 'payload':{ 'val':1} , 'source': 'to_ui/%s/NAD/5/Source/Satellite' %self._ident , 'type' : 'NAD/5/NewSource' })
                            elif Message[2] == 2:                    
                                events.append({ 'payload':{ 'val':1} , 'source': 'to_ui/%s/NAD/5/Source/CAB/SAT' %self._ident , 'type' : 'NAD/5/NewSource' })
                            elif Message[2] == 3:                    
                                events.append({ 'payload':{ 'val':1} , 'source': 'to_ui/%s/NAD/5/Source/VCR' %self._ident , 'type' : 'NAD/5/NewSource' })
                            elif Message[2] == 4:                    
                                events.append({ 'payload':{ 'val':1} , 'source': 'to_ui/%s/NAD/5/Source/Video/4' %self._ident , 'type' : 'NAD/5/NewSource' })
                            elif Message[2] == 5:                    
                               events.append({ 'payload':{ 'val':1} , 'source': 'to_ui/%s/NAD/5/Source/Tuner' %self._ident , 'type' : 'NAD/5/NewSource' })
                            elif Message[2] == 6:                    
                                events.append({ 'payload':{ 'val':1} , 'source': 'to_ui/%s/NAD/5/Source/Ext/5/1' %self._ident , 'type' : 'NAD/5/NewSource' })
        return events        
    
    def GetCommand( self , Command , Params = None ):        
        message = []
        if Command == "setvolume":
            if Params.has_key("val"):
                vol = int(Params["val"])
                if (vol > 0) & (vol < 100):
                    volume = vol - 81
                    if volume < 0:
                        volume = volume + 256
                    message = (21,23,volume)
        #for commands where the second byte is 22, this is sending the NAD an IR command 
        elif Command == "up":
                #Up on the dvd menus
                message = (22, 133, 154, 93)
        elif Command == "down":
                #down on the dvd menus
                message = (22, 133, 154, 94)
        elif Command == "left":                
                message = (22, 133, 154, 96)
        elif Command == "right":
                message = (22, 133, 154, 95)
        elif Command == "ok":
                message = (22, 133, 154, 102)
        elif Command == "forward":
                #skips forward a scene
                message = (22, 133, 154, 224)
        elif Command == "rewind":
                #skips backward a scene
                message = (22, 133, 154, 225)
        elif Command == "menu":
                #opens the dvd menu
                message = (22, 133 ,154 , 89)
        elif Command == "subs":
                #switch subs
                message = (22, 133, 154, 92)
        elif Command == "audio":
                #switch audio track
                message = (22, 133, 154, 45)        
        elif Command == "mute":
                message = (21,24,1)
        elif Command == "unmute":
                message = (21,24,0)
        elif Command == "standby":
                message = (21,21,0)
        elif Command == "on":
                message = (21,21,1)
        elif Command == "play":
                message = (21,88,1)
        elif Command == "stop":
                message = (21,88,0)
        elif Command == "pause":
                message = (21,88,2)
        elif Command == "setsource":
                if Params.has_key("source"):
                    if Params["source"] == "DVD":
                        message = (21,53,0)
                    elif Params["source"] == "Satellite":
                        message = (21,53,1)
                    elif Params["source"] == "CAB/SAT":
                        message = (21,53,2)
                    elif Params["source"] == "VCR":
                        message = (21,53,3)
                    elif Params["source"] == "Video/4":
                        message = (21,53,4)
                    elif Params["source"] == "Tuner":
                        message = (21,53,5)
                    elif Params["source"] == "External/5/1":
                        message = (21,53,6)        
        return message        

class NADProtocolHandler():
#Messages are decoded into a list of strings
#Messages are encoded into a byte list

    def __init__(self):        
        self._log = logging.getLogger( "EventHandlers.Serial" )
        self._buffer = []
        
    def Decode(self,Message):
        messages = []
        self._log.debug("In message is : %s" %str(Message))
        for x in Message:
            
            if type(x) == str:                
                self._buffer.append(ord(x))
            else:
                self._buffer.append(x)
        self._log.debug("Buffer is now : %s" %self._buffer)
        #as it is a raw socket we could get anything down it so we need to walk the byte stream and check it is in order
        started = False
        closed = False
        error = False
        startedindex = 0
        cleaned = []
        self._log.debug("Attempting to clean incoming message")
        for x in range(0,len(self._buffer)):
            if x == len(self._buffer) -1:
                self._log.debug("End of message clean section : %s" %self._buffer[startedindex:])
                cleaned.extend(self._buffer[startedindex:])
            
            elif self._buffer[x] == 1:
                if started & (not closed):
                    #an error condition ,we hit the start of another packet before we closed
                    self._log.debug("Dirty section : %s" %self._buffer[startedindex:x])
                    startedindex = x
                    started = True
                    closed = False
                    error = False 
                    continue
                elif closed & started & (not error):
                    self._log.debug("New clean section: %s" %self._buffer[startedindex:x])
                    cleaned.extend(self._buffer[startedindex:x]) 
                    startedindex = x
                    started = True
                    closed = False
                    error = False 
                else:
                    self._log.debug("Started new message section")
                    startedindex = x
                    started = True
             
            elif self._buffer[x] == 2:
                if started == False:
                    #we finished before we started!
                    self._log.debug("Cleaning error, closed before opening")
                    error = True
                    continue
                else:
                    self._log.debug("Found end deliminator")
                    if self._buffer[x+1] == 1:
                        self._log.debug("Deliminator + 1 is : %s" %self._buffer[x+1])
                        error = True
                    elif self._buffer[x+1] == 94:                        
                        self._log.debug("Deliminator + 1 is : %s" %self._buffer[x+1])
                        if self._buffer[x+2] == 1:                            
                            self._log.debug("Deliminator + 1 is : %s" %self._buffer[x+1])
                            error = True
                        else:
                            self._log.debug("Closed at end of section")
                            closed = True
                    else:        
                        self._log.debug("Closed at end of section")
                        closed = True
            
        self._log.debug("Cleaned buffer is %s" %cleaned)
        self._buffer = cleaned    
        if self._buffer.count(1) > 0:
            messagecount = self._buffer.count(1)
            self._log.debug("Messagecount : %i " %messagecount)
            for x in range(0,messagecount):
                try:
                    startindex = self._buffer.index(1)
                    endindex = self._buffer.index(2)
                except ValueError, Ve:
                    continue               
                message = []
                self._log.debug("Startindex is %i , Endindex is %i" %(startindex,endindex))
                if endindex != -1:
                    if startindex < endindex:
                        crc = 99999999
                        self._log.debug("After endindex is %s" %str(self._buffer[endindex:]))
                        if len(self._buffer) > (endindex+1):
                            if self._buffer[endindex+1] == 94:
                                #94 is a control code which means that the CRC mapped to a control code so it was replaced
                                self._log.debug("CRC is overlapping with control code")
                                if len(self._buffer) > (endindex+2):
                                    if self._buffer[endindex+2] == 94:
                                        #we dont do anything to it if it is 94
                                        crc = 94
                                    else:
                                        crc = self._buffer[endindex+2] & 191
                                else:
                                    self._log.debug("CRC Not complete")
                            else:
                                crc = self._buffer[endindex+1]
                        self._log.debug("CRC is %i" %crc)
                        if crc != 999999999999999999:
                            for y in range(startindex+1,endindex):                        
                                self._log.debug("Message is : %s Current Val is : %s" %(self._buffer[y],message))
                                if self._buffer[y-1] == 94:
                                    continue
                                elif self._buffer[y] == 94:
                                    if self._buffer[y+1] == 94:
                                        message.append(94)
                                    else:
                                        message.append(self._buffer[y+1] & 191)       
                                else:
                                    message.append(self._buffer[y])
                            del self._buffer[startindex:endindex]
                            try:
                                startindex = self._buffer.index(1)
                                del self._buffer[0:startindex]
                            except ValueError , Ve:
                                self._buffer = []
                    else:
                        #somehow we the end delimiter is before the start
                        #this is probably because we missed the startindex of the previous message somehow 
                        #we remove it to stop the buffer becoming a memory leak
                        del self._buffer[0:startindex]
                    
                    self._log.debug("Buffer is %s" %self._buffer)
                    self._log.debug("Message is %s" %message)            
                    
                if (message != None) & (crc != 0):
                    temp = 0
                    for x in message:
                        temp += x
                    temp = temp % 256
                    temp = temp ^ 255    
                    if temp == crc:
                        messages.append(message)
                    else:
                        self._log.error("Message had invalid crc : %s" %message)
        return messages     
        
    def Encode(self,Message):
        #message should be a list of bytes
        encoded  = []
        if Message != None:
            encoded.append(1)
            crc = 0
            for x in range(0,len(Message)):
                crc += int(Message[x])
                if Message[x] == 94:
                    encoded.extend((94,94))
                elif (Message[x] >= 0) & (Message[x] <= 19):
                    encoded.extend(( 94 , Message[x] | 64))
                else:
                    encoded.append(Message[x])
            encoded.append(2)
            crc = crc % 256
            crc = crc ^ 255
            if (crc >= 0) & (crc <= 19):
                encoded.append(94)
                encoded.append(crc | 64)
            else:
                encoded.append(crc)
        return encoded
    
    
    
    
    
    
    
    
    
    
    
    

# $Id: LutronDriver.py 2760 2008-09-19 14:29:53Z graham.klyne $
