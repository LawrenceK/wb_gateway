#
#   Quick spike to read through a file and replace placeholders with elements
#
#   This is because the XML routines in python munge the XML and collapse any non XML bits.
#
#
#
#
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import XML, fromstring, tostring

LIGHTING_TEMPLATE_KID_LOCATION = "/opt/webbrick/site/templates/armour/templates/lighting_template.kid"
AV_TEMPLATE_KID_LOCATION = "/opt/webbrick/site/templates/armour/templates/av_template.kid"
HOMEPAGE_TEMPLATE_KID_LOCATION = "/opt/webbrick/site/templates/armour/templates/homepage_template.kid"
LAYOUT_TEMPLATE_KID_LOCATION = "/opt/webbrick/site/templates/armour/templates/layout_template.kid"

LIGHTING_TEMPLATE_KID_LOCATION_IPOD = "/opt/webbrick/site/templates/armour_itouch/templates/lighting_template.kid"
AV_TEMPLATE_KID_LOCATION_IPOD = "/opt/webbrick/site/templates/armour_itouch/templates/av_template.kid"
HOMEPAGE_TEMPLATE_KID_LOCATION_IPOD = "/opt/webbrick/site/templates/armour_itouch/templates/homepage_template.kid"
LAYOUT_TEMPLATE_KID_LOCATION_IPOD = "/opt/webbrick/site/templates/armour_itouch/templates/layout_template.kid"

EXTERITY_LIGHTING_TEMPLATE_JS_LOCATION = "/opt/webbrick/site/templates/ant/templates/lighting_template.js"
EXTERITY_MAIN_TEMPLATE_HTML_LOCATION = "/opt/webbrick/site/templates/ant/templates/exterity_template.html"
EXTERITY_TEMPLATE_JS_LOCATION = "/opt/webbrick/site/templates/ant/templates/main_template.js"

SITE_DIRECTORY = "/opt/webbrick/site/templates/"
#devices is a list of devices provisioned , Location is the location we are rendering the UI for, the output files take the format location_pagename.kid


def BuildWelcome(Locations):
    #TODO Build the welcome.kid file and populate it with buttons linking to the different locations
    pass
    
def StringListSub(Args , Stringlist):
    print "STRINGSUB : Args %s , Stringlist %s" %(Args,Stringlist)
    subbed = []
    for line in Stringlist:
        if '%' in line:
            line = line %Args
            print "STRINGSUB : Subbed %s" %line
        subbed.append(line)
    return subbed

def RenderNormalUI(Devices , Location):
    layout_template_file = open(LAYOUT_TEMPLATE_KID_LOCATION)
    layout_template = layout_template_file.readlines()
    
    
    lighting_template_file  = open(LIGHTING_TEMPLATE_KID_LOCATION)
    lighting_template  = lighting_template_file.readlines()
    lighting_template = StringListSub({"location" : Location} , lighting_template)    
    
    exterity_lighting_js_file  = open(EXTERITY_LIGHTING_TEMPLATE_JS_LOCATION)
    exterity_lighting_js  = exterity_lighting_js_file.readlines()
    
    exterity_template_js_file = open(EXTERITY_TEMPLATE_JS_LOCATION)
    exterity_template_js = exterity_template_js_file.readlines()  
    
    exterity_template_file = open(EXTERITY_MAIN_TEMPLATE_HTML_LOCATION)
    exterity_template = exterity_template_file.readlines()
    exterity_template = StringListSub({"location" : Location} , exterity_template)        
    
    av_template_file = open(AV_TEMPLATE_KID_LOCATION)
    av_template = av_template_file.readlines()
    av_template = StringListSub({"location" : Location} , av_template)        
    
    #homepage_template_file = open(HOMEPAGE_TEMPLATE_KID_LOCATION)
    #homepage_template = homepage_template_file.readlines()
    #homepage_template = StringListSub({"location" : Location} , homepage_template)    
    
    print "Rendering Location : %s" %Location
    if Location == "Mobile":
        #we would want to render a UI that has an appropriate select of all devices for a mobile device
        #messages.append("Mobile device UI not implemented")
        pass
    else:
        print "Rendering lighting buttons"
        lighting_page , exterity_js , exterity_lighting_js ,  lighting_messages = RenderLighting(lighting_template, exterity_template_js,  exterity_lighting_js , Location , Devices)
        print "Rendering AV buttons"
        av_page , av_messages = RenderAVButtons(av_template , Location , Devices)
        #print "Rendering Homepage"
        #homepage , homepage_messages = RenderHomePage(homepage_template , Location , Devices)
        print "Rendering Layout page"
        layout_page , layout_messages = RenderLayoutPage(layout_template , Location , Devices)
        
        #messages.extend(lighting_messages)
        #messages.extend(av_messages)
        #messages.extend(homepage_messages)
        
    lightingfile = open(SITE_DIRECTORY + "armour/" + Location + "_lighting.kid", 'w')
    avfile = open(SITE_DIRECTORY + "armour/" + Location + "_av.kid" , 'w')
    #homefile = open(SITE_DIRECTORY + "armour/" + Location + "_homepage.kid" , 'w')
    layoutfile = open(SITE_DIRECTORY + "armour/" + Location + "_layout.kid" , 'w')
    
    exteritylightsjs_file = open(SITE_DIRECTORY + "ant/" + Location + "_lighting.js", 'w')
    exterity_file = open(SITE_DIRECTORY + "ant/" + Location + "_exterity.html" , 'w')
    exterityjs_file = open(SITE_DIRECTORY + "ant/" + Location + "_main.js" , 'w')
    
    layoutfile.writelines(layout_page)
    lightingfile.writelines(lighting_page)
    avfile.writelines(av_page)
    #homefile.writelines(homepage)

    exterity_file.writelines(exterity_template)
    exteritylightsjs_file.writelines(exterity_lighting_js)
    exterityjs_file.writelines(exterity_js)

