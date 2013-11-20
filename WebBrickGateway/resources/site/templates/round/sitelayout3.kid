<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round

left_title = ""
top_title = ""
bottom_title = ""
show_left = True
show_top = True
show_bottom = True
itouch_icon = ""

def box_class(tt):
    if tt:
        return "rect8pxboxwtitle"
    return "rect8pxbox"
?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:extends="WebBrickGateway.templates.widgets_round" 
        >
    <head>
        <title>Webbrick home automation</title>
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <!-- ! This link provides a custom icon for short cuts on an Apple Home screen (iTouch/iPhone) -->
        <link py:if="itouch_icon" rel="apple-touch-icon" href="/static/activeskin/images/itouchicons/${itouch_icon}" />
        <!-- ! default icon -->
        <link py:if="itouch_icon == ''" rel="apple-touch-icon" href="/static/activeskin/images/itouchicons/webbrick.png" />
        
        <link href="/static/activeskin/css/screen.css" rel="stylesheet" type="text/css" />
        <link href="/static/activeskin/css/home.css" rel="stylesheet" type="text/css" />
        <!--[if IE 7]>  
          <link href="/static/activeskin/css/screenie7.css" rel="stylesheet" type="text/css" media="all"/>
        <![endif]-->
        
        <!-- ! This style sheet loads specific styles for Safari to enable a better display of pages on the iTouch --> 
        <link href="/static/activeskin/css/screensafari.css" rel="stylesheet" type="text/css" />
        
        <link href="/static/activeskin/css/mediasourcecontrol.css" rel="stylesheet" type="text/css" />
        
        <span py:if="javascript == 'yes'" py:strip="True">
            <script py:if="hasattr(self, 'debug')" src="/static/javascript/MochiKit.uncompressed.js" type="text/javascript"></script>
            
            <script py:if="not hasattr(self, 'debug')" src="/static/javascript/MochiKit.js" type="text/javascript"></script>
            <!-- !flash support -->
            <script src="/static/javascript/AC_OETags.js" type="text/javascript"></script>

            <!-- !WebBrick,js connects to onload and initialises panel elements -->
            
            <script src="/static/javascript/WebBrick.js" type="text/javascript"></script>
            <script src="/static/javascript/WbStrings.js" type="text/javascript"></script>
            <script src="/static/javascript/WbButton.js" type="text/javascript"></script>
            <script src="/static/javascript/WbNumericDisplay.js" type="text/javascript"></script>
            <script src="/static/javascript/WbTimeDisplay.js" type="text/javascript"></script>
            <script src="/static/javascript/WbTextDisplay.js" type="text/javascript"></script>
            <script src="/static/javascript/WbNumericSlider.js" type="text/javascript"></script>
            <script src="/static/javascript/WbNumericBar.js" type="text/javascript"></script>
            <script src="/static/javascript/keyCheck.js" type="text/javascript"></script>
            <script src="/static/javascript/NumericPad.js" type="text/javascript"></script>
            <script src="/static/javascript/WbNumericEntry.js" type="text/javascript"></script>
            <script src="/static/javascript/WbTextEntry.js" type="text/javascript"></script>
            <script src="/static/javascript/WbTimeEntry.js" type="text/javascript"></script>
            <script src="/static/javascript/WbDayEntry.js" type="text/javascript"></script>
            <script src="/static/javascript/WbOnOffEntry.js" type="text/javascript"></script>
            <script src="/static/javascript/WbEnableEntry.js" type="text/javascript"></script>
            <script src="/static/javascript/WbFlashMeter.js" type="text/javascript"></script>
            <script src="/static/javascript/WbFlashButton.js" type="text/javascript"></script>
            <script src="/static/javascript/WbDynamicImage.js" type="text/javascript"></script>
            <script src="/static/javascript/WbImageIndicator.js" type="text/javascript"></script>
            <script src="/static/javascript/WbHideableBox.js" type="text/javascript"></script>
            <script src="/static/activeskin/javascript/flashControls.js" type="text/javascript"></script>
            <script src="/static/javascript/itouch/addressbar.js" type="application/x-javascript"></script> 
            
            <script py:if="hasattr(self, 'debug')" src="/static/javascript/debug.js" type="text/javascript"></script>
        </span>

    </head>
    <body>
    <!-- ! Onload event to hide the scroll bar on iTouch, when in ladscape mode 
    <body onload="setTimeout(function() { window.scrollTo(0, 1) }, 100);">--> 

    <div id="background"><div id="backgroundscatter">&nbsp;</div></div>

    <div id="topbar">
    	<div id="topbarleft" onClick="history.back()">back</div>
        <div id="topbarcentre" onClick="window.location='/'">
            <img src="/static/activeskin/images/topbartitlehome.png" width="80" height="44" />
        </div>
 
        <div id="topbarright">
        
            <div id="topbarsettingsicon" onClick="window.location='/template/settings_overview'">
                <img src="/static/activeskin/images/topbarsettingsicon.png" />
            </div>
            <div id="topbarhelpicon" onClick="window.location='/template/guide'">
                <img src="/static/activeskin/images/topbarhelpicon.png" />
            </div>
        </div>
    </div>

    <div id="content">
        <div py:if="show_left == True" id="leftbox">
            <table cellpadding="0" cellspacing="0" class="rect8pxboxwtitle" id="leftboxtable">
                <tr>
                    <td class="tl"></td>
                    <td class="t">
                        <h1 py:if="left_title" py:content="left_title">&nbsp;</h1>
                    </td>
                    <td class="tr"></td>
                </tr>
                <tr>
                    <td class="l"></td>
                    <td class="m">
                        <wb:leftboxcontent id="leftboxcontent">
                            To be replaced by page specific content
                        </wb:leftboxcontent>
                    </td>
                    <td class="r"></td>
                </tr>
                <tr>
                    <td class="bl"></td>
                    <td class="b"></td>
                    <td class="br"></td>
                </tr>
            </table>
        </div>
        
        <div py:if="show_top == True" id="topbox">
            <table cellpadding="0" cellspacing="0" class="${box_class(top_title)}" id="topboxtable">
                <tr>
                    <td class="tl"></td>
                    <td class="t">
                        <h1 py:if="top_title" py:content="top_title">&nbsp;</h1>
                    </td>
                    <td class="tr"></td>
                </tr>
                <tr>
                    <td class="l"></td>
                    <td class="m">
                        <wb:topboxcontent id="topboxcontent">
                            To be replaced by page specific content
                        </wb:topboxcontent>
                    </td>
                    <td class="r"></td>
                </tr>
                <tr>
                    <td class="bl"></td>
                    <td class="b"></td>
                    <td class="br"></td>
                </tr>
            </table>
        </div>
        
        <div py:if="show_bottom == True" id="botbox">
            <table cellpadding="0" cellspacing="0" class="rect8pxbox" id="botboxtable">
                <tr>
                    <td class="tl"></td>
                    <td class="t">
