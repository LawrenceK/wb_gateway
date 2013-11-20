<?python
#layout_params['page_title'] = ""
layout_params['page_heading'] = "Step 2 - Device Configuration"

device_description = ""
message = ""
?>
<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="'layout.kid'" >
        
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}contentbox'" id="contentbox">

<?python
devid = device_description["id"]["val"]
?>    
        <span id="deviceTitle" devID='${devid}' WbLoad="attachDevice(this,'${devid}')" > Connections for Device ${device_description["id"]["val"]}</span>
        <span id="deviceInfoSynopsis" WbLoad="walkSources(this,'${devid}')">Waiting...</span>
        <form name="GwConfigConfigure" action="/wbgwcnf/GwConfigConfigureAction" method="post">
            <input type="text" name="dev_id" style="visibility:hidden;" value="${device_description['id']['val']}" />
            <div id="DevConnSelectorBox" >
                <select size="20"
                        onchange="showConnOptions(this)" 
                        id="DevConnSelector" 
                        name="DevConnSelector">
                    <option class="OptAttn" value="waiting">(Waiting for selection)</option>
                </select>
            </div>
            <button id="makeConnection" type="submit" name="action" value="connect">Make Connection</button>
            <div id="connOptionsBox" >
                <select size="20"
                        onchange="showSinkDetails(this)" 
                        id="connOptions" 
                        name="connOptions">
                    <option class="OptAttn" value="waiting">(Waiting for selection)</option>
                </select>
                <div id="sinkDetail">
                    Waiting for selection
                </div>
            </div>
            <div id="serverMessage">
                <div py:for="msg in message">
                 ${msg}
                </div>
            </div>            
        </form>
        
              <div id = "ConfigWarning" >
        <form name="GwConfigWarning" action="/wbgwcnf/GwConfigStep2" method="get">
            <button id="done" type="submit" name="action" value="continue" >Done</button>
        </form>
        </div>
        
      
    </div>

</html>