def RenderIpodUI(Devices , Location):    
    layout_template_file = open(LAYOUT_TEMPLATE_KID_LOCATION_IPOD)
    layout_template = layout_template_file.readlines()
    
    
    lighting_template_file  = open(LIGHTING_TEMPLATE_KID_LOCATION_IPOD)
    lighting_template  = lighting_template_file.readlines()
    lighting_template = StringListSub({"location" : Location} , lighting_template)    
    
    av_template_file = open(AV_TEMPLATE_KID_LOCATION_IPOD)
    av_template = av_template_file.readlines()
    av_template = StringListSub({"location" : Location} , av_template)        
    
    
    exterity_lighting_js_file  = open(EXTERITY_LIGHTING_TEMPLATE_JS_LOCATION)
    exterity_lighting_js  = exterity_lighting_js_file.readlines()
    
    exterity_template_js_file = open(EXTERITY_TEMPLATE_JS_LOCATION)
    exterity_template_js = exterity_template_js_file.readlines()  
    
    exterity_template_file = open(EXTERITY_MAIN_TEMPLATE_HTML_LOCATION)
    exterity_template = exterity_template_file.readlines()
    exterity_template = StringListSub({"location" : Location} , exterity_template)    
    
    #homepage_template_file = open(HOMEPAGE_TEMPLATE_KID_LOCATION_IPOD)
    #homepage_template = homepage_template_file.readlines()
    #homepage_template = StringListSub({"location" : Location} , homepage_template)    
    
    print "Rendering Location : %s" %Location
    if Location == "Mobile":
        #we would want to render a UI that has an appropriate select of all devices for a mobile device
        #messages.append("Mobile device UI not implemented")
        pass
    else:
        print "Rendering lighting buttons"
        lighting_page , exterity_js , exterity_lighting_js ,  lighting_messages = RenderLighting(lighting_template, exterity_template_js,  exterity_lighting_js , Location , Devices)
        print "Rendering AV buttons"
        av_page , av_messages = RenderAVButtons(av_template , Location , Devices)
        #print "Rendering Homepage"
        #homepage , homepage_messages = RenderHomePage(homepage_template , Location , Devices)
        print "Rendering Layout page"
        layout_page , layout_messages = RenderLayoutPage(layout_template , Location , Devices)
        
        #messages.extend(lighting_messages)
        #messages.extend(av_messages)
        #messages.extend(homepage_messages)
        
    lightingfile = open(SITE_DIRECTORY + "armour_itouch/" + Location + "_lighting.kid", 'w')
    avfile = open(SITE_DIRECTORY + "armour_itouch/" + Location + "_av.kid" , 'w')
    #homefile = open(SITE_DIRECTORY + "armour_itouch/" + Location + "_homepage.kid" , 'w')
    layoutfile = open(SITE_DIRECTORY + "armour_itouch/" + Location + "_layout.kid" , 'w')
    
    layoutfile.writelines(layout_page)
    lightingfile.writelines(lighting_page)
    avfile.writelines(av_page)
    #homefile.writelines(homepage)


def BuildUI(Devices , Location):
    messages = []
    messages.append("The following configuration steps were carried out :")
    #cache the template files
    RenderIpodUI(Devices,Location)
    RenderNormalUI(Devices,Location)
    return messages
    
