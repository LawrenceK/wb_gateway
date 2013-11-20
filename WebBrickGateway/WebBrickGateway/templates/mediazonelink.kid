<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" 
    xmlns:wb="http://id.webbrick.co.uk/" 
    py:extends="'master.kid'">

${output_head( name )}

<body>

<!-- override some of the styles -->
<link href="/static/css/media.css" rel="stylesheet" type="text/css" />


    ${output_nav(name)}
    
    <table>
        <tr py:for='k in clients'>
            <td class="textPresent" py:content='"Link %s To " % (clients[k])' />
            <wb:simpleButton wbTarget='/media/dozonelink?rid=${rid}&amp;target=${k}'
                py:content='name'/>
        </tr>
    </table>

    ${output_site_info_bar()}

</body>

</html>
