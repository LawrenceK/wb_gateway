# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id$
#
# Tom Bushby
#
# This is not a test, rather a proof-of-concept.
#
# To start the servers, you must start TestEventHTTPRouter1Console.py and
# TestEventHTTPRouter2Console.py from the Python command line while in 
# your virtual environment (from two different terminals) within three
# seconds of each other.
#
# This file creates a router, HTTP server and a HTTP Client (which listens
# to the HTTP server spawned by Router2Console). The Router2Console
# will do exactly the same, except the HTTP Client spawned by that
# process will listen to this process's HTTP server.
#
# This script will, after setting up the router, servers and clients,
# will send out an event to the Router2Console. Router2Console
# will listen for the events and then send back a response event to this
# console.
#
# The HTTP Clients in these instances are running in Simplex mode. All communication
# between the two consoles are via the HTTP Clients pushing data and events to their
# respective HTTP Servers, and the HTTP Server's main router will then listen for all
# interested events received by the HTTP Server.
#
# Events are published by the main router, picked up by the HTTP Client via a routeEventFrom
# subscription and then automatically forwarded to the respective HTTP Server. The event
# will then be forwarded via another routeEventFrom to Router2Console's main router.
#
# When logging, WARN is used instead of INFO, due to the current environment's output when
# using INFO means that there is too much information to easily view the sending and receiving
# events.


import sys
import unittest
import logging
import time

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
rootlogger.setLevel(logging.DEBUG)
filelogformatter = logging.Formatter('%(created)f - %(asctime)s %(msecs)d %(levelname)s %(name)s %(message)s', "%H:%M:%S")
logformat = filelogformatter
strhandler = logging.StreamHandler(sys.stdout)
log_level = logging.DEBUG
strhandler.setLevel(log_level)
strhandler.setFormatter(logformat)
rootlogger.addHandler(strhandler)
    
# Setup multiple event handlers; the first set of handlers
# handle the first outgoing event, the Incoming handles the incoming events
# and the eventHandlerOutgoing handles the outgoing events that are spawned by the incoming events.
def subHandler(h,sts):
    h.subcount += 1
    h.dosub     = sts
    return

def unsubHandler(h,sts):
    h.subcount -= 1
    h.unsub     = sts
    return

def eventHandler(h,e):
    h.evcount += 1
    h.event    = e
    return makeDeferred(StatusVal.OK)
  
def subHandlerOutgoing(h,sts):
    h.subcount += 1
    h.dosub     = sts
    return

def unsubHandlerOutgoing(h,sts):
    h.subcount -= 1
    h.unsub     = sts
    return

def eventHandlerOutgoing(h,e):
    h.evcount += 1
    h.event    = e
    return makeDeferred(StatusVal.OK)
      
    
def subHandlerIncoming(h,sts):
    h.subcount += 1
    h.dosub     = sts
    return

def unsubHandlerIncoming(h,sts):
    h.subcount -= 1
    h.unsub     = sts
    return

# Listen for all incoming events, and then send an outgoing event of the type to be picked up by Router2Console
def eventHandlerIncoming(h,e):
    h.evcount += 1
    h.event    = e
    if h.event.getType() == "to/router/original":
        rootlogger.warn("== Received an incoming event, event number: %s ==", router.getCount())
        
        # Increment the counter for the incoming events. Sleep so that we don't have a continuous loop of events.
        router.inC()        
        time.sleep(0.5)
    
        # Make and publish an event back to Router2Console
        eventType = "to/router/2"
        eventSource = "source/router1"
        router1EventAgentOutgoing = makeEventAgent(uri="router1EventAgentOutgoing")
        router1EventHandlerOutgoing = makeEventHandler(
            uri="router1EventAgentOutgoing", handler=eventHandlerOutgoing,
            initSubscription=subHandlerOutgoing, endSubscription=unsubHandlerOutgoing)
        router1EventHandlerOutgoing.subcount = 0
        router1EventHandlerOutgoing.evcount = 0

        event = makeEvent(evtype=eventType, source=eventSource, payload=router.getCount())

        rootlogger.warn("== Sending out event, number: %s ==", router.getCount())
        status2 = router.getR1().publish(router1EventHandlerOutgoing, event) ## R1 publishes the main event, R2C picks it up and forwards it to TestEventHTTPRouter1Console.py
        rootlogger.warn("== The event has completed being published ==")

    return makeDeferred(StatusVal.OK)


