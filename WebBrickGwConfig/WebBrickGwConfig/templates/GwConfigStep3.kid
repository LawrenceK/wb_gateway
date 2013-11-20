<?python
#layout_params['page_title'] = ""
layout_params['page_heading'] = "Step 3 - Build UI"

message = ""
?>
<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="'layout.kid'" >
        
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}contentbox'" id="contentbox">
    
        <div id="topFade" />
        <div id="leftFade" />
        <div id="rightFade" />
        <div id="contentboxBottom">
            <div id="botFade" />
        </div>
    
        <form class="leftBox" name="GwConfigStep3" action="/wbgwcnf/GwConfigStep3Action" method="post">
             <button type="submit" name="action" value="buildUI">Build UI</button>
             <button type="submit" name="action" value="done">Done</button>   
             <a href="/sendevent/restart?type=gateway"> Restart Gateway </a>
        </form>
        
        
        
        <div id="serverMessage">
            <div py:for="msg in message">
                 <div>${msg}</div>
            </div>
        </div>

    </div>

</html>
