#
#  Class to handle mapping of an event to one or more new events
#
#  Lawrence Klyne
#
#
import logging

from EventLib.Event import Event, makeEvent

from EventLib.EventAgent import EventAgent
from EventLib.EventHandler import EventHandler

from EventHandlers.BaseHandler import BaseHandler
from EventHandlers.Utils import *

from WebBrickLibs.ParameterSet import ParameterSet

_log = logging.getLogger("EventHandlers.SerialDataConvertor")

#
# WebBrick time event generator
#
MATCH_VALUE = 1
MATCH_CHAR = 2
class MatchEntry( object ):
    def __init__ (self, cfg):
        # configure with offset and value
        _log.debug("\nMatchEntry %s", cfg)
        self._offset = int(cfg["offset"])
        if cfg.has_key("value"):
            self._value = int(cfg["value"])
            self._type = MATCH_VALUE
        elif cfg.has_key('char'):
            
            self._char = cfg['char'][0]
            self._type = MATCH_CHAR
        else:
            _log.error("Missing match value/char %s", cfg )
        #_log.debug("Configured %s", self )
    
    def match( self, db ):
        # Match entry against byte array passed in.
        _log.debug("Test %s against %s", self, db )
        
        if len(db) > self._offset:
            if self._type == MATCH_VALUE:
                _log.debug("Test VALUE:  %s against %s", self._value, ord(db[self._offset]) )
                return ord(db[self._offset]) == self._value
            elif self._type == MATCH_CHAR:
                _log.debug("Test CHAR:  %s against %s", self._char, db[self._offset] )
                return db[self._offset] == self._char
        return False
        
    def __str__( self ):
        if self._type == MATCH_VALUE:
            return "MatchEntry %i : %i" % (self._offset, self._value)
        if self._type == MATCH_CHAR:
            return "MatchEntry %i : %s" % (self._offset,self._char)
            
class SerialDataConvertor( BaseHandler ):
    """
    
    """

    def __init__ (self, localRouter):
        super(SerialDataConvertor,self).__init__( localRouter )
        global _log
        _log = self._log

    def configureActions( self, cfgDict ):
        self._log.debug("configureActions %s" % (cfgDict) )
        result = None
        
        if cfgDict.has_key("newEvent"):
            neList = cfgDict["newEvent"]
            mList = list()
            if not isinstance( cfgDict["newEvent"], list ):
                neList = list()
                neList.append(cfgDict["newEvent"])
                
            if cfgDict.has_key("match"):
                if isinstance( cfgDict["match"], list ):
                    for me in cfgDict["match"]:
                        mList.append( MatchEntry( me ) )
                else:
                    mList.append( MatchEntry( cfgDict["match"] ) )
            result = (mList,neList)
                
        self._log.debug("configureActions %s", result )
        return result

    def doActions( self, actions, inEvent ):
        if actions and inEvent.getPayload() and inEvent.getPayload().has_key( "data" ):
            oldPayload = inEvent.getPayload()
            dbs = inEvent.getPayload()["data"]
            doSend = True
            mList = actions[0]
            for m in actions[0]:
                if not m.match(dbs):
                    doSend = False
                
            if doSend:
                for ne in actions[1]:
                    self._log.debug( 'Send %s', ne )
                    #    <newEvent type="avamplifier/volume/current" source="avamplifier/1/volume/main/current">
                    #        <other_data attr='val' offsetb='5' type="int"/>
                    #    </newEvent>

                    od = dict()
                    if ne.has_key("copy_other_data"):
                        cpList = ne["copy_other_data"]
                        for key in cpList:
                            if '%' in cpList[key]:
                                if oldPayload and oldPayload.has_key( cpList[key] ):
                                    od[key] = oldPayload[ cpList[key] % oldPayload ] 
                            else:
                                if oldPayload and oldPayload.has_key( cpList[key] ):
                                    od[key] = oldPayload[ cpList[key] ]
                    
                    if ne.has_key("other_data"):
                        odd = ne["other_data"]
                        self._log.debug( 'other_data %s', odd )
                        ofs = int(odd["offsetb"])
                        cnt = 1
                        if odd.has_key("lenb"):
                            cnt = int(odd["lenb"])
                            st = dbs[ofs:ofs+cnt]
                        else:
                            st = dbs[ofs:]
                        if odd["type"] == "int":
                            od[odd["attr"]] = ord(st[0])
                        elif odd["type"] == "hex_string":
                            od[odd["attr"]] = int( st, 16 )
                        elif odd["type"] == "int_string":
                            od[odd["attr"]] = int( st )
                        elif odd["type"] == "dec_ascii":
                            #takes a string of bytes formatted 10;30;30;40: and attemtps to conver them to characters 
                            st = st.rstrip(':')
                            vals = st.split(";")
                            od[odd["attr"]] = ''
                            for value in vals:
                                if value != '':
                                    od[odd["attr"]] += chr(int(value))
                        elif odd["type"] == "dec_int":
                            #takes a string of bytes formatted 10;30;30;40: and turns extracts one int from it at the given offset
                            st = st.rstrip(':')
                            vals = st.split(";")
                            od[odd["attr"]] = ''
                            for value in vals:
                                if value != '':
                                    od[odd["attr"]] = int(value)          
                        elif odd["type"] == "8_bit_checksum":
                            #adds an 8 bit checksum on the end of the payload
                            checksum = 0
                            st = st.rstrip(':')
                            od[odd["attr"]] = st                            
                            vals = st.split(";")
                            for value in vals:
                                if value != '':
                                    checksum += int(value)
                            checksum = checksum % 256
                            checksum = checksum ^ 255
                            od[odd["attr"]] += ';2;%s:' % str(checksum)  
        
                            
                    self.sendEvent( makeEvent( ne["type"], ne["source"], od ) )
