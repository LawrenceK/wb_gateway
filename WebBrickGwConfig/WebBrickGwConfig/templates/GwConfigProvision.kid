<?python
#layout_params['page_title'] = ""
layout_params['page_heading'] = "Step 1 - Device Provisioning"

device_description = ""
startechtype = ""
startechdevices = []
?>
<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="'layout.kid'" >
        
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}contentbox'" id="contentbox">
        <form name="GwConfigProvision" action="/wbgwcnf/GwConfigProvisionAction" method="post">
            <input type="text" name="dev_id" style="visibility:hidden;" value="${device_description['id']['val']}" />
               
            <div py:if='device_description["type"]["val"] == "Imerge"' py:strip="True">
                <div><h3>Imerge Provisioning</h3></div>


                <div>Please enter a name for your Imerge box: <input type="text" name="new_name" value="${device_description['name']['val']}"/></div>
                <div>Please enter a device location: 
                    <select name = "location">
                        <option name = 'Rack' class = "OptNorm" value = "Rack">Rack</option>
                        <option name = 'Livingroom' class = 'OptNorm' value ="Livingroom">Livingroom</option>
                        <option name = 'Bedroom' class = 'OptNorm' value = "Kitchen">Kitchen</option>
                        <option name = 'Diningroom' class = 'OptNorm' value = "Bedroom">Bedroom</option>
                    </select>
                </div>
                <button type="submit" name="action" value="upnp_done">Done</button>
            </div> 

            <div py:if='device_description["type"]["val"] == "Sonos"' py:strip="True">
                <div><h3>Sonos Provisioning</h3></div>

                <div>Please enter a name for your Sonos box: <input type="text" name="new_name" value="${device_description['name']['val']}"/></div>
                <div>Please enter a device location: 
                    <select name = "location">
                        <option name = 'Rack' class = "OptNorm" value = "Rack">Rack</option>
                        <option name = 'Livingroom' class = 'OptNorm' value ="Livingroom">Livingroom</option>
                        <option name = 'Bedroom' class = 'OptNorm' value = "Kitchen">Kitchen</option>
                        <option name = 'Diningroom' class = 'OptNorm' value = "Bedroom">Bedroom</option>
                    </select>
                </div>
                <button type="submit" name="action" value="upnp_done">Done</button>
            </div>

            <div py:if='device_description["type"]["val"] == "WebBrick"' py:strip="True">
                <div><h3>WebBrick Provisioning</h3></div>
     
                <div>Please enter a new IP Address: <input type="text" name="new_ip" value="${device_description['ip']['val']}"/> </div>
                <div>Please enter a node name: <input type="text" name="node_name" value="${device_description['name']['val']}"/></div>
                <div>Please enter a node number: <input type="text" name="node_number" value="${device_description['number']['val']}"/></div>
                <button type="submit" name="action" value="webbrick_done">Done</button>
            </div>
            
            <div py:if='device_description["type"]["val"] == "Exterity_Encoder"' py:strip="True">
                <div><h3>Exterity Encoder Provisioning</h3></div>
                <input type="text" style="visibility:hidden;" name="new_ip" value="${device_description['ip']['val']}"/>
                 <input type="text" style="visibility:hidden;" name="web_url" value="1"/>
                <div>IP Address: ${device_description['ip']['val']}</div>
                <div>Please enter a device name: <input type="text" name="name" value="${device_description['name']['val']}"/></div>
                <div>Please enter a device location: 
                    <select name = "location">
                        <option name = 'Rack' class = "OptNorm" value = "Rack">Rack</option>
                        <option name = 'Livingroom' class = 'OptNorm' value ="Livingroom">Livingroom</option>
                        <option name = 'Bedroom' class = 'OptNorm' value = "Kitchen">Kitchen</option>
                        <option name = 'Diningroom' class = 'OptNorm' value = "Bedroom">Bedroom</option>
                    </select>
                </div>
                <button type="submit" name="action" value="exterity_done">Done</button>
            </div>       
            <div py:if='device_description["type"]["val"] == "Exterity_Decoder"' py:strip="True">
                <div><h3>Exterity Decoder Provisioning</h3></div>
                  
                <div>Please enter a new IP Address: <input type="text" name="new_ip" value="${device_description['ip']['val']}"/> </div>
                <div>Please enter the IP Address of the gateway serving the Exterity homepage: <input type="text" name="web_url" value="192.168.1.14"/> </div>
                <div>Please enter a device name: <input type="text" name="name" value="${device_description['name']['val']}"/></div>
                <div>Please enter a device location: 
                    <select name = "location">
                        <option name = 'Rack' class = "OptNorm" value = "Rack">Rack</option>
                        <option name = 'Livingroom' class = 'OptNorm' value ="Livingroom">Livingroom</option>
                        <option name = 'Bedroom' class = 'OptNorm' value = "Kitchen">Kitchen</option>
                        <option name = 'Diningroom' class = 'OptNorm' value = "Bedroom">Bedroom</option>
                    </select>
                </div>
                <button type="submit" name="action" value="exterity_done">Done</button>
            </div>            
            <div py:if='device_description["type"]["val"] == "Skybox"' py:strip="True">
                <div><h3>Skybox provisoning</h3></div>
                    <input type="text" name="skyTx" style="visibility:hidden;" value="${device_description['txid']['val']}" />
                    <input type="text" name="skyRx" style="visibility:hidden;" value="${device_description['rxid']['val']}" />
                    <div>Please enter a new IP Address for Skybox RS232 (Receiver): <input type="text" name="skyRxip" value="${device_description['rxip']['val']}"/> </div>
                    <div>Please enter a new IP Address for Dusky Controller (Transmitter): <input type="text" name="skyTxip" value="${device_description['txip']['val']}"/> </div>
                    <div>Please enter a device name: <input type="text" name="name" value="${device_description['name']['val']}"/></div>
                    <div>Please enter a device location: 
                        <select name = "location">
                            <option name = 'Rack' class = "OptNorm" value = "Rack">Rack</option>
                            <option name = 'Livingroom' class = 'OptNorm' value ="Livingroom">Livingroom</option>
                            <option name = 'Bedroom' class = 'OptNorm' value = "Kitchen">Kitchen</option>
                            <option name = 'Diningroom' class = 'OptNorm' value = "Bedroom">Bedroom</option>
                        </select>
                    </div>
                    <br/>
                    <button type="submit" name="action" value="skybox_done">Done</button>
            </div>
             
            <div py:if='device_description["type"]["val"] == "Startech"' py:strip="True">
                <div py:if='startechtype == ""' py:strip="True">
                    <div><h3>Startech RS232 Over IP adapter provisoning</h3></div>
                    
                    <div>Selected Startech adapter is : ${device_description['ip']['val']}</div>
                    <div>Please select the device connected to this adapter: 
                        <select name = "devicetype">
                        <option name = "NAD Visio 5" class = "OptNorm">NAD Visio 5</option>
                        <option name = "Lutron Homeworks" class = 'OptNorm'>Lutron Homeworks</option>
                        <option name = "Skybox" class = 'OptNorm'>Skybox</option>
                        </select>
                    </div>
                    <br/>
                    <button type="submit" name="action" value="Startech_Type_Chosen">Next</button>
                </div>
 
                <div py:if='startechtype == "NAD Visio 5"' py:strip="True">
                    <div><h3>NAD 5 Provisioning</h3></div>
               
                    <div>Please enter a new IP Address: <input type="text" name="new_ip" value="${device_description['ip']['val']}"/> </div>
                    <div>Please enter a device name: <input type="text" name="name" value="${device_description['name']['val']}"/></div>
                    <div>Please enter a device location: 
                        <select name = "location">
                        <option name = 'Rack' class = "OptNorm" value = "Rack">Rack</option>
                        <option name = 'Livingroom' class = 'OptNorm' value ="Livingroom">Livingroom</option>
                        <option name = 'Bedroom' class = 'OptNorm' value = "Kitchen">Kitchen</option>
                        <option name = 'Diningroom' class = 'OptNorm' value = "Bedroom">Bedroom</option>
                        </select>
                    </div>
                    <br/>
                    <button type="submit" name="action" value="NAD5_done">Done</button>
                </div>              
 
                <div py:if='startechtype == "Lutron Homeworks"' py:strip="True">
                    <div><h3>Lutron Controller Provisioning</h3></div>
                    <br/>
                    <div>Please enter a new IP Address: <input type="text" name="new_ip" value="${device_description['ip']['val']}"/> </div>
                    <div>Please enter a device name: <input type="text" name="name" value="${device_description['name']['val']}"/></div>
                    <div>Please enter a device location: 
                        <select name = "location">
                         <option name = 'Rack' class = "OptNorm" value = "Rack">Rack</option>
                        <option name = 'Livingroom' class = 'OptNorm' value ="Livingroom">Livingroom</option>
                        <option name = 'Bedroom' class = 'OptNorm' value = "Kitchen">Kitchen</option>
                        <option name = 'Diningroom' class = 'OptNorm' value = "Bedroom">Bedroom</option>
                        </select>
                    </div>
                    <br/>
                    <button type="submit" name="action" value="lutron_done">Done</button>
                </div>  
                
                <div py:if='startechtype == "Skybox"' py:strip="True">
                    <div><h3>Skybox provisoning</h3></div>
                    <input type="text" name="device_one_id" style="visibility:hidden;" value="${device_description['id']['val']}" />
                    
                    <div>Please select a transmit and receive pair for the Skybox</div>
                    <br/>
                    <div>The currently selected device is : ${device_description['ip']['val']} </div>
                    <div>The currently selected device type is : 
                        <select name = 'device_one_type'>
                            <option name = "DuskyTx" class = "OptNorm" value = "skyTx">Dusky Controller (Transmitter)</option>
                            <option name = "SkyRx" class = "OptNorm" value = "skyRx">Direct Skybox RS232 Connection (Receiver)</option>
                        </select>
                    </div>
                    <br/>
                    <div>The other device is : 
                        <select name = 'device_two_id'>
                            <tr py:for='rs232 in startechdevices'>
                                <option name = "${rs232['name']['val']}" class = "OptNorm" value = "${rs232['id']['val']}">${rs232['name']['val']}</option>
                            </tr>
                        </select>
                    </div>
                    <div>The other device type is : 
                        <select name = 'device_two_type'>                            
                            <option name = "SkyRx" class = "OptNorm" value = "skyRx">Direct Skybox RS232 Connection (Receiver)</option>
                            <option name = "DuskyTx" class = "OptNorm" value = "skyTx">Dusky Controller (Transmitter)</option>
                        </select>
                    </div>
                    
                    <br/>                 
                    <button type="submit" name="action" value="Skybox_Paired">Next</button>
                   
                </div>
                
                <div py:if='startechtype == "Dusky Sky Controller"' py:strip="True">
                    <input type="text" name="skyTx" style="visibility:hidden;" value="${device_description['id']['val']}" />
                    <div><h3>Skybox provisoning</h3></div>

                    <div>Please select the Startech adapter connected to the corresponding Skybox RS232 port :
                        <br/>
                        <select name = "skyRx">
                            <tr py:for='rs232 in startechdevices'>
                                <option name = "${rs232['name']['val']}" class = "OptNorm" value = "${rs232['id']['val']}">${rs232["name"]["val"]}</option>
                            </tr>
                        </select>    
                    </div>
                    <br/>
                    <button type="submit" name="action" value="Skybox_Paired">Next</button>
                </div>
            
            </div>
        </form>
    </div>

</html>
