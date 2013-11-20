
<?python
#layout_params['page_title'] = ""
layout_params['page_heading'] = "Step 2 - Keypad Button Configuration"

device_description = ""
message = ""
devid = "Default"
keypadid = "Default"
device_description = ""
?>


<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="'layout.kid'" >


    <div py:match="item.tag == '{http://id.webbrick.co.uk/}contentbox'" id="contentbox">
        
        <form class="rightBox" name="GwConfigKeypads" action = "/wbgwcnf/GwConfigKeypadsButtonAction" method="post" >
            <input type = "text" style = "display:none" name = "devid" value = "${devid}"/>
            <input type = "text" style = "display:none" name = "keypadid" value = "${keypadid}"/>
            <select size="20" id="ButtonSelector" name="ButtonSelector" onchange = "showButtonInfo(this,'${devid}')" wbLoad = "walkButtons('${keypadid}', '${devid}')">
                <option class = "OptAttn" value="waiting">(Waiting for server)</option>
            </select>                         
           
        <div><h3>Add Button</h3>
            Button Number : 
                <select id = "NewButtonSelector" name = "NewButtonSelector">
                    <div py:if='device_description["type"]["val"] == "Lutron"' py:strip = "True">
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
                        <option id = "23" class = "OptNorm" name ="23">23</option>
                        <option id = "24" class = "OptNorm" name ="24">24</option>    
                    </div>       
                    <div py:if='device_description["type"]["val"] == "WebBrick"' py:strip = "True">
                        <option id = "01" class = "OptNorm" name ="Scene 0">Scene 0</option>
                        <option id = "01" class = "OptNorm" name ="Scene 1">Scene 1</option>
                        <option id = "02" class = "OptNorm" name ="Scene 2">Scene 2</option>
                        <option id = "03" class = "OptNorm" name ="Scene 3">Scene 3</option>
                        <option id = "04" class = "OptNorm" name ="Scene 4">Scene 4</option>
                        <option id = "05" class = "OptNorm" name ="Scene 5">Scene 5</option>
                        <option id = "06" class = "OptNorm" name ="Scene 6">Scene 6</option>
                        <option id = "07" class = "OptNorm" name ="Scene 7">Scene 7</option>
                        <option id = "08" class = "OptNorm" name ="Scene 8">Scene 8</option>
                        <option id = "09" class = "OptNorm" name ="Scene 9">Scene 9</option>
                        <option id = "10" class = "OptNorm" name ="Scene 10">Scene 10</option>
                        <option id = "11" class = "OptNorm" name ="Scene 11">Scene 11</option>
                        <option id = "12" class = "OptNorm" name ="Digital Out 0">Digital Out 0</option>
                        <option id = "12" class = "OptNorm" name ="Digital Out 1">Digital Out 1</option>
                        <option id = "13" class = "OptNorm" name ="Digital Out 2">Digital Out 2</option>
                        <option id = "14" class = "OptNorm" name ="Digital Out 3">Digital Out 3</option>
                        <option id = "14" class = "OptNorm" name ="Digital Out 4">Digital Out 4</option>
                    </div>        
                </select>
            Icon :
                <select id = "NewButtonIconSelect" name = "NewButtonIconSelect">
                    <option id = "Light" class = "OptNorm" name ="Light" value = "light">Light</option>
                    <option id = "Curtains_Open" class = "OptNorm"  value = "curtainopen">Curtains Open</option>
                    <option id = "Curtains_Close" class = "OptNorm" value = "curtainclose">Curtains Close</option> 
                </select>
            
           
            <button type="submit" name="action" value="add">Add</button>
            <div>
                <button type="submit" name = "action" value = "done">Done</button>
            </div>
        </div>
        </form>
    </div>

</html>
