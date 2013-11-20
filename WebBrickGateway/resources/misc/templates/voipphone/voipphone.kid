<?xml version='1.0' encoding='utf-8'?>
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

<root xmlns:py="http://purl.org/kid/ns#" 
      xmlns:wb="http://id.webbrick.co.uk/" >

<!-- wb:voipmenu -->
    <span py:match="item.tag=='{http://id.webbrick.co.uk/}voipmenu'" py:strip="" >
        <SnomIPPhoneMenu py:if="model == 'snom'">
            ${item.text}
            ${item.getchildren()}
        </SnomIPPhoneMenu>

<!-- Need to add correct alterm=natives for other IP phones -->
        <AastraIPPhoneTextMenu py:if="model == 'aastra'" destroyOnExit="yes">
            ${item.text}
            ${item.getchildren()}
        </AastraIPPhoneTextMenu>
    </span>

<!-- wb:voipmenuitem -->
    <span py:match="item.tag=='{http://id.webbrick.co.uk/}voipmenuitem'" py:strip="" >
        <MenuItem py:if="model == 'snom'">
            ${item.getchildren()}
        </MenuItem>
        <MenuItem py:if="model == 'aastra'">
            ${item.getchildren()}
        </MenuItem>
    </span>

<!-- wb:voipsoftkeyitem -->
    <span py:match="item.tag=='{http://id.webbrick.co.uk/}voipsoftkeyitem'" py:strip="" >
        <SoftKeyItem py:if="model == 'snom'">
            ${item.text}
            ${item.getchildren()}
        </SoftKeyItem>
    </span>

<!-- wb:voipmenutitle -->
    <span py:match="item.tag=='{http://id.webbrick.co.uk/}voipmenutitle'" py:strip="" >
        <Title py:if="model == 'snom'">
            ${item.text()}
            ${item.getchildren()}
        </Title>
        <Title py:if="model == 'aastra'">
            ${item.text()}
            ${item.getchildren()}
        </Title>
    </span>

<!-- wb:voipmenuitemname -->
    <span py:match="item.tag=='{http://id.webbrick.co.uk/}voipmenuitemname'" py:strip="" >
        <Name py:if="model == 'snom'">
            ${item.text()}
            ${item.getchildren()}
        </Name>
        <Prompt py:if="model == 'aastra'">
            ${item.text()}
            ${item.getchildren()}
        </Prompt>
    </span>

    <span py:match="item.tag=='{http://id.webbrick.co.uk/}voipurl'" py:strip="" >
        <URL py:if="model == 'snom'">
            ${item.text()}
        </URL>
        <URI py:if="model == 'aastra'">
            ${item.text()}
        </URI>
    </span>

</root>
