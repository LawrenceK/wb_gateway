<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python
from turbogears import config as tgconfig
import re
serverHost = "127.0.0.1:%s"%(tgconfig.get("server.socket_port", "8080", False, "global" ))
zoneLimit = 0

def getCurrentValue( uri ):
    """
    attempt to retrieve the current value of the uri passed
    """
    try:
        from WebBrickLibs.WbAccess import GetHTTPXmlDom
        from MiscLib.DomHelpers import getNamedNodeText
        dom = GetHTTPXmlDom( serverHost, uri )    # need to know self address
        if dom:
            return getNamedNodeText(dom, 'val')
    except:
        from logging import getLogger
        getLogger( "WebBrickGateway.templates.widgets" ).exception( "getCurrentValue %s " % (uri) )
    return '' 

    
def zoneEvLog(searchSpec):
    payload=""
    fname = "/var/log/webbrick/EventLog.log"
    inFn = file(fname)
    for line in inFn:
        if re.search(searchSpec,line):
            payload = payload + "<br/>" + line
    return payload

?>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:ui="ui" >
	  
<head>
	<link href="/static/css/diag.css" type="text/css" rel="stylesheet" />
 </head>
<body>

    <?python 
        zoneLimit = getCurrentValue( "/eventstate/zone/count" )
        if zoneLimit == '':
            zoneLimit = 0
        else:
            zoneCount = int(zoneLimit)
            zoneLimit = int(zoneLimit) + 1
        
        zoneGrps = list()
        for z in range(1,zoneLimit):
            zoneGrps.append(getCurrentValue("/eventstate/zone%s/groupnumber" % z))
            
        hsLimit = getCurrentValue( "/eventstate/heatsource/count" )
        if hsLimit == '':
            hsLimit = 0
        else:
            hsCount = int(hsLimit)
            hsLimit = int(hsLimit) + 1


    ?>

<a href='#' onClick="window.location.reload()">Reload</a>
<a href='/template/diag'>Diagnostics Home</a>
<a href='/'>Interface Home</a>
    
<h1>Zone Events</h1>

<p>These events are taken from the current event log and sorted by <b>zones</b> and their associated <b>zonegroups</b></p>
<p><b>heatsources</b> are at the end of the list</p>

<!--
<h2>Lighting</h2>

    ${XML(zoneEvLog("[L,l]ighting|[I,i]nternal"))}
-->

<h2>Zones</h2>

    <div py:for='zoneNr in range(1,zoneLimit,1)'>
        <span py:if='1'>
            <h3>Events for ${getCurrentValue("/eventstate/zone%s/name?attr=name" % zoneNr)} (zone${zoneNr}) and zonegroup ${zoneGrps[zoneNr-1]}</h3>
            ${XML(zoneEvLog("zone%s/run|zone%s/stop|zonegroup/%s/" % (zoneNr,zoneNr,zoneGrps[zoneNr-1])))} <!-- lists start at 0 zones at 1 -->
        </span>
    </div>

<h2>HeatSources</h2>

    <div py:for='hsNr in range(1,hsLimit,1)' >
        <span py:if='1'>
            <h3>Events for ${getCurrentValue("/eventstate/heatsource/%s/availability?attr=name" % hsNr)} - (Heatsource${hsNr})</h3>
            ${XML(zoneEvLog("heatsource/%s/requestrun|heatsource/%s/requeststop" % (hsNr,hsNr)))}
        </span>
    </div>
    

</body>
</html>