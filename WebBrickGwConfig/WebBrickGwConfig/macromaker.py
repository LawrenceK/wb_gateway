# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

 

from xml.etree.ElementTree import *

from MiscLib.DomHelpers import *
from xml.dom.minidom import parseString

SITE_DIRECTORY = "/opt/webbrick/site/eventdespatch/"
def Test():
    commands = getDictFromXmlFile( "commands.txt" ) 
    command = commands["command"]

    conditional = command["conditional"]
    send = command["send"]
    params = command["params"]
    complete = command["complete"]
    interfaces = Element("eventInterfaces")
    newStage = SubElement(interfaces , "eventInterface")
    newStage.attrib["module"] = "EventHandlers.Compound"
    newStage.attrib["name"] = "Compound" 
    Params = {"val1":"lutronTelnet" , "val2":"1" , "val3":"4" , "val4":"1" , "val5":'1' , "val6":"0"}
   
    a = makeInitialStates(newStage)
    

    z = makeBeginSubscription(newStage , 1 , "TestMacro")
    
    
    p = makeConditionalSubscription( newStage,conditional,Params )
    
   
    m = makeEndSubscription(newStage, complete , Params)
    
    
  
    x = makeTriggerCompound(newStage , send , conditional , Params)
    

    n = makeConditionalFailCompound(newStage , send , conditional , Params)
    
   
    y = makeCompletedCompound(newStage , complete, 1 , "TestMacro" , Params) 
    
   
    f = makeFalseStartCompound(newStage) 
    
    
    
    
    txt = tostring(interfaces)
    prettyxml =  parseString(txt).toprettyxml() 
    
    f = open("macro.xml",'w')
    f.write( prettyxml )
    f.close()

 
def TestMakeMacro():
    
    OutFile = "testmacro.xml"
    TestConditional =   {"type" : "Test/Command/Type" , "source" : "Test/Command/Sub/val1_%(val1)" + "s" + "/val2_%(val2)" + "s" , "attr" : "val" ,  "val":"%(val3)" + "s" }
    TestTriggerPayload  = { "this" : 'is' , 'a' : 'test' , 'payload' : 'test' , 'val4' : '%(val4)' + "s"}
    TestTrigger = { "type" : "Test/Trigger/Type" , "source" : "Test/Trigger/Source" , "payload" : TestTriggerPayload } 
    TestComplete = { "type" : "Test/Complete/Type" , "source" : "Test/Command/Sub/val1_%(val1)" + "s" + "/val2_%(val2)" + "s" , "attr" : "val" ,  "val":"%(val3)" + "s", "attr" : "val" , "val" : "1"}
    TestParams = { "val1" : "testval1" , "val2" : "testval2" , "val3" : "testval3" , "val4" : "testval4" } 
    TestCommand = { "conditional" : TestConditional , "trigger" : TestTrigger , "complete" : TestComplete }
    MakeMacro( OutFile , {'TestCommand1' : {"command":TestCommand , "params" : TestParams } , 'TestCommand2' : {"command":TestCommand , "params" : TestParams } } , "TestMacro" )
     
    
def CreateMacros(Devices,Location):
    print "MAKEMCR: Iterating devices"
    locationdispatch = '<eventInterfaces>' 
    for device in Devices:
        #check if the device is in the right location
        if Devices[device]['location']['val'] == Location:
            print "MAKEMCR: Device found in correct location : %s" %Devices[device]['name']['val']
            if Devices[device].has_key('connections'): 
                print "MAKEMCR: Iterating device outputs for terminated output"
                for connection in Devices[device]['connections']:
                    #print "RENDERAV: Output : %s" %connection
                    if connection.has_key("sources"):
                        for source in connection['sources']: 
                            #we look for terminated sources as they are a head of the connection trees
                            if source.has_key('status'):
                                if source['status']['val'] == "terminated":
                                    print "MAKEMCR: Found terminated source : %s" %source['name']['val']
                                    locationdispatch +=(MakeMacros(Devices[device],Devices , Location))
                                   # print "MAKEMCR: Locationdispatch is %s" %locationdispatch
                                    #we get a none button if we failed to find any method to switch to that sink
                             
    locationdispatch += '</eventInterfaces>'
    locationdispatch = parseString(locationdispatch)
    f = open(SITE_DIRECTORY + "%s_Macros.xml" %Location ,'w')
    f.write(locationdispatch.toprettyxml())
    f.close()

    
