<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_armour

?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="'layout.kid'" 
        py:extends="WebBrickGateway.templates.widgets_armour">
        
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}contentbox'" id="contentbox">
       <!-- This si where the actual page content goes-->
       <table>
            <tr>
                <td> Box1
                </td>
                <td>Box2
                </td>
                <td>Box3
                </td>
            </tr>
            <tr>
                <td>Box4
                </td>
                <td>Box5
                </td>
                <td>Box6
                </td>
            </tr>
        </table>
    </div>

</html>