def RenderLayoutPage(layout_template , Location , Devices):
    nadID = "NADNOTFOUND"
    for device in Devices:
        if Devices[device]["location"]["val"] == Location:
            if Devices[device]["type"]["val"] == "NAD Visio 5":
                nadID = Devices[device]["id"]["val"]
    layout_page = StringListSub({"location" : Location , "nadID" : nadID } , layout_template)    
    return layout_page , "Rendered layout page"
    
def RenderAVButtons(AV_Template , Location , Devices):
    sources = []
    startsources = "<sources>"      
    endsources = "</sources>"     
    start = 0
    end = 0
    messages = []
    for line in AV_Template:
        if (line.find(startsources) >= 0):
            start = AV_Template.index(line)
        if (line.find(endsources) >= 0):
            end = AV_Template.index(line)
    if start != 0 and end != 0:
        del AV_Template[start+1:end] # remove anything that is already there

    # At this point, the template is clean and new elements can be added
    print "RENDERAV: Iterating devices" 
    for device in Devices:
        #check if the device is in the right location
        if Devices[device]['location']['val'] == Location:
            print "RENDERAV: Device found in correct location : %s" %Devices[device]['name']['val']
            if Devices[device].has_key('connections'): 
                print "RENDERAV: Iterating device outputs for terminated output"
                for connection in Devices[device]['connections']:
                    print "RENDERAV: Output : %s" %connection
                    if connection.has_key("sources"):
                        for source in connection['sources']: 
                            #we look for terminated sources as they are a head of the connection trees
                            if source.has_key('status'):
                                if  source['status']['val'] == "terminated":
                                    print "RENDERAV: Found terminated source : %s" %source['name']['val']
                                    buttons = MakeButtons(connection , Devices[device],Devices , Location)
                                    #we get a none button if we failed to find any method to switch to that sink
                                    for button in buttons:
                                        print "Inserting button into template :%s" %button
                                        AV_Template.insert (start+1 , button + '\n' )
                                        messages.append("Added button : %s" %button)
    return AV_Template , messages
    

LOCAL_SINK_TEMPLATE = "/opt/webbrick/site/templates/armour/templates/local_template.kid"
EXTERITYWEB_SINK_TEMPLATE = "/opt/webbrick/site/templates/armour/templates/exterityweb_template.kid"
MYRYADCD_TEMPLATE = "/opt/webbrick/site/templates/armour/templates/myryadcd_template.kid"
NADTUNER_TEMPLATE = "/opt/webbrick/site/templates/armour/templates/local_template.kid"
NADDVD_TEMPLATE = "/opt/webbrick/site/templates/armour/templates/naddvd_template.kid"
SKY_TEMPLATE = "/opt/webbrick/site/templates/armour/templates/sky_template.kid"
SKY_PRESETS_TEMPLATE = "/opt/webbrick/site/templates/armour/templates/sky_presets_template.kid"
UPNP_TEMPLATE = "/opt/webbrick/site/templates/armour/templates/upnp_template.kid"
VLC_TEMPLATE = "/opt/webbrick/site/templates/armour/templates/vlc_template.kid"

LOCAL_SINK_TEMPLATE_IPOD = "/opt/webbrick/site/templates/armour_itouch/templates/local_template.kid"
EXTERITYWEB_SINK_TEMPLATE_IPOD = "/opt/webbrick/site/templates/armour_itouch/templates/exterityweb_template.kid"
MYRYADCD_TEMPLATE_IPOD = "/opt/webbrick/site/templates/armour_itouch/templates/myryadcd_template.kid"
NADTUNER_TEMPLATE_IPOD = "/opt/webbrick/site/templates/armour_itouch/templates/local_template.kid"
NADDVD_TEMPLATE_IPOD = "/opt/webbrick/site/templates/armour_itouch/templates/naddvd_template.kid"
SKY_TEMPLATE_IPOD = "/opt/webbrick/site/templates/armour_itouch/templates/sky_template.kid"
SKY_PRESETS_TEMPLATE_IPOD = "/opt/webbrick/site/templates/armour_itouch/templates/sky_presets_template.kid"
UPNP_TEMPLATE_IPOD = "/opt/webbrick/site/templates/armour_itouch/templates/upnp_template.kid"
VLC_TEMPLATE_IPOD = "/opt/webbrick/site/templates/armour_itouch/templates/vlc_template.kid"

def MakeLocalSinkPage(Location):
    localfile = open(LOCAL_SINK_TEMPLATE)
    localpage = localfile.readlines()
    localpage = StringListSub( {"location":Location}, localpage  )
    output = open(SITE_DIRECTORY + "armour/" + "%s_local.kid" %Location, 'w')
    output.writelines(localpage)
    
    localfile = open(LOCAL_SINK_TEMPLATE_IPOD)
    localpage = localfile.readlines()
    localpage = StringListSub( {"location":Location}, localpage  )
    output = open(SITE_DIRECTORY + "armour_itouch/" + "%s_local.kid" %Location, 'w')
    output.writelines(localpage)
   

