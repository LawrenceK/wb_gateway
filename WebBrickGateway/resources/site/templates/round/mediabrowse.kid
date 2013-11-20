<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round

layout_params['left_title'] = ""
layout_params['show_left'] = True
layout_params['top_title'] = " "
layout_params['show_bottom'] = False

import string, urllib
# helper to turn an item into a display string.
def item_string( itm ):
    return string.join( [itm[k] for k in ('artist','creator','album','title') if itm.has_key(k) and itm[k] ], "/" )

?>

<html py:layout="'sitelayout3.kid'" xmlns:py="http://purl.org/kid/ns#"  xmlns:wb="http://id.webbrick.co.uk/" 
        py:extends="WebBrickGateway.templates.widgets_round, 'zone_lists' ">
        
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}leftboxcontent'" id="leftboxcontent">
        <ul class="divider29px">
            <li>
                <wb:simpleLinkList class="objCenter" target='/media/client?rid=${rid}' py:content='name'/>
            </li>
            <span py:for="bt in breadcrumb" py:if="bt[0]" py:strip="True">
                <li>
                    <wb:simpleLinkList class="objCenter" target ='/media/list?id=${urllib.quote(bt[1])}&amp;rid=${urllib.quote(rid)}&amp;offset=0&amp;limit=${limit}' py:content='bt[0]'/>
                </li>
            </span>
<!--            
            <li>
                <wb:simpleLinkList class="objCenter" width="10%" target="/media/list?rid=${rid}&amp;id=&amp;offset=0&amp;limit=${limit}">Top</wb:simpleLinkList>
            </li>
-->            
<!--           
            <li>
                <wb:simpleLinkList class="objCenter" width="10%" target="">Up</wb:simpleLinkList>
            </li>
-->            
        </ul>
    </div>

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}topboxcontent'" id="topboxcontent">
        <!-- Insert content for top right box in here -->
        <h1>
            <wb:simpleLinkList
                target='/media/list?id=${urllib.quote(id)}&amp;rid=${urllib.quote(rid)}&amp;offset=0&amp;limit=${limit}'
                iconimage='rect8pxlistwtitle/pagefirst.png' />
            <wb:simpleLinkList
                target='/media/list?id=${urllib.quote(id)}&amp;rid=${urllib.quote(rid)}&amp;offset=${offset-limit}&amp;limit=${limit}'
                iconimage='rect8pxlistwtitle/pageprev.png' />
            <wb:simpleLinkList
                target='/media/list?id=${urllib.quote(id)}&amp;rid=${urllib.quote(rid)}&amp;offset=${offset+limit}&amp;limit=${limit}'
                iconimage='rect8pxlistwtitle/pagenext.png' />
            <wb:simpleLinkList
                target='/media/list?id=${urllib.quote(id)}&amp;rid=${urllib.quote(rid)}&amp;offset=${total-limit}&amp;limit=${limit}'
                iconimage='rect8pxlistwtitle/pagelast.png' />
        </h1>

        <div>
            <wb:simpleButton 
                    py:if='items and items[0]["canQueue"]'
                    iconimage='smallQueue.png'
                    wbTarget='/media/queue?id=${urllib.quote(id)}&amp;rid=${urllib.quote(rid)}'
                    baseClassName="queue"
                    >Add all to Queue</wb:simpleButton>
            <wb:simpleButton 
                    py:if='items and items[0]["canPlay"]'
                    iconimage='smallPlay.png'
                    wbTarget='/media/play?id=${urllib.quote(id)}&amp;rid=${urllib.quote(rid)}'
                    baseClassName="play"
                    >Clear Q and Add All</wb:simpleButton>
        </div>
        <div style="clear:both"></div>
        
        <div>
            <ul class="divider29px">
                <li py:for='item in items'>
                    <wb:simpleLinkList
                            py:if='item["isContainer"]'
                            target='/media/list?id=${urllib.quote(item["id"])}&amp;rid=${urllib.quote(rid)}&amp;offset=0&amp;limit=${limit}'
                            py:content='item_string(item)'>
                        The title of the item (artist album title)
                    </wb:simpleLinkList>
                    <wb:simpleAction
                            py:if='not item["isContainer"] and item["canQueue"]'
                            wbTarget='/media/queue?id=${urllib.quote(item["id"])}&amp;rid=${urllib.quote(rid)}'
                            baseClassName="action"
                            py:content='item_string(item)'>
                        The title of the item (artist album title)
                    </wb:simpleAction>
                    <wb:simpleAction
                            py:if='not item["isContainer"] and not item["canQueue"] and item["canPlay"]'
                            wbTarget='/media/play?id=${urllib.quote(item["id"])}&amp;rid=${urllib.quote(rid)}'
                            baseClassName="action"
                            py:content='item_string(item)'>
                        The title of the item (artist album title)
                    </wb:simpleAction>
                    <span
                            class="textPresent"
                            py:if='not item["isContainer"] and not item["canQueue"] and not item["canPlay"]'
                            py:content='item_string(item)'>
                        The title of the item (artist album title)
                    </span>
                </li>
            </ul>
        </div>
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        <!-- Insert content for bottom right box in here -->
        Bottom Content
    </div>

</html>
