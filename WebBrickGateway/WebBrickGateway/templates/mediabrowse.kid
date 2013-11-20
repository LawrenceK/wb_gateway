<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<?python 
import urllib, string
from urllib import quote
# helper to turn an item into a display string.
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
            <wb:simpleLink class="objCenter" target='/media/client?rid=${rid}' py:content='name'/>
            <span py:for="bt in breadcrumb">
                <wb:simpleLink py:if="bt[0]" class="objCenter" target ='/media/list?id=${urllib.quote(bt[1])}&amp;rid=${urllib.quote(rid)}&amp;offset=0&amp;limit=${limit}' py:content='bt[0]'/>
            </span>
            <wb:simpleLink class="objCenter" width="10%" target="/media/list?rid=${rid}&amp;id=&amp;offset=0&amp;limit=${limit}">Top</wb:simpleLink>
            <wb:simpleLink class="objCenter" width="10%" target="">Up</wb:simpleLink>
        </tr>
        <tr class="rule"><td colspan='4' class="ruleBar">&nbsp;</td></tr>
    </table>
    <table class="navTable">
        <tr>
            <col width="20%" />
            <col width="20%" />
            <col width="20%" />
            <col width="20%" />
            <col width="20%" />
            <wb:simpleLink 
                    py:if='offset&gt;0'
                    target='/media/list?id=${urllib.quote(id)}&amp;rid=${urllib.quote(rid)}&amp;offset=0&amp;limit=${limit}'
                    >
                First
            </wb:simpleLink>
            <td py:if='offset==0'>&nbsp;</td>
            <wb:simpleLink 
                    py:if='offset&gt;0'
                    target='/media/list?id=${urllib.quote(id)}&amp;rid=${urllib.quote(rid)}&amp;offset=${offset-limit}&amp;limit=${limit}'
                    >
                Previous
            </wb:simpleLink>
            <td py:if='offset==0'>&nbsp;</td>
            <td>&nbsp;</td>
            <wb:simpleLink
                    py:if='offset+count&lt;total'
                    target='/media/list?id=${urllib.quote(id)}&amp;rid=${urllib.quote(rid)}&amp;offset=${offset+limit}&amp;limit=${limit}'
                    >
                Next
            </wb:simpleLink>
            <td py:if='offset+count&gt;=total'>&nbsp;</td>
            <wb:simpleLink 
                    py:if='offset+count&lt;total'
                    target='/media/list?id=${urllib.quote(id)}&amp;rid=${urllib.quote(rid)}&amp;offset=${total-limit}&amp;limit=${limit}'
                    >
                Last
            </wb:simpleLink>
            <td py:if='offset+count&gt;=total'>&nbsp;</td>
        </tr>
    </table>

    <table>
        <tr py:for='item in items'>
            <!-- this is intended to be a clear queue and add -->
            <wb:simpleButton 
                    py:if='item["canQueue"]'
                    wbTarget='/media/queue?id=${urllib.quote(item["id"])}&amp;rid=${urllib.quote(rid)}'
                    baseClassName="queue"
                    >&nbsp;</wb:simpleButton>
            <!-- this is something that can be played directly, maybe all should have it -->
            <!-- If the item is a container then we clear the queue and add and play -->
            <wb:simpleButton 
                    py:if='item["canPlay"]'
                    wbTarget='/media/play?id=${urllib.quote(item["id"])}&amp;rid=${urllib.quote(rid)}'
                    baseClassName="play"
                    >&nbsp;</wb:simpleButton>
            <wb:simpleLink
                    py:if='item["isContainer"]'
                    target='/media/list?id=${urllib.quote(item["id"])}&amp;rid=${urllib.quote(rid)}&amp;offset=0&amp;limit=${limit}'
                    py:content='item_string(item)'>
                The title of the item (artist album title)
            </wb:simpleLink>
            <td
                    class="textPresent"
                    py:if='not item["isContainer"]'
                    py:content='item_string(item)'>
                The title of the item (artist album title)
            </td>
        </tr>
    </table>

</body>

</html>
