from EventHandlers.HttpAction import HttpAction
from MiscLib.DomHelpers import getDictFromXmlString
from EventLib.Event import *
from EventHandlers.BaseHandler import BaseHandler
from EventLib.SyncDeferred import makeDeferred
from EventLib.Status import StatusVal
import time
import logging

ANALOG_SET_TIMEOUT = 1
DIGITAL_SET_TIMEOUT = 1

class AnalogOutput(BaseHandler):
    def __init__(self,eType,eSource,localrouter,wbTarget,aoNum):        
        super(AnalogOutput,self).__init__(localrouter)
        
        self.localrouter = localrouter
        self.wbTarget = wbTarget
        #assume the webbrick node number is equal to the last digit of the ip address
        self.nodeNum = wbTarget.split('.')[3]
        self.targetVal = 0
        self.eType = eType
        self.eSource = eSource
        self.aoNum = str(aoNum)
        
        self.aoCmd = 'AA;' + str(aoNum) + ';%(val)s:'
        self.httpAction = HttpAction(localrouter)
        self.httpAction.configure( self.MakeHttpConfig(eType,eSource,wbTarget) )
        self.httpAction.start()
        self.localrouter.subscribe( 20 , self , 'http://id.webbrick.co.uk/events/webbrick/AO' ,  'webbrick/' + self.nodeNum + '/AO/' + self.aoNum)
            
    def MakeHttpConfig(self,eType,eSource,wbTarget):
        cfg = {}
        cfg['eventtype'] = {}
        cfg['eventtype']['type'] = eType
        cfg['eventtype']['eventsource'] = {}
        cfg['eventtype']['eventsource']['source'] = eSource
        cfg['eventtype']['eventsource']['event'] = {}
        cfg['eventtype']['eventsource']['event']['url'] = {}
        cfg['eventtype']['eventsource']['event']['url']['cmd'] = "GET"
        cfg['eventtype']['eventsource']['event']['url']['uri'] = '/cfg.spi?com=' + self.aoCmd
        cfg['eventtype']['eventsource']['event']['url']['address'] = 'http://' + wbTarget
        cfg['name'] = 'HttpAction'
        cfg['module'] = 'EventHandlers.HttpAction'
        return cfg
    
    def initSubscription(self,status):
        pass
    
    def getUri(self):
        return "ANALOG_OUTPUT/" + self.wbTarget + '/' + self.aoNum 
    
    def SetAO(self,Val):
        if Val >= 0 and Val <= 100:
            newEvent = makeEvent( self.eType,self.eSource , {'val' : str(Val)} )         
            self.localrouter.publish(newEvent.getSource() , newEvent)   
            self.targetVal = int(Val)
        else:
            raise Exception("Warning , analog set point out of range : " + str(Val))        
            
    
    def doHandleEvent(self,handler,inEvent):
        if inEvent.getType() == 'http://id.webbrick.co.uk/events/webbrick/AO':
            if inEvent.getSource() == 'webbrick/' + self.nodeNum + '/AO/' + self.aoNum:
                if inEvent.getPayload()['val'] != self.targetVal:
                    self.SetAO(self.targetVal)
        return makeDeferred(StatusVal.OK)
        
