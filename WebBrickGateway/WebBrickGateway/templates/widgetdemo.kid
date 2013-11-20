<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/" 
    py:extends="'master.kid'">
	
<style  TYPE="text/css">
td      { 
		  border-width: thin ;
		  border-collapse: collapse ;
          border-color: rgb(0%,0%,0%) ;		
        }

</style>

${output_head("Widget Demo")}

<body>

${output_nav("Widget Demos")}

<table class="navTable">

    <tr>
        <wb:caption>wb:simpleLink</wb:caption>
        <wb:simpleLink target="/">Home</wb:simpleLink>
        <wb:caption>wb:simpleButton</wb:caption>
        <wb:simpleButton wbSource="/eventstate/widgetdemo/buttonstate"
				wbTarget="/sendevent/widgetdemo/buttonstate"
			>
			simpleButton
		</wb:simpleButton>
    </tr>
    <tr>
        <wb:caption>wb:textDisplay</wb:caption>
		<wb:textDisplay wbSource="/local/time">wb:textDisplay</wb:textDisplay>
        <wb:caption>wb:numericDisplay</wb:caption>
		<wb:numericDisplay 
				wbSource="/eventstate/widgetdemo/numeric" 
				prefix="Outside:" 
				format="##.#" 
				postfix="&ordm;C">
			wb:numericDisplay
		</wb:numericDisplay>
    </tr>
    <tr>
        <wb:caption>wb:timeDisplay</wb:caption>
		<wb:timeDisplay wbSource="/eventstate/widgetdemo/time?attr=time"
            >
            wb:timeDisplay
        </wb:timeDisplay>
    </tr>
    <tr>
        <wb:caption>wb:numericEntry</wb:caption>
        <wb:numericEntry 
                prefix="Outside:" 
                format="##.#" 
                postfix="&ordm;C"
                wbSource="/eventstate/widgetdemo/numeric" 
                wbTarget="/sendevent/widgetdemo/numeric"
                wbTitle="Numeric Entry Demo"
            >
            wb:numericEntry
        </wb:numericEntry>
        <wb:caption>wb:timeEntry</wb:caption>
        <wb:timeEntry 
                wbSource="/eventstate/widgetdemo/time?attr=time"
                wbTarget="/sendevent/widgetdemo/time"
                wbTitle="Time Entry Demo"
            >
            wb:timeEntry
        </wb:timeEntry>
    </tr>
    <tr>
        <wb:caption>wb:onoffEntry</wb:caption>
        <wb:onoffEntry wbSource="/eventstate/widgetdemo/onoffstr?attr=onoff"
                wbTarget="/sendevent/widgetdemo/onoffstr"
                wbTitle="OnOff Entry Demo"
            >
            wb:onoffEntry
        </wb:onoffEntry>
        <wb:caption>wb:dayEntry</wb:caption>
        <wb:dayEntry wbSource="/eventstate/widgetdemo/day?attr=day"
                wbTarget="/sendevent/widgetdemo/day"
                wbTitle="Day Entry Demo"
            >
            wb:dayEntry
        </wb:dayEntry>
    </tr>
    <tr>
        <wb:caption>wb:enableEntry</wb:caption>
        <wb:enableEntry wbSource="/eventstate/widgetdemo/enablestr"
                wbTarget="/sendevent/widgetdemo/enablestr"
            >
            wb:enableEntry
        </wb:enableEntry>
    </tr>
    <tr>
        <wb:caption>wb:flashButton</wb:caption>
        <wb:flashButton wbSource="/eventstate/widgetdemo/buttonstate"
				wbTarget="/sendevent/widgetdemo/buttonstate"
			>
			wb:flashButton
		</wb:flashButton>
        <wb:caption>wb:flashMeter</wb:caption>
		<wb:flashMeter 
				wbSource="/eventstate/widgetdemo/numeric" 
				prefix="Outside:" 
				format="##.#" 
				postfix="&ordm;C">
			wb:flashMeter
		</wb:flashMeter>
    </tr>
    <tr>
        <wb:caption>wb:flashDimmer</wb:caption>
		<wb:flashDimmer 
				wbSource="/eventstate/widgetdemo/numeric" 
				wbTarget="/sendevent/widgetdemo/numeric?val="
			>
			wb:flashDimmer
		</wb:flashDimmer>
    </tr>
    <tr>
        <wb:caption>wb:dynamicImage</wb:caption>
		<wb:dynamicImage wbSource="/eventstate/widgetdemo/imageuri"
			>
			wb:dynamicImage
		</wb:dynamicImage>
    </tr>
    <tr>
        <wb:caption>wb:imageIndicator</wb:caption>
		<td><wb:imageIndicator wbSource="/eventstate/widgetdemo/enablestr"
			>
			wb:imageIndicator
		</wb:imageIndicator></td>
        <wb:caption>wb:imageIndicator</wb:caption>
		<td><wb:imageIndicator wbSource="/eventstate/widgetdemo/enablestr"
            imageUris="/static/images/closed.png,/static/images/open.png"
			>
			wb:imageIndicator
		</wb:imageIndicator></td>
    </tr>
</table>
</body>

</html>