def MakeVLCSinkPage(Location , Device):
    localfile = open(VLC_TEMPLATE)
    localpage = localfile.readlines()
    localpage = StringListSub( {"location":Location  , "ip" : Device["ip"]["val"] }, localpage  )
    output = open(SITE_DIRECTORY + "armour/" + "%s_%s_vlc.kid" %(Device["name"]["val"] , Location), 'w')
    output.writelines(localpage)
    
    localfile = open(VLC_TEMPLATE_IPOD)
    localpage = localfile.readlines()
    localpage = StringListSub( {"location":Location  , "ip" : Device["ip"]["val"] }, localpage  )
    output = open(SITE_DIRECTORY + "armour_itouch/" + "%s_%s_vlc.kid" %(Device["name"]["val"] , Location), 'w')
    output.writelines(localpage)
    
def MakeExterityWebSinkPage(Location):
    localfile = open(EXTERITYWEB_SINK_TEMPLATE)
    localpage = localfile.readlines()
    localpage = StringListSub( {"location":Location}, localpage  )
    output = open(SITE_DIRECTORY + "armour/" + "%s_exterityweb.kid" %Location, 'w')
    output.writelines(localpage)
    
    localfile = open(EXTERITYWEB_SINK_TEMPLATE_IPOD)
    localpage = localfile.readlines()
    localpage = StringListSub( {"location":Location}, localpage  )
    output = open(SITE_DIRECTORY + "armour_itouch/" + "%s_exterityweb.kid" %Location, 'w')
    output.writelines(localpage)
    
    
def MakeSkySinkPage(Location , Device):
    
    if Device.has_key("txid") and Device.has_key("rxid"):
        localfile = open(SKY_TEMPLATE)
        localpage = localfile.readlines()
        print "Device has txid and rx id , loading template %s" %Device
        localpage = StringListSub( {"location":Location , "txid" : Device["txid"]['val'] , "rxid" : Device["rxid"]['val']} , localpage  )
        output = open(SITE_DIRECTORY + "armour/" + "%s_sky.kid" %Location, 'w')
        output.writelines(localpage)
        
        
        localfile = open(SKY_PRESETS_TEMPLATE)
        localpage = localfile.readlines()
        print "Device has txid and rx id , loading template %s" %Device
        localpage = StringListSub( {"location":Location , "txid" : Device["txid"]['val'] , "rxid" : Device["rxid"]['val']} , localpage  )
        output = open(SITE_DIRECTORY + "armour/%s_sky_presets.kid" %Location, 'w')
        output.writelines(localpage)  
        
        localfile = open(SKY_TEMPLATE_IPOD)
        localpage = localfile.readlines()
        print "Device has txid and rx id , loading template %s" %Device
        localpage = StringListSub( {"location":Location , "txid" : Device["txid"]['val'] , "rxid" : Device["rxid"]['val']} , localpage  )
        output = open(SITE_DIRECTORY + "armour_itouch/" + "%s_sky.kid" %Location, 'w')
        output.writelines(localpage)
        
        
        localfile = open(SKY_PRESETS_TEMPLATE_IPOD)
        localpage = localfile.readlines()
        print "Device has txid and rx id , loading template %s" %Device
        localpage = StringListSub( {"location":Location , "txid" : Device["txid"]['val'] , "rxid" : Device["rxid"]['val']} , localpage  )
        output = open(SITE_DIRECTORY + "armour_itouch/%s_sky_presets.kid" %Location, 'w')
        output.writelines(localpage) 

def MakeNADTunerSinkPage(Location , Device):
    
    if Device.has_key("id") :
        localfile = open(NADTUNER_TEMPLATE)
        localpage = localfile.readlines()
        print "Device has id , rendering NADTuner page for device on ip %s" %Device["ip"]["val"]
        localpage = StringListSub( {"location":Location , "id" : Device["id"]['val'] , } , localpage  )
        output = open(SITE_DIRECTORY + "armour/" + "%s_nadtuner.kid" %Location, 'w')
        output.writelines(localpage)
        
        localfile = open(NADTUNER_TEMPLATE_IPOD)
        localpage = localfile.readlines()
        print "Device has id , rendering NADTuner page for device on ip %s" %Device["ip"]["val"]
        localpage = StringListSub( {"location":Location , "id" : Device["id"]['val'] , } , localpage  )
        output = open(SITE_DIRECTORY + "armour_itouch/" + "%s_nadtuner.kid" %Location, 'w')
        output.writelines(localpage)