# Test class
class TestEventRouterHTTP1():
    def setUp(self):
        self.R1  = None
        self.R2  = None
        self.R3C = None
        return

    def getR3C(self):
        return self.R3C
        
    def getR1(self):
        return self.R1
        
    # Each event is tagged with a unique
    # ID so that it can be easily viewed in the console output.
    # This is sent as the payload of the event.    
    def getCount(self):
        d = dict(EVENT=self.count)
        return d

    def inC(self):
        self.count += 1

    def setUpRouter(self):
        self.setUp()
        try:
            self.count = 0
            self.R1  = EventRouter("R1")
            self.R2  = EventRouterHTTPS("R2S","localhost",8082)
            # Wait for Router2Console to also setup it's server. Then connect the clients.
            time.sleep(3)
            self.R3C = EventRouterHTTPC("R3C","localhost",8083,True)
        except Exception, e:
            print_exc()
        
        # Wildcard event source
        self.R1.routeEventFrom(evtype="to/router/original",router=self.R2) ## R2 routes all events wtih evtype to R1 for processing (INCOMING)
        self.R3C.routeEventFrom(evtype="to/router/2",router=self.R1) ## R3C tells R1 to route all events with evtype to R3C (OUTGOING)     
        return

    def sendTestEvent(self):
        print("sendTestEvent start")
        self.setUpRouter()
        
        # Listen for incoming events using a custom handler.
        eventType = "to/router/original"
        eventSource = "source/router2"
        router1EventAgentIncoming = makeEventAgent(uri="router1EventAgentIncoming")
        router1EventHandlerIncoming = makeEventHandler(
                uri="router1EventAgentIncoming", handler=eventHandlerIncoming,
                initSubscription=subHandlerIncoming, endSubscription=unsubHandlerIncoming)
        router1EventHandlerIncoming.subcount = 0
        router1EventHandlerIncoming.evcount = 0        
        status = self.R1.subscribe(60, router1EventHandlerIncoming, evtype=eventType, source=eventSource) #R1 subscribes to eventType to send a response back   

        # Set the counter to 1, make our first event.       
        self.inC()
       
        eventType = "to/router/2"
        eventSource = "source/router1"
        event = makeEvent(evtype=eventType, source=eventSource, payload=router.getCount())
        self.sendTestEventDo(self.R3C, self.R1, event, eventType, eventSource) # Send the event
        print("sendTestEvent end")
        
    def sendTestEventDo(self, r1, r2, evt, eventType, eventSource):
        # Send the first event, using a custom handler
        router1EventAgent = makeEventAgent(uri="router1EventAgent")
        router1EventHandler = makeEventHandler(
                uri="router1EventAgent", handler=eventHandler,
                initSubscription=subHandler, endSubscription=unsubHandler)
        router1EventHandler.subcount = 0
        router1EventHandler.evcount = 0
        status = r1.subscribe(60, router1EventHandler, evtype=eventType, source=eventSource)    ## R2C subscribes to all interested events (e.g. eventType)
        time.sleep(1)
        rootlogger.warn("== Router 1 has subscribed to incoming events ==")
        
        status2 = r2.publish(router1EventHandler, evt) ## R1 publishes the main event, R3C picks it up and forwards it to TestEventHTTPRouter2Console.py
        rootlogger.warn("== First event has finished publishing ==")       

# Start the server and send the first event
print "Console loaded."
router = TestEventRouterHTTP1()
router.sendTestEvent()