def StringSub(Args , String):
    #print "STRINGSUB : Args %s , String %s" %(Args,String)
    if '%' in String:
        String = String %Args
        #print "STRINGSUB : Subbed %s" %String
    return String
    
def DictSub(Args , Dictionary):
    #print "DICTSUB : Args %s , Dictionary %s" %(Args,Dictionary)
    for key in Dictionary:
        if '%' in Dictionary[key]:
            Dictionary[key] = Dictionary[key] %Args
           # print "STRINGSUB : Subbed %s" %Dictionary[key]
    return Dictionary
    
def GetCompatibleSources(Type, Focus , Devices):
    result = []
    print "MACROMCR: Finding sinks compatible with : %s , %s" %(Type , Focus)
    for device in Devices:
        if Devices[device].has_key("connections"):
            for connection in Devices[device]['connections']:
                if connection.has_key("sources"):
                    for source in connection['sources']:
                        if source["focus"]["val"] == Focus and source["type"]["val"] == Type:
                            result.append( { 'deviceId':device , 'source':source ,'connection':connection } )
    return result      
    
      
def GlobalSink(Sink , Macros , Macrostring ,  MacroName , Device , Devices , Location , Depth):
    print "MAKEMCR: Found global sink : %s" %Sink
    sources = GetCompatibleSources(Sink['type']['val'] , 'global' , Devices)
    for source in sources:
        currentMacrostring = Macrostring
        print "MAKEMCR: Found potential connection for a global sink : %s" %(source) 
        for command in Sink['commands']:
            #print "MAKEMCR: Adding command %s" %command
            commandname = command['name'] 
            #global sinks are a special case , we grab the parameters from potential sources, not from the sink itself
            commandparams = source['source']['parameters']
            if Device.has_key('ip'):
                commandparams["ip"] = Device['ip']['val']
            print "MAKEMCR: Parameters grabbed from potential source are %s" %commandparams
            commandparams = DictSub({"id" : Device['id']['val'] } , commandparams)
            print "MAKEMCR: Parameters for command are %s" %commandparams
            #print "MAKEMCR: Available commands are %s" %Device["commands"]
            if commandname in Device['commands']:
                command = Device['commands'][commandname]
                currentMacrostring += makeDispatch(command , Depth , """%(macroname)s""" , commandparams)
                currentDepth = Depth + 1
                #print "MAKEMCR: Added macro , macrostring is now %s" %Macrostring
                
        connectedto = source['deviceId']
        sourceMName = MacroName + Device['name']['val'] + Sink['name']['val'] 
        Macros = MakeMacroRecur(Macros , currentMacrostring , sourceMName , Devices[connectedto] , Devices , Location , Depth)
    return Macros
        
def ConnectedSink(Sink , Macros , Macrostring ,  MacroName , Device , Devices , Location , Depth):
    print "MAKEMCR: Found connected sink"           
    for command in Sink['commands']:
        #print "MAKEMCR: Adding command %s" %command
        commandname = command['name'] 
        commandparams = command['params']                    
        commandparams = DictSub({"id" : Device['id']['val'] } , commandparams)
        print "MAKEMCR: Parameters for command are %s" %commandparams
        #print "MAKEMCR: Available commands are %s" %Device["commands"]
        if commandname in Device['commands']:
            command = Device['commands'][commandname]
            Macrostring += makeDispatch(command , Depth , """%(macroname)s""" , commandparams)
            Depth +=1
            #print "MAKEMCR: Added macro , macrostring is now %s" %Macrostring
            
    connectedto = Sink['connectedto']['val'][0:3]
    MacroName = MacroName + Device['name']['val'] + Sink['name']['val'] 
    Macros = MakeMacroRecur(Macros , Macrostring , MacroName , Devices[connectedto] , Devices , Location , Depth) 
    return Macros
    
