<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round
?>
<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="'sitelayout3.kid'" 
        py:extends="WebBrickGateway.templates.widgets_round">

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}leftboxcontent'" id="leftboxcontent">
        <div>
            <p>Input Buttons</p>
            <wb:simpleButton wbTarget="/sendevent/widgetdemo?type=http://id.webbrick.co.uk/events/config/set&amp;val=0">
                Issue 0
            </wb:simpleButton>
            <wb:simpleButton wbTarget="/sendevent/widgetdemo?type=http://id.webbrick.co.uk/events/config/set&amp;val=1">
                Issue 1
            </wb:simpleButton>
            <wb:simpleButton wbTarget="/sendevent/widgetdemo?type=http://id.webbrick.co.uk/events/config/set&amp;val=2">
                Issue 2
            </wb:simpleButton>
            <wb:simpleButton wbTarget="/sendevent/widgetdemo?type=http://id.webbrick.co.uk/events/config/set&amp;val=3">
                Issue 3
            </wb:simpleButton>
            <wb:simpleButtonAndLink 
                    wbTarget="/sendevent/widgetdemo?type=http://id.webbrick.co.uk/events/config/set&amp;val=0"
                    wbPageLink="/"
                    >
                Issue 0 and Home
            </wb:simpleButtonAndLink>
        </div>
        
        <div>
            <p>wb:Simple Button</p>
            <wb:simpleButton 
                    wbTarget="/sendevent/widgetdemo?type=http://id.webbrick.co.uk/events/config/set" 
                    wbSource="/eventstate/widgetdemo">        	
                Default
            </wb:simpleButton>
            
            <wb:simpleButton 
                    wbTarget="/sendevent/widgetdemo?type=http://id.webbrick.co.uk/events/config/set" 
                    wbSource="/eventstate/widgetdemo"
                    stateVals="Open,Closed,Ajar,Error"
                    baseClassName="door">        	
                Door
            </wb:simpleButton>
            
            <wb:simpleButton 
                    wbTarget="/sendevent/widgetdemo?type=http://id.webbrick.co.uk/events/config/set" 
                    wbSource="/eventstate/widgetdemo"
                    stateVals="Open,Closed,Ajar,Error"
                    baseClassName="gate">        	
                Gate
            </wb:simpleButton>
            
            <wb:simpleButton 
                    wbTarget="/sendevent/widgetdemo?type=http://id.webbrick.co.uk/events/config/set" 
                    wbSource="/eventstate/widgetdemo"
                    stateVals="Blank,Tick">        	
                button Blank/Tick
            </wb:simpleButton>
            
            <wb:simpleIndicatorButton 
                    wbSource="/eventstate/widgetdemo"
                    stateVals="Open,Closed,Ajar,Error"
                    baseClassName="gate">        	
                Indicator
            </wb:simpleIndicatorButton>

            <wb:simpleIndicatorButton 
                    wbSource="/eventstate/widgetdemo"
                    stateVals="Open,Closed,Ajar,Error"
                    baseClassName="gate">
                <wb:textDisplay wbSource="/eventstate/widgetdemo/onoff?attr=onoff"></wb:textDisplay>            
            </wb:simpleIndicatorButton>
            
        </div>
    </div>
        
    <div py:match="item.tag=='{http://id.webbrick.co.uk/}topboxcontent'" id="topboxcontent">
        <p>wb:textDisplay      wb:textDisplay      wb:numericDisplay       wb:timeDisplay</p>
    
        <wb:textDisplayButton wbSource="/eventstate/widgetdemo/onoff?attr=onoff"></wb:textDisplayButton>
        
        <wb:textDisplayButton wbSource="/eventstate/widgetdemo/day?attr=day"></wb:textDisplayButton>

        <wb:numericDisplayButton 
            wbSource="/eventstate/widgetdemo/numeric" 
            prefix="Outside:" 
            format="##.#" 
            postfix="&ordm;C">
            wb:numericDisplay
        </wb:numericDisplayButton>
        
        <wb:timeDisplayButton wbSource="/eventstate/widgetdemo/time?attr=time">
            wb:timeDisplay
        </wb:timeDisplayButton>
        <p>wb:onoffEntry wb:dayEntry wb:numericEntry wb:timeEntry</p>
        
        <wb:onoffEntryButton 
            wbSource="/eventstate/widgetdemo/onoff?attr=onoff"
            wbTarget="/sendevent/widgetdemo/onoff"
            wbTitle="On Off Entry Demo">
        </wb:onoffEntryButton>
        
        <wb:dayEntryButton 
            wbSource="/eventstate/widgetdemo/day?attr=day"
            wbTarget="/sendevent/widgetdemo/day"
            wbTitle="Day Entry Demo">
        </wb:dayEntryButton>
                            
        <wb:numericEntryButton 
            prefix="Outside:" 
            format="##.#" 
            postfix="&ordm;C"
            wbSource="/eventstate/widgetdemo/numeric" 
            wbTarget="/sendevent/widgetdemo/numeric"
            wbTitle="Numeric Entry Demo">
            wb:numericEntry
        </wb:numericEntryButton>
        
        <wb:timeEntryButton 
            wbSource="/eventstate/widgetdemo/time?attr=time"
            wbTarget="/sendevent/widgetdemo/time"
            wbTitle="Time Entry Demo">
        </wb:timeEntryButton>
        
        <wb:enableEntryButton 
            wbSource="/eventstate/widgetdemo/numeric" 
            wbTarget="/sendevent/widgetdemo/numeric"
            prefix="prefix "
            postfix=" X">
        </wb:enableEntryButton>
        
        <wb:BackButton />
        <wb:BackButton>Done<img src="/static/activeskin/images/smallQueue.png"/></wb:BackButton>
        
    </div>
    
    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        <div>
            <table>
                <tr>
                    <td>
                        <wb:textDisplay wbSource="/eventstate/widgetdemo/onoff?attr=onoff"></wb:textDisplay>
                    </td>
                    <td>
                        <wb:textDisplay wbSource="/eventstate/widgetdemo/day?attr=day"></wb:textDisplay>
                    </td>
                    <td>
                        <wb:numericDisplay
                            wbSource="/eventstate/widgetdemo/numeric" 
                            prefix="Outside:" 
                            format="##.#" 
                            postfix="&ordm;C">
                            wb:numericDisplay
                        </wb:numericDisplay>
                    </td>
                    <td>
                        <wb:timeDisplay wbSource="/eventstate/widgetdemo/time?attr=time">
                            wb:timeDisplay
                        </wb:timeDisplay>
                    </td>
                </tr>
                <tr>
                    <td>
                        <wb:onoffEntry
                            wbSource="/eventstate/widgetdemo/onoff?attr=onoff"
                            wbTarget="/sendevent/widgetdemo/onoff"
                            wbTitle="On Off Entry Demo">
                        </wb:onoffEntry>
                    </td>
                    <td>
                        <wb:dayEntry
                            wbSource="/eventstate/widgetdemo/day?attr=day"
                            wbTarget="/sendevent/widgetdemo/day"
                            wbTitle="Day Entry Demo">
                        </wb:dayEntry>
                    </td>
                    <td>
                        <wb:numericEntry
                            prefix="Outside:" 
                            format="##.#" 
                            postfix="&ordm;C"
                            wbSource="/eventstate/widgetdemo/numeric" 
                            wbTarget="/sendevent/widgetdemo/numeric"
                            wbTitle="Numeric Entry Demo">
                            wb:numericEntry
                        </wb:numericEntry>
                    </td>
                    <td>
                        <wb:timeEntry
                            wbSource="/eventstate/widgetdemo/time?attr=time"
                            wbTarget="/sendevent/widgetdemo/time"
                            wbTitle="Time Entry Demo">
                        </wb:timeEntry>
                    </td>
                </tr>
                <tr>
                    <td>
                        <wb:simpleIndicator
                                wbSource="/eventstate/widgetdemo"
                                stateVals="Open,Closed,Ajar,Error"
                                baseClassName="gate">        	
                            Indicator
                        </wb:simpleIndicator>
                    </td>
                </tr>
            </table>
        </div>
        
    </div>

</html>
