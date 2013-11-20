# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 


from EventLib.Event import Event
import time

defaults = { "slope" : {"type" : "internal/hvac/slope" , "source" : "mixingcircuit/%s" , "key" : "val"} , 
            "offset" : {"type" : "internal/hvac/offset" , "source" : "mixingcircuit/%s" , "key" : "val" } , 
            "outsidetemp" : {"type" : "internal/hvac/outsidetemp", "source" : "mixingcircuit/%s" , "key" : "val" },
            "actualtemp" : {"type" : "internal/hvac/actualtemp" , "source" : "mixingcircuit/%s", "key" : "val" }
           }

class MixingCircuit:
    def __init__(self,cfgDict,hvac):
        self.key = cfgDict["key"]
        self.hvac = hvac
        self.demand = False
        self.settleTime = int(cfgDict["settletime"])
        self.nextTime = time.time() + self.settleTime

        self.hotterDirectionKey = cfgDict["valve"]["hotter"]["direction"]
        self.coolerDirectionKey = cfgDict["valve"]["cooler"]["direction"]
        self.valveKey = cfgDict["valve"]["key"]
        
        self.pumpKey = None
        if cfgDict.has_key("pump"):
            self.pumpKey = cfgDict["pump"]["key"]
        
        self.actualtemp = None
        self.outsidetemp = None
        
        self.subscriptions = { "slope" : {"type" : "" , "source" : "" , "key" : ""} , 
            "offset" : {"type" : "" , "source" : "" , "key" : "" } , 
            "outsidetemp" : {"type" : "", "source" : "" , "key" : "" },
            "actualtemp" : {"type" : "" , "source" : "", "key" : "" }
           }
        self.subEvent("offset",cfgDict)
        self.subEvent("slope",cfgDict)
        self.subEvent("outsidetemp",cfgDict)
        self.subEvent("actualtemp",cfgDict)
        
        #setup stepping points
        """
        Stepping points dict
        { "<diff>" : "<stepsize>" }
        validate for overlaps
        for the moment diff is always positive, direction of change decided in code
        deadband is taken as stepsize 0
        """
        self.stepDict = {}
        for key in cfgDict:
            if key.find("step") != -1:
                stepSize = int(key[5:])
                self.stepDict[int(cfgDict[key])] = stepSize
                
    def subEvent(self,string,cfgDict):
        if cfgDict.has_key(string):
            event = Event(cfgDict[string]["type"],cfgDict[string]["source"],None)
            self.subscriptions[string]["type"] = cfgDict[string]["type"]
            self.subscriptions[string]["source"] = cfgDict[string]["source"]
            self.subscriptions[string]["key"] = cfgDict[string]["key"]

        else:
            event = Event(defaults[string]["type"],defaults[string]["source"] %cfgDict["key"],None)
            self.subscriptions[string]["type"] = defaults[string]["type"]
            self.subscriptions[string]["source"] = defaults[string]["source"] %cfgDict["key"]
            self.subscriptions[string]["key"] = defaults[string]["key"]

        self.hvac.subEvent(event,self)        
            
        
    def getTarget(self):
        target =  self.offset - (self.slope * self.outsidetemp) 
        return target
        
    def newEvent(self,event):
        eType = event.getType()
        eSource = event.getSource()
        
        if eType == self.subscriptions["slope"]["type"] and eSource == self.subscriptions["slope"]["source"]:
            self.slope = float(event.getPayload()["val"])
            if self.demand:
                self.nextTime = time.time() + self.settleTime
                self.checkStatus()
            
        elif eType == self.subscriptions["offset"]["type"] and eSource == self.subscriptions["offset"]["source"]:
            self.offset = float(event.getPayload()["val"])
            if self.demand:
                self.nextTime = time.time() + self.settleTime
                self.checkStatus()
            
        elif eType == self.subscriptions["outsidetemp"]["type"] and eSource == self.subscriptions["outsidetemp"]["source"]:
            self.outsidetemp = float(event.getPayload()["val"]) 
            if self.nextTime < time.time() and self.demand:
                self.nextTime = time.time() + self.settleTime
                self.checkStatus()
                
        elif eType == self.subscriptions["actualtemp"]["type"] and eSource == self.subscriptions["actualtemp"]["source"]:
            self.actualtemp = float(event.getPayload()["val"])
            if self.nextTime < time.time() and self.demand:
                self.nextTime = time.time() + self.settleTime
                self.checkStatus()
        
    def checkStatus(self):
        if self.actualtemp != None and self.outsidetemp != None and self.offset != None and self.slope != None:
            diff = self.actualtemp - self.getTarget() 
            if diff != 0:
                stepSize = self.getStepSize(diff) 
                if stepSize == 0:
                    pass
                else:                   
                    self.sendNewValvePosition(stepSize,diff)
         
    def onDemand(self):
        if self.pumpKey != None:
            self.hvac.actionComponent("pump", self.pumpKey,"TURN ON")
        self.demand = True
        
    def onNoDemand(self):
         if self.pumpKey != None:
            self.hvac.actionComponent("pump", self.pumpKey,"TURN OFF")
         self.sendNewValvePosition(100,1)
         self.demand = False
        
    def getStepSize(self,difference):
        diff = abs(difference)
        currentStepTemp = 0
        currentStepSize = 0
        for stepTemp in self.stepDict:

            if stepTemp <= diff:
                if currentStepTemp < stepTemp:
                    currentStepTemp = stepTemp
                    currentStepSize = self.stepDict[stepTemp]
        return currentStepSize
                               
    def sendNewValvePosition(self,valveStepSize,diff):
        """ Valve Step Size is a percentage value in which direction to move
            we look up the direction we need to move based if it is positive/negative
            positive = hotter
            negative = colder
        """          
        if diff > 0:
            #make cooler
            self.hvac.actionComponent("valve",self.valveKey,{ "turn" : self.coolerDirectionKey , "amount" : valveStepSize })
        if diff < 0:
            #make hotter
            self.hvac.actionComponent("valve",self.valveKey,{ "turn" : self.hotterDirectionKey , "amount" : valveStepSize })
        #if diff is zero we should not be here
            
            
        
        
        
    
