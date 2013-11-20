<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_tabbed

selected_tab = 1
poller_interval =  False

?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:extends="WebBrickGateway.templates.widgets_tabbed" 
        >
    <head>
        <title>Evinox Smart Control - powered by WebBrick Systems</title>
        
        <!-- Style sheets that are loaded -->
        <link href="/static/tabbedskin/css/main.css" rel="stylesheet" type="text/css" />
        <link href="/static/tabbedskin/css/tabbar.css" rel="stylesheet" type="text/css" />
        <link href="/static/tabbedskin/css/botbar.css" rel="stylesheet" type="text/css" />
        <link href="/static/tabbedskin/css/setpointcontrol.css" rel="stylesheet" type="text/css" />
        <link href="/static/tabbedskin/css/schedule.css" rel="stylesheet" type="text/css" />
        <link href="/static/tabbedskin/css/buttons.css" rel="stylesheet" type="text/css" />
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
            <script src="/static/javascript/WbFlashGraph.js" type="text/javascript"></script>
            <script src="/static/javascript/WbImageIndicator.js" type="text/javascript"></script>
            <script src="/static/javascript/WbDynamicClass.js" type="text/javascript"></script>
            <script src="/static/javascript/WbHideableBox.js" type="text/javascript"></script>
            <script src="/static/activeskin/javascript/flashControls.js" type="text/javascript"></script>
            <script src="/static/javascript/itouch/addressbar.js" type="application/x-javascript"></script> 
            
            
            <link href="/static/css/form.css" rel="stylesheet" type="text/css" />
            <script src="/static/javascript/graphs/swfobject.js" type="text/javascript"></script>
            <script src="/static/javascript/graphs/json2.js" type="text/javascript"></script>
            <script src="/static/javascript/graphs/graphs.js" type="text/javascript"></script>
            

            <!-- Javascript for tabbed interface -->

		    <script src="/static/tabbedskin/javascript/prototype.js" type="text/javascript"></script>
		    <script src="/static/tabbedskin/javascript/widget.schedule.js" type="text/javascript"></script>
		    <script src="/static/tabbedskin/javascript/widget.spinner.js" type="text/javascript"></script>
		    <script src="/static/tabbedskin/javascript/widget.tabbar.js" type="text/javascript"></script>
		    <script src="/static/tabbedskin/javascript/widget.tempslider.js" type="text/javascript"></script>
		    <!-- <link href="/static/css/tabbed/screen.css" media="screen" rel="stylesheet" type="text/css" />	-->
            
            <script py:if="hasattr(self, 'debug')" src="/static/javascript/debug.js" type="text/javascript"></script>
            <script py:if="poller_interval" type="text/javascript">
                initPoller( poller_interval );
            </script>
        </span>

    </head>

    <body>

    
    
        <!-- BEGIN: Temporary Tab Bar -->
        <!-- 
        <div id="tabbar">
	        <table>
	            <tr>
	                <td class="tabtermla"/>
	                <td class="tabmida">
	                    <a href="/template/welcome">controls</a>
	                </td>
	                <td class="tabinterrai"/>
	                <td class="tabmidi">
	                    <a href="/template/status">status</a>
                    </td>
                    
                    <td class="tabinterrii"/>
                    <td class="tabmidi">
                        <a href="/template/boiler">boiler</a>
                    </td>
                    <td class="tabinterrii"/>
                    
                    <td class="tabmidi">
                        <a href="/template/ashp">ASHP</a>
                    </td>
                   
                    <td class="tabtermri"/>
                </tr>
            </table>
        </div>
        -->
        <!-- END: Temporary Tab Bar -->	

        <!-- BEGIN: Real Tab Bar -->
        <!--
        <wb:tabbar
                labels="controls,status,history,solar"
                links="/template/welcome,/template/status,/template/history,/template/solar"
                width="100%">
            &nbsp;
        </wb:tabbar>
        -->
        <!-- END: Real Tab Bar -->
        
        
        <!-- BEGIN: Beta Tab Bar -->
        <div id="tabbar">
			<script language="JavaScript">
				var tabbar = new Proto.Tabbar({
			            tabbar_id: 'tabbar',
			            tabs_data: [
				            {
					            label:'general',
					            href:'/template/welcome'
				            },
                            {
                                label:'controls',
                                href:'/template/controls'
                            },
                            {
					            label:'status',
					            href:'/template/status'
				            },
				            {
					            label:'plant',
					            href:'/template/plant'
				            },
			            ]
		                }
				    );
				tabbar.drawWithActive(${selected_tab});
			</script>
		</div>
        <!-- END: Real Tab Bar -->

        <div id="content">
           
            <wb:tabcontent id="tabcontent">
                To be replaced by page/tab specific content
            </wb:tabcontent>

        </div>

        <div id="botbar">
	        <div id="botbarleft">
		        <div class="botbarpill">
			        <div class="botbarpillleft">&nbsp;</div>
			        <div class="botbarpillmid">
		                <wb:textDisplay 
		                        wbSource="/local/time/24h" 
		                        prefix="" 
		                        postfix="">
	                        &nbsp;
                        </wb:textDisplay>
			        </div>
			        <div class="botbarpillright">&nbsp;</div>
		        </div>
	        </div>
	        <div class="botbarhelp" onclick="window.location='/template/help'" />
	        <div 
	             wbLoad="loadDynamicClass()"
	             default_class="botbaralertclear"
	             wbSource="/eventstate/alerts" 
	             onclick="window.location='/template/alerts'" 
	             />
        </div>
    
    </body>
</html>
