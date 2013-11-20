<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_no_td
?>

<html py:layout="'sitelayout.kid'" xmlns:py="http://purl.org/kid/ns#"  xmlns:wb="http://id.webbrick.co.uk/" 
        py:extends="WebBrickGateway.templates.widgets_no_td">
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}leftbox'" id="leftbox">
        <!-- Insert content for left box in here -->
    </div>

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}topbox'" id="topbox">
        <!-- Insert content for top right box in here -->
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botbox'" id="botbox">
        <!-- Insert content for bottom right box in here -->
    </div>

</html>
