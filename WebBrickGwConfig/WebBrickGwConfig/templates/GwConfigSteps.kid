<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="'layout.kid'" >
        
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}contentbox'" id="contentbox">
        <a href="/wbgwcnf/GwConfigStep1">
            <div class="sub_heading">Step 1: Discover and Provision IP Devices</div>
            <p class="paragraph">
                Step one allows you to discover IP devices as they get connected and to set 
                their operation parameters during provisioning. Devices of one type have to
                be added one after another to avoid IP conflicts and to allow unique identification.
            </p>
        </a>
        <a href="/wbgwcnf/GwConfigStep2">
            <div class="sub_heading">Step 2: Configure IP Devices </div>
            <p class="paragraph">
                Step two will guide you through specifying device connections and interactions. 
            </p>
        </a>
        <a href="/wbgwcnf/GwConfigStep3">
            <div class="sub_heading">Step 3: Render UI</div>
            <p class="paragraph">
                Step three will give you the opportunity to build the user interface and allow you to restart the gateway. 
            </p>
        </a>
    </div>

</html>
