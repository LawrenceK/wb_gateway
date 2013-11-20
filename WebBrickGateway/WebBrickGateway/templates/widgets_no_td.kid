<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<?python 
def getCurrentValue( uri ):
    """
    attempt to retrieve the current value of the uri passed
    """
    try:
        from WebBrickLibs.WbAccess import GetHTTPXmlDom
        from MiscLib.DomHelpers import getNamedNodeText
        dom = GetHTTPXmlDom( "127.0.0.1:8080", uri )    # need to know self address
        if dom:
            return getNamedNodeText(dom, 'val')
    except:
        from logging import getLogger
        getLogger( "WebBrickGateway.templates.widgets" ).exception( "getCurrentValue %s " % (uri) )
    return ''
    
def getFlashMovie( item, default ):
    # generate the flash movie name
    flashMovie = item.get('flashMovie')
    if not flashMovie:
        flashMovie = default
    if not flashMovie.startswith( "/" ):
        flashMovie = "/static/flash/" + flashMovie
    return flashMovie
?>

<html xmlns="http://www.w3.org/1999/xhtml" 
      xmlns:py="http://purl.org/kid/ns#" 
      xmlns:wb="http://id.webbrick.co.uk/">

<!-- !for debugging what is not happening it can be usefull to see dictionaries at various points try self.__dict__ -->
<table py:def="output_dictionary( dct )">
    <tr py:for="ky in dct">
        <td>${ky}</td>
        <td py:if="isinstance( dct[ky], dict )" >${output_dictionary(dct[ky])}</td>
        <td py:if="not isinstance( dct[ky], dict )" >${str(dct[ky])}</td>
    </tr>
</table>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}simpleLink'" py:strip="" >
    <span py:if="flash == 'xxx'"
                wbType="FlashButton" 
                wbTarget="${item.get('target')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                title="${item.text}"
                flashMovie="/static/flash/SimpleISOButton2.swf"
                >
        ${item.text}
        ${item.getchildren()}
    </span>

    <span py:if="flash &lt;&gt; 'xxx' and javascript == 'yes'"
                onClick="window.location=&apos;${item.get('target')}&apos;" 
                class="navBarSmall" 

                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                >
        ${item.text}
        ${item.getchildren()}
    </span>
<!--    
    !<div py:if="flash &lt;&gt; 'xxx' and javascript == 'yes'"
                style="width:100%; height:100%; position:relative;"
                >
        <div class="backgroundimageactive" style="width:100%; height:100%; position:absolute; left:0px; top:0px; z-index:1; ">
            <img src="/static/images/UnSelectedBlue.png" style="width:100%; height:100%;" />
        </div>
        <div style="width:100%;position:absolute; left:0px; top:10%; vertical-align:middle; text-align:center;z-index:2; "
                onClick="window.location=&apos;${item.get('target')}&apos;" 
                class="navBarSmall" 
                wbType="simpleLink"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
            >
            ${item.text}
            ${item.getchildren()}
        </div>
    </div>
-->
    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="navBarSmall">
        <a href="${item.get('target')}">
            ${item.text}
            ${item.getchildren()}
        </a>
    </span>
</span>


<span py:match="item.tag=='{http://id.webbrick.co.uk/}textDisplay'" py:strip="" >
    <span py:if="javascript == 'yes'"
                wbType="Text" 
                wbLoad='loadTextDisplay(&apos;${item.get("prefix")}&apos;,&apos;${item.get("postfix")}&apos;)'
                wbSource="${item.get('wbSource')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                py:content="getCurrentValue( item.get('wbSource') )"
    />
    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="textPresent"
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    />
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}numericDisplay'" py:strip="" >
    <span py:if="javascript == 'yes'"
                wbType="Numeric" 
                wbLoad='loadNumericDisplay(&apos;${item.get("prefix")}&apos;,&apos;${item.get("format")}&apos;,&apos;${item.get("postfix")}&apos;)'
                wbSource="${item.get('wbSource')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    />
    <span py:if="javascript == 'no'"
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="numericInfo"
    />
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}numericEntry'" py:strip="" >
    <span py:if="javascript == 'yes'"
                wbType="WbNumericEntry"
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                wbLoad='loadWbNumericEntry(&apos;${item.get("prefix")}&apos;,&apos;${item.get("format")}&apos;,&apos;${item.get("postfix")}&apos;)'
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    >&nbsp;</span>
    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="numericInfo"
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    >&nbsp;</span>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}timeDisplay'" py:strip="" >
    <span py:if="javascript == 'yes'"
                wbType="WbTimeDisplay" 
                wbSource="${item.get('wbSource')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                py:content="getCurrentValue( item.get('wbSource') )"
    >--:--</span>
    <span py:if="javascript == 'no'"
                py:content="getCurrentValue( item.get('wbSource') )"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="numericInfo"
    >--:--</span>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}timeEntry'" py:strip="" >
    <span py:if="javascript == 'yes'"
                wbType="WbTimeEntry" 
                wbTitle="${item.get('wbTitle')}"
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                py:content="getCurrentValue( item.get('wbSource') )"
    >--:--</span>
    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="numericInfo"
                py:content="getCurrentValue( item.get('wbSource') )"
    >--:--</span>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}onoffEntry'" py:strip="" >
    <span py:if="javascript == 'yes'"
                wbType="WbOnOffEntry" 
                wbTitle="${item.get('wbTitle')}"
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                py:content="getCurrentValue( item.get('wbSource') )"
    >Ignore</span>
    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="WbOnOffEntry"
                py:content="getCurrentValue( item.get('wbSource') )"
    >Ignore</span>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}dayEntry'" py:strip="" >
    <span py:if="javascript == 'yes'"
                wbType="WbDayEntry" 
                wbTitle="${item.get('wbTitle')}"
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                py:content="getCurrentValue( item.get('wbSource') )"
    >-------</span>
    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="numericdisplay"
                py:content="getCurrentValue( item.get('wbSource') )"
    >-------</span>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}simpleButton'" py:strip="" >
    <span py:if="flash == 'xxx'"
                wbType="FlashButton" 
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('target')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                title="${item.text}"
                flashMovie="/static/flash/SimpleISOButton2.swf"
                >
        ${item.getchildren()}
    </span>

    <span py:if="flash &lt;&gt; 'xxx' and javascript == 'yes'"
                wbType="PushButton" 
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                py:content="[item.text] + item[:]"
                >
    </span>
