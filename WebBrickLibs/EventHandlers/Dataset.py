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

_log = logging.getLogger("EventHandlers.Dataset")

#
# WebBrick time event generator
#
class DataColumn( object ):
    def __init__ (self, cfg):
        # configure with offset and value
        _log.debug("DataColumn %s", cfg)
        self._index = int(cfg["column"])
        self._name = cfg["name"]
        self._attr = cfg["attr"]
        self._value = ""
        _log.debug("Configured %s", self )

    def update( self, inEvent ):
        od = inEvent.getPayload()
        if od and od.has_key(self._attr):
            self._value = od[self._attr]

    def clear( self ):
        self._value = ""

    def get( self ):
        return str(self._value)
        
    def __str__( self ):
        return "DataColumn %i : %s -> %s" % (self._index, self._attr, self._name)

ACTION_NONE = 0
ACTION_CSV = 1
ACTION_XML = 2
ACTION_EVENT = 3
ACTION_CLEAR = 4

class Action( object ):
    def __init__ (self, cfg):
        # configure with offset and value
        _log.debug("Action %s", cfg)
        ac = cfg["action"].lower()
        self._action = ACTION_NONE
        self._streamname = ""
        self._type = ""
        self._source = ""
        self._element = ""
        if ac == "csv":
            self._action = ACTION_CSV
            self._streamname = cfg["logstream"]
        elif ac == "xml":
            self._action = ACTION_XML
            self._streamname = cfg["logstream"]
            if cfg.has_key("element"):
                self._element = cfg["element"]
            else:
                self._element = "entry"
        elif ac == "event":
            self._action = ACTION_EVENT
            self._type = cfg["type"]
            self._source = cfg["source"]
        elif ac == "clear":
            self._action = ACTION_CLEAR
            
        _log.debug("Configured %s", self )
        
        #            <action action="write" logstream="Dataset.1"/>
        #            <action action="event" type="dataset/4" source="dataset/house"/>
        #            <action action="clear" />
        
    def __str__( self ):
        return "Action %i : '%s' '%s' '%s'" % (self._action,self._streamname,self._type,self._source)

class Dataset( BaseHandler ):
    """
    
    """

    def __init__ (self, localRouter):
        super(Dataset,self).__init__( localRouter )
        global _log
        _log = self._log
        self._colcount = 0
        self._columns = {}

    def configure( self, cfgDict ):
        if cfgDict.has_key("columns"):
            #self._colcount = int(cfgDict["columns"])
            pass
            
        super(Dataset,self).configure( cfgDict )

    def start(self):
        # turn self._columns[de._index] into a list
        self._log.debug("start %s", self._columns )
        kys = self._columns.keys()
        kys.sort()
        self._log.debug("Keys %s", kys )
        nlist = [self._columns[idx] for idx in kys]
        self._columns = nlist
        self._log.debug("start as list %s", self._columns )

        super(Dataset,self).start()
    
    def configureActions( self, cfgDict ):
        self._log.debug("configureActions %s" % (cfgDict) )
        dList = list()  # data columns
        aList = list()  # actions
        #            <data column="1" name="date" attr="datestr"/>
        #            <data column="2" name="time" attr="timestr"/>
        #            <action action="write" logstream="Dataset.1"/>
        #            <action action="event" type="dataset/4" source="dataset/house"/>
        #            <action action="clear" />
        
        if cfgDict.has_key("data"):
            if isinstance( cfgDict["data"], list ):
                for de in cfgDict["data"]:
                    dList.append(DataColumn(de))
            else:
                dList.append(DataColumn(cfgDict["data"]))

        # update global list as opposed to the distinct action list
        for de in dList:
            self._log.debug("DataColumn %s", de )
            if self._columns.has_key(de._index):
                # error duplicate column
                self._log.error( "Duplicate column index %i in %s", de._index, cfgDict )
            else:
                self._columns[de._index] = de
                if de._index > self._colcount:
                    self._colcount = de._index
                    
        self._log.debug("New Columns %s %s", self._colcount, self._columns )
                    
        if cfgDict.has_key("action"):
            if isinstance( cfgDict["action"], list ):
                for de in cfgDict["action"]:
                    aList.append(Action(de))
            else:
                aList.append(Action(cfgDict["action"]))
        
        result = (dList,aList)
        self._log.debug("configureActions %s", result )
        
        return result

    def doActions( self, actions, inEvent ):
        for de in actions[0]:
            # update from event
            de.update(inEvent)
            
        for ae in actions[1]:
            # perform action
            if ae._action == ACTION_CSV:
                # write an event log entry
                ntry = ",".join( [de.get() for de in self._columns] )
                ls = logging.getLogger(ae._streamname)
                ls.info( ntry )
                
            elif ae._action == ACTION_XML:
                atts = "".join( [" %s='%s' " % (de._name, de._value) for de in self._columns] )
                elms = "".join( ["<%s>%s</%s>" % (de._name, de._value, de._name) for de in self._columns] )
                ntry = "<%s %s>%s</%s>" % (ae._element, atts, elms, ae._element)
                ls = logging.getLogger(ae._streamname)
                ls.info( ntry )
                    
            elif ae._action == ACTION_EVENT:
                # create an event
                od = dict()
                for de in self._columns:
                    od[de._name] = de._value
                self.sendEvent( makeEvent( ae._type, ae._source, od ) )
                
            elif ae._action == ACTION_CLEAR:
                # clear current data values
                for de in self._columns:
                    de.clear()

            
