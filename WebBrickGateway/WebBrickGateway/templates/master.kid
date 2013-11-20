<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets
try:
    import templates.sitetemplate as sitetemplate
except ImportError:
    import WebBrickGateway.templates.sitetemplate as sitetemplate

?>

<html xmlns="http://www.w3.org/1999/xhtml" 
      xmlns:py="http://purl.org/kid/ns#" 
      xmlns:wb="http://id.webbrick.co.uk/"
      py:extends="WebBrickGateway.templates.widgets, sitetemplate" >

<head py:def="output_head(title)">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${title}</title>
    <?python 
        if not hasattr(self, 'javascript'):
            javascript = 'no'
    ?>
    <span py:if="javascript == 'no'">
        <link href="/static/css/panel_nojs.css" rel="stylesheet" type="text/css" />
    </span>

    <span py:if="javascript == 'yes'" py:strip="True">
        <link href="/static/css/panel.css" rel="stylesheet" type="text/css" />
        
        <script py:if="hasattr(self, 'debug')" src="/static/javascript/MochiKit.uncompressed.js" type="text/javascript"></script>

        <script py:if="not hasattr(self, 'debug')" src="/static/javascript/MochiKit.js" type="text/javascript"></script>

        <!-- WebBrick,js connects to onload and initialises panel elements -->
        <script src="/static/javascript/WebBrick.js" type="text/javascript"></script>
        <script src="/static/javascript/WbBackGround.js" type="text/javascript"></script>
        <script src="/static/javascript/WbButton.js" type="text/javascript"></script>
        <script src="/static/javascript/WbNumericDisplay.js" type="text/javascript"></script>
        <script src="/static/javascript/WbTimeDisplay.js" type="text/javascript"></script>
        <script src="/static/javascript/WbTextDisplay.js" type="text/javascript"></script>
        <script src="/static/javascript/WbNumericSlider.js" type="text/javascript"></script>
        <script src="/static/javascript/WbNumericBar.js" type="text/javascript"></script>
        <script src="/static/javascript/keyCheck.js" type="text/javascript"></script>
        <script src="/static/javascript/NumericPad.js" type="text/javascript"></script>
        <script src="/static/javascript/WbNumericEntry.js" type="text/javascript"></script>
        <script src="/static/javascript/WbTextEntry.js" type="text/javascript"></script>
        <script src="/static/javascript/WbEnableEntry.js" type="text/javascript"></script>
        <script src="/static/javascript/WbOnOffEntry.js" type="text/javascript"></script>
        <script src="/static/javascript/VlcPlugin.js" type="text/javascript"></script>
        <script src="/static/javascript/WbFlashMeter.js" type="text/javascript"></script>
        <script src="/static/javascript/WbFlashButton.js" type="text/javascript"></script>
        <script src="/static/javascript/WbDynamicImage.js" type="text/javascript"></script>
        <script src="/static/javascript/WbImageIndicator.js" type="text/javascript"></script>
        <script src="/static/javascript/WbStrings.js" type="text/javascript"></script>
        <script src="/static/javascript/WbFlashGraph.js" type="text/javascript"></script>

        <script py:if="hasattr(self, 'debug')" src="/static/javascript/debug.js" type="text/javascript"></script>
    </span>
</head>

<!-- TODO chnaage background image handling -->
<span py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:strip="" >
    <body py:if="javascript == 'yes'"
            py:attrs="item.items()" 
            wbType="WbBackGround" 
            wbSource="/eventstate/background">

        <div py:if="item.get('header')!='No'">
            <div py:if="tg_flash" class="flash" py:content="tg_flash"></div>
        </div>
        <div py:replace="[item.text] + item[:]"/>
    </body>

    <body py:if="javascript == 'no'"
            py:attrs="item.items()">
        <div py:if="item.get('header')!='No'">
            <div py:if="tg_flash" class="flash" py:content="tg_flash"></div>
        </div>
        <div py:replace="[item.text] + item[:]"/>
    </body>
</span>

</html>
