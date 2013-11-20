<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<?python 
from turbogears import config as tgconfig
serverHost = "127.0.0.1:%s"%(tgconfig.get("server.socket_port", "8080", False, "global" ))
def getCurrentValue( uri ):
    """
    attempt to retrieve the current value of the uri passed
    """
    try:
        from WebBrickLibs.WbAccess import GetHTTPXmlDom
        from MiscLib.DomHelpers import getNamedNodeText
        dom = GetHTTPXmlDom( serverHost, uri )    # need to know self address
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

<!-- for debugging what is not happening it can be usefull to see dictionaries at various points try self.__dict__ -->
<table py:def="output_dictionary( dct )">
    <tr py:for="ky in dct">
        <td>${ky}</td>
        <td py:if="isinstance( dct[ky], dict )" >${output_dictionary(dct[ky])}</td>
        <td py:if="not isinstance( dct[ky], dict )" >${str(dct[ky])}</td>
    </tr>
</table>

<span py:def="output_current_value( uri )" py:content="getCurrentValue( uri )" py:strip="True">
    ${item.text}
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}simpleLink'" py:strip="" >
    <td py:if="flash == 'xxx'"
                wbType="FlashButton" 
                wbTarget="${item.get('target')}"
                class="${item.get('class') or 'navBarSmall'}" 
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                title="${item.text}"
                flashMovie="/static/flash/SimpleISOButton2.swf"
                >
        ${item.text}
        ${item.getchildren()}
    </td>


    <?python
    # Work out if we have been given a target
    target = item.get('target')
    if target: click="window.location='" + target + "'" 
    if not target: click="history.back()"
    ?>

    <!-- onClick="window.location=&apos;${item.get('target') or &apos;history.back()&apos;}&apos;" -->
    <td py:if="flash &lt;&gt; 'xxx' and javascript == 'yes'"
                onClick="${click}"
                wbType="simpleLink"
                class="${item.get('class')}" 
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                >
        ${item.text}
        ${item.getchildren()}
    </td>

    <td py:if="javascript == 'no'"
                class="${item.get('class') or 'navBarSmall'}" 
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                >
        <a href="${item.get('target')}">
            ${item.text}
            ${item.getchildren()}
        </a>
    </td>
</span>


