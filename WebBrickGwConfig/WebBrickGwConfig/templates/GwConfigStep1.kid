<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="'layout.kid'" >
        
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}contentbox'" id="contentbox">
        <form name="GwConfigStep1" action="/wbgwcnf/GwConfigStep1Action" method="post">
        
            <select id="NewDevicesSelector" name="NewDevicesSelector" size="20" wbLoad="loadNewDevicesSelector()" >
                <option class="OptAttn" value="waiting">(Waiting for server)</option>
            </select>
            <button type="submit" name="action" value="discover">Discover</button>
            <button type="submit" name="action" value="provision">Provision</button>
            
            <select size="20" id="KnownDevicesSelector" name="KnownDevicesSelector" wbLoad="loadKnownDevicesSelector()">
                <option class="OptAttn" value="waiting">(Waiting for server)</option>
            </select>
            <button type="submit" name="action" value="reprovision">Re-Provision</button>
            <button type="submit" name="action" value="done">Done</button>
        </form>
    </div>

</html>