class DigitalOutput(BaseHandler):
    
    def __init__(self,eType,eSource,localrouter,wbTarget,doNum):        
        super(DigitalOutput,self).__init__(localrouter)              
        self.localrouter = localrouter
        self.wbTarget = wbTarget
        #assume the node number is equal to the last digit of the ip address
        self.nodeNum = wbTarget.split('.')[3]        
        self.eType = eType
        self.eOnSource = eSource + '/on'
        self.eOffSource = eSource + '/off'
        self.eDwellSource = eSource + '/dwell'
        self.doNum = str(doNum)
        self.onCmd = 'DO;' + str(doNum) + ';N:'
        self.offCmd = 'DO;' + str(doNum) + ';F:'
        self.dwellCmd = 'DO;' + str(doNum) + ';D;%(val)s:'
        self.httpAction = HttpAction(localrouter)
        self.httpAction.configure( self.MakeHttpConfig() )
        self.httpAction.start()
        self.dwellTime = -1
        self.localrouter.subscribe( 20 , self , 'http://id.webbrick.co.uk/events/webbrick/DO' ,  'webbrick/' + self.nodeNum + '/DO/' + self.doNum)
        
    def MakeHttpConfig(self):
        cfg = {}
        cfg['eventtype'] = [{},{},{}]
        cfg['eventtype'][0]['type'] = self.eType
        cfg['eventtype'][0]['eventsource'] = {}
        cfg['eventtype'][0]['eventsource']['source'] = self.eOnSource
        cfg['eventtype'][0]['eventsource']['event'] = {}
        cfg['eventtype'][0]['eventsource']['event']['url'] = {}
        cfg['eventtype'][0]['eventsource']['event']['url']['cmd'] = 'GET'
        cfg['eventtype'][0]['eventsource']['event']['url']['uri'] = '/cfg.spi?com=' + self.onCmd
        cfg['eventtype'][0]['eventsource']['event']['url']['address'] = self.wbTarget
        
        cfg['eventtype'][1]['type'] = self.eType
        cfg['eventtype'][1]['eventsource'] = {}
        cfg['eventtype'][1]['eventsource']['source'] = self.eOffSource
        cfg['eventtype'][1]['eventsource']['event'] = {}
        cfg['eventtype'][1]['eventsource']['event']['url'] = {}
        cfg['eventtype'][1]['eventsource']['event']['url']['cmd'] = 'GET'
        cfg['eventtype'][1]['eventsource']['event']['url']['uri'] = '/cfg.spi?com=' + self.offCmd
        cfg['eventtype'][1]['eventsource']['event']['url']['address'] = self.wbTarget
        
        cfg['eventtype'][2]['type'] = self.eType
        cfg['eventtype'][2]['eventsource'] = {}
        cfg['eventtype'][2]['eventsource']['source'] = self.eDwellSource
        cfg['eventtype'][2]['eventsource']['event'] = {}
        cfg['eventtype'][2]['eventsource']['event']['url'] = {}
        cfg['eventtype'][2]['eventsource']['event']['url']['cmd'] = 'GET'
        cfg['eventtype'][2]['eventsource']['event']['url']['uri'] = '/cfg.spi?com=' + self.dwellCmd
        cfg['eventtype'][2]['eventsource']['event']['url']['address'] = self.wbTarget
        
        cfg['name'] = 'HttpAction'
        cfg['module'] = 'EventHandlers.HttpAction'
        return cfg
    
    def initSubscription(self,status):
        pass
    
    def getUri(self):
        return "DIGITAL_OUTPUT/" + self.wbTarget + '/' + self.doNum 
        
    def turnOn(self,dwell = 0):
        if dwell > 8:
            #TODO deal with this better somehow
            #dwell must be above 8 seconds as below that are the dwell presets
            newEvent = makeEvent (self.eType,self.eDwellSource,{'val':str(int(dwell))} )
            self.dwellAmount = dwell
            self.dwellTime = time.time() + dwell
        else:
            newEvent = makeEvent( self.eType, self.eOnSource,  {} )      
            self.dwellTime = 0    
            self.dwellAmount = 0  
        self.targetVal = '1' 
        self.localrouter.publish(newEvent.getSource() , newEvent)
    
    def turnOff(self):
        newEvent = makeEvent( self.eType,self.eOffSource , {} )         
        self.localrouter.publish(newEvent.getSource() , newEvent)   
        self.targetVal = '0'
        
    def doHandleEvent(self,handler,inEvent):
        if inEvent.getType() == 'http://id.webbrick.co.uk/events/webbrick/DO':
            if inEvent.getSource() == 'webbrick/' + self.nodeNum + '/DO/' + self.doNum:
                if inEvent.getPayload()['state'] != self.targetVal:
                    if self.targetVal == '0':          
                        self._log.error("Webbrick DO not at target value is off , should be on")
                        self.turnOff()
                    elif self.targetVal == '1':
                        #check if we were dwelling
                        if self.dwellAmount:
                            if self.dwellTime < time.time():
                                #dwell time has expired being off is fine
                                self.targetVal = '0'
                            else:
                                #dwell not expired , dwell must have failed to set
                                self._log.error("Webbrick DO not at target value is off , should be on for %i seconds" %self.dwellTime)
                                self.turnOn(self.dwellAmount)
                        else:                    
                            self._log.error("Webbrick DO not at target value is off , should be on")
                            self.turnOn()
        return makeDeferred(StatusVal.OK)






