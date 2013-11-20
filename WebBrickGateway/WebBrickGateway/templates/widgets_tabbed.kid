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

<span py:def="output_current_value( uri )" py:content="getCurrentValue( uri )" py:strip="True">
    ${item.text}
</span>


<span py:match="item.tag=='{http://id.webbrick.co.uk/}BackButton'" py:strip="" >
    
    <div py:if="javascript == 'yes'"
                wbType="SimpleLink" 
                onClick="history.back()" 
                class="backButton"
                >
        <div class="noniconbutton" >
            <img class="noniconbuttonleft" src="/static/activeskin/images/button/buttonleft.png"/>
            <div class="buttonlabel">
                <div class="buttonbodyoverlay">
                    <div py:if="item.text" class="buttonbodycontent" py:content="[item.text] + item[:]">Back</div>
                    <div py:if="not item.text" class="buttonbodycontent">Back</div>
                    <img class="buttoncap" src="/static/activeskin/images/button/buttonright.png"/>
                </div>
            </div>
        </div>
    </div>

    <span py:if="javascript == 'no'"
                >
        <a onClick="history.back()" >
            <img py:if="iconimage" src="/static/activeskin/images/${item.get('iconimage')}" width="29" height="29" class="zoneicon" />
            Back
        </a>
    </span>
</span>



<span py:match="item.tag=='{http://id.webbrick.co.uk/}textDisplay'" py:strip="" >
    <div  py:if="javascript == 'yes'"
            py:content="getCurrentValue( item.get('wbSource') )"
            wbType="Text" 
            wbLoad='loadTextDisplay(&apos;${item.get("prefix")}&apos;,&apos;${item.get("postfix")}&apos;)'
            wbSource="${item.get('wbSource')}"
            width="${item.get('width')}"
            height="${item.get('height')}"
            baseClassName="${item.get('baseClassName')}"
            class="${item.get('baseClassName') or 'text'}Dormant"
            >
    </div>
    
    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                class="textPresent"
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    />
</span>


<span py:match="item.tag=='{http://id.webbrick.co.uk/}numericDisplay'" py:strip="" >
    <div  py:if="javascript == 'yes'"
            wbType="Numeric" 
            wbLoad='loadNumericDisplay(&apos;${item.get("prefix")}&apos;,&apos;${item.get("format")}&apos;,&apos;${item.get("postfix")}&apos;)'
            wbSource="${item.get('wbSource')}"
            width="${item.get('width')}"
            height="${item.get('height')}"
            baseClassName="${item.get('baseClassName')}"
            class="${item.get('baseClassName') or 'numeric'}Info"
            py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
            >
    </div>
    <span py:if="javascript == 'no'"
            py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
            width="${item.get('width')}"
            height="${item.get('height')}"
            baseClassName="${item.get('baseClassName')}"
            class="${item.get('baseClassName') or 'numeric'}Info"
    />
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}numericEntryButton'" py:strip="" >
        <div py:if="javascript == 'yes'"
                wbType="WbNumericEntry"
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="${item.get('baseClassName') or 'numeric'}Info"
                wbLoad='loadWbNumericEntry(&apos;${item.get("prefix")}&apos;,&apos;${item.get("format")}&apos;,&apos;${item.get("postfix")}&apos;)'
                >
            <div class="left"/>
            <div class="center">
                <div class="text" py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )" >
                    &nbsp;
                </div>
            </div>
            <div class="right" />    

        </div>

    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="${item.get('baseClassName') or 'numeric'}Info"
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    >&nbsp;</span>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}timeEntryButton'" py:strip="" >
        <div py:if="javascript == 'yes'"
                wbType="WbTimeEntry"
                wbTitle="${item.get('wbTitle')}"
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="${item.get('baseClassName') or 'numeric'}Info"
                >
            <div class="left"/>
            <div class="center">
                <div class="buttonbodycontent" py:content="getCurrentValue( item.get('wbSource') )">--:--</div>
            </div>
            <div class="right" />

        </div>


    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="${item.get('baseClassName') or 'numeric'}Info"
                py:content="getCurrentValue( item.get('wbSource') )"
    >--:--</span>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}simpleButton'" py:strip="" >
    <div py:if="javascript == 'yes'"
            wbType="PushButton" 
            wbSource="${item.get('wbSource')}"
            wbTarget="${item.get('wbTarget')}"
            width="${item.get('width')}"
            height="${item.get('height')}"
            baseClassName="${item.get('baseClassName')}"
            class="${item.get('baseClassName') or 'button'}Dormant"
            stateVals="${item.get('stateVals')}"
            >
        <div class="left"/>
        <div class="center">
            <div class="text" py:content="[item.text] + item[:]" >
                &nbsp;
            </div>
        </div>
        <div class="right" />
        
    </div>
    
    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                stateVals="${item.get('stateVals')}"
                class="${item.get('baseClassName') or 'button'}Dormant"
        >
        <a href="${item.get('wbTarget')}">
            <div class="buttonicon"/>
            <div class="buttonlabel" py:content="[item.text] + item[:]">&nbsp;</div>
        </a>
    </span>
