<?python
error = ""
?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="'layout.kid'" >
        
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}contentbox'" id="contentbox">
        <form name="GwConfigError" action="/wbgwcnf/GwConfigSteps" method="get">
            <!-- Error Message --> 
            <div> Error! </div>
            <div> The following Error occured: "${error}" </div>
            <button type="submit" name="action" value="continue" >Continue</button>
        </form>
    </div>

</html>
