# $Id: Utils.py 3268 2009-09-01 16:18:16Z simon.hughes $
#
#  Class to handle event actions that are implemented as an HTTP request.
#
#
import logging

from EventLib.Event import Event, makeEvent
#from WbEvent import WbEvent, WbEventOther
#from WebBrickLibs.ParameterSet import ParameterSet

_log = logging.getLogger( "EventHandlers.Utils" )

def makeNewEvent( desc, oldEvent, xtra, data=None ):
    """
    Create a new event using the description in desc.
    The desc is a dictionary containing an event type and event source
    It may also contain
        initial other_data - this data is append to new event
        initial copy_other_data - command to copy data for the new event from oldEvent or xtra
    oldEvent is the other_data from an existing event
    xtra is a dictionary of values from an arbitrary source.
    data is a dictionary that is always appended to the new event as payload 
    """
    newOd = dict()
    oldOd = None
    if oldEvent:
        oldOd = oldEvent.getPayload()
       
     # has incoming stuff got any % symbols in it, attempt substitution
    if oldOd != '':
        if desc.has_key("type"):
            if '%' in desc["type"]:
                desc["type"] = desc["type"] % oldEvent.getPayload()
        if desc.has_key("source"):
            if '%' in desc["source"]:
                desc["source"] = desc["source"] % oldEvent.getPayload()   
         
    if desc.has_key("other_data"):
        for v in desc["other_data"]:
            if '%' in desc["other_data"][v]:
                newOd[v] = desc["other_data"][v] % oldEvent.getPayload()
            else:
                newOd[v] = desc["other_data"][v]     

                    # empty.
    #attempt string substitution here too
    if desc.has_key("copy_other_data"):
        cpList = desc["copy_other_data"]
        for key in cpList:
            if '%' in cpList[key]:
                if xtra and xtra.has_key( cpList[key] ):
                    newOd[key] = xtra[ cpList[key] % oldEvent.getPayload() ] 
                elif oldOd and oldOd.has_key( cpList[key] ):
                    newOd[key] = oldOd[ cpList[key] % oldEvent.getPayload() ] 
            else:
                if xtra and xtra.has_key( cpList[key] ):
                    newOd[key] = xtra[ cpList[key] ]
                elif oldOd and oldOd.has_key( cpList[key] ):
                    newOd[key] = oldOd[ cpList[key] ]

    # append/update payload 
    if data:
        newOd.update(data)
        
    # may be empty.
    if newOd and len(newOd) == 0:
        newOd = None

    return Event( desc["type"], desc["source"], newOd )

def validateNewEvent( desc ):
    """
    Validate the content of a new event description and log errors is invalid
    return True if valid else False
    It may also contain
        initial other_data
        a command to copy data for the event other data from oldEvent or xtra
    oldEvent is the other_data from an existing event
    xtra is a dictionary of values from an arbitrary source.
    """
    result = True
    errStr = ""
    if not desc.has_key("type"):
        result = False
        errStr.append( "no event type" )
    if not desc.has_key("source"):
        result = False
        errStr.append( "no event source" )

    if desc.has_key("other_data"):
        # other data should be a dictionary of name value pairs.
        od = desc["other_data"]
        if not isinstance( od, dict ):
            result = False
            errStr.append( "other data is not a dictionary (name value pairs)" )
        else:
            # what other tests
            pass

    if desc.has_key("copy_other_data"):
        # should be a sequence type, define better
        pass

    if not result:
        _log.error("newEvent invalid %s (%s)" % (errStr,desc) )

    return result
