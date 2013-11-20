<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/">
    <head>
        <title>Webbrick home automation</title>
        <link href="/static/css/userinterface.css" rel="stylesheet" type="text/css" />
    </head>
    <body>
        <div id="background">
            <div id="backgroundscatter">&nbsp;</div>
        </div>
        <div id="content">
        <h1>User Interface Preferences</h1>
        <p>
            Clicking on the following items will set the preffered interface for the browser type that 
            you are currently using to view this page with. So if you are viewing this page with Firefox
            you are setting the Interface preferences for ANY Firefox browser, not just the one on your PC.
        </p>
        <table>
            <colgroup span="4" width="25%"></colgroup>
            
    <!--    
        <tr>
            <td class="select_item"> <a href="/userinterface/change?alinksonly=yes">Use ALinks Only</a></td>
            <td class="select_item"> <a href="/userinterface/change?alinksonly=no">Allow OnClick</a></td>
        </tr>
    -->    
        <!-- auto fill this section with user templates sets -->
        <tr>
            <th class="sub_heading" colspan="4">Desktop Skins</th>
        </tr>
        <tr>
            <td class="select_item"> <a href="/userinterface/change?templateModule=templates.square">Square Skin</a></td>
            <td class="select_item"> <a href="/userinterface/change?templateModule=templates.round">Round Skin</a></td>
            <td class="select_item"> <a href="/userinterface/change?templateModule=templates.tabbed">Tabbed Skin</a></td>
            <td class="select_item"> <a href="/userinterface/change?templateModule=templates">Legacy Skin</a></td>
        </tr>
        <tr>
            <td class="select_item" colspan="4"> &nbsp;</td>
        </tr>
        <tr>
            <th class="sub_heading" colspan="4">Mobile Skins</th>
        </tr>
        <tr>
            <td class="select_item"> <a href="/userinterface/change?templateModule=templates.square.itouch">Square iTouch Skin</a></td>
            <td class="select_item"> <a href="/userinterface/change?templateModule=templates.round.itouch">Round iTouch Skin</a></td>
            <td class="select_item"> <a href="/userinterface/change?templateModule=templates.tabbed.itouch">Tabbed iTouch Skin</a></td>
            <td class="select_item"> <a href="/userinterface/change?templateModule=templates.mobile">Legacy Mobile Skin</a></td>
        </tr>
        <tr>
            <td class="select_item" colspan="4"> &nbsp;</td>
        </tr>
        <tr>
            <th class="sub_heading" colspan="4">Further Settigns</th>
        </tr>
        
        <tr>
            <td class="select_item" colspan="1"> &nbsp;</td>
            <td class="select_item"> <a href="/userinterface/change?javascript=yes">JavaScript Yes</a></td>
            <td class="select_item"> <a href="/userinterface/change?javascript=no">JavaScript No</a></td>
            <td class="select_item" colspan="1"> &nbsp;</td>
        </tr>
        <tr>
            <td class="select_item" colspan="1"> &nbsp;</td>
            <td class="select_item"> <a href="/userinterface/change?flash=yes">Macromedia Flash Yes</a></td>
            <td class="select_item"> <a href="/userinterface/change?flash=no">Macromedia Flash No</a></td>
            <td class="select_item" colspan="1"> &nbsp;</td>
        </tr>
        <tr>
            <td class="select_item" colspan="4"> &nbsp;</td>
        </tr>
        <tr>
            <td class="select_item" colspan="1"> &nbsp;</td>
            <td class="select_item" colspan="2"> <a id="done_button" href="/">Done</a></td>
            <td class="select_item" colspan="1"> &nbsp;</td>
        </tr>
        
    <!--    
        <tr>
            <td class="select_item"> <a href="/userinterface/change?templateModule=WebBrickGateway.templates">WebBrickGateway.templates</a></td>
            <td class="select_item"> <a href="/userinterface/change?templateModule=WebBrickGateway.templates.flash">WebBrickGateway.templates.flash</a></td>
            <td class="select_item"> <a href="/userinterface/change?templateModule=WebBrickGateway.templates.snom">WebBrickGateway.templates.snom</a></td>
            <td class="select_item"> <a href="/userinterface/change?templateModule=WebBrickGateway.templates.simple">WebBrickGateway.templates.simple</a></td>
        </tr>
    -->
    <!--    
        <tr>
            <td class="select_item"> <a href="/userinterface/change?tgformat=xml">XML</a></td>
            <td class="select_item"> <a href="/userinterface/change?tgformat=xhtml">xHTML</a></td>
            <td class="select_item"> <a href="/userinterface/change?tgformat=html">HTML</a></td>
        </tr>
    -->
    </table>
    </div>
    </body>

</html>
