<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_tabbed
from WebBrickGateway.templates.widgets_tabbed import getCurrentValue

import zone_embed

layout_params['selected_tab'] = 4
# This sets the pooling period of widgets to 30 sec
layout_params['custom_poller'] = 30

pagemax = 8

def countLimit(n,s):
    if (s-1+pagemax) <= n: return (s-1+pagemax) 
    if (s-1+pagemax) > n: return n

def isMore(n,s):
    if (s-1+pagemax) < n : return True
    else : return False
 
?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="sitelayout.kid" 
        py:extends="zone_embed,WebBrickGateway.templates.widgets_tabbed">


    <div py:match="item.tag == '{http://id.webbrick.co.uk/}tabcontent'" id="tabcontent">

    <?python 
        zoneLimit = getCurrentValue( "/eventstate/zone/count" )
        if zoneLimit == '':
            zoneLimit = 0
        else:
            zoneLimit = int(zoneLimit) + 1

        if not 'start_at' in locals(): start_at = 1
        start_at = int(start_at) 
    ?>


        <div class="controls_top_area" >
            <div id="tight">
            <span py:for='zoneNr in range(start_at,countLimit(zoneLimit,start_at),1)' py:strip='True'>
               ${output_zone_button( "zone%s"%zoneNr, 
                                     "zone%s"%zoneNr, 
                                     getCurrentValue("/eventstate/zone%s/name?attr=name"%zoneNr)  )}
            </span>
            <span py:if='isMore(zoneLimit,start_at)' py:strip='True'>
              <div class="button">
                <div class="left"/>
                <div class="centerwide" onclick="window.location='/template/tabbed/allzones?start_at=${start_at+pagemax-2}'">
                    <div class="textwide">
                        More
                    </div>
                </div>
                <div class="right" />
              </div>
            </span>
            </div>
        </div>
    </div>
    
</html>