def MakeNADDVDSinkPage(Location , Device):
    
    if Device.has_key("id") :
        localfile = open(NADDVD_TEMPLATE)
        localpage = localfile.readlines()
        print "Device has id , rendering NADDVD page for device on with id %s" %Device["id"]["val"]
        localpage = StringListSub( {"location":Location , "id" : Device["id"]['val'] , } , localpage  )
        output = open(SITE_DIRECTORY + "armour/" + "%s_naddvd.kid" %Location, 'w')
        output.writelines(localpage)
        
        localfile = open(NADDVD_TEMPLATE_IPOD)
        localpage = localfile.readlines()
        print "Device has id , rendering NADDVD page for device on with id %s" %Device["id"]["val"]
        localpage = StringListSub( {"location":Location , "id" : Device["id"]['val'] , } , localpage  )
        output = open(SITE_DIRECTORY + "armour_itouch/" + "%s_naddvd.kid" %Location, 'w')
        output.writelines(localpage)
        
        
def MakeMyryadCDSinkPage(Location , Device):
    
    if Device.has_key("ip"):
        localfile = open(MYRYADCD_TEMPLATE)
        localpage = localfile.readlines()
        print "RENDERAV: Rendering Myryad CD page for device on IP %s" %Device["ip"]
        localpage = StringListSub( {"location":Location , "ip" : Device["ip"]['val'] }, localpage  )
        output = open(SITE_DIRECTORY + "armour/" + "%s_myryadcd.kid" %Location, 'w')
        output.writelines(localpage)
        
        localfile = open(MYRYADCD_TEMPLATE_IPOD)
        localpage = localfile.readlines()
        print "RENDERAV: Rendering Myryad CD page for device on IP %s" %Device["ip"]
        localpage = StringListSub( {"location":Location , "ip" : Device["ip"]['val'] }, localpage  )
        output = open(SITE_DIRECTORY + "armour_itouch/" + "%s_myryadcd.kid" %Location, 'w')
        output.writelines(localpage)
        
def MakeUpnpSinkPage(Location , Device , Sink):
    
    if Device.has_key("ip"):
        localfile = open(UPNP_TEMPLATE)
        localpage = localfile.readlines()
        print "RENDERAV: Rendering UPNP Renderer page for device on UDN %s" %Device["udn"]
        localpage = StringListSub( {"location":Location , "udn" : Sink["udn"]['val'] }, localpage  )
        output = open(SITE_DIRECTORY + "armour/" + "%s_%s_upnp.kid" %(Device["id"]["val"] , Location),  'w')
        output.writelines(localpage)
        
        localfile = open(UPNP_TEMPLATE_IPOD)
        localpage = localfile.readlines()
        print "RENDERAV: Rendering UPNP Renderer page for device on UDN %s" %Device["udn"]
        localpage = StringListSub( {"location":Location , "udn" : Sink["udn"]['val'] }, localpage  )
        output = open(SITE_DIRECTORY + "armour_itouch/" + "%s_%s_upnp.kid" %(Device["id"]["val"] , Location),  'w')
        output.writelines(localpage)

  
