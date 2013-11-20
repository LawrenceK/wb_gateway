<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_tabbed

layout_params['selected_tab'] = 3


def setPref(st,ps,name,ds):
    if int(st) == ps:
        if name in ds:
            return ds.index(name)
    else:
        return st
        
?>
<html xmlns="http://www.w3.org/1999/xhtml" 
    xmlns:py="http://purl.org/kid/ns#" 
    xmlns:wb="http://id.webbrick.co.uk/"
    py:layout="sitelayout.kid" 
    py:extends="WebBrickGateway.templates.widgets_tabbed" 
    >


<div py:match="item.tag == '{http://id.webbrick.co.uk/}tabcontent'" id="tabcontent">

<?python
from urllib2 import urlopen

optlist = file=urlopen("http://localhost:8080/jsonfiles/runtime_xml")
visibleSets = [0,1]   


if not 'set0' in locals(): set0 = 0
if not 'set1' in locals(): set1 = 1
if not 'gdate' in locals(): gdate = "Today"

if (not gdate) or (gdate=="Today"):
    graphbase = urlopen("http://localhost:8080/jsondata/runtime_xml.log/rgraph.xml")
    temp1 = urlopen("http://localhost:8080/jsondata/runtime_xml.log/rgraph.xml")
else:
    graphbase = urlopen(("http://localhost:8080/jsondata/runtime_xml.log.%s/rgraph.xml" % (gdate)))
    temp1 = urlopen(("http://localhost:8080/jsondata/runtime_xml.log.%s/rgraph.xml" % (gdate)))

temp2 = eval("".join(temp1.readlines()))
datasetNames = []

for dataset in temp2["datasets"]:
   datasetNames.append(dataset["text"])
   
set0 = setPref(set0,0,"boiler",datasetNames)
set1 = setPref(set1,1,"ashp-heating",datasetNames)

visibleSets[0] = int(set0)    
visibleSets[1] = int(set1)

?>


<script type="text/javascript">
   var chartData = ${graphbase} ;
</script>    

<div>
    <center id="dropdowns">
        <wb:dropDown
            options="${optlist}"
            wbSource="${gdate}"
            wbTarget="gdate"
            display="isodate"
			prefix="Date: " 	
			postfix=""
        />
        <wb:dropDown
            options='{"options":${str(datasetNames)}}'
            wbSource="${datasetNames[int(set0)]}"
            wbTarget="set0"
            display="names"
			prefix="Line 0: " 	
			postfix=""
        />
        <wb:dropDown
            options='{"options":${str(datasetNames)}}'
            wbSource="${datasetNames[int(set1)]}"
            wbTarget="set1"
            display="names"
			prefix="Line 1: " 	
			postfix=""
        />
    </center>
</div>

<center>
    <wb:flashGraph 
        width="720"
        height="320"
        minYval="0"
        maxYval="60"
        xLabels="time"
        xStep="10"
        activeSets="${str(visibleSets)}"
        gTitle="Run Times"
        yLabelStyle="18,444444"
    />
    

</center>



</div>

</html>


