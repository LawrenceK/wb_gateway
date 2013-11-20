# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: ValueConvert.py 3682 2010-08-03 15:11:15Z andy.harris $
#
#  Class to handle mapping of an event to one or more new events, mapping the value attribute.
#
#  Lawrence Klyne
#
#
import logging

from EventLib.Event             import Event, makeEvent
from EventLib.Status            import StatusVal
from EventLib.SyncDeferred      import makeDeferred

from EventHandlers.BaseHandler  import BaseHandler
from EventHandlers.EventMapper  import EventMapper

from Utils import makeNewEvent
_log = logging.getLogger( "EventHandlers.ValueConvert" )

#
#
class ValueConvert( EventMapper ):
    """
    This event interface is used to create a new event with the only attribute based on mapping the value attribute.

    The configuration for an ValueConvert entry is as follows:

    <eventInterface module='EventHandlers.ValueConvert' name='ValueConvert'>
        <eventtype type="">
            <eventsource source="webbrick/100/AI/0" >
                <event>
                    <newEvent type="local/value" source="local/Humidity/0" offset="20" multiplier="1.4">
                        <>
                    </newEvent>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>

        eventtype, eventsource, event, params as as per BaseHandler.
        additonally is one or more newEvent elements that define the new event to be isssued. The type and source
        attributes of the newEvent element specify the event type and source. 
        
        The attributes offset and multipler are used to process the Val attribute of the source event by subtrating offset 
        and multiplying by multiplier.
    
    """

    def __init__ (self, localRouter):
        self._log = _log
        super(ValueConvert,self).__init__(localRouter)

    def doActions( self, actions, inEvent ):
        _log.debug( 'doActions %s %s' % ( actions, inEvent ) )
        if actions and inEvent.getPayload():
            
            for action in actions:
                _log.debug( 'Generate event %s' % ( action ) )
                evOd = inEvent.getPayload()
                
                # ensure backward compatibility and default to scaling
                conversion = "scale"
                
                if action.has_key( "conversion" ):
                    conversion = action["conversion"]
                    self._log.debug("Conversion is %s" %conversion)                    
                # scaling conversion required
                if conversion == "scale":
                    preoffset = 0.0
                    postoffset = 0.0
                    multiplier = 1.0
                    divisor = 1.0
                    val = 1.0
                    od = dict()
                    
                    # get the conversion parameters from the eventdespatch,
                    # if these are specified
                    if action.has_key( "preoffset" ):
                        preoffset = float(action["preoffset"])
                    elif action.has_key( "offset" ):
                        preoffset = float(action["offset"])

                    if action.has_key( "postoffset" ):
                        postoffset = float(action["postoffset"])

                    if action.has_key( "multiplier" ):
                        multiplier = float(action["multiplier"])

                    if action.has_key( "divisor" ):
                        divisor = float(action["divisor"])
                    
                    # get the conversion parameters from payload of incoming 
                    # event, if these are specified
                    if evOd.has_key( "preoffset" ):
                        preoffset = float(evOd["preoffset"])
                        _log.info( 'Using preoffset from payload: %s' % ( preoffset ) )
                        
                    if evOd.has_key( "postoffset" ):
                        postoffset = float(evOd["postoffset"])
                        _log.info( 'Using postoffset from payload: %s' % ( postoffset ) )
                    
                    if evOd.has_key( "multiplier" ):
                        multiplier = float(evOd["multiplier"])
                        _log.info( 'Using multiplier from payload: %s' % ( multiplier ) )

                    if evOd.has_key( "divisor" ):
                        divisor = float(evOd["divisor"])
                        _log.info( 'Using divisor from payload: %s' % ( divisor ) )

                    # get the value to be scaled from the payload of incoming
                    # event (has to be specified) 
                    if evOd.has_key( "val" ):
                        val = float(evOd["val"])
                    else:
                        _log.debug( 'No Payload "val" in: %s' % ( action ) )
                    
                    if action.has_key( "copy_other_data" ):
                        od['newVal'] = ( (val - preoffset)*multiplier/divisor) + postoffset
                        self.sendEvent( makeNewEvent( action, inEvent, od ) )
                        
                # hex to decimal conversion required
                if conversion == "hex_to_dec":
                    # setting default input and output types
                    informat = "string"
                    outformat = "int"
                    value = "00"
                    od = dict()
                    
                    if action.has_key( "informat" ):
                        informat = action["informat"]
                    
                    if action.has_key( "outformat" ):
                        outformat = action["outformat"]
                    
                    if evOd.has_key( "val" ):
                        value = evOd["val"]
                    
                    if action.has_key( "attr" ):
                        if informat == "string":
                            if outformat == "int":
                                od[action["attr"]] = int( value, 16 )
                            elif outformat == "string":
                                od[action["attr"]] = string(int( value, 16 ))    
                        self.sendEvent( makeNewEvent( action, inEvent, None, od ) )
                
                 # integer to decimal conversion required
                if conversion == "dec_to_hex":
                    # setting default input and output types
                    informat = "int"
                    outformat = "string"
                    value = 0
                    od = dict()
                    
                    if action.has_key( "informat" ):
                        informat = action["informat"]
                    
                    if action.has_key( "outformat" ):
                        outformat = action["outformat"]
                    
                    if evOd.has_key( "val" ):
                        value = int(evOd["val"])
                    
                    if action.has_key( "attr" ):
                        if informat == "int":
                            if outformat == "string":
                                od[action["attr"]] = hex(value)
                            
                            elif outformat == "bytes_dec":
                                od[action["attr"]+"1"] = ord(hex(value)[2:3])
                                if hex(value)[3:4]:
                                    od[action["attr"]+"2"] = ord(hex(value)[3:4])
                                else:
                                    od[action["attr"]+"2"] = ord('0')
                        self.sendEvent( makeNewEvent( action, inEvent, None, od ) )
                if action.has_key( "attr" )!= True:
                    action["attr"] = "val"
                if conversion == "NAD_to_dec":
                #this converts the list of bytes recieved from a NAD products RS232 port into the bytes that represent the actual payload, this should work for the NAD Viso Five and Four
                #see nad_rs232_1.03.doc for protocol definition
                    if action.has_key( "incommingattr" ):
                        attrkey = action["incommingattr"]
                    else:
                        attrkey = "val"
                    value = 0                    
                    od = dict()
                    if evOd.has_key( attrkey ):
                        value = str(evOd[attrkey])
                    x = 0
                    # we should be recieving a string with bytes as their decimal value seperated by a ; and terminated by a :
                    splt = value.rstrip(':')
                    splt = splt.split(';')
                    od[action["attr"]] = ''    
                    # go through our list of bytes in decimal format
                    while x < len(splt):               
                        if x == len(splt)-1:
                            #we should not have got here as that means we never encountered the checksum byte
                            #so we assume the data must be mangled somehow
                            _log.error("NAD_to_int : Did not find checksum, data is invalid" %(checksum,value[x+1]))
                            od = ''
                            break                            
                        elif int(float(splt[x])) == 94:
                            #94 is the flag byte which means the next byte is reserved keyword bitwise ORed with 64
                            # to get the value back we bitwise AND it with 191
                            # unless the next value is 94 in which we just take 94 as the value
                            if splt[x+1] == '94':
                                od[action["attr"]] += '94;'
                                x +=2
                            else:
                                od[action["attr"]] += str(int(float(splt[x+1])) & 191) + ';'
                                x+= 2
                            continue 
                        elif int(float(splt[x])) == 1:
                            #1 is the control byte to indicate the start of an update so we ignore it and jump to the next one
                            x+=1
                            continue   
                        elif int(float(splt[x])) == 2:
                            # 2 means the next byte will be the checksum for the data so we verify it then finish
                            checksum = 0
                            for y in od[action["attr"]].split(';'):
                                if y != '':
                                    checksum+= int(y)
                            checksum = checksum % 256
                            checksum = checksum ^ 255
                            if checksum == int(float(splt[x+1])):
                                od[action["attr"]] = od[action["attr"]].rstrip(';')
                                od[action["attr"]] += ':'
                                #we break here as we have reached the end of what we should be parsing
                                break
                            else:
                                _log.error("NAD_to_int : Checksum failure , is %i expected %s" %(checksum,splt[x+1]))
                                od = ''
                                #we break here as we have reached the end of what we should be parsing
                                break                               
                        elif int(float(splt[x])) == 0 | ((int(float(splt[x])) >= 3) & (int(float(splt[x])) <= 19)):
                            #Currently none of the reserved control bytes are actually used so if we get any we ignore them
                            _log.error("NAD_to_int : Unlisted control character '%s' , ignoring" %splt[x])
                        else:
                            #not a control byte so it must be part of the data we are trying to read
                            od[action["attr"]] += splt[x] + ';'
                            x+=1

                    #dont send the event if we have nothing to send
                    if od != '':
                        self.sendEvent( makeNewEvent( action, inEvent, None, od ) )
                                 
                if conversion == "dec_to_NAD":
                    #this converts a command into a format for transmission to a NAD product via RS232
                    #see nad_rs232_1.03.doc for protocol definition
                    value = 0
                    od = dict()
                    if evOd.has_key( "val" ):
                        value = evOd["val"]
                    x = 0
                    if value != '':
                        splt = value.rstrip(':')
                        splt = splt.split(';')
                        #nad packets always start with 1
                        od[action["attr"]] = '1;'    
                        while x < len(splt):
                            if int(float(splt[x])) == 94:
                                #we want to represent 94  which is a special control byte so in our outgoing packet so we insert two of them
                                od[action["attr"]] += '94;94'
                                x+=1
                                continue 
                            elif (int(float(splt[x])) >= 0) & (int(float(splt[x])) <= 19):
                                #all control characters must have a 94 preceeding them and they must be bitwise ORed with 64
                                od[action["attr"]] += '94;' + str(int(float(splt[x]))|64) + ';'
                                x+= 1
                            else:
                                od[action["attr"]] +=  ('%i'%int(float(splt[x]))) + ';'
                                x+= 1                      
                        #we need to add the 8 bit checksum , we do not include the first byte in the checksum and we use the original unencoded values for the data
                        checksum = 0
                        for y in splt:
                            checksum+= int(float(y))
                        checksum = checksum % 256
                        checksum = checksum ^ 255
                        od[action["attr"]] += '2;%i:' %checksum    
                        self.sendEvent( makeNewEvent( action, inEvent, None, od ) )   
                    else:
                        self._log.error("int_to_NAD payload was empty! We cant encode a blank payload!")
                   
