<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<!-- NOTE with this version the widgets are in spans and not td, so if using tables for layout YOU need to include the TD -->

<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_new_event
try:
    import templates.sitetemplate as sitetemplate
except ImportError:
    import WebBrickGateway.templates.sitetemplate as sitetemplate

?>

<html xmlns="http://www.w3.org/1999/xhtml" 
      xmlns:py="http://purl.org/kid/ns#" 
      xmlns:wb="http://id.webbrick.co.uk/"
      py:extends="WebBrickGateway.templates.widgets_new_event, sitetemplate" >

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
        
        <script type="text/javascript" src="/eventlib/tests/static/javascript/DeferredMonad.js"></script>
        <script type="text/javascript" src="/widgets/WidgetFunctions.js"></script>

        <script type="text/javascript" src="/eventlib/static/javascript/URI.js"></script>
        <script type="text/javascript" src="/eventlib/static/javascript/Status.js"></script>
        <script type="text/javascript" src="/eventlib/static/javascript/Event.js"></script>
        <script type="text/javascript" src="/eventlib/static/javascript/EventEnvelope.js"></script>
        <script type="text/javascript" src="/eventlib/static/javascript/EventSerializer.js"></script>
        <script type="text/javascript" src="/eventlib/static/javascript/EventAgent.js"></script>
        <script type="text/javascript" src="/eventlib/static/javascript/EventHandler.js"></script>
        <script type="text/javascript" src="/eventlib/static/javascript/EventRouter.js"></script>
        <script type="text/javascript" src="/eventlib/static/javascript/EventRouterHTTPC.js"></script>
        <script type="text/javascript" src="/widgets/SimpleButton.js"></script>
        <script type="text/javascript" src="/widgets/NumericDisplay.js"></script>
        <link type="text/css"         href="/widgets/SimpleButton.css" rel="stylesheet" />

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
