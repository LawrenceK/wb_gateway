<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
from WebBrickGateway.templates.graphutil import getvals, getTimes

#
#  This is the local version of graph.prop
#
graphbase = "".join(file("static/css/graph.prop").readlines())

?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

<script src="/static/javascript/graphs/swfobject.js" type="text/javascript"></script>
<script src="/static/javascript/graphs/json2.js" type="text/javascript"></script>
<script src="/static/javascript/graphs/graphs.js" type="text/javascript"></script>
	
	
${output_head("Temperature Graphs")}

<?python
from xml.etree.ElementTree import ElementTree
from urllib2 import urlopen
uri = "http://localhost:8080/template/gatherData"
xmldata = ElementTree(file=urlopen(uri))
?>

<body>

${output_nav("Temperatures")}


<script type="text/javascript">

swfobject.embedSWF("/static/flash/open-flash-chart.swf", "my_chart", "1000", "800", "9.0.0");

var chartData = ${graphbase} ;

gTitle("Temperatures") ;
gLabels(${getTimes(xmldata,'time')}) ;

gValues("0",${getvals(xmldata,'outside')}) ;
gName("0","Outside");

gValues("1",${getvals(xmldata,'kitchen_air')}) ;
gName("1","Kitchen");

gValues("2",${getvals(xmldata,'hot_water')}) ;
gName("2","Hot Water");

gValues("3",${getvals(xmldata,'master_bed')}) ;
gName("3","Master Bed");

</script>

<br />
<center>
	<div class="objCenter" id="my_chart"></div>
</center>

${output_site_info_bar()}

</body>
</html>



