<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<?python 
import sitetemplate
def getCurrentValue( uri ):
    """
    attempt to retrieve the current value of the uri passed
    """
    try:
        from WebBrickLibs.WbAccess import GetHTTPXmlDom
        from MiscLib.DomHelpers import getNamedNodeText
        dom = GetHTTPXmlDom( "localhost:8080", uri )    # need to know self address
        return getNamedNodeText(dom, 'val')
    except:
        from logging import getLogger
        getLogger( "WebBrickGateway.kid.useNoJavaScript" ).exception( "getCurrentValue" )
    return ''
?>

<html xmlns="http://www.w3.org/1999/xhtml" 
      xmlns:py="http://purl.org/kid/ns#" 
      xmlns:ui="ui" 
      xmlns:wb="http://id.webbrick.co.uk/"
      py:extends="sitetemplate" >

<head py:def="output_head(title)">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${title}</title>
    <link href="/static/css/panel_nojs.css" rel="stylesheet" type="text/css" />
</head>

<table py:def="output_nav( location )" class="navTable">
    <tr>
        <wb:simpleLink width="20%" target="/">Home Menu</wb:simpleLink>
        <td class="infoBar" id="menuTitle">${location}</td>
        <!-- !Needs conversion for non javascript -->
            <td width="12%" class="navBarSmall">
                <a href = "javascript:history.back()">Back</a>
            </td>
            <td width="12%" class="navBarSmall">
                <a href="javascript:location.reload()">Refresh</a>
            </td>
        <wb:simpleLink width="12%" target="/template/guide">Guide</wb:simpleLink>
    </tr>
    <tr class="rule"><td colspan='4' class="ruleBar">&nbsp;</td></tr>
</table>

<!-- The default site/location info bar -->
<table py:def="output_site_info_bar()" class="infoTable">
  <tr>
    <wb:textDisplay width='20%' wbSource="/local/time" prefix="" postfix="">Left</wb:textDisplay>
    <wb:textDisplay wbSource="/local/messages" prefix="" postfix="">Middle</wb:textDisplay>
    <wb:numericDisplay wbSource="/wbsts/test/Tmp/0" prefix="" format="##.#" postfix="&ordm;C">Right</wb:numericDisplay>
  </tr>
</table>

<!-- for debugging what is not happening it can be usefull to see dictionaries at various points try self.__dict__ -->
<table py:def="output_dictionary( dct )">
    <tr py:for="ky in dct">
        <td>${ky}</td>
        <td py:if="isinstance( dct[ky], dict )" >${output_dictionary(dct[ky])}</td>
        <td py:if="not isinstance( dct[ky], dict )" >${str(dct[ky])}</td>
    </tr>
</table>


<span py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:strip="" >

    <body
            py:attrs="item.items()">
        <div py:if="item.get('header')!='No'">
            <div py:if="tg_flash" class="flash" py:content="tg_flash"></div>
        </div>
        <div py:replace="[item.text] + item[:]"/>
    </body>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}simpleLink'" py:strip="" >
    <td
                colspan="${item.get('colspan')}"
                width="${item.get('width')}"
                class="navBarSmall">
        <a href="${item.get('target')}">
            ${item.text}
            ${item.getchildren()}
        </a>
    </td>
</span>


<!-- entity conversion -->
<span py:match="item.tag=='{http://id.webbrick.co.uk/}textDisplay'" py:strip="" >
    <td
            py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
                wbLoadX='loadTextDisplay(&apos;${item.get("prefix")}&apos;,&apos;${item.get("postfix")}&apos;)'
                width="${item.get('width')}"
                colspan="${item.get('colspan')}"
                class="textdisplay"
                >
        Text
    </td>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}numericDisplay'" py:strip="" >
    <td
            py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
                wbLoadX='loadNumericDisplay(&apos;${item.get("prefix")}&apos;,&apos;${item.get("format")}&apos;,&apos;${item.get("postfix")}&apos;)'
                width="${item.get('width')}"
                colspan="${item.get('colspan')}"
                class="numericdisplay"
                >
        Number
    </td>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}simpleButton'" py:strip="" >

    <td
            width="${item.get('width')}"
            colspan="${item.get('colspan')}"
            class="button"
        >
        <a href="${item.get('wbTarget')}"
            py:content="item.text"
        >
            Button
        </a>
    </td>

</span>

</html>
