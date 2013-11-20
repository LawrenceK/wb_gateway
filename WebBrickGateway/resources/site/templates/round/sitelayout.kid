<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_no_td
?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:extends="WebBrickGateway.templates.widgets_no_td" 
         >
    <head>
        <title>Webbrick home automation</title>
        <meta name="apple-mobile-web-app-capable" content="yes" />
        
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

    <div id="background"><div id="backgroundscatter">&nbsp;</div></div>

    <div id="topbar">
    	<div id="topbarleft">back</div>
    	<div id="topbarcentre"><img src="/static/activeskin/images/topbartitlehome.png" width="80" height="44" /></div>
    	<div id="topbarright">
    		<div id="topbarsettingsicon"><img src="/static/activeskin/images/topbarsettingsicon.png" /></div>
    		<div id="topbarhelpicon">
                <wb:simpleLink target="/template/guide"><img src="/static/activeskin/images/topbarhelpicon.png" /></wb:simpleLink>            
            </div>
    	</div>
    </div>

    <div id="content">
        <wb:leftbox id="leftbox">
            To be replaced by page specific content
        </wb:leftbox>

        <wb:topbox id="topbox">
            To be replaced by page specific content
        </wb:topbox>

        <wb:botbox id="botbox">
            To be replaced by page specific content
        </wb:botbox>
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
                            imageUris="/static/images/notReady.png,/static/images/clear.png,/static/images/HWActive.png"/>
                    </li>
        			<li id="earlystart" style="display:none">
                        <wb:imageIndicator wbSource="/eventstate/earlyStart/enabled"
                            imageUris="/static/images/clear.png,/static/images/earlyBird.png"/>                    
                    </li>
        			<li id="earlystart">
                    </li>
        			<li id="houseempty" style="display:none">
                    </li>
        			<li id="nightindicator">
                        <wb:imageIndicator wbSource="/eventstate/time/isDark?attr=state"
                            imageUris="/static/activeskin/images/statusicons/dayindicator.png, /static/activeskin/images/statusicons/nightindicator.png"/>
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