<!-- !
                        <h1 py:if="bottom_title" py:content="bottom_title">&nbsp;</h1>
-->                        
                    </td>
                    <td class="tr"></td>
                </tr>
                <tr>
                    <td class="l"></td>
                    <td class="m">
                        <wb:botboxcontent id="botboxcontent">
                            To be replaced by page specific content
                        </wb:botboxcontent>
                    </td>
                    <td class="r"></td>
                </tr>
                <tr>
                    <td class="bl"></td>
                    <td class="b"></td>
                    <td class="br"></td>
                </tr>
            </table>
        </div>
    </div>
    
    <div id="botbar">
        <div id="botbarleft">
        	<div class="botbarpill" id="temppill">
        		<div class="botbarpillleft">&nbsp;</div>
        		<div class="botbarpillmid" id="temppillmid">
                    <div class="botbarpillcontent">
                        <wb:numericDisplay width='18%' wbSource="/eventstate/temperature/outside" prefix="" format="##.#" postfix="&ordm;C">&nbsp;</wb:numericDisplay>
                    </div>
                </div>
        		<div class="botbarpillright">&nbsp;</div>
        	</div>
        </div>
        <div id="botbarright">
        	<div id="botbarwebbricklogo"><img src="/static/activeskin/images/botbarwebbricklogo.png" /></div>
        	<div class="botbarpill" id="iconpill">
        		<div class="botbarpillleft">&nbsp;</div>
        		<div class="botbarpillmid" id="iconpillmid"><div class="botbarpillcontent" id="statusicons">
        		<ul>
        			<li id="houseoccupied">
                        <wb:imageIndicator wbSource="/eventstate/occupants/home"
                            imageUris="/static/activeskin/images/statusicons/houseempty.png,/static/activeskin/images/statusicons/houseoccupied.png"/>
                    </li>
        			<li id="hwactive">
                        <wb:imageIndicator wbSource="/eventstate/zone1/state?attr=state"
                            imageUris="/static/activeskin/images/statusicons/notReady.png,/static/images/clear.png,/static/activeskin/images/statusicons/HWActive.png"/>
                    </li>
        			<li id="earlystart" >
                        <wb:imageIndicator wbSource="/eventstate/earlyStart/enabled"
                            imageUris="/static/images/clear.png,/static/activeskin/images/statusicons/earlystart.png"/>                    
                    </li>
        			<li id="houseempty" style="display:none">
                    </li>
        			<li id="nightindicator">
                        <wb:imageIndicator wbSource="/eventstate/time/isDark?attr=state"
                            imageUris="/static/activeskin/images/statusicons/dayindicator.png,/static/activeskin/images/statusicons/nightindicator.png"/>
                    </li>
        			<li id="standby" style="display:none">
                    </li>

        		</ul>
        		</div></div>
        		<div class="botbarpillright">&nbsp;</div>
        	</div>
        	<div class="botbarpill" id="timepill">
        		<div class="botbarpillleft">&nbsp;</div>
        		<div class="botbarpillmid" id="timepillmid">
                    <div class="botbarpillcontent">
                        <wb:textDisplay width='8%' wbSource="/local/time" prefix="" postfix="">&nbsp;</wb:textDisplay>
                    </div>
                </div>
        		<div class="botbarpillright">&nbsp;</div>
        	</div>	
        </div>
    </div>
    
    </body>
</html>