def RenderButton(Sink , MacroId , Depth , Location , Device):
    #This creates the button based on the device description, and determines what the click through page  should be and builds the click through page
    button = ''
    MacroId = MacroId.replace(' ' , '_')
    print "RENDERAV: Rendering button,  compressed Id is %s , Depth is %s , Sinktype is : %s" %(MacroId,Depth,Sink)
    #Determine button events
    startType = "%s/Macro/Begin" %MacroId
    startSource = "%s/Begin/Stage/1" %MacroId
    endType = "%s/Macro" %MacroId
    endSource = "%s/Begin/Stage%i" %(MacroId , Depth)
    button = ''

    #Determine correct click through page
    clickthrough = ''
    if Sink['ui']['val'] == "Local":
        button = """<wb:simpleButtonAndLink wbTarget = "/sendevent/%s/Begin/Stage/0?type=%s/Macro/Begin" \n wbPageLink="/template/%s_local" baseClassName="local">%s</wb:simpleButtonAndLink>""" %(MacroId,MacroId,Location, Sink["name"]["val"])
        MakeLocalSinkPage(Location)
    
    elif Sink['ui']['val'] == "ExterityWeb":
        button = """<wb:simpleButtonAndLink wbTarget = "/sendevent/%s/Begin/Stage/0?type=%s/Macro/Begin" \n wbPageLink="/template/%s_exterityweb" baseClassName="www">%s</wb:simpleButtonAndLink>""" %(MacroId,MacroId,Location, Sink["name"]["val"])
        MakeExterityWebSinkPage(Location)    
        
    elif Sink['ui']['val'] == "Skybox":   
        #TODO Change to Sky baseclass
        #TODO Sky is two pages , do both    
        button = """<wb:simpleButtonAndLink wbTarget = "/sendevent/%s/Begin/Stage/0?type=%s/Macro/Begin" \n wbPageLink="/template/%s_sky" baseClassName="satellite">%s</wb:simpleButtonAndLink>""" %(MacroId,MacroId,Location , Sink["name"]["val"])
        MakeSkySinkPage(Location , Device)
        
    elif Sink['ui']['val'] == "VLC":   
        #TODO Change to Sky baseclass
        #TODO Sky is two pages , do both    
        button = """<wb:simpleButtonAndLink wbTarget = "/sendevent/%s/Begin/Stage/0?type=%s/Macro/Begin" \n wbPageLink="/template/%s_%s_vlc" baseClassName="pc">%s</wb:simpleButtonAndLink>""" %(MacroId,MacroId, Device["name"]["val"] , Location , Sink["name"]["val"])
        MakeVLCSinkPage(Location , Device)
        
    elif Sink['ui']['val'] == "NADTuner":
        #TODO Change to Tuner baseclass
        button = """<wb:simpleButtonAndLink wbTarget = "/sendevent/%s/Begin/Stage/0?type=%s/Macro/Begin" \n wbPageLink="/template/%s_nadtuner" baseClassName="tuner">%s</wb:simpleButtonAndLink>""" %(MacroId,MacroId,Location , Sink["name"]["val"])
        MakeNADTunerSinkPage(Location , Device)

    elif Sink['ui']['val'] == "NADDVD":
        #TODO Change to DVD baseclass
        button = """<wb:simpleButtonAndLink wbTarget = "/sendevent/%s/Begin/Stage/0?type=%s/Macro/Begin" \n wbPageLink="/template/%s_naddvd" baseClassName="dvd">%s</wb:simpleButtonAndLink>""" %(MacroId,MacroId,Location , Sink["name"]["val"])
        MakeNADDVDSinkPage(Location , Device)

    elif Sink['ui']['val'] == "MyryadCD":
        #TODO CD Baseclass
        button = """<wb:simpleButtonAndLink wbTarget = "/sendevent/%s/Begin/Stage/0?type=%s/Macro/Begin" \n wbPageLink="/template/%s_myryadcd" baseClassName="cd">%s</wb:simpleButtonAndLink>""" %(MacroId,MacroId,Location , Sink["name"]["val"])
        MakeMyryadCDSinkPage(Location , Device)

    elif Sink['ui']['val'] == "UPnPRenderer":    
        #TODO CD Baseclass
        button = """<wb:simpleButtonAndLink wbTarget = "/sendevent/%s/Begin/Stage/0?type=%s/Macro/Begin" \n wbPageLink="/template/%s_%s_upnp" baseClassName="upnp">%s</wb:simpleButtonAndLink>""" %(MacroId,MacroId,Device['id']['val'], Location , Sink["name"]["val"])
        MakeUpnpSinkPage(Location , Device , Sink)

    print "Rendered button is %s" %button
    return button
    
def GetCompatibleSources(Type, Focus , Devices):
    result = []
    print "RENDERAV: Finding sinks compatible with : %s , %s" %(Type , Focus)
    for device in Devices:
        if Devices[device].has_key("connections"):
            for connection in Devices[device]["connections"]:
                if connection.has_key("sources"):
                    for s in connection['sources']:
                        if s["focus"]["val"] == Focus and s["type"]["val"] == Type:
                            result.append( { 'deviceId' : device , 'source' : s , 'connection' : connection} )
    return result
                
