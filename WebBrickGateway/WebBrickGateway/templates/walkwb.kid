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

<h3>WebBrick Nodes</h3>
<table>
	<colgroup span="3" width="5%"/>
	<colgroup span="2" width="15%"/>
	<colgroup span="4" width="5%"/>
    <th>Node</th>
    <th>Name</th>
    <th>Status</th>
    <th>Time</th>
    <th>Last Event Seen</th>
    <th>CT/0</th>
    <th>CT/1</th>
    <th>CT/2</th>
    <th>CT/3</th>
    <th>CT/4</th>
	<tr py:for="wb in webbricks">
        <td py:content="wb['node']"/>
        <td py:content="wb['name']"/>
	<td py:if="wb['status']">
	No UDP
	</td>
	<td py:if="not wb['status']">
	Ok
	</td>
        <td py:content="wb['time']"/>
        <td py:content="wb['event']"/>
	<td py:for="j in ctRange">
		<span py:if="getCurrentValue(buildTemp(wb['node'],j))" py:strip="True" >${getCurrentValue(buildTemp(wb['node'],j))}&ordm;C </span>
	</td>
	</tr>
</table>



</body>
</html>