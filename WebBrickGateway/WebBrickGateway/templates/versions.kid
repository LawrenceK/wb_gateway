<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<?python 
from turbogears import config as tgconfig
serverHost = "127.0.0.1:%s"%(tgconfig.get("server.socket_port", "8080", False, "global" ))

wbRange = range(20,46)
ctRange = range(0,4)

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

def buildTemp(wbnum,ctnum):
	"""
	Build a temperature URI
	"""
	return "/wbsts/%d/CT/%d" % (wbnum,ctnum)
    
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:ui="ui" >
	  
<head>
	<link href="/static/css/diag.css" type="text/css" rel="stylesheet" />
 </head>
<body>

<a href='#' onClick="window.location.reload()">Reload</a>
<a href='/template/diag'>Diagnostics Home</a>
<a href='/'>Interface Home</a>

<h3>Gateway Versions</h3>
<table>
	<colgroup span="2" width="50%"/>
    <th>Egg</th>
    <th>Version</th>
    <tr>
        <td>WebBrickLibs</td>
        <td>${getCurrentValue("/eventstate/WebBrickLibs?attr=build")}</td>
    </tr>
    <tr>
        <td>WebBrickGateway</td>
        <td>${getCurrentValue("/eventstate/WebBrickGateway?attr=build")}</td>
    </tr>
    <tr>
        <td>WebBrickRes</td>
        <td>${getCurrentValue("/eventstate/WebBrickRes?attr=build")}</td>
    </tr>
    <tr>
        <td>WebBrickConfig</td>
        <td>${getCurrentValue("/eventstate/WebBrickConfig?attr=build")}</td>
    </tr>
    <tr>
        <td>WebBrickDocs</td>
        <td>${getCurrentValue("/eventstate/WebBrickDoc?attr=build")}</td>
    </tr>
</table>

</body>
</html>