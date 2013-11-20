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

def getZGLimit():
    zoneGroupLimit = getCurrentValue( "/eventstate/zonegroup/count" )
    if zoneGroupLimit == '':
        zoneGroupLimit = 0
    else:
        zoneGroupLimit = int(zoneGroupLimit) + 1
    return zoneGroupLimit

def getEVLogs():
    import os, fnmatch
    fnlist = []
    for fn in os.listdir("/var/log/webbrick/"):
        if fnmatch.fnmatchcase(fn,"EventLog.*.*"):
            fnlist.append(fn)
    return fnlist


    
def zoneEvLog(searchSpec):
    fnlist = getEVLogs()
    fnlist.append("EventLog.log")
    payload=""
    for fn in fnlist:
        inFn = file("/var/log/webbrick/"+fn)
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
    
<h1>ZoneGroup Events</h1>

<p>These events are taken from all the available current logs (i.e. before the logs get stored in the history folder)</p>

<h2>Zones</h2>

    <div py:for='zg in range(1,getZGLimit(),1)'>
        <span py:if='1'>
            <h3>Events for ZoneGroup${zg}</h3>
            ${XML(zoneEvLog("zonegroup/%s/[rs]" % (zg)))} <!-- lists start at 0 zonegroups at 1 -->
        </span>
    </div>


</body>
</html>
