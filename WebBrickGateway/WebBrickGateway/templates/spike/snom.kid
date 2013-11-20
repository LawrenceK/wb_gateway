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
      py:extends="'master.kid'" py:strip="">
    <SnomIPPhoneText>
        <Title>Hot Water</Title>
        <Prompt>Prompt Text</Prompt>
        <Text>
            Hot water temperature ${getCurrentValue( '/wbsts/house2/Tmp/1' )} C
        </Text>
    </SnomIPPhoneText>
</root>