""" XML """
class Boiler():
    def __init__(self,cfgDict):
        print "test"
    #def turnOn(self):
        #dostuff
        
    #def turnOff(self):
        #dostuff
        
""" XML """        
class Solar():
    def __init__(self,cfgDict):
        print "test"
    #def doAction(self):
    #def turnOn(self):
        #alwayson
    #def turnOff(self):
        #alwayson

""" XML """
class GroundSource():
    def __init__(self,cfgDict):
        print "test"
    #def turnOn(self):
        #on
    #def turnOff(Self):
        #off

""" XML """
class AirSource():
    def __init__(self,cfgDict):
        print "test"
    #def setMode(self):
        #stuff    
    #def turnOn(self):
        #on
    #def turnOff(self):
        #off
""" 
XML
<valve name="<valve name>" key="<unique key>" type="<diverting>|<mixing>">
        <directions>
            <direction name="Triangle Square (hot only)" key="TS" wbTarget ="10.100.100.102" cmd ="DO;1;N:" /> 
            <direction name="Circle Square (cold only)" key="CS" wbTarget ="10.100.100.102" cmd ="DO;2;N:" />
        </directions>
</valve>

Step inbetween the two directions
"""

class Valve():
    def __init__(self,cfgDict,localrouter):
        self.localrouter = localrouter
        self.currentpos = 0
        self.name = cfgDict["name"]
        self.key = cfgDict["key"]
        self.type = cfgDict["type"]
        
        if self.type == "digital":
            self.makeDigital(cfgDict['directions'])
        elif self.type == "digitalTimed":
            self.makeDigitalTimed(cfgDict['directions'])
        elif self.type == "analog":
            self.makeAnalog(cfgDict['directions'])
        else:
            raise Exception("Too many valve directions")
        
    def makeAnalog(self,directions):
        #analog valves are assumed to operate on the same analog output
        #we dont need to worry about conflict states
        self.move = {}
        self.wbTarget = directions[0]['wbTarget']
        #assume both are the same analog output
        self.aOutput = directions[0]['ao']
        aX = int(directions[0]['val'])
        aY = int(directions[1]['val'])
        if aX > aY:
            moveToX = 1
            moveToY = -1
            self.min = aY
            self.max = aX
        else:
            moveToX = -1
            moveToY = 1
            self.min = aX
            self.max = aY
        
        self.range = float(self.max - self.min)
        self.move[directions[0]['key']] = moveToX
        self.move[directions[1]['key']] = moveToY
        
        self.ao = AnalogOutput('internal/hvac/analogoutput', 'hvac/valve/' + self.key + '/' + self.aOutput ,self.localrouter,self.wbTarget,self.aOutput)    
        
    def makeDigital(self,directions):
        #spring loaded valves use one digital output and are either on or off, with no dwell time
        #we dont need to worry about conflict states
        if directions[0]['do'] == directions[1]['do']:    
            self.dOutput = directions[0]['do']
            self.wbTarget = directions[0]['wbTarget']                        
            self.move = {}
            #check the states are valid
            if directions[0]['state'] != '1' or directions[0]['state'] != '0': 
                if directions[1]['state'] != '1' or directions[1]['state'] != '1':
                    self.do = DigitalOutput('internal/hvac/digitaloutput' , 'hvac/valve/' + self.key + '/' + self.dOutput , self.localrouter , self.wbTarget , self.dOutput)
                    self.move[directions[0]['key']] = directions[0]['state']
                    self.move[directions[1]['key']] = directions[1]['state']
        else:
            #two different digital outputs are not supported
            raise Exception("Error while configuring valve, digital valves should use the same output")
        
    def makeDigitalTimed(self,directions):
        #make use of two digital outputs, the webbrick is told to dwell , we need to make sure we dont issue dwells on the other DO while the other is still dwelling
        #we dont track the position of the valve
        self.move = {}
        if directions[0]['do'] == directions[1]['do']:
            raise Exception("Error while configuring valve, digital timed valves should use different outputs")
        self.wbTarget = directions[0]['wbTarget']
        self.dOut1 = directions[0]['do']
        self.dOut2 = directions[1]['do']
        #the outputs could be on different webbrick , unlikely but possible
        self.wbTarget1 = directions[0]['wbTarget']
        self.wbTarget2 = directions[1]['wbTarget']
        
        do1 = DigitalOutput('internal/hvac/digitalout' , 'hvac/valve/' + self.key + '/' + self.dOut1 , self.localrouter,self.wbTarget,self.dOut1)
        do2 = DigitalOutput('internal/hvac/digitalout' , 'hvac/valve/' + self.key + '/' + self.dOut2 , self.localrouter,self.wbTarget,self.dOut2)
        self.move[directions[0]['key']] = (do1,float(directions[0]['pc']))
        self.move[directions[1]['key']] = (do2,float(directions[1]['pc']))
        
        
    def action(self,actionDict):
        for key in actionDict:
            if key == "turn":
                doTurn(actionDict)
    
    def doTurn(self,direction,amount = 0):
        """ 
            Amount is a % value of direction of the turn
        """
        if self.type == "analog":
            setPoint = int(self.aTurn(direction,amount))
            self.ao.SetAO(setPoint)
        elif self.type == "digital":
            #solo digitals are either on or off
            if self.move[direction] == '1':
                self.do.turnOn()
            else:
                self.do.turnOff()
        elif self.type == "digitalTimed":
            #turn off the other DO
            for d in self.move:
                if d != direction:
                    self.move[d][0].turnOff()
            self.move[direction][0].turnOn(amount * self.move[direction][1] )
                   
            
            
    
    def aTurn(self,direction,amount):
        m = self.move[direction]        
        moveamount = m * (amount * (self.range / 100))
        self.currentpos = self.currentpos + moveamount
        if self.currentpos < self.min:
            self.currentpos = self.min
        elif self.currentpos > self.max:
            self.currentpos = self.max
        return self.currentpos
                    