def TerminatedSink(Sink , Macros , Macrostring ,  MacroName , Device , Devices , Location , Depth):    
    print "MAKEMCR: Found terminated sink, required commands are %s" %Sink['commands']
    for command in Sink['commands']:
        commandname = command['name'] 
        commandparams = command['params']
        #txid and rxid indicate a skybox , this is a special case which uses two serial devices
        if Device.has_key('txid') and Device.has_key('rxid'):
            commandparams = DictSub({"txid" : Device['txid']['val'] , "rxid" : Device['rxid']['val'] } , commandparams)
        elif Device.has_key('ip'):          
            commandparams = DictSub({"id" : Device['id']['val'] , 'ip' : Device['ip']['val'] } , commandparams)
        else:
            commandparams = DictSub({"id" : Device['id']['val'] } , commandparams)
        print "MAKEMCR: Parameters for command are %s" %commandparams
        #print "MAKEMCR: Available commands for the device are %s" %Device['commands']
        if commandname in Device['commands']:
            print "MAKEMCR: Writing dispatch for command %s" %Device['commands'][commandname]
            command = Device['commands'][commandname]            
            Macrostring += makeDispatch(command , Depth , """%(macroname)s"""  , commandparams)
            Depth+=1
            
    MacroName = MacroName + Sink['name']['val']
    print "MAKEMCR: Unformatted MacroName is %s" %MacroName
    MacroName = MacroName.replace(' ' , '_')        
    Macrostring = StringSub({"macroname" : MacroName } , Macrostring)
    Macrostring += """\n<!-- This is the end of a macro -->\n"""
    #print "MAKEMCR: Macros is %s" %Macros
    Macros +=(Macrostring)        
    return Macros
    
def MakeMacroRecur(Macros , Macrostring ,  MacroName , Device , Devices , Location , Depth):
    print "MAKEMCR: Iterating connections on Device : %s" %Device['name']['val']
    for connection in Device['connections']:
        if connection.has_key('sinks'):
            for sink in connection['sinks']:
                if sink['focus']['val'] == 'global':
                    Macros = GlobalSink(sink, Macros , Macrostring ,  MacroName , Device , Devices , Location , Depth)
                    
                elif sink['status']['val'] == 'connected':     
                    Macros = ConnectedSink(sink, Macros , Macrostring ,  MacroName , Device , Devices , Location , Depth)
                    
                elif sink['status']['val'] == 'terminated':
                    Macros = TerminatedSink(sink, Macros , Macrostring ,  MacroName , Device , Devices , Location , Depth)                
    print "MAKEMCR: Finished Iterating connections on Device : %s" %Device['name']['val']
    return Macros    
    

def MakeMacros(Device , Devices , Location):    
    return MakeMacroRecur('' , '' , '' , Device , Devices , Location , 0)
            

def makeDispatch(Command , StageNumber , MacroName , Params = None):
    
    dispatch = "<!-- \n\n\n\t\t\t ===== This is Macro %s ===== \n\n\n\t -->" %MacroName
    dispatch += "<!-- \n\n\t\t === This is Command : %s , The Stage is : %i  === \n\n-->" %(Command , StageNumber)
    if Command.has_key("conditional"):
        conditional = Command["conditional"]
    else:
        conditional = None
    send = Command["send"]
    if Command.has_key("complete"):
        complete = Command["complete"]
    else:
        complete = None
    newStage = Element("eventInterface")
    newStage.attrib["module"] = "EventHandlers.Compound"
    newStage.attrib["name"] = "Compound" 
    
    makeInitialStates(newStage)
    makeBeginSubscription(newStage , StageNumber , MacroName)
    if conditional:
        makeConditionalSubscription( newStage, conditional , Params )
    
    makeTriggerCompound(newStage , send , conditional , Params)
    if conditional:
        makeConditionalFailCompound(newStage , send , conditional , Params)    
    makeCompletedCompound(newStage , complete, StageNumber , MacroName , Params)
    if complete:
        makeEndSubscription(newStage, complete , Params)        
    else:
        makeSkipSubscription(newStage,  send , Params)
         
    makeFalseStartCompound(newStage) 
    dispatch = tostring(newStage)
   
    return dispatch
        