def MakeButtonsRecur(Connection , Buttons, Device , OtherDevices , ParentIds , Depth , Location):
    print "RENDERAV: Iterating device sinks %s" %Device['id']['val']
    if 'sinks' in Connection:
        for sink in Connection['sinks']:
            #print "RENDERAV: Current sink is %s" %connection['sink']
            if sink['focus']['val'] == 'global':
                #if a sink is of a global focus , we assume it is connected to every source of the same type and focus
                print "RENDERAV: Found global sink"
                sources = GetCompatibleSources(sink['type']['val'],'global',OtherDevices)
                for source in sources:
                    print "RENDERAV: Found source compatible with global sink : %s" %source
                    Buttons = MakeButtonsRecur(source['connection'] , Buttons , OtherDevices[source['deviceId']] , OtherDevices , ParentIds + Device['name']['val'] + sink['name']['val'] ,  Depth + 1 , Location)
                    
            elif sink['status']['val'] == 'connected':
                #chase down tree
                print "RENDERAV: Found connected sinks , connected device is : %s , checking connected device" %OtherDevices[sink['connectedto']['val'][0:3]]['name']['val']
                print "RENDERAV: Current Ids is %s" %(ParentIds + ':' + sink['id']['val'])
                #get the connection
                connectedDevice = OtherDevices[sink['connectedto']['val'][0:3]]
                connected_Device_Connection = ''
                if 'connections' in connectedDevice:
                    print "RENDERAV: Looking for the connection grouping on the connected device %s" %connectedDevice["connections"]
                    for c in connectedDevice['connections']:
                        if 'sources' in c:
                            for s in c['sources']:
                                if s['id']['val'] == sink['connectedto']['val']:
                                    connected_Device_Connection = c        
                Buttons = MakeButtonsRecur(connected_Device_Connection , Buttons , OtherDevices[sink['connectedto']['val'][0:3]] , OtherDevices , ParentIds + Device['name']['val'] + sink['name']['val'] ,  Depth + 1 , Location) 
            elif sink['status']['val'] == 'terminated':
                #render button for it 
                print "RENDERAV: Found terminated sink , rendering button/menu"
                newButton = RenderButton(sink , ParentIds + sink['name']['val'] , Depth + 1 , Location , Device)
                Buttons.append(newButton)
            else:
                #unconnected or invalid state, ignore it
                print "RENDERAV: unconnected sink is %s" %sink['name']
    print "RENDERAV: Finished iterating device sinks %s" %Device['id']['val']         
    return Buttons            
    
                               
def MakeButtons(Connection , Device , OtherDevices , Location):
    buttons = []
    buttons = MakeButtonsRecur(Connection , buttons , Device , OtherDevices , '' , 0 , Location)          
    print "Rendered buttons are %s" %buttons  
    return buttons              
    
    
    
    