</span>


<span py:match="item.tag=='{http://id.webbrick.co.uk/}simpleLinkButton'" py:strip="" >

    <div py:if="flash &lt;&gt; 'xxx' and javascript == 'yes'"
                wbType="SimpleLink"
                onClick="window.location=&apos;${item.get('target')}&apos;"
                baseClassName="${item.get('baseClassName')}"
                class="simpleLinkButton"
                stateVals="${item.get('stateVals')}"
                >
        <div class="left"/>
        <div class="center">
            <div class="text" py:content="[item.text] + item[:]" >
                &nbsp;
            </div>
        </div>
        <div class="right" />
    </div>

    <span py:if="javascript == 'no'"
                >
        <a href="${item.get('target')}">
            <img py:if="iconimage" src="/static/activeskin/images/${item.get('iconimage')}" width="29" height="29" class="zoneicon" />
            ${item.text}
            ${item.getchildren()}
        </a>
    </span>
</span>






<!-- ! a widget that triggers the target and when complete changes the current page -->
<span py:match="item.tag=='{http://id.webbrick.co.uk/}simpleButtonAndLink'" py:strip="" >
    <div py:if="javascript == 'yes'"
                wbType="PushButton" 
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                wbPageLink="${item.get('wbPageLink')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="${item.get('baseClassName') or 'button'}Dormant"
                stateVals="${item.get('stateVals')}"
                >
        <div class="buttoniconcontainer"/>
        <div class="buttonicon"/>
        <div class="buttoniconoverlay"/>
        <div class="buttonlabel">
            <div class="buttonbodyoverlay" py:content="[item.text] + item[:]">&nbsp;</div>
            <img class="buttoncap" src="/static/activeskin/images/button/buttonright.png"/>
        </div>
                
    </div>
    
    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                stateVals="${item.get('stateVals')}"
                class="${item.get('baseClassName') or 'button'}Dormant"
        >
        <a href="${item.get('wbTarget')}">
            <div class="buttoniconcontainer"/>
            <div class="buttonicon"/>
            <div class="buttoniconoverlay"/>
            <div class="buttonlabel">
                <div class="buttonbodyoverlay" py:content="[item.text] + item[:]">&nbsp;</div>
                <img class="buttoncap" src="/static/activeskin/images/button/buttonright.png"/>
            </div>
        </a>
    </span>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}simpleAction'" py:strip="" >
    <span py:if="javascript == 'yes'"
                wbType="PushButton" 
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName') or 'action'}"
                class="${item.get('baseClassName') or 'action'}Dormant"
                stateVals="${item.get('stateVals')}"
                >
        <img py:if="item.get('iconimage')" src="/static/activeskin/images/${item.get('iconimage')}" width="29" height="29" class="zoneicon" />
        ${item.text}
        ${item.getchildren()}
    </span>
    
    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName') or 'action'}"
                stateVals="${item.get('stateVals')}"
                class="${item.get('baseClassName') or 'button'}Dormant"
        >
        <a href="${item.get('wbTarget')}">
            <img py:if="item.get('iconimage')" src="/static/activeskin/images/${item.get('iconimage')}" width="29" height="29" class="zoneicon" />
            ${item.text}
            ${item.getchildren()}
        </a>
    </span>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}simpleIndicatorButton'" py:strip="" >
    <div py:if="javascript == 'yes'"
                wbType="Indicator" 
                wbSource="${item.get('wbSource')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="${item.get('baseClassName') or 'indicator'}Dormant"
                stateVals="${item.get('stateVals')}"
                >
        <div class="buttoniconcontainer"/>
        <div class="buttonicon"/>
        <div class="buttoniconoverlay"/>
        <div class="buttonlabel">
            <div class="buttonbodyoverlay" py:content="[item.text] + item[:]">&nbsp;</div>
            <img class="buttoncap" src="/static/activeskin/images/button/buttonright.png"/>
        </div>
                
    </div>
    
    <!-- !This needs work on it -->
    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                stateVals="${item.get('stateVals')}"
                class="${item.get('baseClassName') or 'indicator'}Dormant"
        >
        <div class="buttoniconcontainer"/>
        <div class="buttonicon"/>
        <div class="buttoniconoverlay"/>
        <div class="buttonlabel">
            <div class="buttonbodyoverlay" py:content="[item.text] + item[:]">&nbsp;</div>
            <img class="buttoncap" src="/static/activeskin/images/button/buttonright.png"/>
        </div>
    </span>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}simpleIndicator'" py:strip="" >
    <span py:if="javascript == 'yes'"
                wbType="Indicator" 
                wbSource="${item.get('wbSource')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="${item.get('baseClassName') or 'indicator'}Dormant"
                stateVals="${item.get('stateVals')}"
                >
        <div class="buttonicon"/>${[item.text] + item[:]}
    </span>
    
    <!-- !This needs work on it -->
    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                stateVals="${item.get('stateVals')}"
                py:content="[item.text] + item[:]"
                class="${item.get('baseClassName') or 'indicator'}Dormant"
        >
    </span>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}imageButton'" py:strip="" >

    <div py:if="javascript == 'yes'"
                wbType="PushButton" 
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                baseClassName="${item.get('baseClassName')}"
                stateVals="${item.get('stateVals')}"
                class="${item.get('baseClassName')}item"
                >
        <div class="${item.get('baseClassName')}item">
            <div class="${item.get('baseClassName')}icon">
                <img src="/static/activeskin/images/${item.get('iconimage')}" 
                        width="${item.get('width')}" 
                        height="${item.get('height')}" 
                         />
                ${item.text}
                ${item.getchildren()}
            </div>
        </div>
    </div>
    
    <span py:if="javascript == 'no'"
                baseClassName="${item.get('baseClassName')}"
                stateVals="${item.get('stateVals')}"
                class="${item.get('baseClassName')}item"
        >
        <div class="${item.get('baseClassName')}item">
            <a href="${item.get('wbTarget')}">
                <div class="${item.get('baseClassName')}icon">
                    <img src="/static/activeskin/images/${item.get('iconimage')}" 
                        width="${item.get('width')}" 
                        height="${item.get('height')}" />
                    ${item.text}
                    ${item.getchildren()}
                </div>
            </a>
        </div>
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
                class="${item.get('baseClassName') or 'button'}Dormant"
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
                class="${item.get('baseClassName') or 'button'}Dormant"
                py:content="[item.text] + item[:]"
                >
    </span>

    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="${item.get('baseClassName') or 'button'}Dormant"
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
                meterTitle="${item.get('meterTitle')}"
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
                class="${item.get('baseClassName') or 'numeric'}Dormant"
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    />
    <span py:if="javascript == 'no'"
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="${item.get('baseClassName') or 'button'}Info"
    />
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}volumeControl'" py:strip="" >
    <div py:if="flash == 'yes' and javascript == 'yes'"
                id="volumecontrolcontainer"
                wbType="FlashVolumeControl" 
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                >
            <script language="javascript">
                AC_FL_RunContent(
                        'codebase', 'http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,0,0',
                        'width', '290',
                        'height', '30',
                        'src', 'volumecontrol',
                        'quality', 'high',
                        'pluginspage', 'http://www.macromedia.com/go/getflashplayer',
                        'align', 'middle',
                        'play', 'true',
                        'loop', 'true',
                        'scale', 'showall',
                        'wmode', 'window',
                        'devicefont', 'false',
                        'id', 'volumecontrol',
                        'bgcolor', '#f2f2f2',
                        'name', 'volumecontrol',
                        'menu', 'true',
                        'allowScriptAccess','sameDomain',
                        'movie', '/static/activeskin/images/mediaplayer/volumecontrol.swf',
                        'salign', ''
                        ); //end AC code
            </script>
    </div>
    
    <div py:if="flash &lt;&gt; 'yes' and javascript == 'yes'">
        <span wbType="WbNudgeNumericEntry" 
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                width="${item.get('width') or 100}"
                height="${item.get('height') or 10}"
                py:content="getCurrentValue( item.get('wbSource') )"
                />
        <br/>
        <span wbType="NumericBar"
                    wbSource="${item.get('wbSource')}"
                    wbDuration="100"
                
                    minvalue="0" 
                    maxvalue="100"
                    curvalue="${getCurrentValue( item.get('wbSource') )}"
                
                    width="${item.get('width') or 100}"
                    height="${item.get('height') or 10}"
                
                    baseClassName="${item.get('baseClassName')}"
                    class="${item.get('baseClassName') or 'NumericBar'}" />
    </div>
