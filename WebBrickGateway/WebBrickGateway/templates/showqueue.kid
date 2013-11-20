<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<?python 
import urllib, string
from urllib import quote
# helper to turn a media item into a display string.
def item_string( itm ):
    return string.join( [itm[k] for k in ('artist','creator','album','title') if itm.has_key(k) and itm[k] ], "/" )
    #return "%s/ %s/ %s" % (itm.get('artist', ''), itm.get('album', ''), itm.get('title', '') )
?>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/" 
    py:extends="'master.kid'">

${output_head( "Track Browse" )}

<body>

<!-- override some of the styles -->
<link href="/static/css/media.css" rel="stylesheet" type="text/css" />

    <table class="navTable">
        <tr>
            <wb:simpleLink width="6%" class="objCenter" target="/">Home</wb:simpleLink>
            <td class="infoBar" id="menuTitle">
                Current Queue
            </td>
            <wb:simpleLink class="objCenter" target='/media/client?rid=${rid}' py:content='name'/>
            <wb:simpleLink width="10%" target="/media/playqueue?rid=${rid}">Play Queue</wb:simpleLink>
            <wb:simpleLink width="10%" target="/media/clearqueue?rid=${rid}">Clear Queue</wb:simpleLink>
        </tr>
        <tr class="rule"><td colspan='4' class="ruleBar">&nbsp;</td></tr>
    </table>

    <table>
        <tr py:for='item in items'>
        <td
                class="textPresent"
                py:content='item_string(item)'>
            The title of the item (artist album title)
        </td>
<!--
        <wb:simpleButton 
                wbTarget='/media/deletefromqueue?id=${urllib.quote(item["id"])}&amp;rid=${urllib.quote(rid)}'
                >Delete</wb:simpleButton>
-->
        </tr>
    </table>

</body>

</html>