""" 
XML
<pumps>
    <pump name ="UFH Pump" key="kasjdfkl3" wbTarget = "10.100.100.102" on="DO;1;N" off="DO;1;F"/>
</pump>
"""
   
class Pump():
    def __init__(self,cfgDict,localrouter):
        #stuff
        #wbTarget
        #wbCmd
        cfgXml =""" <eventInterface module='EventHandlers.HttpAction' name='HttpAction' usetwisted='0'>
                        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
                            <!-- events from a source of a specific type -->
                            <eventsource source="webbrick/100/TD/0" >
                                <!-- all events from a single source -->
	                            <event>
                                    <params>
                                    </params>
		                            <url cmd="GET" address="localhost:59999" uri="/test?medianame=ITunes&amp;mediacmd=volup" />
                                    Test
	                            </event>
                            </eventsource>
                        </eventtype>
                    </eventInterface>
                """
        
        self.httpAction = HttpAction(thisRouter)
        self.httpAction.configure(cfgXml)
        
    def doAction(self,actionDict):
        for key in actionDict:
            if key == "TURN_ON":
                self.turnOn()
            elif key == "TURN_OFF":
                self.turnOff()
        return {"GETURL" : url}
        
    def turnOn(self):
        self.hvac("dosomething")
        return {"GETURL" : url}
        
    def turnOff(self):
        self.hvac("dosomething")
        return {"GETURL" : url}
