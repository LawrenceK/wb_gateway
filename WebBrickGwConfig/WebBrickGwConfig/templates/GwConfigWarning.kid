<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="'layout.kid'" >
        
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}contentbox'" id="contentbox">
        <form name="GwConfigWarning" action="/wbgwcnf/GwConfigSteps" method="get">
            <br/>
            You are about to start configuring your Armour IP System. 
            <br/>
            <br/>
            Please only proceed if you know what you are doing. 
            <br/>
            <br/>
            <button type="submit" name="action" value="continue" >Proceed</button>
        </form>
    </div>

</html>
