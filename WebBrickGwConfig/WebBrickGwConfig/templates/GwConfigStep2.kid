<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="'layout.kid'" >
        
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}contentbox'" id="contentbox">
        <form class="leftBox" name="GwConfigStep2" action="/wbgwcnf/GwConfigStep2Action" method="post">
        
            
            <select size="20" id="KnownDevicesSelector" name="KnownDevicesSelector" wbLoad="loadKnownDevicesSelector(showInfo)">
                <option class="OptAttn" value="waiting">(Waiting for server)</option>
            </select>
            <button type="submit" name="action" value="configure">Configure</button>
            <button type="submit" name="action" value="done">Done</button>
        </form>
        
        <div id="deviceInfoBox">
            <!-- This box contains the device info -->
            No Device Selected
        </div>
    </div>

</html>
