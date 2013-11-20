<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python
from turbogears import config as tgconfig
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

def getPressure():
    pressure = getCurrentValue( "/eventstate/pressure/current" )
    if pressure == '':
        return None
    else:
        return pressure

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
            zoneCount = 0
        else:
            zoneCount = int(zoneLimit)
            zoneLimit = int(zoneLimit) + 1
            

    ?>
<a href='#' onClick="window.location.reload()">Reload</a>
<a href='/template/diag'>Diagnostics Home</a>
<a href='/'>Interface Home</a>

<h2>Zone Diagnostics</h2>

<div py:if='getPressure()'>
<p>Current System Pressure is ${getPressure()} bar</p>
</div>

<h3> Found ${zoneCount} zones </h3>
<p>
zones may not be visible for upto 2 minutes after start-up
</p>
<table>
  <colgroup span="10" width="9%"></colgroup>
    <tr>
    <th>Name</th>
    <th>status</th>
    <th>cmd source</th>
    <th>target</th>
    <th>zone temp</th>
    <th>min temp</th>
    <th>enabled</th>
    <th>occupied</th>
    <th>follow occupancy</th>
    <th>weather</th>
    </tr>
    <tr py:for='zoneNr in range(1,zoneLimit,1)' onClick='window.location=&apos;/template/templates/zoneControl${zoneNr}&apos;' >
    <div py:if='1'>
    <td> ${getCurrentValue('/eventstate/zone%s/name?attr=name' % zoneNr)}
    </td>
    <td> ${getCurrentValue('/eventstate/zone%s/state?attr=status' % zoneNr)} 
    </td>
    <td> ${getCurrentValue('/eventstate/zone%s/state?attr=cmdsource' % zoneNr)}
    </td>
    <td> ${getCurrentValue('/eventstate/zone%s/state?attr=targetsetpoint' % zoneNr)}  &ordm;C
    </td>
    <td> 
    <span py:if="getCurrentValue('/eventstate/zone%s/state?attr=zoneTemp' % zoneNr)" py:strip="True" > ${getCurrentValue('/eventstate/zone%s/state?attr=zoneTemp' % zoneNr)}&ordm;C </span>
    </td>
    <td> ${getCurrentValue('/eventstate/zone%s/state?attr=minzonetemp' % zoneNr)}  &ordm;C
    </td>
    <td> ${getCurrentValue('/eventstate/zone%s/state?attr=enabled' % zoneNr)}  
    </td>
    <td> ${getCurrentValue('/eventstate/zone%s/state?attr=occupied' % zoneNr)}
    </td>
    <td> ${getCurrentValue('/eventstate/zone%s/state?attr=followoccupancy' % zoneNr)}
    </td>
    <td> 
        <span py:if="getCurrentValue('/eventstate/zone%s/state?attr=weathercompensation' % zoneNr) == '1'" py:strip="True" > Run </span>
        <span py:if="getCurrentValue('/eventstate/zone%s/state?attr=weathercompensation' % zoneNr) == '0'" py:strip="True" > Hold </span>
    </td>
    </div>
    </tr>
</table>

</body>

</html>