def makeTriggerCompound(NewStage , SendEvtInfo , Conditional = None , Params = None):
    #make compound to send the event we want the macro to trigger
    if SendEvtInfo.has_key("type") & SendEvtInfo.has_key("source"):
        NewStage.append(Comment("""This compound creates the event that the macro needs to send to perform its function We check variables to make sure we are starting the macro This is the trigger """))
        compound = SubElement( NewStage , "compound" )
        #compound.append(Comment("\n\t\t"))
        paramstag = SubElement( compound , "params" )
        #paramstag.append(Comment("\n\t\t\t"))

        testEq = SubElement ( paramstag , "testEq" )
        testEq.attrib["name"]  = "completed"
        testEq.attrib["value"] = "false"
        testEq.attrib["type"] = "string"
        #paramstag.append(Comment("\n\t\t\t"))

        testEq2 = SubElement ( paramstag , "testEq" ) 
        testEq2.attrib["name"] = "started"
        testEq2.attrib["value"] = "true"
        testEq2.attrib["type"] = "string"
        #paramstag.append(Comment("\n\t\t\t"))

        testEq3 = SubElement ( paramstag , "testEq" ) 
        testEq3.attrib["name"] = "storing"
        testEq3.attrib["value"] = "false"
        testEq3.attrib["type"] = "string"
        #paramstag.append(Comment("\n\t\t\t"))
        if Conditional:
            testEq4 = SubElement ( paramstag , "testEq" ) 
            testEq4.attrib["name"] = "storevariable"
            testEq4.attrib["value"] = stringSub(Conditional["val"] , Params)
            testEq4.attrib["type"] = "string"
            #paramstag.append(Comment("\n\t\t"))
        
        #compound.append(Comment("\n\t\t"))
        newEvent = SubElement ( compound , "newEvent" ) 
        newEvent.attrib["type"] = stringSub( SendEvtInfo["type"] , Params )
        newEvent.attrib["source"] = stringSub( SendEvtInfo["source"] , Params )
        
        if SendEvtInfo.has_key("payload"):
            #newEvent.append(Comment("\n\t\t\t"))
            copyOtherData = SubElement ( newEvent , "other_data" )
            for x in SendEvtInfo["payload"]:
                copyOtherData.attrib[ x ] = stringSub(SendEvtInfo["payload"][x] , Params)
        #newEvent.append(Comment("\n\t\t"))
        #compound.append(Comment("\n\t"))
        return tostring(compound)
        
def makeConditionalFailCompound(NewStage , SendEvtInfo , Conditional = None , Params = None):
    #make compound to send the event we want the macro to trigger
    if SendEvtInfo.has_key("type") & SendEvtInfo.has_key("source"):
        NewStage.append(Comment("This compound is for when we have a conditional for the trigger, and it fails, because we need to set started to false to indicate the macro did not start"))
        
        compound = SubElement( NewStage , "compound" )
        #compound.append(Comment("\n\t\t"))
        paramstag = SubElement( compound , "params" )
        #paramstag.append(Comment("\n\t\t\t"))

        testEq = SubElement ( paramstag , "testEq" )
        testEq.attrib["name"]  = "completed"
        testEq.attrib["value"] = "false"
        testEq.attrib["type"] = "string"
        #paramstag.append(Comment("\n\t\t\t"))

        testEq2 = SubElement ( paramstag , "testEq" ) 
        testEq2.attrib["name"] = "started"
        testEq2.attrib["value"] = "true"
        testEq2.attrib["type"] = "string"
        #paramstag.append(Comment("\n\t\t\t"))

        testEq3 = SubElement ( paramstag , "testEq" ) 
        testEq3.attrib["name"] = "storing"
        testEq3.attrib["value"] = "false"
        testEq3.attrib["type"] = "string"
        #paramstag.append(Comment("\n\t\t\t"))
        
        if Conditional:
            testEq4 = SubElement ( paramstag , "testNe" ) 
            testEq4.attrib["name"] = "storevariable"
            testEq4.attrib["value"] = stringSub(Conditional["val"] , Params)
            testEq4.attrib["type"] = "string"
            #paramstag.append(Comment("\n\t\t"))
        
        #compound.append(Comment("\n\t\t"))
        newEvent = SubElement ( compound , "newState" ) 
        newEvent.attrib["name"] = "started"
        newEvent.attrib["value"] = "false"
        
        #newEvent.append(Comment("\n\t\t"))
        #compound.append(Comment("\n\t"))
        return tostring(compound)
  
  