<!-- !
    <div py:if="flash &lt;&gt; 'yes' and javascript == 'yes'"
                wbType="WbNudgeNumericEntry"
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                wbPrefix="Volume "
                wbFormat="##"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="${item.get('baseClassName') or 'numeric'}Info"
                py:content=" 'Volume %s' % ( getCurrentValue( item.get('wbSource') ) )"
    >
    &nbsp;
    </div>
-->
    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="${item.get('baseClassName') or 'numeric'}Info"
                py:content=" 'Volume %s' % ( getCurrentValue( item.get('wbSource') ) )"
    >&nbsp;</span>
</span>

<span py:match="item.tag=='{http://id.webbrick.co.uk/}positionIndicator'" py:strip="" >
    <div py:if="flash == 'yes' and javascript == 'yes'"
                id="positionindicatorcontainer"
                wbType="FlashPositionIndicator" 
                wbDuration="${item.get('wbDuration')}"
                wbCurPosition="${item.get('wbCurPosition')}"
                wbTrack="${item.get('wbTrack')}"
                wbState="${item.get('wbState')}"
                width="${item.get('width')}"
                height="${item.get('height')}"
                >
				<script language="javascript">
                    AC_FL_RunContent(
                        'codebase', 'http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,0,0',
                        'width', '285',
                        'height', '44',
                        'src', 'songpositionindicator',
                        'quality', 'high',
                        'pluginspage', 'http://www.macromedia.com/go/getflashplayer',
                        'align', 'middle',
                        'play', 'true',
                        'loop', 'true',
                        'scale', 'showall',
                        'wmode', 'window',
                        'devicefont', 'false',
                        'id', 'songpositionindicator',
                        'bgcolor', '#f2f2f2',
                        'name', 'songpositionindicator',
                        'menu', 'true',
                        'allowScriptAccess','sameDomain',
                        'movie', '/static/activeskin/images/mediaplayer/songpositionindicator.swf',
                        'salign', ''
                        ); //end AC code
                </script>
    </div>
    <span py:if="flash &lt;&gt; 'yes' and javascript == 'yes'"
                wbType="NumericBar"
                wbSource="${item.get('wbCurPosition')}"
                wbDuration="${item.get('wbDuration')}"
                wbCurPosition="${item.get('wbCurPosition')}"
                
                minvalue="0" 
                maxvalue="${getCurrentValue( item.get('wbDuration') )}"
                curvalue="${getCurrentValue( item.get('wbCurPosition') )}"
                
                width="${item.get('width') or 100}"
                height="${item.get('height') or 10}"
                
                baseClassName="${item.get('baseClassName')}"
                class="${item.get('baseClassName') or 'NumericBar'}"
    >&nbsp;</span>
    
    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="${item.get('baseClassName') or 'numeric'}Info"
                py:content=" '%s%s' % ( getCurrentValue( item.get('wbCurPosition') ), item.get('postfix') )"
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
                meterTitle="${item.get('meterTitle')}"
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
                class="${item.get('baseClassName') or 'numeric'}Info"
                wbLoad='loadWbNumericEntry(&apos;${item.get("prefix")}&apos;,&apos;${item.get("format")}&apos;,&apos;${item.get("postfix")}&apos;)'
                py:content=" '%s%s%s' % ( item.get('prefix'), getCurrentValue( item.get('wbSource') ), item.get('postfix') )"
    >&nbsp;</span>
    <span py:if="javascript == 'no'"
                width="${item.get('width')}"
                height="${item.get('height')}"
                baseClassName="${item.get('baseClassName')}"
                class="${item.get('baseClassName') or 'numeric'}Info"
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
        src="/static/activeskin/images/statusicons/clear.png" />
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

<span py:match="item.tag=='{http://id.webbrick.co.uk/}hideableBox'" py:strip="" >
    <div wbType="WbHideableBox" py:content="[item.text] + item[:]" location="${item.get('location') or 'bottom'}">
    </div>
</span>

<!-- note we use gTitle rather than title which seems to be reserved -->
<span py:match="item.tag=='{http://id.webbrick.co.uk/}flashGraph'" py:strip="" >
    <link href="/static/css/form.css" rel="stylesheet" type="text/css" />
    <script src="/static/javascript/graphs/swfobject.js" type="text/javascript"></script>
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
    <span  py:if="javascript == 'yes'"
                wbType="WbDropDown"
                wbSource="${item.get('wbSource')}"
                wbTarget="${item.get('wbTarget')}"
                options="${item.get('options')}"
                display="${item.get('display')}"
                py:content=" '%s%s%s' % ( item.get('prefix'), item.get('wbSource'), item.get('postfix') )"
                >
    </span>


    <span py:if="javascript == 'no'">
        Requires Javascript
    </span>
</span>

</html>