def RenderLighting(Lighting_Template , Exterity_Template , Exterity_Lighting_js , Location , Devices):
            
                
    lighting = "<lighting>"      # enough to let us know.
    elighting = "</lighting>"      # enough to let us know.
    start = 0
    end = 0
    for line in Lighting_Template:
        if (line.find(lighting) >= 0):
            start = Lighting_Template.index(line)
        if (line.find(elighting) >= 0):
            end = Lighting_Template.index(line)

    del Lighting_Template[start+1:end] # remove anything that is already there
    
    exteritylightStartString = "<span>Lighting Control</span>"      # enough to let us know.
    exterityLightStart = 0
    
    for line in Exterity_Template:
        if (line.find(exteritylightStartString) >= 0):
            exterityLightLine = Exterity_Template.index(line)
            exterityLightIndex = line.find(exteritylightStartString) + 29 
            
    # At this point, lines is clean and new elements can be added
    for device in Devices:
        if Devices[device]["type"]["val"] == "Lutron" or Devices[device]["type"]["val"] == "WebBrick":
            if Devices[device]["keypads"] != {}:
                for keypad in Devices[device]['keypads']:
                    if keypad['location']['val'] == Location:
                        
                        deviceid = Devices[device]['id']['val']
                        processor = keypad['processor']['val']
                        link = keypad['link']['val']
                        keypadid  = keypad['number']['val']
                        if Devices[device]["type"]["val"] == "Lutron":    
                            for button in keypad['buttons']:
                                
                                #generate UI button
                                newLight = Element("wb:simpleButton")
                                buttonid  = button['number']['val']
                                newLight.attrib["wbTarget"] = "/sendevent/serial/send/action?type=serial/action&cmd=send&id=%s&action=togglelight&processor=%s&link=%s&keypad=%s&light=%s" %(deviceid,processor,link,keypadid,buttonid)
                                newLight.attrib["wbSource"] = "/eventstate/Lutron/Device/Id/%s/Processor_%s/Link_%s/Keypad_%s/Light_%s?attr=val" %( deviceid , keypad['processor']['val'] , keypad['link']['val'] , keypad['number']['val'], button['number']['val'])
                                newLight.attrib["baseClassName"] = button['icon']['val']                                
                                if button['icon']['val'] == "light":
                                    newLight.attrib["stateVals"] = "Off,On,Fast,Slow" 
                                newLight.text = "Light %s" %(button['number']['val'])        
                                Lighting_Template.insert(start+1,tostring(newLight)+"\n")
                                
                                #generate Exterity UI button
                                params =  {"button_function" : "bfunct" + deviceid + processor + link + keypadid + buttonid, "button_name" : "Light " + button["number"]["val"] , "id" : deviceid , "processor" : processor , "link" : link , "keypad" : keypadid , "button" : button["number"]["val"] }
                                functionString = """function %(button_function)s() \n{\n\t sendEvent("/sendevent/serial/send/action?type=serial/action&cmd=send&id=%(id)s&action=togglelight&processor=%(processor)s&link=%(link)s&keypad=%(keypad)s&light=%(button)s" ); \n}""" %params
                                buttonString = """<span class="clickable" onClick="%(button_function)s()">%(button_name)s</span>""" %params
                                Exterity_Template[exterityLightLine] = Exterity_Template[exterityLightLine][:exterityLightIndex] + buttonString + Exterity_Template[exterityLightLine][exterityLightIndex:]                               
                                Exterity_Lighting_js.append(functionString)
                                
                        elif Devices[device]["type"]["val"] == "WebBrick":
                            for button in keypad['buttons']:
                                newLight = Element("wb:simpleButton")
                                buttonid  = button['number']['val']
                                if "Scene" in buttonid:
                                    #render UI button
                                    scene = buttonid[6:]
                                    newLight.attrib["wbTarget"] = "/sendevent/select/scene?type=armour/webbrick/lighting&scene=%s&webbrick=%s" %(scene,Devices[device]['ip']['val'])    
                                                                    
                                    if int(scene) <= 7:
                                        newLight.attrib["wbSource"] = "/eventstate/scene/bank/lower/states?attr=scene%s" %scene
                                    else:
                                        newLight.attrib["wbSource"] =  "/eventstate/scene/bank/upper/states?attr=scene%s" %scene  
                                        
                                    newLight.attrib["baseClassName"] = button['icon']['val']
                                    if button['icon']['val'] == "light":
                                        newLight.attrib["stateVals"] = "Off,On,Fast,Slow"
                                    newLight.text = "Light %s" %(button['number']['val'])        
                                    Lighting_Template.insert(start+1,tostring(newLight)+"\n")    
                                    #render Exterity button
                                    params =  {"button_function" : "bfunct" + deviceid + processor + link + keypadid + "S" + scene, "button_name" : "Scene " + scene , "webbrick" : Devices[device]['ip']['val'] , "scene" : scene}
                                    functionString = """function %(button_function)s() \n{\n\t sendEvent("/sendevent/select/scene?type=armour/webbrick/lighting&scene=%(scene)s&webbrick=%(webbrick)s" ); \n}""" %params
                                    buttonString = """<span class="clickable" onClick="%(button_function)s()">%(button_name)s</span>""" %params
                                    Exterity_Template[exterityLightLine] = Exterity_Template[exterityLightLine][:exterityLightIndex] + buttonString + Exterity_Template[exterityLightLine][exterityLightIndex:]                              
                                    Exterity_Lighting_js.append(functionString)
                                    
                                if "Digital Out" in buttonid:
                                    #render UI button
                                    digitalout = buttonid[12:]
                                    newLight.attrib["wbTarget"] = "/sendevent/toggle/digital/out?type=armour/webbrick/lighting&output=%s&webbrick=%s" %(digitalout,Devices[device]['ip']['val'])
                                    newLight.attrib["wbSource"] = "/eventstate/webbrick/%s/DO/%s?attr=state" %(Devices[device]['number']['val'] , digitalout) 
                                    newLight.attrib["baseClassName"] = button['icon']['val']
                                    if button['icon']['val'] == "light":
                                        newLight.attrib["stateVals"] = "Off,On,Fast,Slow"
                                    newLight.text = "Light %s" %(button['number']['val'])        
                                    Lighting_Template.insert(start+1,tostring(newLight)+"\n")    
                                    #render Exterity button
                                    params =  {"button_function" : "bfunct" + deviceid + processor + link + keypadid + "D" + digitalout, "button_name" : "Digital Out " + digitalout , "webbrick" : Devices[device]['ip']['val'] , "digitalout" : digitalout}
                                    functionString = """function %(button_function)s() \n{\n\t sendEvent("/sendevent/toggle/digital/out?type=armour/webbrick/lighting&output=%(digitalout)s&webbrick=%(webbrick)s" ); \n}""" %params
                                    buttonString = """<span class="clickable" onClick="%(button_function)s()">%(button_name)s</span>""" %params
                                    Exterity_Template[exterityLightLine] = Exterity_Template[exterityLightLine][:exterityLightIndex] + buttonString + Exterity_Template[exterityLightLine][exterityLightIndex:]                             
                                    Exterity_Lighting_js.append(functionString)
                                    
    return Lighting_Template , Exterity_Template, Exterity_Lighting_js,  "Build messages "        
        
def RenderHomePage(Homepage_Template, Location, Something):
    return Homepage_Template , Location
