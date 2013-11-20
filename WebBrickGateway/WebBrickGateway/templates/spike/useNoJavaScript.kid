<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<?python
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
      xmlns:wb="http://id.webbrick.co.uk/">

<?python
if tg.useragent.browser in ['msie', 'firefox']:
    javascript = 'yes'
else:
    javascript = 'no'
?>

<td py:if="javascript != 'yes' and item.tag=='{http://id.webbrick.co.uk/}simpleLink'" class="navBarSmall">
    <a href="${item.get('target')}">
        ${item.text}
        ${item.getchildren()}
    </a>
</td>

<td py:if="javascript != 'yes' and item.tag=='{http://id.webbrick.co.uk/}textDisplay'" 
        py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
            wbLoadX='loadTextDisplay(&apos;${item.get("prefix")}&apos;,&apos;${item.get("postfix")}&apos;)'
            width="${item.get('width')}"
            >
    Text
</td>

<td py:if="javascript != 'yes' and item.tag=='{http://id.webbrick.co.uk/}numericDisplay'" 
        py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
            wbLoadX='loadNumericDisplay(&apos;${item.get("prefix")}&apos;,&apos;${item.get("format")}&apos;,&apos;${item.get("postfix")}&apos;)'
            width="${item.get('width')}"
            >
    Number
</td>

</html>
