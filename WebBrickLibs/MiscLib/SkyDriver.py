# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: SkyDriver.py 2760 2008-09-19 14:29:53Z graham.klyne $
# This class is responsible for decoding information using the Sky RS232 protocol. The driver class presents an easy to use interface which generates appropriate messages for the sky box
# the driver class also processeses messsages from the lutron and puts them into event format
#  it is designed to accept a continous byte stream and only produce messages when a valid message is decoded
# An important note , the skybox does not accept commands via its RS232 port so Encode and GetCommands remain unimplemented 

import logging
from struct import *

class SkyDriver():

#It accepts a string
#Requests to generate a command takes a string describing the command then a dictionary of parameters for the command

    def __init__( self , Ident ):
        self._lights = dict()
        self._ident = Ident      
        self._log = logging.getLogger( "EventHandlers.Serial" )

    #GetEvents is designed to accept a message from the Lutron device and extract any relevant information from it returning a list of dictionaries in the format { "source": X , "type": X, "payload" : X } 
    def GetEvents( self , Message ):
        events = []
        ChannelNumber = self.GetChannelNumber(Message)
        if ChannelNumber != 0:
            event = {'source': 'Sky/Device/Id/%s/ChannelNumber' %self._ident , 'type' : 'Sky/Device/Update', 'payload' : {'val' : ChannelNumber} }
            events.append(event)
            if int(str(ChannelNumber)[1:3]) > 9:
                event2 = {'source': 'Sky/Device/Id/%s/ShortChannelNumber' %self._ident , 'type' : 'Sky/Device/Update', 'payload' : {'val' : str(ChannelNumber)[1:3]} }
                events.append(event2)
            else:
                event2 = {'source': 'Sky/Device/Id/%s/ShortChannelNumber' %self._ident , 'type' : 'Sky/Device/Update', 'payload' : {'val' : str(ChannelNumber)[2]} }
                events.append(event2)
            self._log.debug("Received channelnumber : %i" %ChannelNumber)
            
        ChannelName = self.GetChannelName(Message)
        if ChannelName != '':
            event = {'source': 'Sky/Device/Id/%s/ChannelName' %self._ident , 'type' : 'Sky/Device/Update', 'payload' : {'val' : unicode(ChannelName)} }
            events.append(event)
            self._log.debug("Received channelame : %s" %ChannelName)
            
        ProgramName = self.GetProgramName(Message)
        if ProgramName != '':
            event = {'source': 'Sky/Device/Id/%s/ProgramName' %self._ident , 'type' : 'Sky/Device/Update', 'payload' : {'val' : unicode(ProgramName)} }
            events.append(event)
            self._log.debug("Received programname : %s" %ProgramName)
            
        ProgramDescription = self.GetProgramDescription(Message)
        if ProgramDescription != '':
            event = {'source': 'Sky/Device/Id/%s/ProgramDescription' %self._ident , 'type' : 'Sky/Device/Update', 'payload' : {'val' : unicode(ProgramDescription)} }
            events.append(event)
            self._log.debug("Received programdescription : %s" %ProgramDescription)
        
        CurrentTime = self.GetCurrentTime(Message)
        if CurrentTime != '':
            event = {'source': 'Sky/Device/Id/%s/CurrentTime' %self._ident , 'type' : 'Sky/Device/Update', 'payload' : {'val' : CurrentTime} }
            events.append(event)
            self._log.debug("Received currenttime : %s" %CurrentTime)

        PowerState = self.GetPowerState(Message)
        if PowerState != '':
            event = {'source': 'Sky/Device/Id/%s/PowerState' %self._ident , 'type' : 'Sky/Device/Update', 'payload' : {'val' :  PowerState} }
            events.append(event)
            self._log.debug("Received PowerState : %s" %PowerState)
            
        StartTime = self.GetStartTime(Message)  
        if StartTime != '':
            event = {'source': 'Sky/Device/Id/%s/StartTime' %self._ident , 'type' : 'Sky/Device/Update', 'payload' : {'val' : StartTime} }
            events.append(event)
            self._log.debug("Received starttime : %s" %StartTime)  
        
        Failure = self.GetFailure(Message)  
        if Failure:
            event = {'source': 'Sky/Device/Id/%s/StartTime' %self._ident , 'type' : 'Sky/Device/Update', 'payload' : {'val' : '--'} }
            events.append(event)
            self._log.debug("Received starttime : %s" %Failure)  
            
            event = {'source': 'Sky/Device/Id/%s/ProgramDescription' %self._ident , 'type' : 'Sky/Device/Update', 'payload' : {'val' : 'Channel Unavailable'} }
            events.append(event)
            self._log.debug("Received programdescription : %s" %ProgramDescription)
            
            event = {'source': 'Sky/Device/Id/%s/ProgramName' %self._ident , 'type' : 'Sky/Device/Update', 'payload' : {'val' : 'Error'} }
            events.append(event)
            self._log.debug("Received programname : %s" %ProgramName)
            
            event = {'source': 'Sky/Device/Id/%s/ChannelName' %self._ident , 'type' : 'Sky/Device/Update', 'payload' : {'val' : '--'} }
            events.append(event)
            self._log.debug("Received channelame : %s" %ChannelName)
            
            event = {'source': 'Sky/Device/Id/%s/ChannelNumber' %self._ident , 'type' : 'Sky/Device/Update', 'payload' : {'val' : '---'} }
            events.append(event)
            
            event2 = {'source': 'Sky/Device/Id/%s/ShortChannelNumber' %self._ident , 'type' : 'Sky/Device/Update', 'payload' : {'val' : '0' } }
            events.append(event2)
            
        return events
        
    
    def GetPacketByType(self,Message,Typename):
        packet = ''
        if len(Typename) == 4:
            if Message.find(Typename) != -1:
                try:
                    start  = Message.find(Typename)            
                    self._log.debug("Found %s in message, , message is %s , data index is %i" %(Typename,Message,start))
                    packetsize = int(Message[start+4:start+7])
                    packet = Message[start:start+packetsize]
                except Exception , e:
                    self._log.error(e)
                    pass        
        return packet
        
    def GetFailure(self,Message):
        #PUCP delimits an error message  
        fail = False      
        if len(Message) > 7:
            packet = self.GetPacketByType(Message,"PUCP")
            if packet.find('Audio Unavailable Please check your digital satellite receiver') != -1:
                fail = True
        return fail
    
    def GetChannelNumber(self,Message):
        #SSCN delimits the channel number        
        channelnumber = 0
        if len(Message) > 7:
            packet = self.GetPacketByType(Message,"SSCN")
            if packet != '':
                channelnumber = int(packet[7:])
                self._log.debug("Channel number is %i" %int(channelnumber))
        return channelnumber
    
    def GetChannelName(self,Message):
        #SSCA delimits the channel number
        channelname = ''
        if len(Message) > 7:
            packet = self.GetPacketByType(Message,"SSCA")
            if packet != '':
                channelname = packet[7:]
                self._log.debug("Channel name is %s" %channelname)
        return channelname

    def GetCurrentTime(self,Message):
        #SSDT0 delimits the channel number
        currenttime = ''
        if len(Message) > 7:
            packet = self.GetPacketByType(Message,"SSDT")
            if packet != '':
                currenttime = packet[7:]
                self._log.debug("Channel name is %s" %currenttime)
        return currenttime
        
    def GetStartTime(self,Message):
        #SST0 delimits the channel number
        starttime = ''
        if len(Message) > 7:
            packet = self.GetPacketByType(Message,"SST0")
            if packet != '':
                starttime = packet[7:]
                self._log.debug("Channel name is %s" %starttime)
        return starttime
        
    def GetPowerState(self,Message):
        #SST0 delimits the channel number
        powerstate = ''
        if len(Message) >= 7:            
            packet = self.GetPacketByType(Message,"SYST")
            if packet != '':
                powerstate = packet[7:]
                #powerstates are inverted on skybox for some reason
                if powerstate == '0':
                    powerstate = '1'
                else:
                    powerstate = '0'
                self._log.debug("PowerState name is %s" %powerstate)
        return powerstate
        
    def GetProgramName(self,Message):
        programname = ''
        if len(Message) > 7:
            packet = self.GetPacketByType(Message,"SSN0")
            if packet != '':
                if packet.find(chr(0x86)) != -1:
                    if packet.find(chr(0x87)) != -1:
                        namestart = packet.find(chr(0x86))
                        nameend = packet.find(chr(0x87)) 
                        programname = packet[namestart+1:nameend]
                        self._log.debug("Channel description is %s" %programname)
        return programname
        
    def GetProgramDescription(self,Message):             
        #SSE0 delimits the channel number
        programdescription = ''
        if len(Message) > 7:
            packet = self.GetPacketByType(Message,"SSE0")
            if packet != '':
                programdescription = packet[7:]
                self._log.debug("Channel description is %s" %programdescription)
        return programdescription
    
           
    def GetCommand( self , Command , Params ):        
        pass     

