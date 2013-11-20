# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

#
# Counters
# 
#  Class to handle counters
#
#  Lawrence Klyne, Andy Harris 12th July 2010, changed to add 'set' action
#
#
import logging

from EventLib.Event import Event, makeEvent

from EventLib.EventAgent import EventAgent
from EventLib.EventHandler import EventHandler

from EventHandlers.BaseHandler import BaseHandler
from EventHandlers.Utils import *

from WebBrickLibs.ParameterSet import ParameterSet

_log = None

class CounterInt( object ):
    def __init__ (self, cfg):
        _log.debug( "CounterInt cfg %s", cfg)
        self._name = cfg["name"]
        self._minimum = 0
        self._maximum = 0
        self._resetvalue = 0
        self._value = 0
        _log.debug( "Counter name %s", self._name)

        if cfg.has_key("minimum"):
            self._minimum = int(cfg["minimum"])
        _log.debug( "Counter minimum %u", self._minimum)

        if cfg.has_key("maximum"):
            self._maximum = int(cfg["maximum"])
        _log.debug( "Counter maximum %u", self._maximum)

        if cfg.has_key("resetvalue"):
            self._resetvalue = int(cfg["resetvalue"])
        _log.debug( "Counter resetvalue %u", self._resetvalue)
        self._value = self._resetvalue

    def reset(self,resetvalue=None):
        if resetvalue:
            self._value = int(resetvalue)
        else:
            self._value = self._resetvalue

    def st(self,setvalue=None):
        if setvalue:
            self._value = int(setvalue)
        else:
            self._value = self._resetvalue

    def incAndTest(self,by,limit):
        self._value = self._value + int(by)
        return limit and self._value >= int(limit)

    def decAndTest(self,by,limit):
        self._value = self._value - int(by)
        return limit and self._value <= int(limit)

    def __str__(self):
        return str(self._value)

class CounterFloat( object ):
    def __init__ (self, cfg):
        _log.debug( "CounterFloat cfg %s", cfg)
        self._name = cfg["name"]
        self._minimum = 0
        self._maximum = 0
        self._resetvalue = 0
        self._value = 0
        _log.debug( "Counter name %s", self._name)

        if cfg.has_key("minimum"):
            self._minimum = float(cfg["minimum"])
        _log.debug( "Counter minimum %u", self._minimum)

        if cfg.has_key("maximum"):
            self._maximum = float(cfg["maximum"])
        _log.debug( "Counter maximum %u", self._maximum)

        if cfg.has_key("resetvalue"):
            self._resetvalue = float(cfg["resetvalue"])
        _log.debug( "Counter resetvalue %u", self._resetvalue)

        self._value = self._resetvalue

    def reset(self,resetvalue=None):
        if resetvalue:
            self._value = float(resetvalue)
        else:
            self._value = self._resetvalue

    def st(self,setvalue=None):
        if setvalue:
            self._value = float(setvalue)
        else:
            self._value = self._resetvalue

    def incAndTest(self,by,limit):
        self._value = self._value + float(by)
        return limit and self._value >= float(limit)

    def decAndTest(self,by,limit):
        self._value = self._value - float(by)
        return limit and self._value <= float(limit)

    def __str__(self):
        return str(self._value)

class Bump( object ):
    def __init__ (self, cfg):
        # type is -1 for decrement, 0 for reset and -1 for decrement
        self._name = cfg["name"]
        self._limit = None
        self._by = 1
        self._resetvalue = None
        self._newEvents = None
        self._key = None

        if cfg.has_key("limit"):
            self._limit = cfg["limit"]
        if cfg.has_key("resetvalue"):
            self._resetvalue = cfg["resetvalue"]
        if cfg.has_key("by"):
            self._by = cfg["by"]
        if cfg.has_key("key"):
            self._key = cfg["key"]

        if cfg.has_key("newEvent"):
            if isinstance( cfg["newEvent"], list ):
                self._newEvents = cfg["newEvent"]
            else:
                self._newEvents = list()
                self._newEvents.append(cfg["newEvent"])