def makeSkipSubscription( NewStage,  EndTriggerInfo , Params = None):

    #subscribe to the event that signifys the macro can finish
    NewStage.append(Comment("Create the subscription to the event we want to listen to signify that the macro action completed successfully"))
        
    if EndTriggerInfo.has_key("source") & EndTriggerInfo.has_key("type"):
        completetype = SubElement(NewStage,"eventtype")
        completetype.attrib["type"] = stringSub( EndTriggerInfo["type"] , Params )
        #completetype.append( Comment("\n\t\t") )
        completedsource = SubElement(completetype,"eventsource")
        completedsource.attrib["source"] = stringSub( EndTriggerInfo["source"] , Params )
        #completedsource.append( Comment("\n\t\t\t") )
        evt = SubElement ( completedsource , "event" )
        #evt.append( Comment("\n\t\t\t\t") )
        action = SubElement ( evt , "action" ) 
        action.attrib["name"] =  "completed"
        action.attrib["value"] = "true"
        #evt.append( Comment("\n\t\t\t\t") )
        action2 = SubElement ( evt , "action" ) 
        action2.attrib["name"] =  "storing"
        action2.attrib["value"] = "false"
        #evt.append( Comment("\n\t\t\t") )
        
      
   
    
def makeCompletedCompound(NewStage, CompletedEvtInfo , StageNumber, MacroName , Params = None):
    NewStage.append(Comment("This compound signals the next stage in the macro to start and cleans up this stage so it ready to start again"))        
    #make the compound to listen for the event that signifies the macro completed
    compound = SubElement ( NewStage , "compound" )
    #compound.append( Comment("\n\t\t") )
    params = SubElement( compound , "params" )
    #params.append( Comment("\n\t\t\t") )
    testEq1 = SubElement ( params , "testEq" )
    testEq1.attrib["name"] = "completed"
    testEq1.attrib["value"] = "true"
    testEq1.attrib["type"] = "string"
    #params.append( Comment("\n\t\t\t") )
    testEq2 = SubElement( params , "testEq" )
    testEq2.attrib["name"] = "started"
    testEq2.attrib["value"] = "true"
    testEq2.attrib["type"] = "string"
    #params.append( Comment("\n\t\t") )
    #compound.append( Comment("\n\t\t") )
    newEvent = SubElement( compound , "newEvent" )
    newEvent.attrib["type"] = "%s/Macro/Begin" %MacroName
    newEvent.attrib["source"] = "%s/Begin/Stage/%i" %(MacroName,StageNumber+1)
    #compound.append( Comment("\n\t\t") )
    newState = SubElement( compound , "newState" )
    newState.attrib["name"] = "started"
    newState.attrib["value"] = "false" 
    #compound.append( Comment("\n\t\t") )
    newState2 = SubElement( compound , "newState" )
    newState2.attrib["name"] = "completed"
    newState2.attrib["value"] = "false"
    #compound.append( Comment("\n\t") )
    
    return tostring(compound)

def makeFalseStartCompound(NewStage):
    NewStage.append(Comment("This compound cleans up if the macro completes before it is started(ie the finishing event we are listening to is caused by another source) , that way we dont complete unless the macro is in progress"))        
    compound = SubElement ( NewStage , "compound" )
    #compound.append( Comment("\n\t\t") )
    params = SubElement( compound , "params" )
    #params.append( Comment("\n\t\t\t") )
    testEq1 = SubElement ( params , "testEq" )
    testEq1.attrib["name"] = "completed"
    testEq1.attrib["value"] = "true"
    testEq1.attrib["type"] = "string"
    #params.append( Comment("\n\t\t\t") )
    testEq2 = SubElement( params , "testEq" )
    testEq2.attrib["name"] = "started"
    testEq2.attrib["value"] = "false"
    testEq2.attrib["type"] = "string"
    #params.append( Comment("\n\t\t") )
    #compound.append( Comment("\n\t\t") )
    newState2 = SubElement( compound , "newState" )
    newState2.attrib["name"] = "completed"
    newState2.attrib["value"] = "false"
    #compound.append( Comment("\n\t") )
    
    return tostring(compound)
    
def makeInitialStates(NewStage):
    #create the initialstates of "completed" "started" and "storevariable"
    NewStage.append(Comment("Set up the initial variables so we dont run into errors later"))        
    completedvar = SubElement(NewStage,"initialState")
    completedvar.attrib["name"] = "completed"
    completedvar.attrib["value"] = "false"
    #NewStage.append( Comment("\n\t") )
    startedvar = SubElement(NewStage,"initialState")
    startedvar.attrib["name"] = "started"
    startedvar.attrib["value"] = "false"
    #NewStage.append( Comment("\n\t") )
    conditionalvar = SubElement(NewStage,"initialState")
    conditionalvar.attrib["name"] = "storevariable"
    conditionalvar.attrib["value"] = "0"    
    #NewStage.append( Comment("\n\t") )
    storingvar = SubElement(NewStage,"initialState")
    storingvar.attrib["name"] = "storing"
    storingvar.attrib["value"] = "false"
        
