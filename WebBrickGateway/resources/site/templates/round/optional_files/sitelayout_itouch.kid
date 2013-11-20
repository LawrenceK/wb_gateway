<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round

page_title = "WBS iTouch Control"
itouch_icon = "webbrick.png"
show_itouch = True
?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:extends="WebBrickGateway.templates.widgets_round" 
        >
    <head>
        <title>${page_title}</title>
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="viewport" content="minimum-scale=1.0, width=device-width, maximum-scale=1" />
        
        <!-- ! This link provides a custom icon for short cuts on an Apple Home screen (iTouch/iPhone) -->
        <link py:if="itouch_icon" rel="apple-touch-icon" href="/static/activeskin/images/itouchicons/${itouch_icon}" />
        <!-- ! default icon -->
        <link py:if="itouch_icon == ''" rel="apple-touch-icon" href="/static/activeskin/images/itouchicons/webbrick.png" />
        
        <link href="/static/activeskin/css/itouch.css" rel="stylesheet" type="text/css" />
        
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

    <div id="topbar">
    	<div id="topbarleft" onClick="history.back()">back</div>
        <div id="topbarcentre" onClick="window.location='/template/itouch_welcome'">
            <img src="/static/activeskin/images/topbartitlehome.png" width="80" height="44" />
        </div>
 
        <div id="topbarright">
        
            <div id="topbarhelpicon" onClick="window.location='/template/itouch_help'">
                <img src="/static/activeskin/images/topbarhelpicon.png" />
            </div>
        </div>
    </div>
    
    <div id="itouch_content">
       
        
        <div py:if="show_itouch == True" id="itouchbox">
            <table cellpadding="0" cellspacing="0" class="rect8pxbox" id="itouchboxtable">
                <tr>
                    <td class="tl"></td>
                    <td class="t">
                    </td>
                    <td class="tr"></td>
                </tr>
                <tr>
                    <td class="l"></td>
                    <td class="m">
                        <wb:itouchboxcontent id="itouchboxcontent">
                            To be replaced by page specific content
                        </wb:itouchboxcontent>
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
    </body>
</html>
