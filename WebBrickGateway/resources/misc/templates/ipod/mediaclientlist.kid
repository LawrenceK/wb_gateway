<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<?python 
kid.enable_import()
import WebBrickGateway.templates.master_no_td
?>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/" 
    py:extends="WebBrickGateway.templates.master_no_td">

${output_head( "Media List" )}

<body>
    ${output_nav("Media Client List")}
    <table>
        <tr py:for='k in clients'>
            <!-- the id allows for the select of a renderer to play a track on -->
            <td>
                <wb:simpleLink
                    target='/media/client?rid=${k}&amp;id=${id}'
                    py:content='"Control %s" %(clients[k])'></wb:simpleLink>
            </td>
            <td>
                <wb:simpleLink width="10%" target="/media/zonelink?rid=${k}"
                    py:content='"Link Zones to %s" % (clients[k])'/>
            </td>
            <td>
                <wb:simpleButton wbTarget='/media/dozoneunlink?target=${k}'
                    py:content='"UnLink %s from ZoneGroup" % (clients[k])'/>
            </td>
            <td>
                <wb:simpleButton wbTarget='/media/dozonelinkall?rid=${k}'
                    py:content='"Link All Zones To %s" % (clients[k])' />
            </td>
        </tr>
        <tr>
            <td/>
            <td/>
            <td/>
            <td>
                <wb:simpleButton wbTarget='/media/dozoneunlinkall'>
                    UnLink All Zones
                </wb:simpleButton>
            </td>
        </tr>
    </table>

</body>
</html>