<span py:match="item.tag=='{http://id.webbrick.co.uk/}textDisplay'" py:strip="" >
    <td py:if="javascript == 'yes'"
                wbType="Text" 
                wbLoad='loadTextDisplay(&apos;${item.get("prefix")}&apos;,&apos;${item.get("postfix")}&apos;)'
                wbSource="${item.get('wbSource')}"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                py:content="getCurrentValue( item.get('wbSource') )"
    />
    <td py:if="javascript == 'no'"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="textPresent"
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    />
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}numericDisplay'" py:strip="" >
    <td py:if="javascript == 'yes'"
                wbType="Numeric" 
                wbLoad='loadNumericDisplay(&apos;${item.get("prefix")}&apos;,&apos;${item.get("format")}&apos;,&apos;${item.get("postfix")}&apos;)'
                wbSource="${item.get('wbSource')}"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    />
    <td py:if="javascript == 'no'"
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="numericInfo"
    />
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}numericEntry'" py:strip="" >
    <td py:if="javascript == 'yes'"
                wbType="WbNumericEntry"
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                wbTitle="${item.get('wbTitle')}"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                wbLoad='loadWbNumericEntry(&apos;${item.get("prefix")}&apos;,&apos;${item.get("format")}&apos;,&apos;${item.get("postfix")}&apos;)'
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    >&nbsp;</td>
    <td py:if="javascript == 'no'"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="numericInfo"
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    >&nbsp;</td>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}timeDisplay'" py:strip="" >
    <td py:if="javascript == 'yes'"
                wbType="WbTimeDisplay" 
                wbSource="${item.get('wbSource')}"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                py:content="getCurrentValue( item.get('wbSource') )"
    >--:--</td>
    <td py:if="javascript == 'no'"
                py:content="getCurrentValue( item.get('wbSource') )"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="numericInfo"
    >--:--</td>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}timeEntry'" py:strip="" >
    <script py:if="javascript == 'yes'" src="/static/javascript/WbTimeEntry.js" type="text/javascript"></script>
    <td py:if="javascript == 'yes'"
                wbType="WbTimeEntry" 
                wbTitle="${item.get('wbTitle')}"
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                py:content="getCurrentValue( item.get('wbSource') )"
    >--:--</td>
    <td py:if="javascript == 'no'"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="numericInfo"
                py:content="getCurrentValue( item.get('wbSource') )"
    >--:--</td>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}onoffEntry'" py:strip="" >
    <td py:if="javascript == 'yes'"
                wbType="WbOnOffEntry" 
                wbTitle="${item.get('wbTitle')}"
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                py:content="getCurrentValue( item.get('wbSource') )"
    >Ignore</td>
    <td py:if="javascript == 'no'"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="WbOnOffEntry"
                py:content="getCurrentValue( item.get('wbSource') )"
    >Ignore</td>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}enableEntry'" py:strip="" >
    <td py:if="javascript == 'yes'"
                wbType="WbEnableEntry" 
                wbTitle="${item.get('wbTitle')}"
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                stateVals="${item.get('stateVals')}"
                wbLoad='loadWbEnableEntry(&apos;${item.get("prefix")}&apos;,&apos;${item.get("postfix")}&apos;)'
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    >Ignore</td>
    <td py:if="javascript == 'no'"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                stateVals="${item.get('stateVals')}"
                class="WbOnOffEntry"
                py:content="getCurrentValue( item.get('wbSource') )"
    >Ignore</td>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}dayEntry'" py:strip="" >
    <script py:if="javascript == 'yes'" src="/static/javascript/WbDayEntry.js" type="text/javascript"></script>
    <td py:if="javascript == 'yes'"
                wbType="WbDayEntry" 
                wbTitle="${item.get('wbTitle')}"
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                py:content="getCurrentValue( item.get('wbSource') )"
    >-------</td>
    <td py:if="javascript == 'no'"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="numericdisplay"
                py:content="getCurrentValue( item.get('wbSource') )"
    >-------</td>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}simpleButton'" py:strip="" >
    <td py:if="flash == 'xxx'"
                wbType="FlashButton" 
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                stateVals="${item.get('stateVals')}"
                title="${item.text}"
                flashMovie="/static/flash/SimpleISOButton2.swf"
                >
        ${item.getchildren()}
    </td>

    <td py:if="flash &lt;&gt; 'xxx' and javascript == 'yes'"
                wbType="PushButton" 
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                stateVals="${item.get('stateVals')}"
                py:content="item.text"
                >
    </td>

    <td py:if="javascript == 'no'"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                stateVals="${item.get('stateVals')}"
            class="button"
        >
        <a href="${item.get('wbTarget')}"
            py:content="item.text"
        >
        </a>
    </td>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}simpleIndicator'" py:strip="" >
    <td py:if="flash == 'xxx'"
                wbType="FlashIndicator" 
                wbSource="${item.get('wbSource')}"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                stateVals="${item.get('stateVals')}"
                title="${item.text}"
                flashMovie="/static/flash/SimpleISOButton2.swf"
                >
        ${item.getchildren()}
    </td>

    <td py:if="flash &lt;&gt; 'xxx' and javascript == 'yes'"
                wbType="Indicator" 
                wbSource="${item.get('wbSource')}"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                stateVals="${item.get('stateVals')}"
                py:content="item.text"
                >
    </td>

    <td py:if="javascript == 'no'"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                stateVals="${item.get('stateVals')}"
            class="indicator"
        >
        <a href="${item.get('wbTarget')}"
            py:content="item.text"
        >
        </a>
    </td>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}flashButton'" py:strip="" >
    <td py:if="flash == 'yes' and javascript == 'yes'"
                wbType="FlashButton" 
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                title="${item.text}"
                flashMovie='${getFlashMovie(item,"SimpleISOButton.swf")}'
                >
    </td>

    <td py:if="flash &lt;&gt; 'yes' and javascript == 'yes'"
                wbType="PushButton" 
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                py:content="item.text"
                >
    </td>

    <td py:if="javascript == 'no'"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
            class="button"
        >
        <a href="${item.get('wbTarget')}"
            py:content="item.text"
        >
        </a>
    </td>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}flashMeter'" py:strip="" >
    <td py:if="flash == 'yes' and javascript == 'yes'"
                wbType="FlashMeter" 
                wbSource="${item.get('wbSource')}"
                wbLoad='loadFlashMeter(&apos;${item.get("prefix")}&apos;,&apos;${item.get("format")}&apos;,&apos;${item.get("postfix")}&apos;)'
                labels="${item.get('labels')}"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width', '200px')}"
                height="${item.get('height', '200px')}"
                baseClassName="${item.get('baseClassName')}"
                metertitle="${item.text.strip()}"
                minvalue="${item.get('minvalue')}"
                maxvalue="${item.get('maxvalue')}"
                curvalue="${item.get('curvalue')}"
                setlow="${item.get('setlow')}"
                sethigh="${item.get('sethigh')}"
                prefix="${item.get('prefix')}"
                postfix="${item.get('postfix')}"
                flashMovie='${getFlashMovie(item,"Simple270.swf")}'
                >
    </td>
    <td py:if="flash &lt;&gt; 'yes' and javascript == 'yes'"
                wbType="Numeric" 
                wbLoad='loadNumericDisplay(&apos;${item.get("prefix")}&apos;,&apos;${item.get("format")}&apos;,&apos;${item.get("postfix")}&apos;)'
                wbSource="${item.get('wbSource')}"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    />
    <td py:if="javascript == 'no'"
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="numericInfo"
    />
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}flashDimmer'" py:strip="" >
    <td py:if="flash == 'yes' and javascript == 'yes'"
                wbType="FlashDimmer" 
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                labels="${item.get('labels')}"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                title="${item.text}"
                flashMovie='${getFlashMovie(item,"TestDimmer.swf")}'
                >
    </td>
    <td py:if="flash &lt;&gt; 'yes' and javascript == 'yes'"
                wbType="WbNumericEntry"
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                wbLoad='loadWbNumericEntry(&apos;${item.get("prefix")}&apos;,&apos;${item.get("format")}&apos;,&apos;${item.get("postfix")}&apos;)'
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    >&nbsp;</td>
    <td py:if="javascript == 'no'"
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="numericInfo"
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    >&nbsp;</td>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}dynamicImage'" py:strip="">
    <!-- uses wbSource to display an image, wbSource specifies the URL of the image. -->
    <!-- the width may have to be aplied to the image and not the TD -->
    <td colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                align="center">
        <img py:if="javascript == 'yes'"
            wbType="DynamicImage"
            wbSource="${item.get('wbSource')}"
            width="${item.get('width')}"
            height="${item.get('height')}"
            default_image="${item.get('default_image')}"
            src="${item.get('default_image')}" />
        <img py:if="javascript == 'no'"
            width="${item.get('width')}"
            height="${item.get('height')}"
            src="${getCurrentValue(item.get('wbSource'))}" />
    </td>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}imageIndicator'" py:strip="">
    <!-- uses wbSource to select an image from a configured list, if is not found then no image. 
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
    <td wbType="Caption" 
        py:content="item.text" 
                colspan="${item.get('colspan')}"
                rowspan="${item.get('rowspan')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
        />
