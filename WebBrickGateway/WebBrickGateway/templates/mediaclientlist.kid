<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/" 
    py:extends="'master.kid'">

${output_head( "Media List" )}

<body>
    ${output_nav("Media Client List")}
    <table>
        <tr py:for='k in clients'>
            <!-- the id allows for the select of a renderer to play a track on -->
	    <wb:simpleLink
                target='/media/client?rid=${k}&amp;id=${id}'
                py:content='"Control %s" %(clients[k])'></wb:simpleLink>
            <wb:simpleLink width="10%" target="/media/zonelink?rid=${k}"
                py:content='"Link Zones to %s" % (clients[k])'/>
            <wb:simpleButton wbTarget='/media/dozoneunlink?target=${k}'
                py:content='"UnLink %s from ZoneGroup" % (clients[k])'/>
            <wb:simpleButton wbTarget='/media/dozonelinkall?rid=${k}'
                py:content='"Link All Zones To %s" % (clients[k])' />
        </tr>
        <tr>
            <td/>
            <td/>
            <td/>
            <wb:simpleButton wbTarget='/media/dozoneunlinkall'>
                UnLink All Zones
            </wb:simpleButton>
        </tr>
    </table>

</body>
</html>