class SkyProtocolHandler():
#Messages are decoded into a list of strings
#Messages are encoded into a byte list

    def __init__(self):        
        self._log = logging.getLogger( "EventHandlers.Serial" )
        self._buffer = ''
#first byte in a sky message is always \n
#followed by 3 bytes indicating the total packet length not including the \n
#following by multiple subpackets
#subpackets take the format of a 4 byte type at the beggining , 3 bytes to indicate length , followed by the data         
    def Decode(self,Message):
        messages = []
        self._log.debug("Incoming section is ##%s##" %Message)
        self._buffer = self._buffer + Message
        self._log.debug("Buffer concated with incoming section is ##%s##" %self._buffer)
        try:
            for x in range(0,self._buffer.count('\n')):
                if self._buffer.find('\n') != 0:
                    self._log.debug("First newline has data before it, deleting junk data : %s" %self._buffer[0:self._buffer.find('\n')])
                    self._buffer=  self._buffer[self._buffer.find('\n'):]
                start = self._buffer.find('\n')
                if self._buffer[start+1] == '\n':
                    start = start+1
                self._log.debug("Startindex is %i" %start)
                #check the buffer is long enough to contain the length information for the message
                if len(self._buffer) > (start + 4):
                    self._log.debug("Buffer[start+1:start+4] is %s " %self._buffer[start+1:start+4])
                    messagelength = int(self._buffer[start+1:start+4])                
                    self._log.debug("Messagelength is %s" %messagelength)
                    #look for the start of the next packet , if it occurs before the supposed message length then the current message is truncated and should be discarded
                    if (self._buffer[start+1:].find('\n') < messagelength) & (self._buffer[start+1:].find('\n') != -1):
                        self._log.debug("Did not receive all of this message, discarding it")
                        end = self._buffer[start+1:].find('\n')
                        self._buffer = self._buffer[end:]
                    else:
                        self._log.debug("Bufferlength is %i , Messagelength +1 is %i" %(len(self._buffer),messagelength+1))
                        if len(self._buffer) >= (messagelength + 1):
                            message = self._buffer[start+4:messagelength-1]
                            self._log.debug("Message is %s" %message)
                            checksum = 0
                            #the checksum is all the bytes in the message (including the newline) summed then mod(256), excluding the checksum byte of course
                            for x in self._buffer[start:start + messagelength -1]:
                                checksum = checksum + ord(x)                        
                            checksum = checksum % 256
                            self._log.debug("Checksum is %s , sent checksum is %s" %(hex(checksum),int(self._buffer[start+messagelength-1:start+messagelength+1],16)))   
                            if  checksum == int(self._buffer[start+messagelength-1:start+messagelength+1],16):                    
                                self._log.debug("Checksum correct")
                                self._buffer = self._buffer[start + messagelength+1:]
                                self._log.debug("Buffer is : #%s#" %self._buffer)
                                messages.append(message)
                            else:
                                self._log.debug("Checksums do not match, discarding message")
                                self._buffer = self._buffer[start + messagelength+1:]
        except:
            #exception occured at some point while trying to process the buffer , probably caused by the skybox sending debug messages 
            self._log.error("Skybox sent garbage, clearing the buffer")
            self._buffer = ''
            
        return messages
    
    def Encode(self,Message):
        pass
    
    
    
    
    
    
    
    
    
    
    

# $Id: LutronDriver.py 2760 2008-09-19 14:29:53Z graham.klyne $