</span>


<!-- note we use gTitle rather than title which seems to be reserved -->
<span py:match="item.tag=='{http://id.webbrick.co.uk/}flashGraph'" py:strip="" >
    <link href="/static/css/form.css" rel="stylesheet" type="text/css" />
    <script src="/static/javascript/graphs/swfobject.js" type="text/javascript"></script>
    <script src="/static/javascript/graphs/json2.js" type="text/javascript"></script>
    <span  py:if="flash == 'yes' and javascript == 'yes'"
                wbType="FlashGraph"
                width="${item.get('width')}"
                height="${item.get('height')}"
                minYval="${item.get('minYval')}"
                maxYval="${item.get('maxYval')}"
                baseClassName="${item.get('baseClassName')}"
                gTitle="${item.get('gTitle')}"     
                xLabels="${item.get('xLabels')}"
                xStep="${item.get('xStep')}"
                yLabelStyle="${item.get('yLabelStyle')}"
                activeSets="${item.get('activeSets')}"
                flashMovie='${getFlashMovie(item,"open-flash-chart.swf")}'
                >
    </span>

    <span py:if="flash &lt;&gt; 'yes' and javascript == 'yes'">
        Requires both Javascript and Flash
    </span>

    <span py:if="javascript == 'no'">
        Requires both Javascript and Flash
    </span>
</span>

<!--    **************    DROP DOWN WIDGET ***************  -->
<span py:match="item.tag=='{http://id.webbrick.co.uk/}dropDown'" py:strip="" >
    <script src="/static/javascript/WbDropDown.js" type="text/javascript"></script>
    <link href="/static/css/dropdown.css" rel="stylesheet" type="text/css" />
    <td  py:if="javascript == 'yes'"
                wbType="WbDropDown"
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                options="${item.get('options')}"
                display="${item.get('display')}"
                py:content=" '%s%s%s' % ( item.get('prefix'), item.get('wbSource'), item.get('postfix') )"
                >
    </td>


    <span py:if="javascript == 'no'">
        Requires Javascript
    </span>
</span>

<!--    **************    GENERIC SLIDER ***************  -->
<span py:match="item.tag=='{http://id.webbrick.co.uk/}slider'" py:strip="" >
    <script type="text/javascript" src="/static/javascript/slider/range.js"></script>
    <script type="text/javascript" src="/static/javascript/slider/timer.js"></script>
    <script type="text/javascript" src="/static/javascript/slider/slider.js"></script>
    <script src="/static/javascript/WbSlider.js" type="text/javascript"></script>
    <div  py:if="javascript == 'yes'"
                wbType="WbSlider"
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                orientation="${item.get('orientation')}"
                height="${item.get('height')}"
                sMax="${item.get('sMax')}"
                >   
                    <div class='objCenter'>
                        <input id='num-input' class='objCenter' />
                    </div>
                    <div class='slider' id="slider">
                        <input id='slider-input' class='slider-input' />
                    </div>
    </div>
    <!-- This widget should automatically fall back if javascript is not available -->
</span>


</html>
