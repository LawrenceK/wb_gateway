
<?python
#layout_params['page_title'] = ""
layout_params['page_heading'] = "Step 2 - Lighting Keypad Configuration"

device_description = ""
message = ""
devid = "Default"
?>


<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="'layout.kid'" >


    <div py:match="item.tag == '{http://id.webbrick.co.uk/}contentbox'" id="contentbox">
        
        <form class="rightBox" name="GwConfigKeypads" action = "/wbgwcnf/GwConfigKeypadsAction" method="post" >  
            <input type = "text" style = "display:none" name = "devid" value = "${devid}"/>
            <select size="20" id="KeypadSelector" name="KeypadSelector" onchange = "showKeyPadInfo(this,'${devid}')" wbLoad = "walkKeypads(this, '${devid}')">
                <option class = "OptAttn" value="waiting">(Waiting for server)</option>
            </select>
            
            <button type="submit" name="action" value="edit_buttons">Edit Buttons</button>
        <div><h3>Add Keypad ${devid}</h3>
        <div py:if='device_description["type"]["val"] == "WebBrick"' py:strip = "True">
            <input type = "text" style = "display:none" name = "NewProcessorSelector" value = "01"/>
            <input type = "text" style = "display:none" name = "NewLinkSelector" value = "01"/>
            <input type = "text" style = "display:none" name = "NewKeyPadSelector" value = "01"/>
        </div>
        <div py:if='device_description["type"]["val"] == "Lutron"' py:strip = "True">
                Processor : 
                    <select id = "NewProcessorSelector" name = "NewProcessorSelector">
                        <option id = "01" class = "OptNorm" name ="01">01</option>
                        <option id = "02" class = "OptNorm" name ="02">02</option>
                        <option id = "03" class = "OptNorm" name ="03">03</option>
                        <option id = "04" class = "OptNorm" name ="04">04</option>
                        <option id = "05" class = "OptNorm" name ="05">05</option>
                        <option id = "06" class = "OptNorm" name ="06">06</option>
                        <option id = "07" class = "OptNorm" name ="07">07</option>
                        <option id = "08" class = "OptNorm" name ="08">08</option>
                        <option id = "09" class = "OptNorm" name ="09">09</option>
                        <option id = "10" class = "OptNorm" name ="10">10</option>
                        <option id = "11" class = "OptNorm" name ="11">11</option>
                        <option id = "12" class = "OptNorm" name ="12">12</option>
                        <option id = "13" class = "OptNorm" name ="13">13</option>
                        <option id = "14" class = "OptNorm" name ="14">14</option>
                        <option id = "15" class = "OptNorm" name ="15">15</option>
                        <option id = "16" class = "OptNorm" name ="16">16</option>                
                    </select>
                Link :
                    <select id = "NewLinkSelector" name = "NewLinkSelector">
                        <option id = "04" class = "OptNorm" name ="04">04</option>
                        <option id = "05" class = "OptNorm" name ="05">05</option>
                        <option id = "06" class = "OptNorm" name ="06">06</option> 
                    </select>
                KeypadNumber :
                    <select id = "NewKeyPadSelector" name = "NewKeyPadSelector">
                        <option id = "01" class = "OptNorm" name ="01">01</option>
                        <option id = "02" class = "OptNorm" name ="02">02</option>
                        <option id = "03" class = "OptNorm" name ="03">03</option>
                        <option id = "04" class = "OptNorm" name ="04">04</option>
                        <option id = "05" class = "OptNorm" name ="05">05</option>
                        <option id = "06" class = "OptNorm" name ="06">06</option>
                        <option id = "07" class = "OptNorm" name ="07">07</option>
                        <option id = "08" class = "OptNorm" name ="08">08</option>
                        <option id = "09" class = "OptNorm" name ="09">09</option>
                        <option id = "10" class = "OptNorm" name ="10">10</option>
                        <option id = "11" class = "OptNorm" name ="11">11</option>
                        <option id = "12" class = "OptNorm" name ="12">12</option>
                        <option id = "13" class = "OptNorm" name ="13">13</option>
                        <option id = "14" class = "OptNorm" name ="14">14</option>
                        <option id = "15" class = "OptNorm" name ="15">15</option>
                        <option id = "16" class = "OptNorm" name ="16">16</option>
                        <option id = "17" class = "OptNorm" name ="17">17</option>
                        <option id = "18" class = "OptNorm" name ="18">18</option>
                        <option id = "19" class = "OptNorm" name ="19">19</option>
                        <option id = "20" class = "OptNorm" name ="20">20</option>
                        <option id = "21" class = "OptNorm" name ="21">21</option>
                        <option id = "22" class = "OptNorm" name ="22">22</option>
                        <option id = "23" class = "OptNorm" name ="23">23</option>
                        <option id = "24" class = "OptNorm" name ="24">24</option>
                        <option id = "25" class = "OptNorm" name ="25">25</option>
                        <option id = "26" class = "OptNorm" name ="26">26</option>
                        <option id = "27" class = "OptNorm" name ="27">27</option>
                        <option id = "28" class = "OptNorm" name ="28">28</option>
                        <option id = "29" class = "OptNorm" name ="29">29</option>
                        <option id = "30" class = "OptNorm" name ="30">30</option>
                        <option id = "31" class = "OptNorm" name ="31">31</option>
                        <option id = "32" class = "OptNorm" name ="32">32</option>
                </select>
            </div>
            Location : 
            <select name = "location">
                <option name = 'Rack' class = "OptNorm" value = "Rack">Rack</option>
                <option name = 'Livingroom' class = 'OptNorm' value = "Livingroom">Livingroom</option>
                <option name = 'Kitchen' class = 'OptNorm' value = "Kitchen">Kitchen</option>
                <option name = 'Bedroom' class = 'OptNorm' value = "Bedroom">Bedroom</option>
            </select>            
            <button type="submit" name="action" value="add">Add</button>
            <div>
            <button type="submit" name="action" value="done">Done</button>
            </div>
            <div id="keypadInfoBox">
                <!-- This box contains the device info -->
                No Device Selected
            </div>
            
        </div>
        </form>
    </div>

</html>
