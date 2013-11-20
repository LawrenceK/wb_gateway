# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestEventRouterHTTP.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Tom Bushby
#
# Please see TestEventHTTPRouter1Console for the description.

import sys
import unittest
import logging
import time
import thread

from Queue     import Queue
from threading import Thread
from traceback import print_exc

sys.path.append("../..")

from MiscLib.Functions         import compareLists
from MiscLib.Logging           import Trace, Info, Warn

from EventLib.Event            import Event, makeEvent
from EventLib.Status           import Status, StatusVal
from EventLib.SyncDeferred     import makeDeferred
from EventLib.EventAgent       import EventAgent, makeEventAgent
from EventLib.EventHandler     import EventHandler, makeEventHandler
from EventLib.EventRouter      import EventRouter
from EventLib.EventRouterHTTPS import EventRouterHTTPS
from EventLib.EventRouterHTTPC import EventRouterHTTPC
from EventLib.EventRouterThreaded import EventRouterThreaded
from TestEventRouter           import TestEventRouter

# Setting up a basic logger with WARN as the default level.
rootlogger = logging.getLogger('')
rootlogger.setLevel(logging.DEBUG)  # Then filter in handlers for less.
filelogformatter = logging.Formatter('%(created)f - %(asctime)s %(msecs)d %(levelname)s %(name)s %(message)s', "%H:%M:%S")
logformat = filelogformatter
strhandler = logging.StreamHandler(sys.stdout)
log_level = logging.DEBUG
strhandler.setLevel(log_level)
strhandler.setFormatter(logformat)
rootlogger.addHandler(strhandler)
    
    
   
# Setup multiple event handlers; the eventHandler handles the incoming events
# and the eventHandlerOutgoing handles the outgoing events that are spawned by the incoming events.    
def subHandlerOutgoing(h,sts):
    h.subcount += 1
    h.dosub     = sts
    return

def unsubHandlerOutgoing(h,sts):
    h.subcount -= 1
    h.unsub     = sts
    return

def eventHandlerOutgoing (h,e):
    h.evcount += 1
    h.event    = e
    return makeDeferred(StatusVal.OK)

def subHandler(h,sts):
    h.subcount += 1
    h.dosub     = sts
    return

def unsubHandler(h,sts):
    h.subcount -= 1
    h.unsub     = sts
    return

def eventHandler(h,e):
    # This is called when R1 picks up a subscribed event
    h.evcount += 1
    h.event    = e
    rootlogger.debug("!!!!!!!!!!!!!!!!!== Received an incoming event, event number: %s ==", h.evcount)
    rootlogger.debug("!!!!!!!!!!!!!!!!!== With payload: %s ==", h.event.getPayload())    
    if h.event.getType() == "to/router/2":
        rootlogger.warn("== Received an incoming event, event number: %s ==", h.evcount)
        rootlogger.warn("== With payload: %s ==", h.event.getPayload())       
        sendBackResponse(count=h.evcount)
    return makeDeferred(StatusVal.OK)

def sendBackResponse(count):
    # Send back an event that the Router1Console's INCOMING handler will pickup.
    eventType = "to/router/original"
    eventSource = "source/router2"
    router2EventAgentOutgoing = makeEventAgent(uri="router2EventAgentOutgoing")
    router2EventHandlerOutgoing = makeEventHandler(
        uri="router2EventAgentOutgoing", handler=eventHandlerOutgoing,
        initSubscription=subHandlerOutgoing, endSubscription=unsubHandlerOutgoing)
    router2EventHandlerOutgoing.subcount = 0
    router2EventHandlerOutgoing.evcount = 0
    
    event = makeEvent(evtype=eventType, source=eventSource)
    
    # Only subscribe the first time around.
    if count == 1: 
        status = router.getR2C().subscribe(60, router2EventHandlerOutgoing, evtype=eventType, source=eventSource)    ## R2C subscribes to all interested events (e.g. eventType)
    # Publish the event to Router1Console
    status2 = router.getR1().publish(router2EventHandlerOutgoing, event) ## R1 publishes the main event, R2C picks it up and forwards it to TestEventHTTPRouter1Console.py
    rootlogger.warn("== Router 2 sent out event ==")
    

# Test class
class TestEventRouterHTTP2():
    def setUp(self):
        self.R1  = None
        self.R3  = None
        self.R2C = None
        return
    
    def getR2C(self):
        return self.R2C
        
    def getR1(self):
        return self.R1

    def setUpRouter(self):
        self.setUp()
        try:
            self.R1  = EventRouter("R1")
            self.R3  = EventRouterHTTPS("R3S","localhost",8083)
            time.sleep(3)
            self.R2C = EventRouterHTTPC("R2C","localhost",8082,True)
        except Exception, e:
            print_exc()
        
        # Wildcard event source
        self.R1.routeEventFrom(evtype="to/router/2",router=self.R3) ## R3 routes all events wtih evtype to R1 for processing (INCOMING)
        self.R2C.routeEventFrom(evtype="to/router/original",router=self.R1) ## R2C tells R1 to route all events with evtype to R2C (OUTGOING)
        return

    def sendTestEvent(self):
        print("sendTestEvent start")
        self.setUpRouter()
        
        eventType = "to/router/2"
        eventSource = "source/router1"
                
        router2EventAgent1 = makeEventAgent(uri="router2EventAgent1")
        router2EventHandler1 = makeEventHandler(
                uri="router2EventAgent1", handler=eventHandler,
                initSubscription=subHandler, endSubscription=unsubHandler)
        router2EventHandler1.subcount = 0
        router2EventHandler1.evcount = 0
        # Subscribe to incoming events and then pass them to the event handler to generate outgoing events.
        status = self.R1.subscribe(60, router2EventHandler1, evtype=eventType, source=eventSource) #R1 subscribes to eventType to send a response back         

        print("sendTestEvent finished")
    
print "Console loaded."
router = TestEventRouterHTTP2()
router.sendTestEvent()

