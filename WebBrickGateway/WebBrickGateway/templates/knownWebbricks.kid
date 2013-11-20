<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:ui="ui" 
    py:extends="'master.kid'">

${output_head( "Known WebBricks" )}

<body>

<script language="javascript">
    reloadTimer = 30 ;
    pollerInterval = 30 ;
</script>
    
${output_nav("Known WebBricks")}

    <table>
        <tr py:for="wb in webbricks" 
                    py:if="wb['status'] and wb['name'] != '???'"
                    onclick="window.open( '/wbproxy/${wb['ipAdr']}', '${wb['name']}' )" class="WbEvents${wb['status']}">
            <td py:content="wb['ipAdr']"/>
            <td py:if="wb['status']">
                No UDP
            </td>
            <td py:if="not wb['status']">
                Ok
            </td>
            <td py:content="wb['name']"/>
            <td py:content="wb['version']"/>
            <td py:content="wb['time']"/>
            <td py:content="wb['event']"/>
        </tr>

        <tr py:for="wb in webbricks" 
                    py:if="wb['status'] and wb['name'] == '???'"
                    onclick="window.open( '/wbproxy/${wb['ipAdr']}', '${wb['name']}' )" class="WbEvents${wb['status']}">
            <td py:content="wb['ipAdr']"/>
            <td py:if="wb['status']">
                No UDP
            </td>
            <td py:if="not wb['status']">
                Ok
            </td>
            <td py:content="wb['name']"/>
            <td py:content="wb['version']"/>
            <td py:content="wb['time']"/>
            <td py:content="wb['event']"/>
        </tr>

        <tr py:for="wb in webbricks" 
                    py:if="not wb['status']"
                    onclick="window.open( '/wbproxy/${wb['ipAdr']}', '${wb['name']}' )" class="WbEvents${wb['status']}">
            <td py:content="wb['ipAdr']"/>
            <td py:if="wb['status']">
                No UDP
            </td>
            <td py:if="not wb['status']">
                Ok
            </td>
            <td py:content="wb['name']"/>
            <td py:content="wb['version']"/>
            <td py:content="wb['time']"/>
            <td py:content="wb['event']"/>
        </tr>
    </table>

    ${output_site_info_bar()}

</body>

</html>