def makeBeginSubscription(NewStage , StageNumber, MacroName):
    #subscribe to the event that we are going to use to trigger the macro stage with
    NewStage.append(Comment("Subscribe to the event that should start this stage of the macro"))        
    begintype = SubElement(NewStage , "eventtype")
    begintype.attrib["type"] = "%s/Macro/Begin" %MacroName
    #begintype.append( Comment("\n\t\t") )
    beginsource = SubElement(begintype,"eventsource")
    beginsource.attrib["source"] = "%s/Begin/Stage/%i" %(MacroName, StageNumber)
    #beginsource.append( Comment("\n\t\t\t") )
    beginevt = SubElement(beginsource,"event")
    #beginevt.append( Comment("\n\t\t\t\t") )
    beginaction = SubElement(beginevt,"action")
    beginaction.attrib["name"] = "started"
    beginaction.attrib["value"] = "true"        
    #beginevt.append( Comment("\n\t\t\t\t") )
    beginaction2 = SubElement(beginevt,"action")
    beginaction2.attrib["name"] = "storing"
    beginaction2.attrib["value"] = "false"        
    #beginevt.append( Comment("\n\t\t\t") )
    #beginsource.append( Comment("\n\t\t") )
    #begintype.append( Comment("\n\t") )
    
def makeConditionalSubscription( NewStage,Conditional, Params = None ):
    #subscribe to an event that we monitor to see if the macro should start or not
    NewStage.append(Comment("Subscribe to the conditional event, so we know what state it is in when we check it when starting the macro"))
        
    if Conditional.has_key("type") & Conditional.has_key("source") & Conditional.has_key("attr"):
        
        conditionaltype = SubElement(NewStage,"eventtype")
        conditionaltype.attrib["type"] = stringSub( Conditional["type"], Params )
        #conditionaltype.append( Comment("\n\t\t") )
        conditionalsource = SubElement( conditionaltype , "eventsource" )
        conditionalsource.attrib["source"] = stringSub( Conditional["source"] , Params )
        #conditionalsource.append( Comment("\n\t\t\t") )
        event = SubElement(conditionalsource,"event")
        #event.append( Comment("\n\t\t\t\t") )
        storeaction = SubElement(event,"action")
        storeaction.attrib["name"] = "storevariable"
        storeaction.attrib["key"] = Conditional["attr"]
        #event.append( Comment("\n\t\t\t\t") )        
        storeaction2 = SubElement(event,"action")
        storeaction2.attrib["name"] = "storing"
        storeaction2.attrib["value"] = "true"
        #event.append( Comment("\n\t\t\t") )
        #conditionalsource.append( Comment("\n\t\t") )
        #conditionaltype.append( Comment("\n\t") )
        
def makeEndSubscription( NewStage , EndTriggerInfo , Params = None):
    #subscribe to the event that signifys the macro can finish
    NewStage.append(Comment("Create the subscription to the event we want to listen to signify that the macro action completed successfully"))
        
    if EndTriggerInfo.has_key("source") & EndTriggerInfo.has_key("type"):
        completetype = SubElement(NewStage,"eventtype")
        completetype.attrib["type"] = stringSub( EndTriggerInfo["type"] , Params )
        #completetype.append( Comment("\n\t\t") )
        completedsource = SubElement(completetype,"eventsource")
        completedsource.attrib["source"] = stringSub( EndTriggerInfo["source"] , Params )
        #completedsource.append( Comment("\n\t\t\t") )
        evt = SubElement ( completedsource , "event" )
        #evt.append( Comment("\n\t\t\t\t") )
        action = SubElement ( evt , "action" ) 
        action.attrib["name"] =  "completed"
        action.attrib["value"] = "true"
        #evt.append( Comment("\n\t\t\t\t") )
        action2 = SubElement ( evt , "action" ) 
        action2.attrib["name"] =  "storing"
        action2.attrib["value"] = "false"
        #evt.append( Comment("\n\t\t\t") )
        
        #completedsource.append( Comment("\n\t\t") )
        #completetype.append( Comment("\n\t") )
        
def stringSub(String,Params):
    if '%' in String:
        String = String %Params
    return String        