#
# WebBrick time event generator
#
class Counters( BaseHandler ):
    """
    """

    def __init__ (self, localRouter):
        super(Counters,self).__init__( localRouter )
        global _log
        _log = self._log
        self._counters = dict()

    def configureCounter( self, cfg ):
        if cfg.has_key("type") and cfg["type"].lower() == "float":
            ne = CounterFloat(cfg)
        else:
            ne = CounterInt(cfg)
        self._counters[ne._name] = ne

    def configure( self, cfgDict ):
        # load counters first so that the actions caan be verified
        if isinstance( cfgDict["counter"], list ):
            for ctr in cfgDict["counter"]:
                self.configureCounter( ctr )
        else:
            # single counter
            self.configureCounter( cfgDict["counter"] )
        super(Counters,self).configure( cfgDict )

    def processList( self, cfgs ):
        result = list()
        if isinstance( cfgs, list ):
            for cfg in cfgs:
                nb = Bump(cfg)
                if self._counters.has_key(nb._name):
                    result.append(nb)
                else:
                    self._log.error("No such counter %s (%s)" % (nb._name,cfg) )
        else:
            nb = Bump(cfgs)
            if self._counters.has_key(nb._name):
                result.append(nb)
            else:
                self._log.error("No such counter %s (%s)" % (nb._name,cfgs) )
        if len(result) > 0:
            return result
        return None

    def configureActions( self, cfgDict ):
        self._log.debug("configureActions %s" % (cfgDict) )
        nevents = None
        incs = None
        decs = None
        resets = None
        sets = None

        if cfgDict.has_key("newEvent"):
            if isinstance( cfgDict["newEvent"], list ):
                nevents = cfgDict["newEvent"]
            else:
                nevents = list()
                nevents.append(cfgDict["newEvent"])

        if cfgDict.has_key("increment"):
            incs = self.processList( cfgDict["increment"])

        if cfgDict.has_key("decrement"):
            decs = self.processList( cfgDict["decrement"])

        if cfgDict.has_key("reset"):
            resets = self.processList( cfgDict["reset"])

        if cfgDict.has_key("set"):
            sets = self.processList( cfgDict["set"])

        return (nevents,incs,decs,resets,sets)

    def makeNewEvent( self, desc ):
        newOd = None

        if desc.has_key("other_data"):
            newOd = dict(desc["other_data"])
        else:
            newOd = dict()  # empty.

        if desc.has_key("copy_other_data"):
            cpList = desc["copy_other_data"]
            for key in cpList:
                if self._counters.has_key(cpList[key]):
                    newOd[key] = self._counters[ cpList[key] ]._value

        # may be empty.
        if newOd and len(newOd) == 0:
            newOd = None

        return Event( desc["type"], desc["source"], newOd )

    def doActions( self, actions, inEvent ):
        # each action is a tuple
        nevents = actions[0]
        incs = actions[1]
        decs = actions[2]
        resets = actions[3]
        sets = actions[4]

        newEvents = list()

        if incs:
            for inc in incs:
                ctr = self._counters[inc._name]
                if ctr.incAndTest(inc._by, inc._limit):
                    # send new events
                    if inc._newEvents:
                        for ne in inc._newEvents:
                            newEvents.append( self.makeNewEvent( ne ) )
                    if inc._resetvalue:
                        ctr.reset(inc._resetvalue)

        if decs:
            for dec in decs:
                ctr = self._counters[dec._name]
                if ctr.decAndTest(dec._by, dec._limit):
                    # send new events
                    if dec._newEvents:
                        for ne in dec._newEvents:
                            newEvents.append( self.makeNewEvent( ne ) )
                    if dec._resetvalue:
                        ctr.reset(dec._resetvalue)

        if resets:
            for reset in resets:
                ctr = self._counters[reset._name]
                if reset._newEvents:
                    for ne in reset._newEvents:
                        newEvents.append( self.makeNewEvent( ne ) )
                # always reset
                ctr.reset(reset._resetvalue)
        #
        #  This is the new set action
        #
        
        if sets:
            for st in sets:
                ctr = self._counters[st._name]
                payload = inEvent.getPayload()
                self._log.debug("Inbound EVENT Payload %s" % payload)
                # set the counter
                if st._key:
                    # use value from incoming event
                    ctr.st(payload[st._key])
                else:    
                    # use fixed value
                    ctr.st(st._by)
                # send the event
                if st._newEvents:
                    for ne in st._newEvents:
                        newEvents.append( self.makeNewEvent( ne ) )
                
                
        if nevents:
            for ne in nevents:
                newEvents.append( self.makeNewEvent( ne ) )

        for ctrName in self._counters:
            ctr = self._counters[ctrName]
            self._log.debug("Counter %s %s" % (ctr._name,ctr) )

        for evnt in newEvents:
            self.sendEvent( evnt )
