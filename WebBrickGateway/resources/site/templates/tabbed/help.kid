<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_tabbed
?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="sitelayout.kid" 
        py:extends="WebBrickGateway.templates.widgets_tabbed">

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}tabcontent'" id="helpcontent">

    <h1>Help and Assistance</h1>
    <p>
        This system manages the following plant:
        <ul>
            <li>Air Source Heat Pump, in lag heating, primary heating and cooling modes</li>
            <li>Gas Boiler, both lead and primary heat source</li>
            <li>Vilavent Heat Recovery Units</li>
            <li>Hot Water, temperature, circulation and storage</li>
            <li>Heat to Under Floor Heating <i>UFH</i> circuit, valves and pump (each room is controlled by another system)</li>
            <li>Heat to towel rail circuit valves and pump</li>
        </ul>
    </p>


        
        <div id="contacts">
            <p><b>Evinox Support</b> 01372 722277</p>
            <p><b>Octagon Support</b> 020 8481 7500</p>
        </div>
        
    </div>
    
</html>