<!--    
    !<div py:if="flash &lt;&gt; 'xxx' and javascript == 'yes'"
                style="width:100%; height:100%; position:relative;"
                >
        <div class="backgroundimageactive" style="width:100%; height:100%; position:absolute; left:0px; top:0px; z-index:1; ">
            <img src="/static/images/UnSelectedBlue.png" style="width:100%; height:100%;" />
        </div>
        <div style="width:100%;position:absolute; left:0px; top:0px; vertical-align:middle; text-align:center;z-index:2;" py:content="item.text"
                wbType="PushButton" 
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                baseClassName="${item.get('baseClassName')}"
            >&nbsp;
        </div>
    </div>
-->
    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
            class="button"
        >
        <a href="${item.get('wbTarget')}"
            py:content="[item.text] + item[:]"
        >
        </a>
    </span>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}flashButton'" py:strip="" >
    <span py:if="flash == 'yes' and javascript == 'yes'"
                wbType="FlashButton" 
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                title="${item.text}"
                flashMovie='${getFlashMovie(item,"SimpleISOButton.swf")}'
                >
    </span>

    <span py:if="flash &lt;&gt; 'yes' and javascript == 'yes'"
                wbType="PushButton" 
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                py:content="[item.text] + item[:]"
                >
    </span>

    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
            class="button"
        >
        <a href="${item.get('wbTarget')}"
            py:content="[item.text] + item[:]"
        >
        </a>
    </span>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}flashMeter'" py:strip="" >
    <span py:if="flash == 'yes' and javascript == 'yes'"
                wbType="FlashMeter" 
                wbSource="${item.get('wbSource')}"
                wbLoad='loadFlashMeter(&apos;${item.get("prefix")}&apos;,&apos;${item.get("format")}&apos;,&apos;${item.get("postfix")}&apos;)'
                labels="${item.get('labels')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                metertitle="${item.text}"
                minvalue="${item.get('minvalue')}"
                maxvalue="${item.get('maxvalue')}"
                curvalue="${item.get('curvalue')}"
                setlow="${item.get('setlow')}"
                sethigh="${item.get('sethigh')}"
                prefix="${item.get('prefix')}"
                postfix="${item.get('postfix')}"
                flashMovie='${getFlashMovie(item,"Simple270.swf")}'
                >
    </span>
    <span py:if="flash &lt;&gt; 'yes' and javascript == 'yes'"
                wbType="Numeric" 
                wbLoad='loadNumericDisplay(&apos;${item.get("prefix")}&apos;,&apos;${item.get("format")}&apos;,&apos;${item.get("postfix")}&apos;)'
                wbSource="${item.get('wbSource')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    />
    <span py:if="javascript == 'no'"
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="numericInfo"
    />
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}volumeControl'" py:strip="" >
    <span py:if="flash == 'yes' and javascript == 'yes'"
                wbType="volumeControl" 
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                >
    </span>
    <span py:if="flash &lt;&gt; 'yes' and javascript == 'yes'"
                wbType="WbNumericEntry"
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
    >&nbsp;</span>
    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="numericInfo"
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    >&nbsp;</span>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}flashDimmer'" py:strip="" >
    <span py:if="flash == 'yes' and javascript == 'yes'"
                wbType="FlashDimmer" 
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                labels="${item.get('labels')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                title="${item.text}"
                flashMovie='${getFlashMovie(item,"TestDimmer.swf")}'
                >
    </span>
    <span py:if="flash &lt;&gt; 'yes' and javascript == 'yes'"
                wbType="WbNumericEntry"
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                wbLoad='loadWbNumericEntry(&apos;${item.get("prefix")}&apos;,&apos;${item.get("format")}&apos;,&apos;${item.get("postfix")}&apos;)'
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    >&nbsp;</span>
    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="numericInfo"
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    >&nbsp;</span>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}dynamicImage'" py:strip="">
    <!-- !uses wbSource to display an image, wbSource specifies the URL of the image. -->
    <!-- !the width may have to be aplied to the image and not the TD -->
    <span 
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                align="center">
        <img py:if="javascript == 'yes'"
            wbType="DynamicImage"
            wbSource="${item.get('wbSource')}"
            src="${getCurrentValue(item.get('wbSource'))}" />
        <img py:if="javascript == 'no'"
            src="${getCurrentValue(item.get('wbSource'))}" />
    </span>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}imageIndicator'" py:strip="">
    <!-- "uses wbSource to select an image from a configured list, if is not found then no image. 
    to enter no image for a 0 return use the empty string when configuring. -->
    <img py:if="javascript == 'yes'"
        wbType="ImageIndicator"
        wbSource="${item.get('wbSource')}"
        imageUris="${item.get('imageUris')}"
        src="/static/images/off.png" />
    <img py:if="javascript == 'no'"
        src="${item.get('imageUris').split(',')[int(getCurrentValue(item.get('wbSource')))]}" />
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}caption'" py:strip="" >
    <span wbType="Caption" 
        py:content="[item.text] + item[:]" 
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
        />
</span>

</html>
